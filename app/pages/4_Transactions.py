"""
Transactions Page
File: app/pages/4_Transactions.py
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import datetime
import streamlit as st
import pandas as pd
from app.auth import require_role, get_current_user
from app.db import run_query, call_proc, call_proc_table, get_accounts_df
from app.ui import page_header, show_result, money

st.set_page_config(page_title="Transactions | BMS", page_icon="💸", layout="wide")
require_role(["MANAGER", "TELLER"])
current_user = get_current_user()
is_manager = current_user["role"] == "MANAGER"

page_header("💸 Transactions & Ledger", "Execute deposits, cash withdrawals, atomic transfers, interest runs, and view history")

tabs = ["📥 Deposit", "📤 Withdraw", "🔄 Transfer", "⚡ Charges", "📈 Monthly Interest", "📜 History", "🧾 Mini Statement"]
t_dep, t_wd, t_tf, t_ch, t_int, t_hist, t_mini = st.tabs(tabs)

# -----------------------------------------------------------------------------
# TAB 1: DEPOSIT
# -----------------------------------------------------------------------------
with t_dep:
    st.subheader("Cash / Counter Deposit")
    active_accs = get_accounts_df(active_only=True)
    if active_accs.empty:
        st.info("No active accounts available.")
    else:
        acc_dict = {
            f"{r['account_no']} | {r['customer_name']} ({r['account_type']}) - Bal: {money(r['balance'])}": r['account_no']
            for _, r in active_accs.iterrows()
        }
        pick_d = st.selectbox("Select Account for Deposit", list(acc_dict.keys()), key="dep_acc")
        sel_acc_d = acc_dict[pick_d]

        with st.form("deposit_form"):
            dep_amt = st.number_input("Deposit Amount (₹) *", min_value=1.0, value=1000.0, step=500.0, format="%.2f")
            dep_submit = st.form_submit_button("Confirm Deposit", type="primary")

            if dep_submit:
                ok, msg = call_proc("sp_deposit", [sel_acc_d, dep_amt, current_user["emp_id"]])
                show_result(ok, msg)
                if ok:
                    st.rerun()

# -----------------------------------------------------------------------------
# TAB 2: WITHDRAW
# -----------------------------------------------------------------------------
with t_wd:
    st.subheader("Cash Withdrawal")
    active_accs_w = get_accounts_df(active_only=True)
    if active_accs_w.empty:
        st.info("No active accounts available.")
    else:
        acc_dict_w = {
            f"{r['account_no']} | {r['customer_name']} ({r['account_type']}) - Bal: {money(r['balance'])}": r['account_no']
            for _, r in active_accs_w.iterrows()
        }
        pick_w = st.selectbox("Select Account for Withdrawal", list(acc_dict_w.keys()), key="wd_acc")
        sel_acc_w = acc_dict_w[pick_w]
        w_row = active_accs_w[active_accs_w["account_no"] == sel_acc_w].iloc[0]

        c_w1, c_w2, c_w3 = st.columns(3)
        with c_w1:
            st.metric("Current Balance", money(w_row["balance"]))
        with c_w2:
            st.metric("Min Balance Required", money(w_row["min_balance"]))
        with c_w3:
            max_withdrawable = max(0.0, float(w_row["balance"]) - float(w_row["min_balance"]))
            st.metric("Max Withdrawable", money(max_withdrawable))

        with st.form("withdraw_form"):
            wd_amt = st.number_input("Withdrawal Amount (₹) *", min_value=1.0, value=500.0, step=500.0, format="%.2f")
            wd_submit = st.form_submit_button("Confirm Withdrawal", type="primary")

            if wd_submit:
                if wd_amt > max_withdrawable:
                    st.error(f"Cannot withdraw {money(wd_amt)}. Maximum allowed withdrawal while maintaining minimum balance is {money(max_withdrawable)}.")
                else:
                    ok, msg = call_proc("sp_withdraw", [sel_acc_w, wd_amt, current_user["emp_id"]])
                    show_result(ok, msg)
                    if ok:
                        st.rerun()

# -----------------------------------------------------------------------------
# TAB 3: TRANSFER
# -----------------------------------------------------------------------------
with t_tf:
    st.subheader("Inter-Account Atomic Transfer")
    active_accs_t = get_accounts_df(active_only=True)
    if len(active_accs_t) < 2:
        st.info("At least two active accounts are required to transfer funds.")
    else:
        acc_dict_from = {
            f"{r['account_no']} | {r['customer_name']} - Bal: {money(r['balance'])}": r['account_no']
            for _, r in active_accs_t.iterrows()
        }
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            from_pick = st.selectbox("From (Sender Account) *", list(acc_dict_from.keys()), key="tf_from")
            from_acc = acc_dict_from[from_pick]
            from_row = active_accs_t[active_accs_t["account_no"] == from_acc].iloc[0]
            st.caption(f"Sender Min Balance: {money(from_row['min_balance'])} | Available: {money(max(0.0, float(from_row['balance']) - float(from_row['min_balance'])))}")

        with col_t2:
            acc_dict_to = {
                f"{r['account_no']} | {r['customer_name']} ({r['account_type']})": r['account_no']
                for _, r in active_accs_t.iterrows() if r['account_no'] != from_acc
            }
            to_pick = st.selectbox("To (Beneficiary Account) *", list(acc_dict_to.keys()), key="tf_to")
            to_acc = acc_dict_to[to_pick]
            to_row = active_accs_t[active_accs_t["account_no"] == to_acc].iloc[0]
            st.info(f"Beneficiary Name: **{to_row['customer_name']}** ({to_row['branch_name']})")

        with st.form("transfer_form"):
            tf_amt = st.number_input("Transfer Amount (₹) *", min_value=1.0, value=1000.0, step=500.0, format="%.2f")
            tf_submit = st.form_submit_button("Execute Transfer", type="primary")

            if tf_submit:
                if from_acc == to_acc:
                    st.error("Sender and receiver accounts must be different.")
                else:
                    ok, msg = call_proc("sp_transfer", [from_acc, to_acc, tf_amt, current_user["emp_id"]])
                    show_result(ok, msg)
                    if ok:
                        st.rerun()

# -----------------------------------------------------------------------------
# TAB 4: CHARGES
# -----------------------------------------------------------------------------
with t_ch:
    if not is_manager:
        st.warning("Only MANAGER role can apply manual service charges or penal charges.")
    else:
        st.subheader("Apply Account Service / Penalty Charge")
        active_accs_c = get_accounts_df(active_only=True)
        if active_accs_c.empty:
            st.info("No active accounts available.")
        else:
            acc_dict_c = {
                f"{r['account_no']} | {r['customer_name']} - Bal: {money(r['balance'])}": r['account_no']
                for _, r in active_accs_c.iterrows()
            }
            ch_pick = st.selectbox("Select Account", list(acc_dict_c.keys()), key="charge_acc")
            ch_acc = acc_dict_c[ch_pick]

            with st.form("charge_form"):
                ch_amt = st.number_input("Charge Amount (₹) *", min_value=1.0, value=150.0, step=50.0, format="%.2f")
                ch_rem = st.text_input("Remarks / Reason *", value="Account maintenance charge")
                ch_submit = st.form_submit_button("Apply Charge", type="primary")

                if ch_submit:
                    ok, msg = call_proc("sp_apply_charge", [ch_acc, ch_amt, ch_rem.strip(), current_user["emp_id"]])
                    show_result(ok, msg)
                    if ok:
                        st.rerun()

# -----------------------------------------------------------------------------
# TAB 5: MONTHLY INTEREST
# -----------------------------------------------------------------------------
with t_int:
    if not is_manager:
        st.warning("Only MANAGER role can trigger monthly interest crediting.")
    else:
        st.subheader("Monthly Interest Credit Process")
        st.write("This set-based procedure calculates and credits monthly interest to all active savings and fixed-deposit accounts based on their configured annual interest rates.")
        
        # Preview eligible accounts
        preview_df = run_query("""
            SELECT a.account_no AS `Account No`, c.name AS `Customer`, t.name AS `Type`,
                   t.interest_rate AS `Annual Rate (%)`, a.balance AS `Current Balance`,
                   ROUND(a.balance * (t.interest_rate / 1200.0), 2) AS `Estimated Monthly Interest`
            FROM account a
            JOIN customer c ON a.customer_id = c.customer_id
            JOIN account_type t ON a.type_id = t.type_id
            WHERE a.status = 'ACTIVE' AND t.interest_rate > 0
              AND ROUND(a.balance * (t.interest_rate / 1200.0), 2) > 0
        """)
        
        if not preview_df.empty:
            st.write(f"**Eligible Accounts Preview ({len(preview_df)} accounts):**")
            p_display = preview_df.copy()
            p_display["Current Balance"] = p_display["Current Balance"].apply(money)
            p_display["Estimated Monthly Interest"] = p_display["Estimated Monthly Interest"].apply(money)
            st.dataframe(p_display, use_container_width=True, hide_index=True)

        confirm_int = st.checkbox("Confirm: I authorize crediting interest to all eligible accounts immediately.")
        if st.button("Run Monthly Interest Credit", type="primary"):
            if not confirm_int:
                st.warning("Please check the confirmation box.")
            else:
                ok, msg = call_proc("sp_credit_interest", [current_user["emp_id"]])
                show_result(ok, msg)
                if ok:
                    st.rerun()

# -----------------------------------------------------------------------------
# TAB 6: HISTORY
# -----------------------------------------------------------------------------
with t_hist:
    st.subheader("Transaction Ledger History")
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        acc_h_options = ["ALL"] + [str(a) for a in run_query("SELECT account_no FROM account ORDER BY account_no")["account_no"].tolist()]
        h_acc = st.selectbox("Filter by Account", acc_h_options)
    with col_h2:
        h_type = st.selectbox("Filter by Type", ["ALL", "DEPOSIT", "WITHDRAW", "TRANSFER_OUT", "TRANSFER_IN", "LOAN_DISBURSE", "LOAN_EMI", "INTEREST", "CHARGE"])
    with col_h3:
        h_limit = st.slider("Max rows to fetch", min_value=25, max_value=500, value=100, step=25)

    q_hist = """
        SELECT txn_id AS `Txn ID`, txn_time AS `Timestamp`, account_no AS `Account No`,
               txn_type AS `Type`, amount AS `Amount`, balance_after AS `Balance After`,
               related_account AS `Related Acc`, remarks AS `Remarks`, done_by_emp AS `Emp ID`
        FROM transactions
        WHERE 1=1
    """
    p_hist = []
    if h_acc != "ALL":
        q_hist += " AND account_no = %s"
        p_hist.append(int(h_acc))
    if h_type != "ALL":
        q_hist += " AND txn_type = %s"
        p_hist.append(h_type)
    q_hist += " ORDER BY txn_time DESC, txn_id DESC LIMIT %s"
    p_hist.append(h_limit)

    df_hist = run_query(q_hist, tuple(p_hist))
    if df_hist.empty:
        st.info("No transactions found matching criteria.")
    else:
        df_h_disp = df_hist.copy()
        df_h_disp["Amount"] = df_h_disp["Amount"].apply(money)
        df_h_disp["Balance After"] = df_h_disp["Balance After"].apply(money)
        st.dataframe(df_h_disp, use_container_width=True, hide_index=True)

        csv = df_hist.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Transactions CSV",
            data=csv,
            file_name=f"transactions_{datetime.date.today()}.csv",
            mime="text/csv",
        )

# -----------------------------------------------------------------------------
# TAB 7: MINI STATEMENT
# -----------------------------------------------------------------------------
with t_mini:
    st.subheader("Account Mini Statement")
    accs_m = get_accounts_df()
    if accs_m.empty:
        st.info("No accounts available.")
    else:
        m_dict = {
            f"{r['account_no']} | {r['customer_name']} ({r['account_type']}) - {money(r['balance'])}": r['account_no']
            for _, r in accs_m.iterrows()
        }
        pick_m = st.selectbox("Select Account for Statement", list(m_dict.keys()), key="mini_acc")
        sel_m_acc = m_dict[pick_m]
        n_txns = st.selectbox("Number of Recent Transactions (N)", [5, 10, 15, 20], index=1)

        if st.button("Generate Mini Statement", type="primary"):
            df_mini = call_proc_table("sp_mini_statement", [sel_m_acc, n_txns])
            if df_mini.empty:
                st.info("No transaction history available for this account.")
            else:
                m_disp = df_mini.copy()
                if "amount" in m_disp.columns:
                    m_disp["amount"] = m_disp["amount"].apply(money)
                if "balance_after" in m_disp.columns:
                    m_disp["balance_after"] = m_disp["balance_after"].apply(money)
                st.dataframe(m_disp, use_container_width=True, hide_index=True)
