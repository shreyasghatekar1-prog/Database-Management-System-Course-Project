"""
Card Management Page
File: app/pages/6_Cards.py
"""

import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
from app.auth import require_role, get_current_user
from app.db import run_query, call_proc, get_accounts_df
from app.ui import page_header, show_result, money

st.set_page_config(page_title="Cards | BMS", page_icon="🪪", layout="wide")
require_role(["MANAGER", "CLERK"])
current_user = get_current_user()

page_header("🪪 Debit & Credit Cards", "Issue new banking cards, view masked card registries, and toggle card block states")

tab1, tab2, tab3 = st.tabs(["📋 All Cards", "✨ Issue Card", "🔒 Block / Unblock Card"])

def mask_card(num: str) -> str:
    """Mask a 16-digit card number to **** **** **** 1234."""
    if not num or len(num) < 16:
        return num
    return f"**** **** **** {num[-4:]}"

# -----------------------------------------------------------------------------
# TAB 1: ALL CARDS
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Issued Cards Directory")
    cards_df = run_query("""
        SELECT c.card_id AS `Card ID`, c.account_no AS `Account No`,
               cust.name AS `Cardholder`, c.card_type AS `Type`,
               c.card_number AS `Card Number`, c.expiry AS `Expiry Date`,
               c.status AS `Status`
        FROM card c
        JOIN account a ON c.account_no = a.account_no
        JOIN customer cust ON a.customer_id = cust.customer_id
        ORDER BY c.card_id DESC
    """)

    if cards_df.empty:
        st.info("No cards issued yet.")
    else:
        disp_cards = cards_df.copy()
        disp_cards["Card Number"] = disp_cards["Card Number"].apply(mask_card)
        st.dataframe(disp_cards, use_container_width=True, hide_index=True)
        st.caption(f"Total issued cards: {len(disp_cards)}")

# -----------------------------------------------------------------------------
# TAB 2: ISSUE CARD
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Issue New Card")
    active_accs = get_accounts_df(active_only=True)
    if active_accs.empty:
        st.info("No active accounts available to issue cards.")
    else:
        acc_dict = {
            f"{r['account_no']} | {r['customer_name']} ({r['account_type']})": r['account_no']
            for _, r in active_accs.iterrows()
        }
        pick_acc = st.selectbox("Select Account *", list(acc_dict.keys()), key="card_acc")
        sel_acc_no = acc_dict[pick_acc]

        card_type = st.selectbox("Card Type *", ["DEBIT", "CREDIT"])

        st.caption("Cards are automatically generated with a 16-digit number and 5-year validity.")

        if st.button("Generate & Issue Card", type="primary"):
            ok, msg = call_proc("sp_issue_card", [sel_acc_no, card_type])
            show_result(ok, msg)
            if ok:
                st.rerun()

# -----------------------------------------------------------------------------
# TAB 3: BLOCK / UNBLOCK CARD
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Update Card Security Status")
    all_cards = run_query("""
        SELECT c.card_id, c.account_no, cust.name AS cardholder,
               c.card_type, c.card_number, c.status
        FROM card c
        JOIN account a ON c.account_no = a.account_no
        JOIN customer cust ON a.customer_id = cust.customer_id
        WHERE c.status IN ('ACTIVE', 'BLOCKED')
        ORDER BY c.card_id
    """)

    if all_cards.empty:
        st.info("No active or blocked cards found.")
    else:
        card_options = {
            f"Card #{r['card_id']} | {mask_card(r['card_number'])} ({r['cardholder']}) - [{r['status']}]": r['card_id']
            for _, r in all_cards.iterrows()
        }
        pick_c = st.selectbox("Select Card", list(card_options.keys()))
        sel_card_id = card_options[pick_c]
        c_row = all_cards[all_cards["card_id"] == sel_card_id].iloc[0]

        st.write(f"**Current Status:** `{c_row['status']}` | **Cardholder:** {c_row['cardholder']}")

        target_status = "BLOCKED" if c_row["status"] == "ACTIVE" else "ACTIVE"
        btn_label = f"Block Card #{sel_card_id}" if target_status == "BLOCKED" else f"Unblock Card #{sel_card_id}"
        btn_type = "secondary" if target_status == "BLOCKED" else "primary"

        confirm_toggle = st.checkbox(f"Confirm changing status to {target_status}")

        if st.button(btn_label, type=btn_type):
            if not confirm_toggle:
                st.warning("Please confirm with the checkbox first.")
            else:
                ok, msg = call_proc("sp_set_card_status", [sel_card_id, target_status])
                show_result(ok, msg)
                if ok:
                    st.rerun()
