# Gamma.app Master Prompt & 28-Slide Deck Content
## How to Use in Gamma (gamma.app)
1. Open **Gamma.app** -> Click **Create New (AI)** -> Select **Paste in text** (or **Import file** and upload this `.md` file).
2. Choose **Presentation** -> Select **Preserve this exact text** (or **Condense / Expand** with **Card-by-Card** split on `---`).
3. In Gamma's **Additional Instructions / Prompt box**, paste the **Gamma Style & Transition Directive** below, then click **Generate** (set card count to **28 cards**).

---

## Gamma Style, Layout & Transition Directive (Paste in Gamma Settings)
```text
Create a 28-slide technical academic presentation for a Database Management Systems (DBMS) Course Project titled "Bank Management System (bank_db): MySQL 8.0 Database Architecture, Queries & Transactional Logic".
- Audience: Computer Engineering DBMS Faculty & Evaluators.
- Focus: 100% on MySQL 8.0 database engineering, 3NF schema, DDL constraints, 17 Stored Procedures, ACID transactions, row-level locking, deadlock prevention, 5 Triggers, 6 Views, Indexes, and advanced DQL/CTE/Window queries. Mention the frontend ONLY once in the Tech Stack table and nowhere else.
- Visual Theme: Dark Navy & Royal Blue (#0F1B33, #1F4E9C) with clean monospace SQL code blocks, structured comparison tables, callout boxes, and flow diagrams.
- Slide Transitions: Enable smooth "Fade" and "Slide-Up" card transitions between slides, with progressive step-by-step reveal on code blocks and transaction flow diagrams.
- Split slides strictly at each "---" divider (28 slides total). Preserve all SQL queries verbatim inside syntax-highlighted SQL code blocks.
```

---

## Full 28-Slide Content (Copy Everything Below into Gamma)

# Slide 1: Title Slide
## Bank Management System (`bank_db`)
### Relational Database Architecture, Transactional Stored Procedures, Triggers & Advanced SQL Logic
- **Course:** Database Management Systems (DBMS) Course Project
- **Department:** Computer Engineering | Vishwakarma Institute of Technology, Pune
- **Academic Year:** 2026–2027
- **Core Database Engine:** MySQL 8.0 (InnoDB Storage Engine, UTF8MB4)
- **Submitted By:** [Name & Roll No.]

---

# Slide 2: Problem Statement & Database-First Philosophy
## Why Banking Requires Strict Database-Level Logic
- **Core Banking Challenges:**
  - Partial money updates during power/network failure lead to inconsistent ledgers.
  - Concurrent bi-directional fund transfers risk race conditions and deadlocks.
  - Application-only validation can be bypassed by direct SQL access or buggy scripts.
  - Lack of automated auditing makes regulatory compliance and fraud tracking impossible.
- **Our Architectural Solution (`bank_db`):**
  - **100% Database-First Business Logic:** Every financial rule lives inside MySQL 8.0 (`InnoDB`) via **17 Stored Procedures**, **5 Automated Triggers**, **6 Relational Views**, and **Declarative Constraints**.
  - **Mathematical Ledger Invariant:** Every account's current balance strictly equals the signed sum of all its ledger transactions.

---

# Slide 3: System Technology Stack
## Database-Centric Architecture Overview
| Layer | Technology Used | Role in Project |
| :--- | :--- | :--- |
| **RDBMS Engine** | **MySQL 8.0+ (InnoDB)** | Core ACID storage, row-level locking, FK enforcement |
| **Database Logic** | **MySQL Stored Procedures (17)** | Atomic money movements, loan EMI math, batch interest |
| **Event Automation** | **MySQL Triggers (5)** | Immutable audit logging, KYC & closed-account guards |
| **Virtual Schemas** | **MySQL Views (6)** | Pre-joined analytical & operational reporting layers |
| **Query Optimization** | **B-Tree Composite Indexes (4)** | High-speed ledger range scans & FK join acceleration |
| **DB Connectivity** | **`mysql-connector-python` + `.env`** | Parameterized `%s` SQL execution & `callproc` |
| **Frontend Stack** | **Python 3.10+, Streamlit, Pandas, Plotly** | *(Thin client interface only — zero business logic in UI)* |

---

# Slide 4: Conceptual & Logical Database Design (10 Entities)
## Core Entities in `bank_db`
| # | Table Name | Primary Key | Purpose & Role in Schema |
| :--- | :--- | :--- | :--- |
| 1 | `branch` | `branch_id` | Bank branches with unique 11-char `ifsc` code |
| 2 | `employee` | `emp_id` | Staff credentials (`SHA2`), roles, and self-FK `manager_id` |
| 3 | `customer` | `customer_id` | Customer demographics & `kyc_status` (`PENDING`/`VERIFIED`/`REJECTED`) |
| 4 | `account_type` | `type_id` | Product rules (`SAVINGS`, `CURRENT`, `FIXED_DEPOSIT`, `min_balance`, `interest_rate`) |
| 5 | `account` | `account_no` | Customer accounts (`AUTO_INCREMENT = 1000100001`), balance & state |
| 6 | `transactions` | `txn_id` | Immutable financial ledger recording every credit/debit & `balance_after` |
| 7 | `loan` | `loan_id` | Loan applications, reducing-balance `emi`, `outstanding`, approval tracking |
| 8 | `loan_payment` | `payment_id` | Individual loan EMI repayment records |
| 9 | `card` | `card_id` | 16-digit `DEBIT`/`CREDIT` cards linked to active accounts |
| 10 | `audit_log` | `log_id` | Trigger-populated compliance trail of all state changes |

---

# Slide 5: Entity Relationship (ER) Diagram & Cardinalities
## Relational Mapping Across All 10 Tables
- **Key Cardinalities:**
  - `branch` (1) $\rightarrow$ (N) `employee` | `branch` (1) $\rightarrow$ (N) `account`
  - `employee` (1) $\rightarrow$ (N) `employee` *(Self-referencing hierarchy via `manager_id`)*
  - `customer` (1) $\rightarrow$ (N) `account` | `customer` (1) $\rightarrow$ (N) `loan`
  - `account_type` (1) $\rightarrow$ (N) `account`
  - `account` (1) $\rightarrow$ (N) `transactions` | `account` (1) $\rightarrow$ (N) `card` | `account` (1) $\rightarrow$ (N) `loan`
  - `loan` (1) $\rightarrow$ (N) `loan_payment`

```sql
-- Summary of Referential Integrity Links
employee.branch_id       -> branch.branch_id
employee.manager_id      -> employee.emp_id (Self-FK)
account.customer_id      -> customer.customer_id
account.type_id          -> account_type.type_id
account.branch_id        -> branch.branch_id
transactions.account_no  -> account.account_no
transactions.done_by_emp -> employee.emp_id
loan.customer_id         -> customer.customer_id
loan.account_no          -> account.account_no
loan.approved_by         -> employee.emp_id
loan_payment.loan_id     -> loan.loan_id
card.account_no          -> account.account_no
```

---

# Slide 6: Database Normalization to Third Normal Form (3NF)
## Eliminating Redundancy & Update Anomalies
- **First Normal Form (1NF):**
  - Every column stores atomic scalar values (no repeating groups or comma-separated lists).
  - Every table defines an explicit Primary Key (`branch_id`, `emp_id`, `customer_id`, `account_no`, `txn_id`, etc.).
- **Second Normal Form (2NF):**
  - All non-key attributes are fully functionally dependent on the complete primary key; zero partial dependencies exist.
- **Third Normal Form (3NF):**
  - Zero transitive dependencies ($X \rightarrow Y \rightarrow Z$):
    - **Product Isolation:** `min_balance` and `interest_rate` depend on `type_id` and are isolated in `account_type` rather than duplicated across `account` rows.
    - **Branch Isolation:** `city` and `ifsc` are isolated in `branch` rather than repeated in `account` or `employee`.
    - **Customer Isolation:** Contact and KYC attributes live solely in `customer`.

---

# Slide 7: DDL Schema Part 1 — Organizational & Customer Tables
## `branch`, `employee`, `customer`, and `account_type` (`sql/01_schema.sql`)
```sql
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
  password_hash CHAR(64) NOT NULL,          -- SHA2(password, 256)
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
  interest_rate DECIMAL(5,2)  NOT NULL DEFAULT 0
) ENGINE=InnoDB;
```

---

# Slide 8: DDL Schema Part 2 — Core Banking & Ledger Tables
## `account`, `transactions`, `loan`, `loan_payment`, `card`, `audit_log`
```sql
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
  outstanding   DECIMAL(15,2) NOT NULL,
  status        ENUM('PENDING','APPROVED','REJECTED','CLOSED') NOT NULL DEFAULT 'PENDING',
  applied_on    DATE NOT NULL DEFAULT (CURRENT_DATE),
  approved_by   INT NULL,
  approved_on   DATE NULL,
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
  FOREIGN KEY (account_no)  REFERENCES account(account_no),
  FOREIGN KEY (approved_by) REFERENCES employee(emp_id)
) ENGINE=InnoDB;
```

---

# Slide 9: Declarative Integrity Constraints & Indexing Strategy
## Enforcing Domain Rules & Accelerating Lookups
- **Declarative Constraints Used:**
  - **`CHECK` Constraints:** `salary > 0`, `balance >= 0`, `amount > 0`, `principal > 0`, `annual_rate > 0`, `tenure_months > 0`.
  - **`ENUM` State Machines:** Restrict `role`, `kyc_status`, `account.status`, `txn_type`, `loan.status`, and `card.status` to valid transitions.
  - **`UNIQUE` Keys:** Enforce uniqueness on `ifsc`, `username`, `phone`, `email`, `account_type.name`, and `card_number`.
- **Performance Indexes (`sql/01_schema.sql`):**
```sql
-- Composite index for account statement queries filtered by account_no and ordered by time
CREATE INDEX idx_txn_acc_time ON transactions(account_no, txn_time);

-- Foreign-key indexes for rapid customer portfolio & branch hierarchy joins
CREATE INDEX idx_account_cust ON account(customer_id);
CREATE INDEX idx_loan_cust    ON loan(customer_id);
CREATE INDEX idx_emp_branch   ON employee(branch_id);
```

---

# Slide 10: Stored Procedure Architecture & Exception Handling Pattern
## Uniform ACID Contract Across All 17 Stored Procedures (`sql/02_procedures.sql`)
- Every mutating stored procedure follows a strict 5-step transactional template:
  1. **Declare `EXIT HANDLER FOR SQLEXCEPTION`** that captures `MESSAGE_TEXT`, formats `'ERROR: ...'` into `OUT p_msg`, and executes `ROLLBACK`.
  2. **Begin explicit transaction** (`START TRANSACTION;`).
  3. **Acquire row-level lock** (`SELECT ... FOR UPDATE`) on target monetary rows.
  4. **Validate business rules** and abort via `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '...'` on violation.
  5. **Update balance + insert ledger row + `COMMIT`** and return `'SUCCESS: ...'`.

```sql
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
  GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
  SET p_msg = CONCAT('ERROR: ', p_msg);
  ROLLBACK;
END;
```

---

# Slide 11: Account Lifecycle Stored Procedures
## `sp_open_account` & `sp_close_account`
- **`sp_open_account` Rules:** Customer must exist with `kyc_status = 'VERIFIED'`; `p_initial_deposit >= min_balance` of the chosen `account_type`; inserts `account` and logs initial `DEPOSIT` transaction atomically.
- **`sp_close_account` Rules:** Locks account row, verifies `balance = 0` and zero `PENDING`/`APPROVED` loans before setting `status = 'CLOSED'`.

```sql
CREATE PROCEDURE sp_close_account(IN p_acc BIGINT, IN p_emp INT, OUT p_msg VARCHAR(255))
BEGIN
  DECLARE v_bal DECIMAL(15,2); DECLARE v_status VARCHAR(10); DECLARE v_active_loans INT DEFAULT 0;
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg); ROLLBACK;
  END;

  START TRANSACTION;
  SELECT balance, status INTO v_bal, v_status FROM account WHERE account_no = p_acc FOR UPDATE;
  IF v_status IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account not found'; END IF;
  IF v_status = 'CLOSED' THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account is already CLOSED'; END IF;
  IF v_bal <> 0 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account balance must be 0 to close'; END IF;

  SELECT COUNT(*) INTO v_active_loans FROM loan
  WHERE account_no = p_acc AND status IN ('PENDING', 'APPROVED');
  IF v_active_loans > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account has active or pending loans and cannot be closed';
  END IF;

  UPDATE account SET status = 'CLOSED' WHERE account_no = p_acc;
  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Account ', p_acc, ' closed successfully');
END$$
```

---

# Slide 12: Core Deposit & Withdrawal Stored Procedures
## `sp_deposit` & `sp_withdraw` with Minimum Balance Enforcement
```sql
CREATE PROCEDURE sp_withdraw(
  IN p_acc BIGINT, IN p_amt DECIMAL(15,2), IN p_emp INT, OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_bal DECIMAL(15,2); DECLARE v_status VARCHAR(10); DECLARE v_min_bal DECIMAL(12,2);
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg); ROLLBACK;
  END;

  START TRANSACTION;
  IF p_amt <= 0 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Amount must be positive'; END IF;

  -- Lock account row and fetch product minimum balance via INNER JOIN
  SELECT a.balance, a.status, t.min_balance
  INTO v_bal, v_status, v_min_bal
  FROM account a JOIN account_type t ON a.type_id = t.type_id
  WHERE a.account_no = p_acc FOR UPDATE;

  IF v_status IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account not found'; END IF;
  IF v_status <> 'ACTIVE' THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account is not active'; END IF;
  IF (v_bal - p_amt) < v_min_bal THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient balance. Must maintain minimum balance';
  END IF;

  UPDATE account SET balance = balance - p_amt WHERE account_no = p_acc;
  INSERT INTO transactions(account_no, txn_type, amount, balance_after, remarks, done_by_emp)
  VALUES (p_acc, 'WITHDRAW', p_amt, v_bal - p_amt, 'Cash withdrawal', p_emp);

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Withdrawn ', p_amt, '. New balance ', v_bal - p_amt);
END$$
```

---

# Slide 13: Atomic Fund Transfer & Deadlock Prevention (`sp_transfer`)
## Ascending Primary-Key Lock Ordering in MySQL InnoDB
- **The Concurrency Problem:** If Transaction 1 transfers from Account `1000100005` $\rightarrow$ `1000100001` while Transaction 2 transfers from `1000100001` $\rightarrow$ `1000100005`, locking `p_from_acc` first causes a circular wait (**Deadlock**).
- **Our Solution in `sp_transfer`:** Always acquire `FOR UPDATE` row locks in **ascending `account_no` order** (`IF p_from_acc < p_to_acc`), eliminating circular wait conditions!

```sql
-- Deadlock-Free Row Locking inside sp_transfer
IF p_from_acc < p_to_acc THEN
  SELECT a.balance, a.status, t.min_balance INTO v_from_bal, v_from_status, v_from_min_bal
  FROM account a JOIN account_type t ON a.type_id = t.type_id WHERE a.account_no = p_from_acc FOR UPDATE;

  SELECT balance, status INTO v_to_bal, v_to_status
  FROM account WHERE account_no = p_to_acc FOR UPDATE;
ELSE
  SELECT balance, status INTO v_to_bal, v_to_status
  FROM account WHERE account_no = p_to_acc FOR UPDATE;

  SELECT a.balance, a.status, t.min_balance INTO v_from_bal, v_from_status, v_from_min_bal
  FROM account a JOIN account_type t ON a.type_id = t.type_id WHERE a.account_no = p_from_acc FOR UPDATE;
END IF;

-- Atomic Debit + TRANSFER_OUT and Credit + TRANSFER_IN
UPDATE account SET balance = balance - p_amt WHERE account_no = p_from_acc;
INSERT INTO transactions(account_no, txn_type, amount, balance_after, related_account, remarks, done_by_emp)
VALUES (p_from_acc, 'TRANSFER_OUT', p_amt, v_from_bal - p_amt, p_to_acc, CONCAT('Transfer to ', p_to_acc), p_emp);

UPDATE account SET balance = balance + p_amt WHERE account_no = p_to_acc;
INSERT INTO transactions(account_no, txn_type, amount, balance_after, related_account, remarks, done_by_emp)
VALUES (p_to_acc, 'TRANSFER_IN', p_amt, v_to_bal + p_amt, p_from_acc, CONCAT('Transfer from ', p_from_acc), p_emp);
```

---

# Slide 14: Set-Based Monthly Interest Calculation (`sp_credit_interest`)
## Temporary Table Batch Processing Without Cursors
- Instead of slow row-by-row cursors, `sp_credit_interest` uses a **set-based temporary table (`tmp_interest`)** to compute monthly interest $\text{Interest} = \text{ROUND}\left(\text{balance} \times \frac{\text{interest\_rate}}{1200}, 2\right)$ for all eligible `ACTIVE` accounts in a single atomic transaction:

```sql
CREATE PROCEDURE sp_credit_interest(IN p_emp INT, OUT p_msg VARCHAR(255))
BEGIN
  DECLARE v_count INT DEFAULT 0;
  -- [SQLEXCEPTION Rollback Handler]
  START TRANSACTION;

  DROP TEMPORARY TABLE IF EXISTS tmp_interest;
  CREATE TEMPORARY TABLE tmp_interest AS
  SELECT a.account_no, a.balance,
         ROUND(a.balance * (t.interest_rate / 1200.0), 2) AS interest
  FROM account a JOIN account_type t ON a.type_id = t.type_id
  WHERE a.status = 'ACTIVE' AND t.interest_rate > 0
    AND ROUND(a.balance * (t.interest_rate / 1200.0), 2) > 0;

  SELECT COUNT(*) INTO v_count FROM tmp_interest;

  IF v_count > 0 THEN
    INSERT INTO transactions(account_no, txn_type, amount, balance_after, remarks, done_by_emp)
    SELECT ti.account_no, 'INTEREST', ti.interest, ti.balance + ti.interest,
           'Monthly interest credit', p_emp
    FROM tmp_interest ti;

    UPDATE account a JOIN tmp_interest ti ON a.account_no = ti.account_no
    SET a.balance = a.balance + ti.interest;
  END IF;

  DROP TEMPORARY TABLE IF EXISTS tmp_interest;
  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Interest credited to ', v_count, ' account(s)');
END$$
```

---

# Slide 15: Loan Origination & Reducing-Balance EMI Math (`sp_apply_loan`)
## In-Database Financial Computation
- Uses the standard reducing-balance amortization formula directly inside MySQL:
  $$r = \frac{\text{annual\_rate}}{12 \times 100}, \quad \text{EMI} = \frac{P \cdot r \cdot (1+r)^n}{(1+r)^n - 1}, \quad \text{Outstanding} = \text{EMI} \times n$$

```sql
-- Excerpt from sp_apply_loan (sql/02_procedures.sql)
SELECT customer_id, status INTO v_owner, v_status FROM account WHERE account_no = p_account_no;
IF v_owner <> p_customer_id THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account does not belong to customer';
END IF;
IF v_status <> 'ACTIVE' THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account is not active';
END IF;

-- Reducing-balance EMI calculation using POW() and ROUND()
SET v_r = (p_annual_rate / 12.0) / 100.0;
SET v_pow = POW(1.0 + v_r, p_tenure_months);
SET v_emi = ROUND((p_principal * v_r * v_pow) / (v_pow - 1.0), 2);
SET v_outstanding = ROUND(v_emi * p_tenure_months, 2);

INSERT INTO loan(customer_id, account_no, principal, annual_rate, tenure_months,
                 emi, outstanding, status, applied_on)
VALUES (p_customer_id, p_account_no, p_principal, p_annual_rate, p_tenure_months,
        v_emi, v_outstanding, 'PENDING', CURRENT_DATE);
```

---

# Slide 16: Loan Approval, Disbursement & Auto-Closure (`sp_approve_loan` & `sp_pay_emi`)
## Role-Checked Disbursement & EMI Repayment Lifecycle
- **`sp_approve_loan`:** Verifies employee role is `MANAGER` or `LOAN_OFFICER`, transitions loan from `PENDING` $\rightarrow$ `APPROVED`, credits `principal` to the customer's account, and logs a `LOAN_DISBURSE` transaction.
- **`sp_pay_emi`:** Verifies `p_amount <= outstanding` and `(balance - p_amount) >= min_balance`, debits the account, inserts `LOAN_EMI` + `loan_payment`, and **automatically closes the loan** when `outstanding` reaches `0`:

```sql
-- Excerpt from sp_pay_emi (sql/02_procedures.sql)
UPDATE account SET balance = balance - p_amount WHERE account_no = v_account_no;

INSERT INTO transactions(account_no, txn_type, amount, balance_after, remarks, done_by_emp)
VALUES (v_account_no, 'LOAN_EMI', p_amount, v_bal - p_amount, CONCAT('EMI for Loan #', p_loan_id), p_emp);

INSERT INTO loan_payment(loan_id, amount, paid_on)
VALUES (p_loan_id, p_amount, CURRENT_TIMESTAMP);

SET v_new_outstanding = v_outstanding - p_amount;
UPDATE loan
SET outstanding = v_new_outstanding,
    status = IF(v_new_outstanding <= 0, 'CLOSED', status)
WHERE loan_id = p_loan_id;
```

---

# Slide 17: Card Issuance, Staff Hierarchy & Mini-Statement Procedures
## Completing the 17 Stored Procedures Suite
- **`sp_issue_card`:** Generates a collision-free random 16-digit card number using a `REPEAT ... UNTIL` loop and sets expiry to `DATE_ADD(CURRENT_DATE, INTERVAL 5 YEAR)`:
```sql
REPEAT
  SET v_card_num = CONCAT(
    LPAD(FLOOR(RAND() * 100000000), 8, '0'),
    LPAD(FLOOR(RAND() * 100000000), 8, '0')
  );
  SELECT COUNT(*) INTO v_exists FROM card WHERE card_number = v_card_num;
UNTIL v_exists = 0 END REPEAT;

INSERT INTO card(account_no, card_type, card_number, expiry, status)
VALUES (p_acc, p_card_type, v_card_num, DATE_ADD(CURRENT_DATE, INTERVAL 5 YEAR), 'ACTIVE');
```
- **`sp_add_employee` & `sp_transfer_employee`:** Hashes credentials via `SHA2(p_password, 256)` and manages branch reassignments.
- **`sp_mini_statement(p_acc, p_n)`:** Returns a result set of the last `n` transactions ordered by `txn_time DESC, txn_id DESC`.

---

# Slide 18: Automated Database Triggers (`sql/03_triggers_views.sql`)
## Preventative Guards (`BEFORE`) & Immutable Audit Logging (`AFTER`)
```sql
-- 1. Prevent modifying a CLOSED account or closing an account with non-zero balance
CREATE TRIGGER trg_account_guard BEFORE UPDATE ON account FOR EACH ROW
BEGIN
  IF OLD.status = 'CLOSED' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Closed account cannot be modified';
  END IF;
  IF NEW.status = 'CLOSED' AND NEW.balance <> 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Closed account balance must be 0';
  END IF;
END$$

-- 2. Enforce KYC verification on every loan INSERT
CREATE TRIGGER trg_loan_kyc BEFORE INSERT ON loan FOR EACH ROW
BEGIN
  DECLARE v_kyc VARCHAR(20);
  SELECT kyc_status INTO v_kyc FROM customer WHERE customer_id = NEW.customer_id;
  IF v_kyc IS NULL OR v_kyc <> 'VERIFIED' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Customer KYC must be VERIFIED for loan application';
  END IF;
END$$

-- 3. Automatically log every ledger insertion & status change (trg_txn_audit, trg_account_status_audit, trg_loan_audit)
CREATE TRIGGER trg_txn_audit AFTER INSERT ON transactions FOR EACH ROW
BEGIN
  INSERT INTO audit_log (table_name, action, record_id, details, logged_at)
  VALUES ('transactions', 'INSERT', CAST(NEW.txn_id AS CHAR),
          CONCAT(NEW.txn_type, ' ', NEW.amount, ' acc ', NEW.account_no), CURRENT_TIMESTAMP);
END$$
```

---

# Slide 19: Relational Views for Operational & Executive Analytics
## 6 Views Abstracting Multi-Table Joins (`sql/03_triggers_views.sql`)
| View Name | Tables Joined / Aggregated | Key Columns Exposed |
| :--- | :--- | :--- |
| `v_account_summary` | `account` $\bowtie$ `customer` $\bowtie$ `account_type` $\bowtie$ `branch` | `account_no`, `customer_name`, `account_type`, `min_balance`, `ifsc`, `balance`, `status` |
| `v_customer_portfolio` | `customer` $\text{LEFT JOIN}$ `account`, `loan` | `total_accounts`, `total_balance`, `active_loans_count`, `total_loan_outstanding` |
| `v_branch_performance` | `branch` $\text{LEFT JOIN}$ `account` + subquery on `employee` | `total_customers`, `total_accounts`, `total_deposits`, `total_employees` |
| `v_daily_transactions` | `transactions` grouped by `DATE(txn_time)`, `txn_type` | `txn_date`, `txn_type`, `txn_count`, `total_amount` |
| `v_loan_outstanding` | `loan` $\bowtie$ `customer` + scalar subquery on `loan_payment` | `principal`, `emi`, `outstanding`, `status`, `total_paid` |
| `v_employee_hierarchy` | `employee e` $\bowtie$ `branch b` $\text{LEFT JOIN}$ `employee m` | `employee_name`, `role`, `branch_name`, `manager_name` |

```sql
CREATE OR REPLACE VIEW v_customer_portfolio AS
SELECT c.customer_id, c.name AS customer_name, c.phone, c.email, c.kyc_status,
  COUNT(DISTINCT a.account_no) AS total_accounts,
  COALESCE(SUM(a.balance), 0.00) AS total_balance,
  COUNT(DISTINCT CASE WHEN l.status = 'APPROVED' THEN l.loan_id END) AS active_loans_count,
  COALESCE(SUM(CASE WHEN l.status = 'APPROVED' THEN l.outstanding ELSE 0.00 END), 0.00) AS total_loan_outstanding
FROM customer c
LEFT JOIN account a ON c.customer_id = a.customer_id AND a.status <> 'CLOSED'
LEFT JOIN loan l ON c.customer_id = l.customer_id AND l.status = 'APPROVED'
GROUP BY c.customer_id, c.name, c.phone, c.email, c.kyc_status;
```

---

# Slide 20: DQL Joins — Multi-Table `INNER JOIN`, `LEFT JOIN` & `SELF JOIN`
## Core Relational Algebra Queries (`sql/05_test_queries.sql`)
```sql
-- 1. 4-Table INNER JOIN: Complete Account, Customer, Product & Branch Directory
SELECT a.account_no, c.name AS customer_name, t.name AS account_type,
       t.min_balance, b.name AS branch_name, b.ifsc, a.balance, a.status
FROM account a
INNER JOIN customer c     ON a.customer_id = c.customer_id
INNER JOIN account_type t ON a.type_id = t.type_id
INNER JOIN branch b       ON a.branch_id = b.branch_id
ORDER BY a.account_no;

-- 2. LEFT OUTER JOIN: Identify Prospective / KYC-Pending Customers With Zero Accounts
SELECT c.customer_id, c.name, c.phone, c.kyc_status, c.created_at
FROM customer c
LEFT JOIN account a ON c.customer_id = a.customer_id
WHERE a.account_no IS NULL;

-- 3. SELF JOIN: Resolve Employee-to-Reporting-Manager Hierarchy
SELECT e.emp_id, e.name AS employee_name, e.role, e.salary,
       COALESCE(m.name, 'Top Management / Self') AS reporting_manager
FROM employee e
LEFT JOIN employee m ON e.manager_id = m.emp_id
ORDER BY e.emp_id;
```

---

# Slide 21: Aggregations, `GROUP BY` + `HAVING` & Scalar/Correlated Subqueries
## Analytical Filtering & Per-Account Latest State (`sql/05_test_queries.sql`)
```sql
-- 1. GROUP BY + HAVING: Branches With Active Deposits Exceeding Rs. 1,00,000
SELECT b.branch_id, b.name AS branch_name, b.city,
       COUNT(a.account_no) AS total_active_accounts,
       SUM(a.balance) AS total_deposits
FROM branch b
JOIN account a ON b.branch_id = a.branch_id
WHERE a.status = 'ACTIVE'
GROUP BY b.branch_id, b.name, b.city
HAVING SUM(a.balance) > 100000.00
ORDER BY total_deposits DESC;

-- 2. Scalar Subquery: Accounts With Balance Strictly Above the Bank-Wide Average
SELECT account_no, customer_id, type_id, balance, status
FROM account
WHERE balance > (SELECT AVG(balance) FROM account WHERE status = 'ACTIVE')
ORDER BY balance DESC;

-- 3. Correlated Subquery: Most Recent Ledger Transaction Per Account
SELECT t1.txn_id, t1.account_no, t1.txn_time, t1.txn_type, t1.amount, t1.balance_after
FROM transactions t1
WHERE t1.txn_time = (
  SELECT MAX(t2.txn_time) FROM transactions t2 WHERE t2.account_no = t1.account_no
)
ORDER BY t1.account_no;
```

---

# Slide 22: Common Table Expressions (CTEs) & `NOT EXISTS` Queries
## Readable Modular SQL & Anti-Semi-Join Logic (`sql/05_test_queries.sql`)
```sql
-- 1. Common Table Expression (WITH Clause): Monthly Inflow Trajectory
WITH MonthlyDeposits AS (
  SELECT DATE_FORMAT(txn_time, '%Y-%m') AS txn_month,
         txn_type,
         amount
  FROM transactions
  WHERE txn_type IN ('DEPOSIT', 'TRANSFER_IN')
)
SELECT txn_month,
       COUNT(*) AS total_inflows,
       SUM(amount) AS total_inflow_amount,
       ROUND(AVG(amount), 2) AS avg_inflow_amount
FROM MonthlyDeposits
GROUP BY txn_month
ORDER BY txn_month DESC;

-- 2. NOT EXISTS: Verified Customers Who Have No Active or Pending Loans
SELECT c.customer_id, c.name, c.phone
FROM customer c
WHERE c.kyc_status = 'VERIFIED'
  AND NOT EXISTS (
    SELECT 1 FROM loan l
    WHERE l.customer_id = c.customer_id
      AND l.status IN ('PENDING', 'APPROVED')
  );
```

---

# Slide 23: MySQL 8.0 Window Functions — Running Balance & Wealth Ranking
## `SUM() OVER (PARTITION BY ...)` & `RANK()` / `DENSE_RANK()`
```sql
-- 1. Progressive Running Balance Audit via Window Partitioning
SELECT account_no, txn_id, txn_time, txn_type, amount,
  SUM(
    CASE
      WHEN txn_type IN ('DEPOSIT', 'TRANSFER_IN', 'INTEREST', 'LOAN_DISBURSE') THEN amount
      ELSE -amount
    END
  ) OVER (PARTITION BY account_no ORDER BY txn_time ASC, txn_id ASC) AS calculated_running_balance,
  balance_after AS recorded_balance_after
FROM transactions
WHERE account_no = 1000100001
ORDER BY txn_time ASC;

-- 2. Customer Wealth Ranking Across All Non-Closed Accounts
SELECT c.customer_id, c.name AS customer_name, c.kyc_status,
       SUM(a.balance) AS total_wealth,
       RANK() OVER (ORDER BY SUM(a.balance) DESC) AS wealth_rank,
       DENSE_RANK() OVER (ORDER BY SUM(a.balance) DESC) AS dense_wealth_rank
FROM customer c
JOIN account a ON c.customer_id = a.customer_id
WHERE a.status <> 'CLOSED'
GROUP BY c.customer_id, c.name, c.kyc_status
ORDER BY wealth_rank;
```

---

# Slide 24: Query Execution Plan Analysis (`EXPLAIN`) & DCL Security
## Verifying Composite Index Usage & Database Privileges
```sql
-- 1. EXPLAIN Execution Plan: Uses composite index idx_txn_acc_time(account_no, txn_time)
EXPLAIN
SELECT txn_id, txn_time, txn_type, amount, balance_after
FROM transactions
WHERE account_no = 1000100001
  AND txn_time >= '2024-08-01'
ORDER BY txn_time DESC;
```
- **`EXPLAIN` Result:** Uses `key: idx_txn_acc_time` (`type: range`), avoiding a full table scan on `transactions` and reading only the matching account rows in index order.

```sql
-- 2. Data Control Language (DCL) & Role-Based Privilege Isolation
CREATE USER 'bms_teller'@'localhost' IDENTIFIED BY 'StrongTellerPass_123!';
GRANT SELECT ON bank_db.v_account_summary TO 'bms_teller'@'localhost';
GRANT EXECUTE ON PROCEDURE bank_db.sp_deposit TO 'bms_teller'@'localhost';
GRANT EXECUTE ON PROCEDURE bank_db.sp_withdraw TO 'bms_teller'@'localhost';
REVOKE EXECUTE ON PROCEDURE bank_db.sp_approve_loan FROM 'bms_teller'@'localhost';
```

---

# Slide 25: Transaction Control Language (TCL) — `COMMIT`, `ROLLBACK` & `SAVEPOINT`
## Demonstrating Atomicity & Durability in InnoDB
```sql
-- Step 1: Inspect initial account balances before transaction
SELECT account_no, balance FROM account WHERE account_no IN (1000100001, 1000100002);

-- Step 2: Start atomic transaction & create savepoint
START TRANSACTION;
UPDATE account SET balance = balance - 1000.00 WHERE account_no = 1000100001;
SAVEPOINT after_sender_debit;

-- Step 3: Simulate downstream failure (e.g., invalid receiver account) & Rollback
ROLLBACK;

-- Step 4: Verify balances are 100% untouched after ROLLBACK
SELECT account_no, balance FROM account WHERE account_no IN (1000100001, 1000100002);
```
- **Why DDL Cannot Be Rolled Back:** In MySQL 8.0, DDL statements (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`) cause an implicit `COMMIT`. Therefore, all operational state changes in `bank_db` are strictly DML inside `InnoDB` transactions.

---

# Slide 26: Mathematical Ledger Consistency Audit (Acceptance Test #13)
## Proving Zero Discrepancy Across All 30 Accounts & 93+ Transactions
- **The Ultimate Banking Audit Query:** Verifies that for **every** account in `bank_db`, `account.balance` equals the exact sum of all signed credits (`DEPOSIT`, `TRANSFER_IN`, `INTEREST`, `LOAN_DISBURSE`) minus all signed debits (`WITHDRAW`, `TRANSFER_OUT`, `LOAN_EMI`, `CHARGE`).
- **Expected Output:** `0 rows` (Zero discrepancy across the entire database).

```sql
SELECT
  a.account_no,
  a.balance AS current_balance,
  ROUND(SUM(
    CASE
      WHEN t.txn_type IN ('DEPOSIT', 'TRANSFER_IN', 'INTEREST', 'LOAN_DISBURSE') THEN t.amount
      WHEN t.txn_type IN ('WITHDRAW', 'TRANSFER_OUT', 'LOAN_EMI', 'CHARGE') THEN -t.amount
      ELSE 0.00
    END
  ), 2) AS calculated_ledger_balance,
  ROUND(a.balance - SUM(
    CASE
      WHEN t.txn_type IN ('DEPOSIT', 'TRANSFER_IN', 'INTEREST', 'LOAN_DISBURSE') THEN t.amount
      WHEN t.txn_type IN ('WITHDRAW', 'TRANSFER_OUT', 'LOAN_EMI', 'CHARGE') THEN -t.amount
      ELSE 0.00
    END
  ), 2) AS discrepancy
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
```

---

# Slide 27: Comprehensive Acceptance Testing Matrix (`TC01`–`TC15`)
## Automated Verification of Constraints, Procedures & Triggers
| Test ID | SQL Operation / Procedure Tested | Expected & Verified Database Result |
| :--- | :--- | :--- |
| **TC01** | `sp_withdraw` below `account_type.min_balance` | `ERROR` signaled; `ROLLBACK` leaves balance unchanged |
| **TC02** | `sp_transfer` with `from_acc = to_acc` | `ERROR: Cannot transfer to the same account` |
| **TC03** | `sp_transfer` to non-existent `account_no` | `ERROR: Receiver account not found`; sender debit rolled back |
| **TC04** | `sp_transfer` valid amount between active accounts | `SUCCESS`: Both balances updated + `TRANSFER_OUT` & `TRANSFER_IN` logged |
| **TC05** | `sp_deposit` into `FROZEN` or `CLOSED` account | `ERROR: Account is not active` |
| **TC06** | `sp_close_account` / `trg_account_guard` with `balance > 0` | `ERROR: Account balance must be 0 to close` |
| **TC07–08** | `sp_open_account` & `trg_loan_kyc` for `PENDING` KYC | `ERROR: Customer KYC must be VERIFIED` |
| **TC09–11** | `sp_approve_loan` & `sp_pay_emi` until `outstanding = 0` | Disburses principal (`LOAN_DISBURSE`); auto-sets `CLOSED` at `0` |
| **TC12–15** | `sp_credit_interest`, Ledger Audit (#13), RBAC & Audit Triggers | Batch interest credited; `0` ledger discrepancy; `audit_log` populated |

---

# Slide 28: Conclusion & Future Database Enhancements
## Summary of Achievements & Roadmap
- **Key DBMS Achievements:**
  - Designed a **10-table 3NF relational schema** in MySQL 8.0 (`InnoDB`) with zero data redundancy.
  - Engineered **17 transactional stored procedures** featuring `SQLEXCEPTION` rollback handlers, `SELECT ... FOR UPDATE` row locking, and ascending primary-key lock ordering for **deadlock prevention**.
  - Automated compliance and invariant enforcement through **5 `BEFORE`/`AFTER` triggers** and **6 analytical views**.
  - Verified **100% mathematical ledger accuracy** across 30 accounts and 93+ seeded transactions.
- **Future Database Enhancements:**
  - **Scheduled MySQL Events (`CREATE EVENT`):** Automate end-of-month interest runs (`sp_credit_interest`) and recurring EMI auto-debits.
  - **Table Partitioning:** Range-partition `transactions` and `audit_log` by year/month for multi-million-row scalability.
  - **Read Replicas:** Offload analytical views (`v_branch_performance`, `v_daily_transactions`) to MySQL read replicas.

