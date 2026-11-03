-- =============================================================================
-- Bank Management System - Triggers and Views
-- File: sql/03_triggers_views.sql
-- =============================================================================

USE bank_db;

-- =============================================================================
-- TRIGGERS
-- =============================================================================

DROP TRIGGER IF EXISTS trg_account_guard;
DROP TRIGGER IF EXISTS trg_txn_audit;
DROP TRIGGER IF EXISTS trg_account_status_audit;
DROP TRIGGER IF EXISTS trg_loan_kyc;
DROP TRIGGER IF EXISTS trg_loan_audit;

DELIMITER $$

-- 1. trg_account_guard (BEFORE UPDATE ON account)
CREATE TRIGGER trg_account_guard
BEFORE UPDATE ON account
FOR EACH ROW
BEGIN
  IF OLD.status = 'CLOSED' THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Closed account cannot be modified';
  END IF;

  IF NEW.status = 'CLOSED' AND NEW.balance <> 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Closed account balance must be 0';
  END IF;
END$$

-- 2. trg_txn_audit (AFTER INSERT ON transactions)
CREATE TRIGGER trg_txn_audit
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
  INSERT INTO audit_log (table_name, action, record_id, details, logged_at)
  VALUES (
    'transactions',
    'INSERT',
    CAST(NEW.txn_id AS CHAR),
    CONCAT(NEW.txn_type, ' ', NEW.amount, ' acc ', NEW.account_no),
    CURRENT_TIMESTAMP
  );
END$$

-- 3. trg_account_status_audit (AFTER UPDATE ON account)
CREATE TRIGGER trg_account_status_audit
AFTER UPDATE ON account
FOR EACH ROW
BEGIN
  IF OLD.status <> NEW.status THEN
    INSERT INTO audit_log (table_name, action, record_id, details, logged_at)
    VALUES (
      'account',
      'STATUS_CHANGE',
      CAST(NEW.account_no AS CHAR),
      CONCAT(OLD.status, '->', NEW.status),
      CURRENT_TIMESTAMP
    );
  END IF;
END$$

-- 4. trg_loan_kyc (BEFORE INSERT ON loan)
CREATE TRIGGER trg_loan_kyc
BEFORE INSERT ON loan
FOR EACH ROW
BEGIN
  DECLARE v_kyc VARCHAR(20);
  SELECT kyc_status INTO v_kyc FROM customer WHERE customer_id = NEW.customer_id;
  IF v_kyc IS NULL OR v_kyc <> 'VERIFIED' THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Customer KYC must be VERIFIED for loan application';
  END IF;
END$$

-- 5. trg_loan_audit (AFTER UPDATE ON loan)
CREATE TRIGGER trg_loan_audit
AFTER UPDATE ON loan
FOR EACH ROW
BEGIN
  IF OLD.status <> NEW.status THEN
    INSERT INTO audit_log (table_name, action, record_id, details, logged_at)
    VALUES (
      'loan',
      'STATUS_CHANGE',
      CAST(NEW.loan_id AS CHAR),
      CONCAT(OLD.status, '->', NEW.status),
      CURRENT_TIMESTAMP
    );
  END IF;
END$$

DELIMITER ;


-- =============================================================================
-- VIEWS
-- =============================================================================

-- 1. v_account_summary: joins account, customer, account_type, branch
CREATE OR REPLACE VIEW v_account_summary AS
SELECT
  a.account_no,
  c.customer_id,
  c.name AS customer_name,
  c.phone,
  c.email,
  t.type_id,
  t.name AS account_type,
  t.min_balance,
  t.interest_rate,
  b.branch_id,
  b.name AS branch_name,
  b.city AS branch_city,
  b.ifsc,
  a.balance,
  a.status,
  a.opened_on
FROM account a
JOIN customer c ON a.customer_id = c.customer_id
JOIN account_type t ON a.type_id = t.type_id
JOIN branch b ON a.branch_id = b.branch_id;

-- 2. v_customer_portfolio: per customer summary of accounts and loans
CREATE OR REPLACE VIEW v_customer_portfolio AS
SELECT
  c.customer_id,
  c.name AS customer_name,
  c.phone,
  c.email,
  c.kyc_status,
  COUNT(DISTINCT a.account_no) AS total_accounts,
  COALESCE(SUM(a.balance), 0.00) AS total_balance,
  COUNT(DISTINCT CASE WHEN l.status = 'APPROVED' THEN l.loan_id END) AS active_loans_count,
  COALESCE(SUM(CASE WHEN l.status = 'APPROVED' THEN l.outstanding ELSE 0.00 END), 0.00) AS total_loan_outstanding
FROM customer c
LEFT JOIN account a ON c.customer_id = a.customer_id AND a.status <> 'CLOSED'
LEFT JOIN loan l ON c.customer_id = l.customer_id AND l.status = 'APPROVED'
GROUP BY c.customer_id, c.name, c.phone, c.email, c.kyc_status;

-- 3. v_branch_performance: per branch summary
CREATE OR REPLACE VIEW v_branch_performance AS
SELECT
  b.branch_id,
  b.name AS branch_name,
  b.city,
  b.ifsc,
  COUNT(DISTINCT a.customer_id) AS total_customers,
  COUNT(DISTINCT a.account_no) AS total_accounts,
  COALESCE(SUM(a.balance), 0.00) AS total_deposits,
  (SELECT COUNT(*) FROM employee e WHERE e.branch_id = b.branch_id AND e.is_active = TRUE) AS total_employees
FROM branch b
LEFT JOIN account a ON b.branch_id = a.branch_id AND a.status <> 'CLOSED'
GROUP BY b.branch_id, b.name, b.city, b.ifsc;

-- 4. v_daily_transactions: per date and txn_type count and total
CREATE OR REPLACE VIEW v_daily_transactions AS
SELECT
  DATE(txn_time) AS txn_date,
  txn_type,
  COUNT(*) AS txn_count,
  SUM(amount) AS total_amount
FROM transactions
GROUP BY DATE(txn_time), txn_type;

-- 5. v_loan_outstanding: loan details with paid amounts
CREATE OR REPLACE VIEW v_loan_outstanding AS
SELECT
  l.loan_id,
  l.customer_id,
  c.name AS customer_name,
  l.account_no,
  l.principal,
  l.annual_rate,
  l.tenure_months,
  l.emi,
  l.outstanding,
  l.status,
  l.applied_on,
  l.approved_by,
  l.approved_on,
  COALESCE((SELECT SUM(lp.amount) FROM loan_payment lp WHERE lp.loan_id = l.loan_id), 0.00) AS total_paid
FROM loan l
JOIN customer c ON l.customer_id = c.customer_id;

-- 6. v_employee_hierarchy: self-join for employee and manager details
CREATE OR REPLACE VIEW v_employee_hierarchy AS
SELECT
  e.emp_id,
  e.name AS employee_name,
  e.role,
  e.salary,
  e.branch_id,
  b.name AS branch_name,
  b.city AS branch_city,
  e.manager_id,
  m.name AS manager_name,
  e.hire_date,
  e.username,
  e.is_active
FROM employee e
JOIN branch b ON e.branch_id = b.branch_id
LEFT JOIN employee m ON e.manager_id = m.emp_id;
