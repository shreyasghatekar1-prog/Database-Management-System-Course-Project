"""
Executive Dashboard Page
File: app/pages/1_Dashboard.py
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
import plotly.express as px
from app.auth import require_login, get_current_user
from app.db import run_query
from app.ui import page_header, money

st.set_page_config(page_title="Dashboard | BMS", page_icon="📊", layout="wide")
require_login()
current_user = get_current_user()

page_header("📊 Executive Banking Dashboard", "Live operational indicators, transaction metrics, and portfolio distributions")

# -----------------------------------------------------------------------------
# 1. KEY PERFORMANCE METRICS
# -----------------------------------------------------------------------------
m_cust = run_query("SELECT COUNT(*) AS total FROM customer")["total"].iloc[0]
m_acc = run_query("SELECT COUNT(*) AS total, COALESCE(SUM(balance), 0) AS deposits FROM account WHERE status = 'ACTIVE'")
active_acc_count = m_acc["total"].iloc[0]
total_deposits = m_acc["deposits"].iloc[0]
m_loans = run_query("SELECT COUNT(*) AS total FROM loan WHERE status = 'APPROVED'")["total"].iloc[0]
m_txns_today = run_query("SELECT COUNT(*) AS total FROM transactions WHERE DATE(txn_time) = CURRENT_DATE")["total"].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Total Customers", int(m_cust))
with c2:
    st.metric("Active Accounts", int(active_acc_count))
with c3:
    st.metric("Total Deposits", money(total_deposits))
with c4:
    st.metric("Active Loans", int(m_loans))
with c5:
    st.metric("Today's Transactions", int(m_txns_today))

st.divider()

# -----------------------------------------------------------------------------
# 2. CHARTS SECTION
# -----------------------------------------------------------------------------
col_c1, col_c2 = st.columns([1.3, 1])

with col_c1:
    st.subheader("Daily Transaction Volume (Last 30 Days)")
    df_daily = run_query("""
        SELECT txn_date, txn_type, total_amount, txn_count
        FROM v_daily_transactions
        WHERE txn_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
        ORDER BY txn_date ASC
    """)
    if df_daily.empty:
        # Fallback to last available dates if sample data is from a fixed past date
        df_daily = run_query("""
            SELECT txn_date, txn_type, total_amount, txn_count
            FROM v_daily_transactions
            ORDER BY txn_date DESC
            LIMIT 30
        """).sort_values("txn_date")

    if not df_daily.empty:
        fig_bar = px.bar(
            df_daily,
            x="txn_date",
            y="total_amount",
            color="txn_type",
            title="Daily Transaction Amounts by Type (₹)",
            labels={"txn_date": "Date", "total_amount": "Amount (₹)", "txn_type": "Type"},
            barmode="stack"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No transaction data available for the selected period.")

with col_c2:
    st.subheader("Accounts Distribution by Type")
    df_acc_type = run_query("""
        SELECT t.name AS `Type`, COUNT(a.account_no) AS `Count`
        FROM account_type t
        LEFT JOIN account a ON t.type_id = a.type_id AND a.status <> 'CLOSED'
        GROUP BY t.name
    """)
    if not df_acc_type.empty:
        fig_pie = px.pie(
            df_acc_type,
            values="Count",
            names="Type",
            title="Active Accounts by Product Type",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No accounts data available.")

st.subheader("Branch Deposits Overview")
df_branch_dep = run_query("SELECT branch_name, total_deposits FROM v_branch_performance ORDER BY total_deposits DESC")
if not df_branch_dep.empty:
    fig_branch = px.bar(
        df_branch_dep,
        x="branch_name",
        y="total_deposits",
        color="branch_name",
        text_auto=True,
        labels={"branch_name": "Branch", "total_deposits": "Deposits (₹)"}
    )
    st.plotly_chart(fig_branch, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# 3. RECENT ACTIVITY TABLE
# -----------------------------------------------------------------------------
st.subheader("Recent Banking Activity (Last 10 Transactions)")
df_recent = run_query("""
    SELECT t.txn_id AS `Txn ID`, t.txn_time AS `Timestamp`,
           t.account_no AS `Account No`, cust.name AS `Customer`,
           t.txn_type AS `Type`, t.amount AS `Amount`,
           t.balance_after AS `Balance After`, t.remarks AS `Remarks`
    FROM transactions t
    JOIN account a ON t.account_no = a.account_no
    JOIN customer cust ON a.customer_id = cust.customer_id
    ORDER BY t.txn_time DESC, t.txn_id DESC
    LIMIT 10
""")

if not df_recent.empty:
    df_r_disp = df_recent.copy()
    df_r_disp["Amount"] = df_r_disp["Amount"].apply(money)
    df_r_disp["Balance After"] = df_r_disp["Balance After"].apply(money)
    st.dataframe(df_r_disp, use_container_width=True, hide_index=True)
else:
    st.info("No recent transactions found.")
