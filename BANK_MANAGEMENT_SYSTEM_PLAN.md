# Bank Management System: Full Implementation Spec (for Antigravity)

> **How to use this file:** Open an empty folder in Antigravity, put this file in it, and give the agent this instruction:
> *"Read BANK_MANAGEMENT_SYSTEM_PLAN.md fully. Build the project exactly as specified, phase by phase (Section 12). Finish and verify each phase before starting the next. Ask me before deviating from the spec."*

---

## 1. Project Summary

**Name:** Bank Management System (BMS)
**Course:** Database Management Systems, academic project
**Goal:** A MySQL-backed banking system where all business rules live in the database (stored procedures, triggers, constraints, views), with a Streamlit dashboard to enter data and view outputs.

**Principles**
- Simple, clean, professional. No over-engineering, no ORM, no unnecessary libraries.
- Business logic is in SQL (procedures and triggers). Python only calls them and displays results.
- Every money movement is atomic (`START TRANSACTION` / `COMMIT` / `ROLLBACK`).
- Every page validates input and shows clear success or error messages.

**Out of scope:** real payments, OTP, multi-currency, email/SMS, deployment.

---

## 2. Tech Stack

| Layer | Tool |
|---|---|
| Database | MySQL 8.0+ (InnoDB) |
| DB driver | `mysql-connector-python` |
| UI | Streamlit |
| Data handling | pandas |
| Charts | Plotly Express |
| Config | `python-dotenv` (`.env`) |
| Python | 3.10+ |

`requirements.txt`:
```
streamlit
mysql-connector-python
pandas
plotly
python-dotenv
```

`.env.example`:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=bank_db
```

---

## 3. Folder Structure

```
bank-management-system/
├── sql/
│   ├── 01_schema.sql          # database, tables, constraints, indexes
│   ├── 02_procedures.sql      # all stored procedures
│   ├── 03_triggers_views.sql  # triggers and views
│   ├── 04_sample_data.sql     # seed data
│   └── 05_test_queries.sql    # demo/viva queries
├── app/
│   ├── main.py                # entry point: login + sidebar navigation
│   ├── db.py                  # connection + helpers
│   ├── auth.py                # login + role permissions
│   ├── ui.py                  # shared UI helpers (page header, formatting)
│   └── pages/
│       ├── 1_Dashboard.py
│       ├── 2_Customers.py
│       ├── 3_Accounts.py
│       ├── 4_Transactions.py
│       ├── 5_Loans.py
│       ├── 6_Cards.py
│       ├── 7_Employees.py
│       └── 8_Reports.py
├── docs/
│   ├── ER_diagram.md          # Mermaid ER diagram
│   └── screenshots/           # filled in manually later
├── .env.example
├── .gitignore                 # .env, __pycache__, .venv
├── requirements.txt
└── README.md
```

---

## 4. Database Design

### 4.1 Entities and Relationships

| Table | Purpose |
|---|---|
| `branch` | Bank branches |
| `employee` | Staff, also used for dashboard login |
| `customer` | Bank customers with KYC status |
| `account_type` | SAVINGS, CURRENT, FIXED_DEPOSIT config |
| `account` | Customer accounts |
| `transactions` | Every money movement (ledger) |
| `loan` | Loan applications and loans |
| `loan_payment` | EMI payments |
| `card` | Debit/credit cards |
| `audit_log` | Trigger-populated audit trail |

**Relationships**
- branch 1:N employee
- employee 1:N employee (manager, self-reference)
- customer 1:N account
- account_type 1:N account
- branch 1:N account
- account 1:N transactions
- customer 1:N loan
- account 1:N loan (disbursement/EMI account)
- loan 1:N loan_payment
- account 1:N card
- employee 1:N transactions (processed by)
- employee 1:N loan (approved by)

All tables must be in **3NF**. Document that in the README.

### 4.2 `sql/01_schema.sql` (create exactly this)

```sql
DROP DATABASE IF EXISTS bank_db;
CREATE DATABASE bank_db CHARACTER SET utf8mb4;
USE bank_db;

CREATE TABLE branch (
  branch_id INT AUTO_INCREMENT PRIMARY KEY,
  name      VARCHAR(80) NOT NULL,
  city      VARCHAR(50) NOT NULL,
  ifsc      VARCHAR(11) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE employee (
  emp_id        INT AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(80) NOT NULL,
  role          ENUM('MANAGER','TELLER','LOAN_OFFICER','CLERK') NOT NULL,
  salary        DECIMAL(10,2) NOT NULL CHECK (salary > 0),
  branch_id     INT NOT NULL,
  manager_id    INT NULL,
  hire_date     DATE NOT NULL DEFAULT (CURRENT_DATE),
  username      VARCHAR(30) NOT NULL UNIQUE,
  password_hash CHAR(64) NOT NULL,          -- SHA2(password,256)
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  FOREIGN KEY (branch_id)  REFERENCES branch(branch_id),
  FOREIGN KEY (manager_id) REFERENCES employee(emp_id)
) ENGINE=InnoDB;

CREATE TABLE customer (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(80) NOT NULL,
  dob         DATE NOT NULL,
  phone       VARCHAR(15) NOT NULL UNIQUE,
  email       VARCHAR(100) NOT NULL UNIQUE,
  address     VARCHAR(200),
  kyc_status  ENUM('PENDING','VERIFIED','REJECTED') NOT NULL DEFAULT 'PENDING',
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE account_type (
  type_id       INT AUTO_INCREMENT PRIMARY KEY,
  name          ENUM('SAVINGS','CURRENT','FIXED_DEPOSIT') NOT NULL UNIQUE,
  min_balance   DECIMAL(12,2) NOT NULL DEFAULT 0,
  interest_rate DECIMAL(5,2)  NOT NULL DEFAULT 0   -- annual %
) ENGINE=InnoDB;

CREATE TABLE account (
  account_no  BIGINT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  type_id     INT NOT NULL,
  branch_id   INT NOT NULL,
  balance     DECIMAL(15,2) NOT NULL DEFAULT 0 CHECK (balance >= 0),
  status      ENUM('ACTIVE','FROZEN','CLOSED') NOT NULL DEFAULT 'ACTIVE',
  opened_on   DATE NOT NULL DEFAULT (CURRENT_DATE),
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
  FOREIGN KEY (type_id)     REFERENCES account_type(type_id),
  FOREIGN KEY (branch_id)   REFERENCES branch(branch_id)
) ENGINE=InnoDB AUTO_INCREMENT=1000100001;

CREATE TABLE transactions (
  txn_id          BIGINT AUTO_INCREMENT PRIMARY KEY,
  account_no      BIGINT NOT NULL,
  txn_type        ENUM('DEPOSIT','WITHDRAW','TRANSFER_OUT','TRANSFER_IN',
                       'LOAN_DISBURSE','LOAN_EMI','INTEREST','CHARGE') NOT NULL,
  amount          DECIMAL(15,2) NOT NULL CHECK (amount > 0),
  balance_after   DECIMAL(15,2) NOT NULL,
  related_account BIGINT NULL,
  txn_time        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  remarks         VARCHAR(200),
  done_by_emp     INT NULL,
  FOREIGN KEY (account_no)  REFERENCES account(account_no),
  FOREIGN KEY (done_by_emp) REFERENCES employee(emp_id)
) ENGINE=InnoDB;

CREATE TABLE loan (
  loan_id       INT AUTO_INCREMENT PRIMARY KEY,
  customer_id   INT NOT NULL,
  account_no    BIGINT NOT NULL,
  principal     DECIMAL(15,2) NOT NULL CHECK (principal > 0),
  annual_rate   DECIMAL(5,2)  NOT NULL CHECK (annual_rate > 0),
  tenure_months INT NOT NULL CHECK (tenure_months > 0),
  emi           DECIMAL(15,2) NOT NULL,
  outstanding   DECIMAL(15,2) NOT NULL,        -- total payable still due
  status        ENUM('PENDING','APPROVED','REJECTED','CLOSED') NOT NULL DEFAULT 'PENDING',
  applied_on    DATE NOT NULL DEFAULT (CURRENT_DATE),
  approved_by   INT NULL,
  approved_on   DATE NULL,
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
  FOREIGN KEY (account_no)  REFERENCES account(account_no),
  FOREIGN KEY (approved_by) REFERENCES employee(emp_id)
) ENGINE=InnoDB;

CREATE TABLE loan_payment (
  payment_id INT AUTO_INCREMENT PRIMARY KEY,
  loan_id    INT NOT NULL,
  amount     DECIMAL(15,2) NOT NULL CHECK (amount > 0),
  paid_on    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (loan_id) REFERENCES loan(loan_id)
) ENGINE=InnoDB;

CREATE TABLE card (
  card_id     INT AUTO_INCREMENT PRIMARY KEY,
  account_no  BIGINT NOT NULL,
  card_type   ENUM('DEBIT','CREDIT') NOT NULL,
  card_number CHAR(16) NOT NULL UNIQUE,         -- randomly generated, fake
  expiry      DATE NOT NULL,
  status      ENUM('ACTIVE','BLOCKED','EXPIRED') NOT NULL DEFAULT 'ACTIVE',
  FOREIGN KEY (account_no) REFERENCES account(account_no)
) ENGINE=InnoDB;

CREATE TABLE audit_log (
  log_id     BIGINT AUTO_INCREMENT PRIMARY KEY,
  table_name VARCHAR(40) NOT NULL,
  action     VARCHAR(20) NOT NULL,
  record_id  VARCHAR(40) NOT NULL,
  details    VARCHAR(255),
  logged_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Indexes
CREATE INDEX idx_txn_acc_time ON transactions(account_no, txn_time);
CREATE INDEX idx_account_cust ON account(customer_id);
CREATE INDEX idx_loan_cust    ON loan(customer_id);
CREATE INDEX idx_emp_branch   ON employee(branch_id);
```

---

## 5. Stored Procedures: `sql/02_procedures.sql`

**Conventions (apply to every procedure)**
- Use `DELIMITER $$`.
- Last parameter is `OUT p_msg VARCHAR(255)`. It returns `'SUCCESS: ...'` or `'ERROR: <reason>'`.
- Each procedure declares:
  ```sql
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;
  ```
- Validation failures use `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '...'`.
- Money rows are locked with `SELECT ... FOR UPDATE` inside `START TRANSACTION`.
- Every successful money movement inserts a row in `transactions` with the correct `balance_after`.

### 5.1 Reference implementation: `sp_deposit` (use as the pattern)

```sql
DELIMITER $$
CREATE PROCEDURE sp_deposit(
  IN p_acc BIGINT, IN p_amt DECIMAL(15,2), IN p_emp INT, OUT p_msg VARCHAR(255))
BEGIN
  DECLARE v_bal DECIMAL(15,2); DECLARE v_status VARCHAR(10);
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;
  START TRANSACTION;
  IF p_amt <= 0 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Amount must be positive'; END IF;
  SELECT balance, status INTO v_bal, v_status FROM account WHERE account_no = p_acc FOR UPDATE;
  IF v_status IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Account not found'; END IF;
  IF v_status <> 'ACTIVE' THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Account is not active'; END IF;
  UPDATE account SET balance = balance + p_amt WHERE account_no = p_acc;
  INSERT INTO transactions(account_no, txn_type, amount, balance_after, remarks, done_by_emp)
    VALUES (p_acc, 'DEPOSIT', p_amt, v_bal + p_amt, 'Cash deposit', p_emp);
  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Deposited ', p_amt, '. New balance ', v_bal + p_amt);
END$$
DELIMITER ;
```

### 5.2 Procedures to implement (all in the same style)

| Procedure | Parameters (before `p_msg`) | Rules |
|---|---|---|
| `sp_open_account` | customer_id, type_id, branch_id, initial_deposit, emp_id | Customer's KYC must be VERIFIED. Initial deposit must be at least the type's `min_balance`. Insert account, then insert a DEPOSIT txn if the deposit is above 0. |
| `sp_close_account` | account_no, emp_id | Balance must be 0 and no active loan on the account. Set status CLOSED. |
| `sp_set_account_status` | account_no, new_status ('ACTIVE'/'FROZEN'), emp_id | Not allowed on CLOSED accounts. |
| `sp_deposit` | account_no, amount, emp_id | As in 5.1. |
| `sp_withdraw` | account_no, amount, emp_id | Account ACTIVE. `balance - amount >= min_balance` of its account type. Insert WITHDRAW txn. |
| `sp_transfer` | from_acc, to_acc, amount, emp_id | `from <> to`. Both exist and are ACTIVE. Lock both rows in **ascending account_no order** (avoids deadlocks). Sender's balance after the debit must be at least `min_balance`. Insert TRANSFER_OUT and TRANSFER_IN rows with `related_account` set. All or nothing. |
| `sp_apply_loan` | customer_id, account_no, principal, annual_rate, tenure_months | Account must belong to the customer and be ACTIVE. Compute EMI: `r = rate/12/100; emi = principal*r*POW(1+r,n)/(POW(1+r,n)-1)` rounded to 2 decimals. `outstanding = emi*tenure`. Status PENDING. |
| `sp_approve_loan` | loan_id, emp_id | Loan must be PENDING. Approver must have role MANAGER or LOAN_OFFICER. Set APPROVED and the approval fields. Credit principal to the account and insert a LOAN_DISBURSE txn. |
| `sp_reject_loan` | loan_id, emp_id | Loan must be PENDING. Set REJECTED. |
| `sp_pay_emi` | loan_id, amount, emp_id | Loan must be APPROVED. `amount <= outstanding`. Debit the loan's account (balance must stay at or above `min_balance`). Insert a LOAN_EMI txn and a `loan_payment` row. Decrease `outstanding`. If it reaches 0, set the loan to CLOSED. |
| `sp_apply_charge` | account_no, amount, remarks, emp_id | Debit the account, no minimum-balance rule, but balance must be at least the amount. Insert a CHARGE txn. |
| `sp_credit_interest` | emp_id | Set-based, monthly. For all ACTIVE accounts whose type has `interest_rate > 0`: `interest = ROUND(balance*rate/1200, 2)`. **First** `INSERT INTO transactions ... SELECT` (`balance_after = balance + interest`), **then** `UPDATE account` to add the interest. Skip rows where interest = 0. Return the number of accounts credited. |
| `sp_issue_card` | account_no, card_type | Account ACTIVE. Generate a random 16-digit number. Expiry is today + 5 years. |
| `sp_set_card_status` | card_id, new_status | Only ACTIVE/BLOCKED. |
| `sp_add_employee`, `sp_transfer_employee` | (see Employees page) | Transfer changes `branch_id` only. |
| `sp_mini_statement` | account_no, n | Return the last n txns (`SELECT` result set). |

---

## 6. Triggers and Views: `sql/03_triggers_views.sql`

### 6.1 Triggers

| Trigger | Event | Behavior |
|---|---|---|
| `trg_account_guard` | BEFORE UPDATE ON account | If `OLD.status='CLOSED'`, signal an error ("Closed account cannot be modified"). If `NEW.status='CLOSED'` and `NEW.balance <> 0`, signal an error. |
| `trg_txn_audit` | AFTER INSERT ON transactions | Insert into `audit_log` (`'transactions'`, `'INSERT'`, txn_id, CONCAT(txn_type,' ',amount,' acc ',account_no)). |
| `trg_account_status_audit` | AFTER UPDATE ON account | If status changed, log `'account'`, `'STATUS_CHANGE'`, account_no, `'OLD->NEW'`. |
| `trg_loan_kyc` | BEFORE INSERT ON loan | Signal an error if the customer's KYC is not VERIFIED. |
| `trg_loan_audit` | AFTER UPDATE ON loan | If status changed, log it. |

### 6.2 Views

| View | Content |
|---|---|
| `v_account_summary` | account_no, customer name, type, branch, balance, status, opened_on (joins 4 tables) |
| `v_customer_portfolio` | per customer: number of accounts, total balance, number of active loans, total outstanding |
| `v_branch_performance` | per branch: customers, accounts, total deposits, number of employees |
| `v_daily_transactions` | per date and txn_type: count and total amount |
| `v_loan_outstanding` | loan_id, customer, principal, emi, outstanding, status, paid so far |
| `v_employee_hierarchy` | employee, role, branch, manager name (self-join) |

---

## 7. Seed Data: `sql/04_sample_data.sql`

Insert in FK-safe order:

- **3 branches** (e.g., Pune Main, Mumbai Central, Nashik), with unique IFSC codes.
- **8 employees**: at least 1 MANAGER per branch (manager_id NULL), plus TELLERs, a LOAN_OFFICER, and a CLERK, with manager_id set. Passwords via `SHA2('admin123',256)` for the manager and `SHA2('pass123',256)` for others.
  - Required logins: `admin` (MANAGER), `teller1` (TELLER), `loan1` (LOAN_OFFICER), `clerk1` (CLERK).
- **3 account types:** SAVINGS (min 1000, 4.0%), CURRENT (min 5000, 0%), FIXED_DEPOSIT (min 10000, 6.5%).
- **20 customers**, with realistic Indian names, unique phones/emails, **3 left with PENDING KYC** and 1 REJECTED.
- **30 accounts** spread across types/branches (inserted via direct INSERT with a starting balance, plus matching DEPOSIT transactions so the ledger matches balances).
- **~100 transactions** across the last 60 days. Use varied types (DEPOSIT, WITHDRAW, TRANSFER pairs, CHARGE) with random-looking `txn_time`. **The ledger must be consistent:** each account's final balance equals its opening deposit plus the signed sum of its transactions.
- **6 loans**: 3 APPROVED (with a few EMI payments), 2 PENDING, 1 REJECTED.
- **10 cards** (mix of DEBIT/CREDIT, 2 BLOCKED).

---

## 8. Python Layer

### 8.1 `app/db.py`

```python
import os, mysql.connector, pandas as pd
from dotenv import load_dotenv
load_dotenv()

def get_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"))

def run_query(sql, params=None) -> pd.DataFrame:
    conn = get_conn()
    try:
        return pd.read_sql(sql, conn, params=params)
    finally:
        conn.close()

def execute(sql, params=None):
    """For simple INSERT/UPDATE (customers, employees). Returns lastrowid."""
    conn = get_conn(); cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        conn.commit()
        return cur.lastrowid
    except Exception:
        conn.rollback(); raise
    finally:
        cur.close(); conn.close()

def call_proc(name, args):
    """Calls a stored procedure whose LAST parameter is OUT p_msg.
    Returns (ok: bool, message: str)."""
    conn = get_conn(); cur = conn.cursor()
    try:
        result = cur.callproc(name, list(args) + [""])
        msg = result[-1]
        return msg.startswith("SUCCESS"), msg
    finally:
        cur.close(); conn.close()

def call_proc_table(name, args) -> pd.DataFrame:
    """For procedures that return a result set (e.g. sp_mini_statement)."""
    conn = get_conn(); cur = conn.cursor()
    try:
        cur.callproc(name, list(args))
        for r in cur.stored_results():
            return pd.DataFrame(r.fetchall(), columns=r.column_names)
        return pd.DataFrame()
    finally:
        cur.close(); conn.close()
```
Always use **parameterized queries** (`%s`). Never build SQL with f-strings from user input.

### 8.2 `app/auth.py`

- Login form on `main.py`: username + password. Verify with
  `SELECT emp_id, name, role FROM employee WHERE username=%s AND password_hash=SHA2(%s,256) AND is_active=1`.
- Store `emp_id`, `name`, `role` in `st.session_state`. Logout button in the sidebar.
- `require_login()` is called at the top of every page; it calls `st.stop()` if not logged in.
- `require_role(allowed_roles)` shows `st.error("Access denied")` and stops if the role is not allowed.

**Role permissions**

| Page | MANAGER | TELLER | LOAN_OFFICER | CLERK |
|---|---|---|---|---|
| Dashboard | ✔ | ✔ | ✔ | ✔ |
| Customers | ✔ (full) | view | view | ✔ (full) |
| Accounts | ✔ | ✔ | view | view |
| Transactions | ✔ | ✔ | ✘ | ✘ |
| Loans | ✔ | ✘ | ✔ | ✘ |
| Cards | ✔ | ✘ | ✘ | ✔ |
| Employees | ✔ | ✘ | ✘ | ✘ |
| Reports | ✔ | ✘ | ✔ | ✘ |

### 8.3 `app/ui.py`
- `page_header(title, subtitle)`: consistent title, caption.
- `show_result(ok, msg)`: `st.success` or `st.error`.
- `money(x)`: formats as `₹1,23,456.00`.
- Inject a small CSS block once for a clean look (card-style metrics, tighter spacing). Keep the default Streamlit theme with a blue primary color set in `.streamlit/config.toml`:
  ```
  [theme]
  primaryColor="#1f4e9c"
  ```

---

## 9. Dashboard Pages (detailed)

Every page: `st.set_page_config(layout="wide")`, `require_login()`, `page_header(...)`, then tabs. Use `st.form` for inputs, `st.dataframe(use_container_width=True)` for tables. Dropdowns for customers/accounts use a formatted label (e.g., `"1000100001 | Rahul Patil | SAVINGS"`) mapped back to the ID. Reload data after every successful action (`st.rerun()` after showing the success message via `st.session_state`).

### 9.1 `main.py`
Login screen (if not logged in). After login: welcome card with name and role, and a quick-links summary. The sidebar shows the logged-in user and the logout button.

### 9.2 Dashboard
- Row of `st.metric` cards: Total Customers, Active Accounts, Total Deposits, Active Loans, Today's Transactions.
- Chart 1: transaction amount per day (last 30 days) by type, from `v_daily_transactions` (Plotly bar, stacked).
- Chart 2: accounts by type (pie).
- Chart 3: branch deposits (bar, from `v_branch_performance`).
- Table: 10 most recent transactions.

### 9.3 Customers
- **Tab "All Customers":** searchable table (name/phone/email filter), KYC status filter.
- **Tab "Add Customer":** name, DOB (must be 18+), phone (10 digits), email (basic format), address. Inserts with PENDING KYC. Show duplicate phone/email errors cleanly.
- **Tab "Update / KYC":** select a customer, edit phone/email/address, and change KYC status (MANAGER/CLERK only).
- **Tab "Customer 360":** select a customer, then show their accounts, loans, and the `v_customer_portfolio` row.

### 9.3b Accounts
- **Tab "All Accounts":** table from `v_account_summary` with filters (type, branch, status).
- **Tab "Open Account":** customer, type, branch, initial deposit. Calls `sp_open_account`.
- **Tab "Manage":** pick an account, then Freeze/Unfreeze (`sp_set_account_status`) or Close (`sp_close_account`), with a confirmation checkbox.
- **Tab "Balance Enquiry":** pick an account, show balance and details.

### 9.4 Transactions
- **Tab "Deposit":** account, amount. `sp_deposit`.
- **Tab "Withdraw":** account, amount. `sp_withdraw`. Show the current balance and minimum balance beside the form.
- **Tab "Transfer":** from account, to account, amount. `sp_transfer`. Show the receiver's name for confirmation before submitting.
- **Tab "Charges":** account, amount, remarks. `sp_apply_charge` (MANAGER only).
- **Tab "Monthly Interest":** button "Credit interest to all savings accounts" with a confirmation checkbox. `sp_credit_interest` (MANAGER only).
- **Tab "History":** filters (account, type, date range), table, **Download CSV** button (`st.download_button`).
- **Tab "Mini Statement":** pick an account and last N, using `sp_mini_statement`.

### 9.5 Loans
- **Tab "Apply":** customer, account (only that customer's active accounts), principal, rate, tenure. Show a live **EMI preview** computed in Python with the same formula before submitting. Calls `sp_apply_loan`.
- **Tab "Pending Approvals":** table of PENDING loans with Approve / Reject buttons (LOAN_OFFICER/MANAGER).
- **Tab "Repay EMI":** pick an APPROVED loan, show EMI and outstanding, amount defaults to EMI. `sp_pay_emi`.
- **Tab "All Loans":** `v_loan_outstanding` with a status filter, and a payment history table for the selected loan.

### 9.6 Cards
- **Issue card:** account, type. `sp_issue_card`.
- **All cards:** table with the card number **masked** (`**** **** **** 1234`), type, expiry, status.
- **Block / Unblock:** pick a card, then `sp_set_card_status`.

### 9.7 Employees (MANAGER only)
- **All employees:** table from `v_employee_hierarchy`.
- **Add employee:** name, role, salary, branch, manager, username, password (stored as `SHA2(%s,256)`).
- **Transfer branch / Deactivate:** update `branch_id` or `is_active`.
- **Branch summary:** `v_branch_performance` with a bar chart.

### 9.8 Reports
All reports show a table and a **Download CSV** button. Charts where noted.
1. Branch performance (bar chart)
2. Top 5 customers by total balance
3. Monthly transaction summary (line chart)
4. Loan portfolio: status counts and total outstanding
5. Dormant accounts (no transaction in the last 30 days)
6. Audit log viewer (filter by table and date)

---

## 10. Required SQL Features for Viva (`sql/05_test_queries.sql`)

Provide at least these, each with a one-line comment explaining the concept:
1. INNER JOIN across 4 tables (account, customer, type, branch)
2. LEFT JOIN: customers with no accounts
3. GROUP BY + HAVING: branches with deposits above a threshold
4. Subquery: accounts with balance above the average
5. Correlated subquery: latest transaction per account
6. Window function: running balance via `SUM() OVER (PARTITION BY account_no ORDER BY txn_time)`
7. Window function: `RANK()` of customers by total balance
8. Self-join: employee with manager name
9. CTE: monthly deposit totals
10. `EXISTS` / `NOT EXISTS` query
11. A transaction demo: successful transfer, then a failing transfer showing the rollback (balances unchanged)
12. Index demo: `EXPLAIN` on the transaction history query

---

## 11. Acceptance Tests (agent must run these and report results)

| # | Test | Expected |
|---|---|---|
| 1 | Withdraw more than allowed (balance below min_balance) | `ERROR`, balance unchanged |
| 2 | Transfer to the same account | `ERROR` |
| 3 | Transfer to a non-existent account | `ERROR`, sender's balance unchanged |
| 4 | Transfer valid amount | Sender down, receiver up, two txn rows |
| 5 | Deposit into FROZEN / CLOSED account | `ERROR` |
| 6 | Close an account with a non-zero balance | `ERROR` |
| 7 | Open account for a PENDING-KYC customer | `ERROR` |
| 8 | Apply loan for a PENDING-KYC customer | `ERROR` (trigger) |
| 9 | Approve loan, then check the account | Balance up by principal, LOAN_DISBURSE txn |
| 10 | Pay EMI until outstanding is 0 | Loan status CLOSED |
| 11 | Pay more than outstanding | `ERROR` |
| 12 | Credit interest | One INTEREST txn per eligible account, balances updated |
| 13 | Ledger check | For every account: sum of signed txns = balance (query provided in test file) |
| 14 | TELLER opens Loans or Employees page | "Access denied" |
| 15 | Each audit trigger | Row appears in `audit_log` |

Add the ledger-consistency check query to `05_test_queries.sql`.

---

## 12. Build Phases (Antigravity: do these in order and verify each)

**Phase 1: Setup**
Create the folder structure, `requirements.txt`, `.env.example`, `.gitignore`, and README skeleton. Create the virtual environment and install dependencies.

**Phase 2: Database**
Write `01_schema.sql` (Section 4.2) and `04_sample_data.sql` (Section 7). Run both against local MySQL. Verify row counts and the ledger consistency.
*(If MySQL isn't installed or running, stop and tell me how to install or start it. Don't switch databases.)*

**Phase 3: Database logic**
Write `02_procedures.sql` (Section 5) and `03_triggers_views.sql` (Section 6). Run them. Test every procedure from the MySQL CLI or a Python script with the acceptance tests in Section 11 (1–13, 15). Fix bugs before continuing.

**Phase 4: Python foundation**
Write `db.py`, `auth.py`, `ui.py`, `.streamlit/config.toml`, and `main.py` with login. Verify login for all four roles.

**Phase 5: Pages (in this order)**
Customers → Accounts → Transactions → Loans → Cards → Employees → Reports → Dashboard. After each page, run it with `streamlit run app/main.py` and exercise every form with a valid and an invalid input.

**Phase 6: Test and polish**
Run all acceptance tests (Section 11). Check role restrictions (test 14). Remove dead code, add docstrings or comments, and make sure every error is shown to the user as a clean message (no stack traces in the UI).

**Phase 7: Docs**
- `docs/ER_diagram.md`: a Mermaid `erDiagram` with all tables, keys, and relationships.
- `05_test_queries.sql` (Section 10).
- `README.md`: overview, features, tech stack, setup steps (below), login credentials, folder structure, normalization note (3NF), and a feature-to-transaction-type list.

**README setup steps to include**
```
1. Install MySQL 8 and Python 3.10+
2. git clone / open folder; python -m venv .venv; activate; pip install -r requirements.txt
3. Copy .env.example to .env and set DB_PASSWORD
4. mysql -u root -p < sql/01_schema.sql
   mysql -u root -p bank_db < sql/02_procedures.sql
   mysql -u root -p bank_db < sql/03_triggers_views.sql
   mysql -u root -p bank_db < sql/04_sample_data.sql
5. streamlit run app/main.py
6. Login: admin / admin123
```

---

## 13. Coding Standards for the Agent

- Keep each page file under about 250 lines. Move repeated code into `ui.py` or `db.py`.
- Use parameterized SQL everywhere.
- No hard-coded credentials. Read from `.env` only.
- Clear names, short comments on non-obvious logic, no unused imports.
- All user-facing messages should be plain English.
- Format money with 2 decimals and the ₹ symbol.
- Don't add features outside this spec. If something is ambiguous, pick the simpler option and note it in the README under "Assumptions".

---

## 14. Definition of Done

- [ ] All 4 SQL scripts run cleanly on a fresh MySQL 8 instance, in order.
- [ ] All 15 acceptance tests pass.
- [ ] Every transaction type works from the dashboard: deposit, withdraw, transfer, charge, interest, loan disbursement, EMI.
- [ ] Every management operation works: customers, accounts, loans, cards, employees.
- [ ] Role-based access works for the 4 roles.
- [ ] README, ER diagram, and test queries are complete.
- [ ] The app starts with one command (`streamlit run app/main.py`) after setup.
