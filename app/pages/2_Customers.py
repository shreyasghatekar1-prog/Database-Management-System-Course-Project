"""
Customer Management Page
File: app/pages/2_Customers.py
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
from app.db import run_query, execute, get_customers_df
from app.ui import page_header, show_result, money

st.set_page_config(page_title="Customers | BMS", page_icon="👥", layout="wide")
require_role(["MANAGER", "TELLER", "LOAN_OFFICER", "CLERK"])
current_user = get_current_user()
can_edit = current_user["role"] in ["MANAGER", "CLERK"]

page_header("👥 Customer Management", "Search profiles, onboard new customers, and update KYC verification status")

tab1, tab2, tab3, tab4 = st.tabs(["📋 All Customers", "➕ Add Customer", "✏️ Update / KYC", "🔍 Customer 360"])

# -----------------------------------------------------------------------------
# TAB 1: ALL CUSTOMERS
# -----------------------------------------------------------------------------
with tab1:
    c1, c2 = st.columns([2, 1])
    with c1:
        search = st.text_input("🔍 Search by Name, Phone, or Email", placeholder="Type keywords...")
    with c2:
        kyc_filter = st.selectbox("Filter by KYC Status", ["ALL", "VERIFIED", "PENDING", "REJECTED"])

    query = """
        SELECT customer_id AS `ID`, name AS `Name`, dob AS `DOB`, phone AS `Phone`,
               email AS `Email`, address AS `Address`, kyc_status AS `KYC Status`,
               created_at AS `Registered On`
        FROM customer
        WHERE 1=1
    """
    params = []
    if kyc_filter != "ALL":
        query += " AND kyc_status = %s"
        params.append(kyc_filter)
    if search.strip():
        query += " AND (name LIKE %s OR phone LIKE %s OR email LIKE %s)"
        pattern = f"%{search.strip()}%"
        params.extend([pattern, pattern, pattern])
    query += " ORDER BY customer_id DESC"

    df_cust = run_query(query, tuple(params) if params else None)
    st.dataframe(df_cust, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(df_cust)} customer record(s).")

# -----------------------------------------------------------------------------
# TAB 2: ADD CUSTOMER
# -----------------------------------------------------------------------------
with tab2:
    if not can_edit:
        st.warning("Only MANAGER and CLERK roles can onboard new customers.")
    else:
        st.subheader("New Customer Registration")
        st.caption("New customers are initially registered with PENDING KYC status.")
        with st.form("add_customer_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Full Name *", placeholder="e.g. Ramesh S. Patil")
                phone = st.text_input("Mobile Phone (10 digits) *", max_chars=10, placeholder="9822000000")
                email = st.text_input("Email Address *", placeholder="ramesh@example.com")
            with col_b:
                max_dob = datetime.date.today() - datetime.timedelta(days=18 * 365 + 5)
                dob = st.date_input("Date of Birth (Must be 18+) *", value=max_dob, max_value=datetime.date.today())
                address = st.text_area("Residential Address", placeholder="Street, Landmark, City, State, PIN")
            
            submit_add = st.form_submit_button("Register Customer", type="primary")

            if submit_add:
                # Age validation
                age_years = (datetime.date.today() - dob).days // 365
                if not name.strip():
                    st.error("Full Name is required.")
                elif len(phone.strip()) != 10 or not phone.strip().isdigit():
                    st.error("Phone number must be exactly 10 digits.")
                elif "@" not in email or "." not in email:
                    st.error("Please provide a valid email address.")
                elif age_years < 18:
                    st.error(f"Customer must be at least 18 years old. (Calculated age: {age_years})")
                else:
                    try:
                        ins_sql = """
                            INSERT INTO customer (name, dob, phone, email, address, kyc_status)
                            VALUES (%s, %s, %s, %s, %s, 'PENDING')
                        """
                        new_id = execute(ins_sql, (name.strip(), dob, phone.strip(), email.strip().lower(), address.strip()))
                        st.success(f"Customer registered successfully! Customer ID: {new_id}")
                    except Exception as e:
                        err_str = str(e)
                        if "Duplicate entry" in err_str:
                            if "phone" in err_str:
                                st.error("A customer with this phone number already exists.")
                            elif "email" in err_str:
                                st.error("A customer with this email address already exists.")
                            else:
                                st.error(f"Duplicate entry error: {err_str}")
                        else:
                            st.error(f"Error creating customer: {err_str}")

# -----------------------------------------------------------------------------
# TAB 3: UPDATE / KYC
# -----------------------------------------------------------------------------
with tab3:
    if not can_edit:
        st.warning("Only MANAGER and CLERK roles can update customer profiles or verify KYC.")
    else:
        st.subheader("Update Customer Profile & KYC Status")
        cust_df = get_customers_df()
        if cust_df.empty:
            st.info("No customers found.")
        else:
            cust_options = {
                f"{row['customer_id']} | {row['name']} ({row['phone']}) - [{row['kyc_status']}]": row['customer_id']
                for _, row in cust_df.iterrows()
            }
            selected_label = st.selectbox("Select Customer to Update", list(cust_options.keys()))
            selected_id = cust_options[selected_label]
            selected_row = cust_df[cust_df["customer_id"] == selected_id].iloc[0]

            with st.form("update_customer_form"):
                u_col1, u_col2 = st.columns(2)
                with u_col1:
                    u_phone = st.text_input("Phone", value=str(selected_row["phone"]), max_chars=10)
                    u_email = st.text_input("Email", value=str(selected_row["email"]))
                with u_col2:
                    current_kyc = selected_row["kyc_status"]
                    kyc_choices = ["PENDING", "VERIFIED", "REJECTED"]
                    u_kyc = st.selectbox("KYC Status", kyc_choices, index=kyc_choices.index(current_kyc))
                    u_address = st.text_area("Address", value=str(selected_row["address"] or ""))

                submit_upd = st.form_submit_button("Save Customer Changes", type="primary")
                if submit_upd:
                    if len(u_phone.strip()) != 10 or not u_phone.strip().isdigit():
                        st.error("Phone must be exactly 10 digits.")
                    elif "@" not in u_email or "." not in u_email:
                        st.error("Valid email is required.")
                    else:
                        try:
                            upd_sql = """
                                UPDATE customer
                                SET phone = %s, email = %s, address = %s, kyc_status = %s
                                WHERE customer_id = %s
                            """
                            execute(upd_sql, (u_phone.strip(), u_email.strip().lower(), u_address.strip(), u_kyc, selected_id))
                            st.success(f"Customer #{selected_id} updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to update customer: {e}")

# -----------------------------------------------------------------------------
# TAB 4: CUSTOMER 360
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("Customer 360° Comprehensive Portfolio")
    all_cust = get_customers_df()
    if all_cust.empty:
        st.info("No customers available.")
    else:
        cust_map = {
            f"{r['customer_id']} | {r['name']} ({r['phone']})": r['customer_id']
            for _, r in all_cust.iterrows()
        }
        chosen_label = st.selectbox("Choose Customer", list(cust_map.keys()), key="c360_select")
        chosen_cid = cust_map[chosen_label]

        # Customer Portfolio Summary from View
        v_port = run_query("SELECT * FROM v_customer_portfolio WHERE customer_id = %s", (chosen_cid,))
        if not v_port.empty:
            p_row = v_port.iloc[0]
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Total Accounts", int(p_row["total_accounts"]))
            with m2:
                st.metric("Total Bank Deposits", money(p_row["total_balance"]))
            with m3:
                st.metric("Active Loans", int(p_row["active_loans_count"]))
            with m4:
                st.metric("Total Loan Outstanding", money(p_row["total_loan_outstanding"]))

        st.markdown("#### Linked Accounts")
        acc_df = run_query("""
            SELECT a.account_no AS `Account No`, t.name AS `Type`, b.name AS `Branch`,
                   a.balance AS `Balance`, a.status AS `Status`, a.opened_on AS `Opened On`
            FROM account a
            JOIN account_type t ON a.type_id = t.type_id
            JOIN branch b ON a.branch_id = b.branch_id
            WHERE a.customer_id = %s
            ORDER BY a.account_no
        """, (chosen_cid,))
        if acc_df.empty:
            st.info("This customer has no bank accounts.")
        else:
            acc_df["Balance"] = acc_df["Balance"].apply(money)
            st.dataframe(acc_df, use_container_width=True, hide_index=True)

        st.markdown("#### Loan History")
        loan_df = run_query("""
            SELECT loan_id AS `Loan ID`, account_no AS `Disbursement Acc`, principal AS `Principal`,
                   annual_rate AS `Rate (%)`, tenure_months AS `Tenure (Mo)`, emi AS `EMI`,
                   outstanding AS `Outstanding`, status AS `Status`, applied_on AS `Applied On`
            FROM loan
            WHERE customer_id = %s
            ORDER BY loan_id DESC
        """, (chosen_cid,))
        if loan_df.empty:
            st.info("No loan records found for this customer.")
        else:
            loan_df["Principal"] = loan_df["Principal"].apply(money)
            loan_df["EMI"] = loan_df["EMI"].apply(money)
            loan_df["Outstanding"] = loan_df["Outstanding"].apply(money)
            st.dataframe(loan_df, use_container_width=True, hide_index=True)
