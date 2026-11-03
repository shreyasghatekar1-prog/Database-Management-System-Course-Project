-- =============================================================================
-- Bank Management System - Course Project Demo & Viva Test Queries
-- File: sql/05_test_queries.sql
-- =============================================================================

USE bank_db;

-- -----------------------------------------------------------------------------
-- 1. INNER JOIN across 4 tables (account, customer, account_type, branch)
-- Retrieves comprehensive account details with customer, product type, and branch metadata.
-- -----------------------------------------------------------------------------
SELECT 
  a.account_no,
  c.name AS customer_name,
  c.phone,
  t.name AS account_type,
  t.min_balance,
  b.name AS branch_name,
  b.ifsc,
  a.balance,
  a.status
FROM account a
INNER JOIN customer c ON a.customer_id = c.customer_id
INNER JOIN account_type t ON a.type_id = t.type_id
INNER JOIN branch b ON a.branch_id = b.branch_id
ORDER BY a.account_no;

-- -----------------------------------------------------------------------------
-- 2. LEFT JOIN: Identify customers who currently have no bank accounts
-- Finds all prospective or KYC-pending customers without an active account link.
-- -----------------------------------------------------------------------------
SELECT 
  c.customer_id,
  c.name,
  c.phone,
  c.kyc_status,
  c.created_at
FROM customer c
LEFT JOIN account a ON c.customer_id = a.customer_id
WHERE a.account_no IS NULL;

-- -----------------------------------------------------------------------------
-- 3. GROUP BY + HAVING: Branches with total deposits above a threshold (e.g. ₹1,00,000)
-- Aggregates branch deposits and filters groups using HAVING.
-- -----------------------------------------------------------------------------
SELECT 
  b.branch_id,
  b.name AS branch_name,
  b.city,
  COUNT(a.account_no) AS total_active_accounts,
  SUM(a.balance) AS total_deposits
FROM branch b
JOIN account a ON b.branch_id = a.branch_id
WHERE a.status = 'ACTIVE'
GROUP BY b.branch_id, b.name, b.city
HAVING SUM(a.balance) > 100000.00
ORDER BY total_deposits DESC;

-- -----------------------------------------------------------------------------
-- 4. Subquery: Accounts with balance strictly above the average bank balance
-- Compares individual account balances against an aggregated scalar subquery.
-- -----------------------------------------------------------------------------
SELECT 
  account_no,
  customer_id,
  type_id,
  balance,
  status
FROM account
WHERE balance > (SELECT AVG(balance) FROM account WHERE status = 'ACTIVE')
ORDER BY balance DESC;

-- -----------------------------------------------------------------------------
-- 5. Correlated subquery: Latest transaction timestamp and details per account
-- Subquery references outer query's account_no to find the most recent ledger row.
-- -----------------------------------------------------------------------------
SELECT 
  t1.txn_id,
  t1.account_no,
  t1.txn_time,
  t1.txn_type,
  t1.amount,
  t1.balance_after
FROM transactions t1
WHERE t1.txn_time = (
  SELECT MAX(t2.txn_time)
  FROM transactions t2
  WHERE t2.account_no = t1.account_no
)
ORDER BY t1.account_no;

-- -----------------------------------------------------------------------------
-- 6. Window function: Progressive running balance verification
-- Calculates cumulative balance running sum partitioned by account ordered by time.
-- -----------------------------------------------------------------------------
SELECT 
  account_no,
  txn_id,
  txn_time,
  txn_type,
  amount,
  CASE 
    WHEN txn_type IN ('DEPOSIT', 'TRANSFER_IN', 'INTEREST', 'LOAN_DISBURSE') THEN amount
    ELSE -amount
  END AS signed_amount,
  SUM(
    CASE 
      WHEN txn_type IN ('DEPOSIT', 'TRANSFER_IN', 'INTEREST', 'LOAN_DISBURSE') THEN amount
      ELSE -amount
    END
  ) OVER (
    PARTITION BY account_no 
    ORDER BY txn_time ASC, txn_id ASC
  ) AS calculated_running_balance,
  balance_after AS recorded_balance_after
FROM transactions
WHERE account_no = 1000100001
ORDER BY txn_time ASC;

-- -----------------------------------------------------------------------------
-- 7. Window function: RANK() of customers by total bank deposits
-- Assigns rank to customers based on total deposited assets across all their accounts.
-- -----------------------------------------------------------------------------
SELECT 
  c.customer_id,
  c.name AS customer_name,
  c.kyc_status,
  SUM(a.balance) AS total_wealth,
  RANK() OVER (ORDER BY SUM(a.balance) DESC) AS wealth_rank,
  DENSE_RANK() OVER (ORDER BY SUM(a.balance) DESC) AS dense_wealth_rank
FROM customer c
JOIN account a ON c.customer_id = a.customer_id
WHERE a.status <> 'CLOSED'
GROUP BY c.customer_id, c.name, c.kyc_status
ORDER BY wealth_rank;

-- -----------------------------------------------------------------------------
-- 8. Self-join: Employee with Reporting Manager name
-- Joins employee table onto itself using manager_id foreign key.
-- -----------------------------------------------------------------------------
SELECT 
  e.emp_id,
  e.name AS employee_name,
  e.role,
  e.salary,
  COALESCE(m.name, 'Top Management / Self') AS reporting_manager,
  m.role AS manager_role
FROM employee e
LEFT JOIN employee m ON e.manager_id = m.emp_id
ORDER BY e.emp_id;

-- -----------------------------------------------------------------------------
-- 9. Common Table Expression (CTE): Monthly deposit breakdown
-- Computes monthly inflow metrics using a readable WITH clause.
-- -----------------------------------------------------------------------------
WITH MonthlyDeposits AS (
  SELECT 
    DATE_FORMAT(txn_time, '%Y-%m') AS txn_month,
    txn_type,
    amount
  FROM transactions
  WHERE txn_type IN ('DEPOSIT', 'TRANSFER_IN')
)
SELECT 
  txn_month,
  COUNT(*) AS total_inflows,
  SUM(amount) AS total_inflow_amount,
  AVG(amount) AS avg_inflow_amount
FROM MonthlyDeposits
GROUP BY txn_month
ORDER BY txn_month DESC;

-- -----------------------------------------------------------------------------
-- 10. EXISTS / NOT EXISTS query
-- Identifies verified customers who do NOT have any active loans.
-- -----------------------------------------------------------------------------
SELECT 
  c.customer_id,
  c.name,
  c.phone
FROM customer c
WHERE c.kyc_status = 'VERIFIED'
  AND NOT EXISTS (
    SELECT 1 
    FROM loan l 
    WHERE l.customer_id = c.customer_id 
      AND l.status IN ('PENDING', 'APPROVED')
  );

-- -----------------------------------------------------------------------------
-- 11. Transaction Demo: ACID Demonstration with Rollback
-- Simulates atomic money transfer with intentional error to demonstrate rollback.
-- -----------------------------------------------------------------------------
-- Step 11a: Record initial balances
SELECT account_no, balance FROM account WHERE account_no IN (1000100001, 1000100002);

-- Step 11b: Demonstration of transaction rollback on failure
START TRANSACTION;
UPDATE account SET balance = balance - 1000.00 WHERE account_no = 1000100001;
-- Intentionally trigger condition: receiver account does not exist
-- In stored procedures, SQLEXCEPTION handler executes ROLLBACK;
ROLLBACK;

-- Step 11c: Confirm balances remained completely untouched
SELECT account_no, balance FROM account WHERE account_no IN (1000100001, 1000100002);

-- -----------------------------------------------------------------------------
-- 12. Index demo: EXPLAIN query execution plan
-- Demonstrates performance index usage on (account_no, txn_time) composite index.
-- -----------------------------------------------------------------------------
EXPLAIN 
SELECT txn_id, txn_time, txn_type, amount, balance_after
FROM transactions
WHERE account_no = 1000100001
  AND txn_time >= '2024-08-01'
ORDER BY txn_time DESC;

-- -----------------------------------------------------------------------------
-- 13. Acceptance Test #13: Ledger Consistency Audit Check
-- For EVERY account: opening balance + sum of signed transactions MUST equal balance.
-- Returns 0 rows if ledger is 100% consistent across all accounts.
-- -----------------------------------------------------------------------------
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
