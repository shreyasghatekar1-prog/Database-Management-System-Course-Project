"""
Loans Management Page
File: app/pages/5_Loans.py
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
from app.auth import require_role, get_current_user
from app.db import run_query, call_proc, get_customers_df, get_accounts_df
from app.ui import page_header, show_result, money

st.set_page_config(page_title="Loans | BMS", page_icon="📑", layout="wide")
require_role(["MANAGER", "LOAN_OFFICER"])
current_user = get_current_user()

page_header("📑 Loan Management", "Originate credit applications, calculate EMIs, evaluate approvals, and process repayments")

tab1, tab2, tab3, tab4 = st.tabs(["📝 Apply for Loan", "⏳ Pending Approvals", "💳 Repay EMI", "📊 All Loans & Payments"])

# -----------------------------------------------------------------------------
# TAB 1: APPLY FOR LOAN
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Originate New Loan Application")
    # Only verified customers can apply (trigger enforced as well)
    ver_custs = get_customers_df(kyc_only="VERIFIED")
    if ver_custs.empty:
        st.info("No VERIFIED KYC customers found.")
    else:
        cust_map = {
            f"{r['customer_id']} | {r['name']} ({r['phone']})": r['customer_id']
            for _, r in ver_custs.iterrows()
        }
        sel_c_label = st.selectbox("Select Customer *", list(cust_map.keys()), key="loan_cust")
        sel_cid = cust_map[sel_c_label]

        # Only that customer's active accounts
        cust_accs = get_accounts_df(active_only=True, customer_id=sel_cid)
        if cust_accs.empty:
            st.error("This customer has no ACTIVE accounts. An active account is required for loan disbursement & repayment.")
        else:
            acc_map = {
                f"{r['account_no']} | {r['account_type']} - Bal: {money(r['balance'])}": r['account_no']
                for _, r in cust_accs.iterrows()
            }
            sel_acc_label = st.selectbox("Disbursement / Repayment Account *", list(acc_map.keys()))
            sel_acc_no = acc_map[sel_acc_label]

            col_p, col_r, col_t = st.columns(3)
            with col_p:
                principal = st.number_input("Principal Amount (₹) *", min_value=10000.0, value=100000.0, step=10000.0, format="%.2f")
            with col_r:
                rate = st.number_input("Annual Interest Rate (%) *", min_value=1.0, max_value=30.0, value=10.5, step=0.25, format="%.2f")
            with col_t:
                tenure = st.number_input("Tenure (Months) *", min_value=3, max_value=120, value=12, step=1)

            # Live EMI preview in Python: r = rate/12/100, emi = P*r*(1+r)^n / ((1+r)^n - 1)
            r_monthly = (rate / 12.0) / 100.0
            pow_val = (1.0 + r_monthly) ** tenure
            emi_preview = round((principal * r_monthly * pow_val) / (pow_val - 1.0), 2)
            total_payable = round(emi_preview * tenure, 2)
            total_interest = round(total_payable - principal, 2)

            st.info(
                f"**📊 Live Loan Calculation Preview:**  \n"
                f"• Monthly EMI: **{money(emi_preview)}**  \n"
                f"• Total Repayable: **{money(total_payable)}**  \n"
                f"• Total Interest Cost: **{money(total_interest)}**"
            )

            if st.button("Submit Loan Application", type="primary"):
                ok, msg = call_proc("sp_apply_loan", [sel_cid, sel_acc_no, principal, rate, tenure])
                show_result(ok, msg)
                if ok:
                    st.rerun()

# -----------------------------------------------------------------------------
# TAB 2: PENDING APPROVALS
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Pending Loan Applications")
    p_loans = run_query("""
        SELECT l.loan_id AS `Loan ID`, l.customer_id AS `Cust ID`, c.name AS `Customer`,
               l.account_no AS `Account No`, l.principal AS `Principal`, l.annual_rate AS `Rate (%)`,
               l.tenure_months AS `Tenure (Mo)`, l.emi AS `EMI`, l.outstanding AS `Outstanding`,
               l.applied_on AS `Applied On`
        FROM loan l
        JOIN customer c ON l.customer_id = c.customer_id
        WHERE l.status = 'PENDING'
        ORDER BY l.loan_id ASC
    """)

    if p_loans.empty:
        st.success("No loan applications pending approval at this time.")
    else:
        p_disp = p_loans.copy()
        p_disp["Principal"] = p_disp["Principal"].apply(money)
        p_disp["EMI"] = p_disp["EMI"].apply(money)
        p_disp["Outstanding"] = p_disp["Outstanding"].apply(money)
        st.dataframe(p_disp, use_container_width=True, hide_index=True)

        st.markdown("#### Process Application Decision")
        loan_choices = {
            f"Loan #{r['Loan ID']} - {r['Customer']} ({r['Principal']})": r['Loan ID']
            for _, r in p_loans.iterrows()
        }
        pick_dec = st.selectbox("Select Pending Loan", list(loan_choices.keys()))
        sel_lid = loan_choices[pick_dec]

        col_app, col_rej = st.columns(2)
        with col_app:
            if st.button(f"✅ Approve & Disburse Loan #{sel_lid}", type="primary", use_container_width=True):
                ok, msg = call_proc("sp_approve_loan", [sel_lid, current_user["emp_id"]])
                show_result(ok, msg)
                if ok:
                    st.rerun()
        with col_rej:
            if st.button(f"❌ Reject Loan #{sel_lid}", type="secondary", use_container_width=True):
                ok, msg = call_proc("sp_reject_loan", [sel_lid, current_user["emp_id"]])
                show_result(ok, msg)
                if ok:
                    st.rerun()

# -----------------------------------------------------------------------------
# TAB 3: REPAY EMI
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Process Loan EMI Payment")
    app_loans = run_query("""
        SELECT l.loan_id, l.customer_id, c.name AS customer_name, l.account_no,
               l.principal, l.emi, l.outstanding, a.balance AS account_balance
        FROM loan l
        JOIN customer c ON l.customer_id = c.customer_id
        JOIN account a ON l.account_no = a.account_no
        WHERE l.status = 'APPROVED' AND l.outstanding > 0
        ORDER BY l.loan_id
    """)

    if app_loans.empty:
        st.info("No active approved loans with outstanding balances found.")
    else:
        l_map = {
            f"Loan #{r['loan_id']} | {r['customer_name']} | EMI: {money(r['emi'])} | Due: {money(r['outstanding'])}": r['loan_id']
            for _, r in app_loans.iterrows()
        }
        l_pick = st.selectbox("Select Active Loan", list(l_map.keys()))
        l_id = l_map[l_pick]
        l_info = app_loans[app_loans["loan_id"] == l_id].iloc[0]

        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            st.metric("Scheduled Monthly EMI", money(l_info["emi"]))
        with col_e2:
            st.metric("Total Outstanding Due", money(l_info["outstanding"]))
        with col_e3:
            st.metric("Account Current Balance", money(l_info["account_balance"]))

        with st.form("emi_payment_form"):
            default_pay = float(min(l_info["emi"], l_info["outstanding"]))
            pay_amt = st.number_input(
                "Payment Amount (₹) *",
                min_value=1.0,
                max_value=float(l_info["outstanding"]),
                value=default_pay,
                step=500.0,
                format="%.2f"
            )
            pay_submit = st.form_submit_button("Pay EMI / Prepay", type="primary")

            if pay_submit:
                if pay_amt > float(l_info["outstanding"]):
                    st.error("Payment cannot exceed total outstanding amount.")
                else:
                    ok, msg = call_proc("sp_pay_emi", [l_id, pay_amt, current_user["emp_id"]])
                    show_result(ok, msg)
                    if ok:
                        st.rerun()

# -----------------------------------------------------------------------------
# TAB 4: ALL LOANS & PAYMENTS
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("Loan Portfolio Overview")
    status_filter = st.selectbox("Status Filter", ["ALL", "APPROVED", "PENDING", "REJECTED", "CLOSED"])

    q_all = "SELECT * FROM v_loan_outstanding WHERE 1=1"
    params_all = []
    if status_filter != "ALL":
        q_all += " AND status = %s"
        params_all.append(status_filter)
    q_all += " ORDER BY loan_id DESC"

    df_all_loans = run_query(q_all, tuple(params_all) if params_all else None)
    if df_all_loans.empty:
        st.info("No loans found.")
    else:
        disp_all = df_all_loans.copy()
        for col_m in ["principal", "emi", "outstanding", "total_paid"]:
            if col_m in disp_all.columns:
                disp_all[col_m] = disp_all[col_m].apply(money)
        st.dataframe(disp_all, use_container_width=True, hide_index=True)

        st.markdown("#### EMI Payment History for Specific Loan")
        loan_pick_id = st.selectbox("Select Loan ID to view payment ledger", df_all_loans["loan_id"].tolist())
        payments_df = run_query("""
            SELECT payment_id AS `Payment ID`, loan_id AS `Loan ID`,
                   amount AS `Amount Paid`, paid_on AS `Date & Time`
            FROM loan_payment
            WHERE loan_id = %s
            ORDER BY payment_id DESC
        """, (loan_pick_id,))

        if payments_df.empty:
            st.caption("No EMI payment records for this loan.")
        else:
            p_disp_tbl = payments_df.copy()
            p_disp_tbl["Amount Paid"] = p_disp_tbl["Amount Paid"].apply(money)
            st.dataframe(p_disp_tbl, use_container_width=True, hide_index=True)
