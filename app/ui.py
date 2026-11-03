"""
Shared UI helpers and formatting utilities for Bank Management System.
File: app/ui.py
"""

import streamlit as st
from app.auth import is_logged_in, get_current_user, logout_user

def init_ui():
    """Inject custom styles and render sidebar user profile."""
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.1rem;
            font-weight: 700;
            color: #1f4e9c;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #555;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #1f4e9c;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 600;
            color: #1f4e9c;
        }
        .status-badge-verified, .status-badge-active, .status-badge-approved {
            color: #155724;
            background-color: #d4edda;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: 600;
        }
        .status-badge-pending, .status-badge-frozen {
            color: #856404;
            background-color: #fff3cd;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: 600;
        }
        .status-badge-rejected, .status-badge-closed, .status-badge-blocked {
            color: #721c24;
            background-color: #f8d7da;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Render sidebar user information if logged in
    with st.sidebar:
        if is_logged_in():
            user = get_current_user()
            st.markdown("### 🏦 BMS Portal")
            st.markdown(f"**User:** {user['name']}")
            st.markdown(f"**Role:** `{user['role']}`")
            st.markdown(f"**Branch ID:** {user['branch_id']}")
            st.divider()
            if st.button("🚪 Logout", key="bms_sidebar_logout_btn", use_container_width=True, type="secondary"):
                logout_user()
        else:
            st.markdown("### 🏦 BMS Portal")
            st.caption("Please log in to continue")

def page_header(title: str, subtitle: str = ""):
    """Render consistent page title and subtitle."""
    init_ui()
    st.markdown(f'<div class="main-header">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="sub-header">{subtitle}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="margin-bottom: 1rem;"></div>', unsafe_allow_html=True)

def show_result(ok: bool, msg: str):
    """Display clean success or error message banner."""
    if ok:
        st.success(msg)
    else:
        st.error(msg)

def money(val) -> str:
    """
    Format numeric values to Indian Rupee representation (e.g. ₹1,23,456.00).
    """
    if val is None:
        return "₹0.00"
    try:
        fval = float(val)
    except (ValueError, TypeError):
        return f"₹{val}"

    is_negative = fval < 0
    fval = abs(fval)

    parts = f"{fval:.2f}".split(".")
    integer_part = parts[0]
    decimal_part = parts[1]

    if len(integer_part) <= 3:
        formatted = integer_part
    else:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted = ",".join(groups) + "," + last_three

    res = f"₹{formatted}.{decimal_part}"
    return f"-{res}" if is_negative else res
