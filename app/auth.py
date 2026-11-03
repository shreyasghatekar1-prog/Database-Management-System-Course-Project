"""
Authentication and role-based access control for Bank Management System.
File: app/auth.py
"""

import streamlit as st
from app.db import get_conn

def authenticate(username: str, password: str):
    """Authenticate employee against MySQL database using SHA2(password, 256)."""
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        sql = """
            SELECT emp_id, name, role, username, branch_id
            FROM employee
            WHERE username = %s
              AND password_hash = SHA2(%s, 256)
              AND is_active = 1
        """
        cur.execute(sql, (username.strip(), password.strip()))
        user = cur.fetchone()
        return user
    finally:
        cur.close()
        conn.close()

def login_user(user_dict: dict):
    """Store logged-in user in session state."""
    st.session_state["logged_in"] = True
    st.session_state["emp_id"] = user_dict["emp_id"]
    st.session_state["name"] = user_dict["name"]
    st.session_state["role"] = user_dict["role"]
    st.session_state["username"] = user_dict["username"]
    st.session_state["branch_id"] = user_dict["branch_id"]

def logout_user():
    """Clear session state and log out."""
    for key in ["logged_in", "emp_id", "name", "role", "username", "branch_id"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def is_logged_in() -> bool:
    """Check if a user is currently logged in."""
    return st.session_state.get("logged_in", False)

def get_current_user():
    """Return dict of current logged in user details."""
    if not is_logged_in():
        return None
    return {
        "emp_id": st.session_state.get("emp_id"),
        "name": st.session_state.get("name"),
        "role": st.session_state.get("role"),
        "username": st.session_state.get("username"),
        "branch_id": st.session_state.get("branch_id")
    }

def require_login():
    """Ensure user is logged in before rendering page; stop execution if not."""
    if not is_logged_in():
        st.warning("Please log in from the Home / Login page to access this system.")
        st.stop()

def require_role(allowed_roles: list):
    """Ensure current user role is within allowed_roles; display error and stop if not."""
    require_login()
    role = st.session_state.get("role")
    if role not in allowed_roles:
        st.error(f"Access denied: Role '{role}' does not have permission to access this page or operation.")
        st.stop()
