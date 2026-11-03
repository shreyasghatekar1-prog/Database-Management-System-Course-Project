"""
Employee Management Page (Manager Only)
File: app/pages/7_Employees.py
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
import plotly.express as px
from app.auth import require_role, get_current_user
from app.db import run_query, execute, call_proc, get_branches_df
from app.ui import page_header, show_result, money

st.set_page_config(page_title="Employees | BMS", page_icon="🏢", layout="wide")
require_role(["MANAGER"])
current_user = get_current_user()

page_header("🏢 Employee & Staff Management", "Manage employee hierarchy, add new staff, transfer branches, and monitor branch capacity")

tab1, tab2, tab3, tab4 = st.tabs(["👥 Staff Hierarchy", "➕ Add Employee", "🔄 Transfer / Deactivate", "🏛️ Branch Summary"])

# -----------------------------------------------------------------------------
# TAB 1: ALL EMPLOYEES
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Bank Organizational Hierarchy")
    emp_df = run_query("""
        SELECT emp_id AS `ID`, employee_name AS `Name`, role AS `Role`,
               salary AS `Salary`, branch_name AS `Branch`, manager_name AS `Reports To`,
               hire_date AS `Hired On`, username AS `Username`,
               IF(is_active = 1, 'ACTIVE', 'INACTIVE') AS `Status`
        FROM v_employee_hierarchy
        ORDER BY branch_id, role, emp_id
    """)

    if emp_df.empty:
        st.info("No employee records found.")
    else:
        disp_emp = emp_df.copy()
        disp_emp["Salary"] = disp_emp["Salary"].apply(money)
        st.dataframe(disp_emp, use_container_width=True, hide_index=True)
        st.caption(f"Total staff members: {len(disp_emp)}")

# -----------------------------------------------------------------------------
# TAB 2: ADD EMPLOYEE
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Onboard New Employee")
    branches = get_branches_df()
    managers = run_query("SELECT emp_id, name, role FROM employee WHERE role = 'MANAGER' AND is_active = 1")

    with st.form("add_employee_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="e.g. Aniket Sawant")
            role = st.selectbox("Role *", ["TELLER", "LOAN_OFFICER", "CLERK", "MANAGER"])
            salary = st.number_input("Monthly Salary (₹) *", min_value=10000.0, value=45000.0, step=5000.0, format="%.2f")
            
            b_map = {f"{r['branch_id']} | {r['name']} ({r['city']})": r['branch_id'] for _, r in branches.iterrows()}
            b_pick = st.selectbox("Assigned Branch *", list(b_map.keys()))
            b_id = b_map[b_pick]

        with col2:
            mgr_options = {"None (Top Level Manager)": None}
            for _, r in managers.iterrows():
                mgr_options[f"Emp #{r['emp_id']} | {r['name']} ({r['role']})"] = r['emp_id']
            m_pick = st.selectbox("Reporting Manager", list(mgr_options.keys()))
            m_id = mgr_options[m_pick]

            username = st.text_input("Login Username *", placeholder="e.g. aniket_s")
            password = st.text_input("Initial Password *", type="password", placeholder="Enter secure password")

        submit_add = st.form_submit_button("Add Employee", type="primary")

        if submit_add:
            if not name.strip() or not username.strip() or not password.strip():
                st.error("Name, username, and password are required fields.")
            else:
                ok, msg = call_proc("sp_add_employee", [name.strip(), role, salary, b_id, m_id, username.strip(), password.strip()])
                show_result(ok, msg)
                if ok:
                    st.rerun()

# -----------------------------------------------------------------------------
# TAB 3: TRANSFER / DEACTIVATE
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Transfer Branch or Modify Employee Status")
    staff_df = run_query("SELECT emp_id, name, role, branch_id, is_active FROM employee ORDER BY emp_id")
    branches = get_branches_df()

    if staff_df.empty:
        st.info("No employees found.")
    else:
        st_map = {
            f"Emp #{r['emp_id']} | {r['name']} ({r['role']}) - Branch {r['branch_id']} [{'ACTIVE' if r['is_active'] else 'INACTIVE'}]": r['emp_id']
            for _, r in staff_df.iterrows()
        }
        pick_emp = st.selectbox("Select Employee", list(st_map.keys()))
        sel_eid = st_map[pick_emp]
        emp_curr = staff_df[staff_df["emp_id"] == sel_eid].iloc[0]

        op = st.radio("Select Operation", ["Transfer to another Branch", "Toggle Active / Inactive Status"])

        if op == "Transfer to another Branch":
            b_map2 = {f"{r['branch_id']} | {r['name']} ({r['city']})": r['branch_id'] for _, r in branches.iterrows() if r['branch_id'] != emp_curr['branch_id']}
            if not b_map2:
                st.info("No other branches to transfer to.")
            else:
                new_b_pick = st.selectbox("New Branch *", list(b_map2.keys()))
                new_b_id = b_map2[new_b_pick]

                if st.button("Execute Branch Transfer", type="primary"):
                    ok, msg = call_proc("sp_transfer_employee", [sel_eid, new_b_id])
                    show_result(ok, msg)
                    if ok:
                        st.rerun()

        elif op == "Toggle Active / Inactive Status":
            curr_active = bool(emp_curr["is_active"])
            new_active = not curr_active
            action_text = "Deactivate" if curr_active else "Reactivate"

            if sel_eid == current_user["emp_id"]:
                st.error("You cannot deactivate your own current login account.")
            else:
                st.write(f"Current status: `{'ACTIVE' if curr_active else 'INACTIVE'}`")
                confirm_toggle = st.checkbox(f"Confirm {action_text} Employee #{sel_eid}")
                if st.button(f"{action_text} Employee", type="secondary" if curr_active else "primary"):
                    if not confirm_toggle:
                        st.warning("Please confirm the checkbox first.")
                    else:
                        try:
                            execute("UPDATE employee SET is_active = %s WHERE emp_id = %s", (1 if new_active else 0, sel_eid))
                            st.success(f"Employee #{sel_eid} {action_text.lower()}d successfully.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to update status: {e}")

# -----------------------------------------------------------------------------
# TAB 4: BRANCH SUMMARY
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("Branch Performance & Resource Allocation")
    b_perf = run_query("SELECT * FROM v_branch_performance ORDER BY branch_id")
    if b_perf.empty:
        st.info("No branch data found.")
    else:
        disp_bp = b_perf.copy()
        disp_bp["total_deposits"] = disp_bp["total_deposits"].apply(money)
        st.dataframe(disp_bp, use_container_width=True, hide_index=True)

        fig = px.bar(
            b_perf,
            x="branch_name",
            y="total_employees",
            title="Employee Count by Branch",
            labels={"branch_name": "Branch", "total_employees": "Employees"},
            color="branch_name",
            text="total_employees"
        )
        st.plotly_chart(fig, use_container_width=True)
