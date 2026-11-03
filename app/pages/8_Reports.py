"""
Analytical Reports & Compliance Audit Page
File: app/pages/8_Reports.py
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from app.auth import require_role
from app.db import run_query
from app.ui import page_header, money

st.set_page_config(page_title="Reports | BMS", page_icon="📈", layout="wide")
require_role(["MANAGER", "LOAN_OFFICER"])

page_header("📈 Analytical Reports & Compliance", "Audit logs, branch metrics, dormant account monitoring, and loan portfolio analytics")

tabs = [
    "🏛️ Branch Performance",
    "💎 Top 5 Customers",
    "📊 Monthly Transactions",
    "📑 Loan Portfolio",
    "💤 Dormant Accounts",
    "🛡️ Audit Trail Log"
]
t1, t2, t3, t4, t5, t6 = st.tabs(tabs)

def download_csv_btn(df: pd.DataFrame, filename: str):
    """Helper to render CSV download button."""
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"📥 Download {filename}",
        data=csv_bytes,
        file_name=filename,
        mime="text/csv"
    )

# -----------------------------------------------------------------------------
# 1. BRANCH PERFORMANCE
# -----------------------------------------------------------------------------
with t1:
    st.subheader("1. Branch Performance & Deposit Distribution")
    bp_df = run_query("SELECT * FROM v_branch_performance ORDER BY total_deposits DESC")
    if bp_df.empty:
        st.info("No data available.")
    else:
        fig_bp = px.bar(
            bp_df,
            x="branch_name",
            y="total_deposits",
            title="Total Deposits by Branch (₹)",
            labels={"branch_name": "Branch", "total_deposits": "Deposits (₹)"},
            color="branch_name",
            text_auto=True
        )
        st.plotly_chart(fig_bp, use_container_width=True)

        disp_bp = bp_df.copy()
        disp_bp["total_deposits"] = disp_bp["total_deposits"].apply(money)
        st.dataframe(disp_bp, use_container_width=True, hide_index=True)
        download_csv_btn(bp_df, "branch_performance.csv")

# -----------------------------------------------------------------------------
# 2. TOP 5 CUSTOMERS
# -----------------------------------------------------------------------------
with t2:
    st.subheader("2. Top 5 High-Net-Worth Customers by Total Balance")
    top5_df = run_query("""
        SELECT c.customer_id AS `Customer ID`, c.name AS `Customer Name`,
               c.phone AS `Phone`, c.email AS `Email`,
               COUNT(a.account_no) AS `Accounts Count`,
               SUM(a.balance) AS `Total Balance`
        FROM customer c
        JOIN account a ON c.customer_id = a.customer_id
        WHERE a.status <> 'CLOSED'
        GROUP BY c.customer_id, c.name, c.phone, c.email
        ORDER BY `Total Balance` DESC
        LIMIT 5
    """)
    if top5_df.empty:
        st.info("No customer accounts found.")
    else:
        disp_top5 = top5_df.copy()
        disp_top5["Total Balance"] = disp_top5["Total Balance"].apply(money)
        st.dataframe(disp_top5, use_container_width=True, hide_index=True)
        download_csv_btn(top5_df, "top_5_customers.csv")

# -----------------------------------------------------------------------------
# 3. MONTHLY TRANSACTION SUMMARY
# -----------------------------------------------------------------------------
with t3:
    st.subheader("3. Monthly Transaction Trend Analysis")
    monthly_df = run_query("""
        SELECT DATE_FORMAT(txn_time, '%Y-%m') AS `Month`,
               txn_type AS `Type`,
               COUNT(*) AS `Count`,
               SUM(amount) AS `Total Amount`
        FROM transactions
        GROUP BY DATE_FORMAT(txn_time, '%Y-%m'), txn_type
        ORDER BY `Month` ASC, `Type`
    """)
    if monthly_df.empty:
        st.info("No transaction data available.")
    else:
        fig_m = px.line(
            monthly_df,
            x="Month",
            y="Total Amount",
            color="Type",
            markers=True,
            title="Monthly Transaction Volume Trend (₹)"
        )
        st.plotly_chart(fig_m, use_container_width=True)

        disp_m = monthly_df.copy()
        disp_m["Total Amount"] = disp_m["Total Amount"].apply(money)
        st.dataframe(disp_m, use_container_width=True, hide_index=True)
        download_csv_btn(monthly_df, "monthly_transactions.csv")

# -----------------------------------------------------------------------------
# 4. LOAN PORTFOLIO
# -----------------------------------------------------------------------------
with t4:
    st.subheader("4. Credit & Loan Portfolio Health")
    loan_summary_df = run_query("""
        SELECT status AS `Status`,
               COUNT(*) AS `Loan Count`,
               SUM(principal) AS `Total Principal`,
               SUM(outstanding) AS `Total Outstanding`,
               SUM(emi) AS `Total Scheduled EMI`
        FROM loan
        GROUP BY status
        ORDER BY `Loan Count` DESC
    """)
    if loan_summary_df.empty:
        st.info("No loan records found.")
    else:
        disp_ls = loan_summary_df.copy()
        for c in ["Total Principal", "Total Outstanding", "Total Scheduled EMI"]:
            disp_ls[c] = disp_ls[c].apply(money)
        st.dataframe(disp_ls, use_container_width=True, hide_index=True)
        download_csv_btn(loan_summary_df, "loan_portfolio_summary.csv")

# -----------------------------------------------------------------------------
# 5. DORMANT ACCOUNTS
# -----------------------------------------------------------------------------
with t5:
    st.subheader("5. Dormant Accounts (No Transactions in Last 30 Days)")
    dormant_df = run_query("""
        SELECT a.account_no AS `Account No`, c.name AS `Customer`,
               t.name AS `Type`, b.name AS `Branch`, a.balance AS `Balance`,
               a.status AS `Status`,
               MAX(tx.txn_time) AS `Last Transaction`
        FROM account a
        JOIN customer c ON a.customer_id = c.customer_id
        JOIN account_type t ON a.type_id = t.type_id
        JOIN branch b ON a.branch_id = b.branch_id
        LEFT JOIN transactions tx ON a.account_no = tx.account_no
        WHERE a.status = 'ACTIVE'
        GROUP BY a.account_no, c.name, t.name, b.name, a.balance, a.status
        HAVING `Last Transaction` IS NULL OR `Last Transaction` < DATE_SUB(NOW(), INTERVAL 30 DAY)
        ORDER BY `Last Transaction` ASC
    """)
    if dormant_df.empty:
        st.success("No dormant accounts detected; all active accounts have had transactions within the last 30 days.")
    else:
        st.warning(f"Found {len(dormant_df)} active account(s) with no activity in the last 30 days.")
        disp_d = dormant_df.copy()
        disp_d["Balance"] = disp_d["Balance"].apply(money)
        st.dataframe(disp_d, use_container_width=True, hide_index=True)
        download_csv_btn(dormant_df, "dormant_accounts.csv")

# -----------------------------------------------------------------------------
# 6. AUDIT TRAIL LOG
# -----------------------------------------------------------------------------
with t6:
    st.subheader("6. Security & Compliance Trigger Audit Trail")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        tbl_filter = st.selectbox("Filter by Table", ["ALL", "transactions", "account", "loan"])
    with col_a2:
        log_limit = st.slider("Max audit entries", min_value=25, max_value=500, value=100, step=25)

    q_audit = "SELECT log_id AS `Log ID`, table_name AS `Table`, action AS `Action`, record_id AS `Record ID`, details AS `Details`, logged_at AS `Logged At` FROM audit_log WHERE 1=1"
    p_audit = []
    if tbl_filter != "ALL":
        q_audit += " AND table_name = %s"
        p_audit.append(tbl_filter)
    q_audit += " ORDER BY log_id DESC LIMIT %s"
    p_audit.append(log_limit)

    audit_df = run_query(q_audit, tuple(p_audit))
    if audit_df.empty:
        st.info("No audit logs found.")
    else:
        st.dataframe(audit_df, use_container_width=True, hide_index=True)
        download_csv_btn(audit_df, "audit_log.csv")
