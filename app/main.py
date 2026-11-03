"""
Bank Management System - Main Entry Point & Authentication
File: app/main.py
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from app.auth import authenticate, login_user, is_logged_in, get_current_user
from app.ui import page_header, show_result, init_ui

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

if not is_logged_in():
    page_header("🏦 Bank Management System", "Internal Core Banking System • Staff Access Portal")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.form("login_form", clear_on_submit=False):
            st.subheader("Employee Login")
            username = st.text_input("Username", placeholder="e.g. admin, teller1, loan1, clerk1")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_btn = st.form_submit_button("Sign In", type="primary", use_container_width=True)
            
            if submit_btn:
                if not username or not password:
                    st.warning("Please provide both username and password.")
                else:
                    try:
                        user = authenticate(username, password)
                        if user:
                            login_user(user)
                            st.success(f"Welcome back, {user['name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials or inactive account.")
                    except Exception as ex:
                        st.error(f"Database error during authentication: {ex}")

    with col2:
        st.info(
            """
            ### Default Demonstration Accounts
            
            | Username | Role | Password | Primary Permissions |
            | :--- | :--- | :--- | :--- |
            | `admin` | **MANAGER** | `admin123` | Full access to all modules, employees & reports |
            | `teller1` | **TELLER** | `pass123` | Deposits, withdrawals, transfers, account ops |
            | `loan1` | **LOAN_OFFICER** | `pass123` | Loan applications, approvals, disbursements |
            | `clerk1` | **CLERK** | `pass123` | Customer onboarding, KYC updates, card issuance |
            """
        )

else:
    user = get_current_user()
    page_header(f"Welcome, {user['name']}", f"Role: {user['role']} | Branch ID: {user['branch_id']}")
    
    st.success(f"You are authenticated as **{user['role']}**. Select an option from the sidebar to proceed.")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Logged In User", user['username'])
    with c2:
        st.metric("Access Tier", user['role'])
    with c3:
        st.metric("Assigned Branch", f"Branch #{user['branch_id']}")
    with c4:
        st.metric("Session Status", "Active")
        
    st.divider()
    
    st.markdown("### Quick Navigation & Role Access")
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown(
            """
            - 📊 **[Dashboard](Dashboard)**: High-level bank metrics, deposit distribution, and recent ledger activity.
            - 👥 **[Customers](Customers)**: Search customer profiles, onboard new clients (18+), and verify KYC.
            - 💳 **[Accounts](Accounts)**: Open savings/current/FD accounts, check balances, freeze or close accounts.
            - 💸 **[Transactions](Transactions)**: Execute cash deposits, withdrawals, atomic transfers, and interest credits.
            """
        )
    with colB:
        st.markdown(
            """
            - 📑 **[Loans](Loans)**: Review applications, calculate EMI schedules, approve/reject, and process EMI repayments.
            - 🪪 **[Cards](Cards)**: Issue instant debit and credit cards, and manage card blocking.
            - 🏢 **[Employees](Employees)** *(Manager Only)*: Staff hierarchy, branch reassignments, and compensation management.
            - 📈 **[Reports](Reports)**: Branch performance benchmarks, dormant accounts, and system-wide audit logs.
            """
        )
