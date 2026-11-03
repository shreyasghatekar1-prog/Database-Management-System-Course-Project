"""
Database connection and execution helpers for Bank Management System.
File: app/db.py
"""

import os
import warnings
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

warnings.filterwarnings('ignore', category=UserWarning)
load_dotenv()

def get_conn():
    """Create and return a MySQL connection using .env configuration."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "bank_db")
    )

def run_query(sql: str, params=None) -> pd.DataFrame:
    """Execute a SELECT query and return results as a pandas DataFrame."""
    conn = get_conn()
    try:
        return pd.read_sql(sql, conn, params=params)
    finally:
        conn.close()

def execute(sql: str, params=None):
    """For simple INSERT/UPDATE queries. Returns lastrowid."""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        conn.commit()
        return cur.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def call_proc(name: str, args):
    """
    Calls a stored procedure whose LAST parameter is OUT p_msg.
    Returns tuple of (ok: bool, message: str).
    """
    conn = get_conn()
    cur = conn.cursor()
    try:
        result = cur.callproc(name, list(args) + [""])
        msg = str(result[-1]) if result and len(result) > 0 else ""
        conn.commit()
        return msg.startswith("SUCCESS"), msg
    except Exception as e:
        return False, f"ERROR: {str(e)}"
    finally:
        cur.close()
        conn.close()

def call_proc_table(name: str, args) -> pd.DataFrame:
    """For procedures that return a result set (e.g. sp_mini_statement)."""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.callproc(name, list(args))
        for r in cur.stored_results():
            return pd.DataFrame(r.fetchall(), columns=r.column_names)
        return pd.DataFrame()
    finally:
        cur.close()
        conn.close()

def get_customers_df(kyc_only: str = None) -> pd.DataFrame:
    """Return DataFrame of customers with optional kyc_status filter."""
    if kyc_only:
        return run_query("SELECT customer_id, name, phone, email, kyc_status, dob, address FROM customer WHERE kyc_status = %s ORDER BY customer_id", (kyc_only,))
    return run_query("SELECT customer_id, name, phone, email, kyc_status, dob, address FROM customer ORDER BY customer_id")

def get_accounts_df(active_only: bool = False, customer_id: int = None) -> pd.DataFrame:
    """Return DataFrame of accounts with balances, types, and customer details."""
    query = """
        SELECT a.account_no, a.customer_id, c.name AS customer_name,
               t.name AS account_type, t.min_balance, a.balance, a.status,
               b.name AS branch_name
        FROM account a
        JOIN customer c ON a.customer_id = c.customer_id
        JOIN account_type t ON a.type_id = t.type_id
        JOIN branch b ON a.branch_id = b.branch_id
        WHERE 1=1
    """
    params = []
    if active_only:
        query += " AND a.status = 'ACTIVE'"
    if customer_id:
        query += " AND a.customer_id = %s"
        params.append(customer_id)
    query += " ORDER BY a.account_no"
    return run_query(query, tuple(params) if params else None)

def get_branches_df() -> pd.DataFrame:
    """Return DataFrame of all branches."""
    return run_query("SELECT branch_id, name, city, ifsc FROM branch ORDER BY branch_id")

def get_account_types_df() -> pd.DataFrame:
    """Return DataFrame of account types with min balance and interest rate."""
    return run_query("SELECT type_id, name, min_balance, interest_rate FROM account_type ORDER BY type_id")

