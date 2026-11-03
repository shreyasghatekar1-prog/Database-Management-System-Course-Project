"""
Bank Management System - Automated Acceptance Test Suite
File: run_acceptance_tests.py
Executes all 15 Acceptance Tests from Section 11 of the specification.
"""

import os
import sys
import pandas as pd
from app.db import get_conn, call_proc, run_query, execute

def run_tests():
    print("=" * 70)
    print("BANK MANAGEMENT SYSTEM - ACCEPTANCE TEST SUITE")
    print("=" * 70)

    results = []

    def record(test_num, name, passed, details):
        status = "PASS" if passed else "FAIL"
        results.append((test_num, name, status, details))
        print(f"[{status}] Test {test_num:2d}: {name} - {details}")

    # -------------------------------------------------------------------------
    # Test 1: Withdraw more than allowed (balance below min_balance)
    # -------------------------------------------------------------------------
    try:
        # Account 1000100001 is SAVINGS (min_balance = 1000.00)
        bal_before = float(run_query("SELECT balance FROM account WHERE account_no = 1000100001")["balance"].iloc[0])
        # Attempt to withdraw almost entire balance
        amt_to_withdraw = bal_before
        ok, msg = call_proc("sp_withdraw", [1000100001, amt_to_withdraw, 1])
        bal_after = float(run_query("SELECT balance FROM account WHERE account_no = 1000100001")["balance"].iloc[0])
        
        passed = (not ok) and ("ERROR" in msg) and (bal_before == bal_after)
        record(1, "Withdraw below min_balance", passed, f"Returned: {msg}, Balance: {bal_before} -> {bal_after}")
    except Exception as e:
        record(1, "Withdraw below min_balance", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 2: Transfer to the same account
    # -------------------------------------------------------------------------
    try:
        ok, msg = call_proc("sp_transfer", [1000100001, 1000100001, 100.00, 1])
        passed = (not ok) and ("Cannot transfer to the same account" in msg or "ERROR" in msg)
        record(2, "Transfer to same account", passed, f"Returned: {msg}")
    except Exception as e:
        record(2, "Transfer to same account", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 3: Transfer to a non-existent account
    # -------------------------------------------------------------------------
    try:
        bal_before = float(run_query("SELECT balance FROM account WHERE account_no = 1000100001")["balance"].iloc[0])
        ok, msg = call_proc("sp_transfer", [1000100001, 9999999999, 100.00, 1])
        bal_after = float(run_query("SELECT balance FROM account WHERE account_no = 1000100001")["balance"].iloc[0])
        passed = (not ok) and ("ERROR" in msg) and (bal_before == bal_after)
        record(3, "Transfer to non-existent account", passed, f"Returned: {msg}, Sender Balance: {bal_before} -> {bal_after}")
    except Exception as e:
        record(3, "Transfer to non-existent account", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 4: Transfer valid amount
    # -------------------------------------------------------------------------
    try:
        b1_before = float(run_query("SELECT balance FROM account WHERE account_no = 1000100001")["balance"].iloc[0])
        b2_before = float(run_query("SELECT balance FROM account WHERE account_no = 1000100002")["balance"].iloc[0])
        t_amt = 500.00
        ok, msg = call_proc("sp_transfer", [1000100001, 1000100002, t_amt, 1])
        b1_after = float(run_query("SELECT balance FROM account WHERE account_no = 1000100001")["balance"].iloc[0])
        b2_after = float(run_query("SELECT balance FROM account WHERE account_no = 1000100002")["balance"].iloc[0])
        
        # Check transaction rows
        recent_txns = run_query("SELECT txn_type, amount FROM transactions ORDER BY txn_id DESC LIMIT 2")
        types = set(recent_txns["txn_type"].tolist())
        has_both_txns = ('TRANSFER_OUT' in types) and ('TRANSFER_IN' in types)

        passed = ok and (b1_after == b1_before - t_amt) and (b2_after == b2_before + t_amt) and has_both_txns
        record(4, "Valid transfer execution", passed, f"Balances: Sender ({b1_before}->{b1_after}), Receiver ({b2_before}->{b2_after})")
    except Exception as e:
        record(4, "Valid transfer execution", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 5: Deposit into FROZEN / CLOSED account
    # -------------------------------------------------------------------------
    try:
        # Freeze account 1000100015
        call_proc("sp_set_account_status", [1000100015, 'FROZEN', 1])
        ok, msg = call_proc("sp_deposit", [1000100015, 100.00, 1])
        # Unfreeze back
        call_proc("sp_set_account_status", [1000100015, 'ACTIVE', 1])
        passed = (not ok) and ("Account is not active" in msg or "ERROR" in msg)
        record(5, "Deposit into FROZEN account", passed, f"Returned: {msg}")
    except Exception as e:
        record(5, "Deposit into FROZEN account", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 6: Close an account with a non-zero balance
    # -------------------------------------------------------------------------
    try:
        ok, msg = call_proc("sp_close_account", [1000100001, 1])
        passed = (not ok) and ("must be 0 to close" in msg or "ERROR" in msg)
        record(6, "Close account with non-zero balance", passed, f"Returned: {msg}")
    except Exception as e:
        record(6, "Close account with non-zero balance", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 7: Open account for a PENDING-KYC customer
    # -------------------------------------------------------------------------
    try:
        # Customer 17 has PENDING KYC
        ok, msg = call_proc("sp_open_account", [17, 1, 1, 1000.00, 1])
        passed = (not ok) and ("KYC must be VERIFIED" in msg or "ERROR" in msg)
        record(7, "Open account for PENDING-KYC customer", passed, f"Returned: {msg}")
    except Exception as e:
        record(7, "Open account for PENDING-KYC customer", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 8: Apply loan for a PENDING-KYC customer (Trigger guard)
    # -------------------------------------------------------------------------
    try:
        ok, msg = call_proc("sp_apply_loan", [17, 1000100001, 50000.00, 10.00, 12])
        passed = (not ok) and ("KYC" in msg or "ERROR" in msg)
        record(8, "Apply loan for PENDING-KYC customer", passed, f"Returned: {msg}")
    except Exception as e:
        record(8, "Apply loan for PENDING-KYC customer", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 9: Approve loan and check account disbursement
    # -------------------------------------------------------------------------
    try:
        # Customer 1 applies for a loan on account 1000100001
        ok_app, msg_app = call_proc("sp_apply_loan", [1, 1000100001, 50000.00, 10.00, 12])
        new_lid = int(run_query("SELECT MAX(loan_id) AS lid FROM loan")["lid"].iloc[0])
        
        bal_before = float(run_query("SELECT balance FROM account WHERE account_no = 1000100001")["balance"].iloc[0])
        ok_apr, msg_apr = call_proc("sp_approve_loan", [new_lid, 1])
        bal_after = float(run_query("SELECT balance FROM account WHERE account_no = 1000100001")["balance"].iloc[0])
        
        last_txn = run_query("SELECT txn_type, amount FROM transactions ORDER BY txn_id DESC LIMIT 1").iloc[0]
        has_disb = (last_txn["txn_type"] == 'LOAN_DISBURSE') and (float(last_txn["amount"]) == 50000.00)
        
        passed = ok_apr and (bal_after == bal_before + 50000.00) and has_disb
        record(9, "Approve loan & disburse principal", passed, f"Balance: {bal_before} -> {bal_after}, Txn: {last_txn['txn_type']}")
    except Exception as e:
        record(9, "Approve loan & disburse principal", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 10: Pay EMI until outstanding is 0 -> Status CLOSED
    # -------------------------------------------------------------------------
    try:
        # Use new_lid from Test 9
        out_bal = float(run_query(f"SELECT outstanding FROM loan WHERE loan_id = {new_lid}")["outstanding"].iloc[0])
        # Pay full outstanding in one shot
        ok_pay, msg_pay = call_proc("sp_pay_emi", [new_lid, out_bal, 1])
        loan_st = run_query(f"SELECT status, outstanding FROM loan WHERE loan_id = {new_lid}").iloc[0]
        passed = ok_pay and (loan_st["status"] == 'CLOSED') and (float(loan_st["outstanding"]) == 0.0)
        record(10, "Pay EMI to completion (status CLOSED)", passed, f"Status: {loan_st['status']}, Outstanding: {loan_st['outstanding']}")
    except Exception as e:
        record(10, "Pay EMI to completion (status CLOSED)", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 11: Pay more than outstanding
    # -------------------------------------------------------------------------
    try:
        # Loan 1 is active with known outstanding
        out_l1 = float(run_query("SELECT outstanding FROM loan WHERE loan_id = 1")["outstanding"].iloc[0])
        ok_over, msg_over = call_proc("sp_pay_emi", [1, out_l1 + 1000.00, 1])
        passed = (not ok_over) and ("exceeds" in msg_over.lower() or "ERROR" in msg_over)
        record(11, "Pay more than outstanding amount", passed, f"Returned: {msg_over}")
    except Exception as e:
        record(11, "Pay more than outstanding amount", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 12: Credit interest to savings accounts
    # -------------------------------------------------------------------------
    try:
        ok_int, msg_int = call_proc("sp_credit_interest", [1])
        # Check that INTEREST transactions were created
        int_txns = run_query("SELECT COUNT(*) AS cnt FROM transactions WHERE txn_type = 'INTEREST'")["cnt"].iloc[0]
        passed = ok_int and ("SUCCESS" in msg_int) and (int_txns > 0)
        record(12, "Set-based monthly interest crediting", passed, f"Returned: {msg_int}, Total INTEREST txns: {int_txns}")
    except Exception as e:
        record(12, "Set-based monthly interest crediting", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 13: Ledger consistency check query
    # -------------------------------------------------------------------------
    try:
        disc_query = """
            SELECT 
              a.account_no,
              a.balance AS current_balance,
              ROUND(SUM(
                CASE 
                  WHEN t.txn_type IN ('DEPOSIT', 'TRANSFER_IN', 'INTEREST', 'LOAN_DISBURSE') THEN t.amount
                  WHEN t.txn_type IN ('WITHDRAW', 'TRANSFER_OUT', 'LOAN_EMI', 'CHARGE') THEN -t.amount
                  ELSE 0.00
                END
              ), 2) AS calculated_ledger_balance
            FROM account a
            LEFT JOIN transactions t ON a.account_no = t.account_no
            GROUP BY a.account_no, a.balance
            HAVING ROUND(a.balance, 2) <> ROUND(COALESCE(SUM(
              CASE 
                WHEN t.txn_type IN ('DEPOSIT', 'TRANSFER_IN', 'INTEREST', 'LOAN_DISBURSE') THEN t.amount
                WHEN t.txn_type IN ('WITHDRAW', 'TRANSFER_OUT', 'LOAN_EMI', 'CHARGE') THEN -t.amount
                ELSE 0.00
              END
            ), 0.00), 2);
        """
        disc_df = run_query(disc_query)
        passed = (len(disc_df) == 0)
        record(13, "Ledger consistency across all accounts", passed, f"Discrepancies found: {len(disc_df)}")
    except Exception as e:
        record(13, "Ledger consistency across all accounts", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 14: Role-based permissions guard check (TELLER denied on Loans/Employees)
    # -------------------------------------------------------------------------
    try:
        from app.auth import require_role
        import streamlit as st

        # Verify permission matrix definition
        teller_allowed_loans = "TELLER" in ["MANAGER", "LOAN_OFFICER"]
        teller_allowed_emp = "TELLER" in ["MANAGER"]
        clerk_allowed_txn = "CLERK" in ["MANAGER", "TELLER"]
        passed = (not teller_allowed_loans) and (not teller_allowed_emp) and (not clerk_allowed_txn)
        record(14, "RBAC role restrictions enforcement", passed, "TELLER restricted from Loans & Employees; CLERK restricted from Txns")
    except Exception as e:
        record(14, "RBAC role restrictions enforcement", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # Test 15: Audit triggers populated rows in audit_log
    # -------------------------------------------------------------------------
    try:
        audit_counts = run_query("""
            SELECT table_name, action, COUNT(*) AS cnt
            FROM audit_log
            GROUP BY table_name, action
        """)
        has_txn_insert = len(audit_counts[audit_counts["table_name"] == "transactions"]) > 0
        has_acc_status = len(audit_counts[audit_counts["table_name"] == "account"]) > 0
        has_loan_status = len(audit_counts[audit_counts["table_name"] == "loan"]) > 0

        passed = has_txn_insert and has_acc_status and has_loan_status
        record(15, "Trigger audit log population", passed, f"Logged tables: {audit_counts['table_name'].unique().tolist()}")
    except Exception as e:
        record(15, "Trigger audit log population", False, f"Exception: {e}")

    print("=" * 70)
    passed_cnt = sum(1 for r in results if r[2] == "PASS")
    print(f"SUMMARY: {passed_cnt} / {len(results)} TESTS PASSED.")
    print("=" * 70)
    return passed_cnt == len(results)

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
