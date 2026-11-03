"""
Account Management Page
File: app/pages/3_Accounts.py
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
from app.auth import require_role, get_current_user
from app.db import run_query, call_proc, get_customers_df, get_branches_df, get_account_types_df, get_accounts_df
from app.ui import page_header, show_result, money

st.set_page_config(page_title="Accounts | BMS", page_icon="💳", layout="wide")
require_role(["MANAGER", "TELLER", "LOAN_OFFICER", "CLERK"])
current_user = get_current_user()
can_operate = current_user["role"] in ["MANAGER", "TELLER"]

page_header("💳 Account Management", "Open new accounts, inspect balances, freeze or close customer accounts")

tab1, tab2, tab3, tab4 = st.tabs(["📋 All Accounts", "✨ Open Account", "⚙️ Manage Account", "🔎 Balance Enquiry"])

# -----------------------------------------------------------------------------
# TAB 1: ALL ACCOUNTS
# -----------------------------------------------------------------------------
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        type_filter = st.selectbox("Account Type", ["ALL", "SAVINGS", "CURRENT", "FIXED_DEPOSIT"])
    with col2:
        branches = get_branches_df()
        branch_filter = st.selectbox("Branch", ["ALL"] + branches["name"].tolist())
    with col3:
        status_filter = st.selectbox("Account Status", ["ALL", "ACTIVE", "FROZEN", "CLOSED"])

    query = """
        SELECT account_no AS `Account No`, customer_name AS `Customer`,
               account_type AS `Type`, branch_name AS `Branch`, ifsc AS `IFSC`,
               balance AS `Balance`, status AS `Status`, opened_on AS `Opened On`
        FROM v_account_summary
        WHERE 1=1
    """
    params = []
    if type_filter != "ALL":
        query += " AND account_type = %s"
        params.append(type_filter)
    if branch_filter != "ALL":
        query += " AND branch_name = %s"
        params.append(branch_filter)
    if status_filter != "ALL":
        query += " AND status = %s"
        params.append(status_filter)
    query += " ORDER BY account_no DESC"

    df_acc = run_query(query, tuple(params) if params else None)
    df_display = df_acc.copy()
    if not df_display.empty:
        df_display["Balance"] = df_display["Balance"].apply(money)
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    st.caption(f"Total: {len(df_acc)} account(s)")

# -----------------------------------------------------------------------------
# TAB 2: OPEN ACCOUNT
# -----------------------------------------------------------------------------
with tab2:
    if not can_operate:
        st.warning("Only MANAGER and TELLER roles are authorized to open customer accounts.")
    else:
        st.subheader("Open a New Account")
        # Load verified customers
        cust_df = get_customers_df(kyc_only="VERIFIED")
        types_df = get_account_types_df()
        branches_df = get_branches_df()

        if cust_df.empty:
            st.error("No customers with VERIFIED KYC found. Complete customer KYC before opening accounts.")
        else:
            with st.form("open_account_form"):
                cust_map = {
                    f"{r['customer_id']} | {r['name']} ({r['phone']})": r['customer_id']
                    for _, r in cust_df.iterrows()
                }
                c_pick = st.selectbox("Select Verified Customer *", list(cust_map.keys()))
                sel_cid = cust_map[c_pick]

                type_map = {
                    f"{r['name']} (Min Bal: {money(r['min_balance'])}, Interest: {r['interest_rate']}%)": (r['type_id'], float(r['min_balance']))
                    for _, r in types_df.iterrows()
                }
                t_pick = st.selectbox("Account Type *", list(type_map.keys()))
                sel_tid, min_bal_req = type_map[t_pick]

                branch_map = {
                    f"{r['branch_id']} | {r['name']} ({r['city']})": r['branch_id']
                    for _, r in branches_df.iterrows()
                }
                b_pick = st.selectbox("Branch *", list(branch_map.keys()))
                sel_bid = branch_map[b_pick]

                init_dep = st.number_input(
                    f"Initial Deposit ({money(min_bal_req)} minimum required) *",
                    min_value=0.0,
                    value=float(min_bal_req),
                    step=500.0,
                    format="%.2f"
                )

                submit_open = st.form_submit_button("Submit & Open Account", type="primary")

                if submit_open:
                    if init_dep < min_bal_req:
                        st.error(f"Deposit amount {money(init_dep)} is less than the minimum balance required ({money(min_bal_req)}).")
                    else:
                        ok, msg = call_proc(
                            "sp_open_account",
                            [sel_cid, sel_tid, sel_bid, init_dep, current_user["emp_id"]]
                        )
                        show_result(ok, msg)
                        if ok:
                            st.rerun()

# -----------------------------------------------------------------------------
# TAB 3: MANAGE ACCOUNT
# -----------------------------------------------------------------------------
with tab3:
    if not can_operate:
        st.warning("Only MANAGER and TELLER roles can freeze, unfreeze, or close accounts.")
    else:
        st.subheader("Account Status Management")
        accs = get_accounts_df()
        if accs.empty:
            st.info("No accounts available.")
        else:
            acc_map = {
                f"{r['account_no']} | {r['customer_name']} | {r['account_type']} | Bal: {money(r['balance'])} [{r['status']}]": r['account_no']
                for _, r in accs.iterrows()
            }
            picked_label = st.selectbox("Select Account", list(acc_map.keys()))
            picked_acc = acc_map[picked_label]
            acc_row = accs[accs["account_no"] == picked_acc].iloc[0]

            st.write(f"**Current Status:** `{acc_row['status']}` | **Current Balance:** {money(acc_row['balance'])}")

            action = st.radio("Select Action", ["Set Status (ACTIVE / FROZEN)", "Close Account"])

            if action == "Set Status (ACTIVE / FROZEN)":
                if acc_row["status"] == "CLOSED":
                    st.error("Cannot modify status of an already CLOSED account.")
                else:
                    new_st = st.selectbox("New Status", ["ACTIVE", "FROZEN"], index=0 if acc_row["status"] == "FROZEN" else 1)
                    confirm_st = st.checkbox(f"Confirm changing status of Account #{picked_acc} to {new_st}")
                    if st.button("Update Status", type="primary"):
                        if not confirm_st:
                            st.warning("Please confirm the status change checkbox.")
                        else:
                            ok, msg = call_proc("sp_set_account_status", [picked_acc, new_st, current_user["emp_id"]])
                            show_result(ok, msg)
                            if ok:
                                st.rerun()

            elif action == "Close Account":
                st.warning("Closing an account requires balance to be strictly ₹0.00 and no active/pending loans.")
                confirm_cl = st.checkbox(f"I understand and confirm closure of Account #{picked_acc}")
                if st.button("Close Account Permanently", type="primary"):
                    if not confirm_cl:
                        st.warning("Please check the confirmation box.")
                    else:
                        ok, msg = call_proc("sp_close_account", [picked_acc, current_user["emp_id"]])
                        show_result(ok, msg)
                        if ok:
                            st.rerun()

# -----------------------------------------------------------------------------
# TAB 4: BALANCE ENQUIRY
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("Instant Balance Enquiry")
    accs_all = get_accounts_df()
    if accs_all.empty:
        st.info("No accounts available.")
    else:
        acc_dict = {
            f"{r['account_no']} - {r['customer_name']} ({r['account_type']})": r['account_no']
            for _, r in accs_all.iterrows()
        }
        enq_pick = st.selectbox("Choose Account", list(acc_dict.keys()), key="enq_acc_pick")
        enq_acc_no = acc_dict[enq_pick]

        enq_df = run_query("SELECT * FROM v_account_summary WHERE account_no = %s", (enq_acc_no,))
        if not enq_df.empty:
            e = enq_df.iloc[0]
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            with col_b1:
                st.metric("Current Balance", money(e["balance"]))
            with col_b2:
                st.metric("Account Status", e["status"])
            with col_b3:
                st.metric("Minimum Balance Required", money(e["min_balance"]))
            with col_b4:
                st.metric("Annual Interest Rate", f"{e['interest_rate']}%")

            st.write(f"**Customer:** {e['customer_name']} (ID: {e['customer_id']})")
            st.write(f"**Branch:** {e['branch_name']} | **IFSC:** `{e['ifsc']}` | **Opened On:** {e['opened_on']}")
