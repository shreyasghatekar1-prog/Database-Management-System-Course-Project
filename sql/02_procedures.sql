-- =============================================================================
-- Bank Management System - Stored Procedures
-- File: sql/02_procedures.sql
-- =============================================================================

USE bank_db;

DROP PROCEDURE IF EXISTS sp_open_account;
DROP PROCEDURE IF EXISTS sp_close_account;
DROP PROCEDURE IF EXISTS sp_set_account_status;
DROP PROCEDURE IF EXISTS sp_deposit;
DROP PROCEDURE IF EXISTS sp_withdraw;
DROP PROCEDURE IF EXISTS sp_transfer;
DROP PROCEDURE IF EXISTS sp_apply_loan;
DROP PROCEDURE IF EXISTS sp_approve_loan;
DROP PROCEDURE IF EXISTS sp_reject_loan;
DROP PROCEDURE IF EXISTS sp_pay_emi;
DROP PROCEDURE IF EXISTS sp_apply_charge;
DROP PROCEDURE IF EXISTS sp_credit_interest;
DROP PROCEDURE IF EXISTS sp_issue_card;
DROP PROCEDURE IF EXISTS sp_set_card_status;
DROP PROCEDURE IF EXISTS sp_add_employee;
DROP PROCEDURE IF EXISTS sp_transfer_employee;
DROP PROCEDURE IF EXISTS sp_mini_statement;

DELIMITER $$

-- -----------------------------------------------------------------------------
-- 1. sp_open_account
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_open_account(
  IN p_customer_id INT,
  IN p_type_id INT,
  IN p_branch_id INT,
  IN p_initial_deposit DECIMAL(15,2),
  IN p_emp INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_kyc VARCHAR(20);
  DECLARE v_min_bal DECIMAL(12,2);
  DECLARE v_acc_no BIGINT;

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF p_initial_deposit < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Initial deposit cannot be negative';
  END IF;

  -- Validate customer and KYC
  SELECT kyc_status INTO v_kyc FROM customer WHERE customer_id = p_customer_id;
  IF v_kyc IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Customer does not exist';
  END IF;
  IF v_kyc <> 'VERIFIED' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Customer KYC must be VERIFIED to open an account';
  END IF;

  -- Validate account type & min balance
  SELECT min_balance INTO v_min_bal FROM account_type WHERE type_id = p_type_id;
  IF v_min_bal IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid account type';
  END IF;
  IF p_initial_deposit < v_min_bal THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Initial deposit must be at least the account type minimum balance';
  END IF;

  -- Validate branch
  IF NOT EXISTS (SELECT 1 FROM branch WHERE branch_id = p_branch_id) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid branch ID';
  END IF;

  -- Insert account
  INSERT INTO account(customer_id, type_id, branch_id, balance, status, opened_on)
  VALUES (p_customer_id, p_type_id, p_branch_id, p_initial_deposit, 'ACTIVE', CURRENT_DATE);
  SET v_acc_no = LAST_INSERT_ID();

  -- If deposit > 0, insert deposit transaction
  IF p_initial_deposit > 0 THEN
    INSERT INTO transactions(account_no, txn_type, amount, balance_after, remarks, done_by_emp)
    VALUES (v_acc_no, 'DEPOSIT', p_initial_deposit, p_initial_deposit, 'Initial account deposit', p_emp);
  END IF;

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Account opened successfully. Account No: ', v_acc_no);
END$$

-- -----------------------------------------------------------------------------
-- 2. sp_close_account
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_close_account(
  IN p_acc BIGINT,
  IN p_emp INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_bal DECIMAL(15,2);
  DECLARE v_status VARCHAR(10);
  DECLARE v_active_loans INT DEFAULT 0;

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  SELECT balance, status INTO v_bal, v_status FROM account WHERE account_no = p_acc FOR UPDATE;
  IF v_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account not found';
  END IF;
  IF v_status = 'CLOSED' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account is already CLOSED';
  END IF;
  IF v_bal <> 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account balance must be 0 to close';
  END IF;

  SELECT COUNT(*) INTO v_active_loans
  FROM loan
  WHERE account_no = p_acc AND status IN ('PENDING', 'APPROVED');

  IF v_active_loans > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account has active or pending loans and cannot be closed';
  END IF;

  UPDATE account SET status = 'CLOSED' WHERE account_no = p_acc;

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Account ', p_acc, ' closed successfully');
END$$

-- -----------------------------------------------------------------------------
-- 3. sp_set_account_status
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_set_account_status(
  IN p_acc BIGINT,
  IN p_new_status VARCHAR(10),
  IN p_emp INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_status VARCHAR(10);

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF p_new_status NOT IN ('ACTIVE', 'FROZEN') THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'New status must be ACTIVE or FROZEN';
  END IF;

  SELECT status INTO v_status FROM account WHERE account_no = p_acc FOR UPDATE;
  IF v_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account not found';
  END IF;
  IF v_status = 'CLOSED' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot modify status of a CLOSED account';
  END IF;

  UPDATE account SET status = p_new_status WHERE account_no = p_acc;

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Account status updated to ', p_new_status);
END$$

-- -----------------------------------------------------------------------------
-- 4. sp_deposit
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_deposit(
  IN p_acc BIGINT,
  IN p_amt DECIMAL(15,2),
  IN p_emp INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_bal DECIMAL(15,2);
  DECLARE v_status VARCHAR(10);

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF p_amt <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Amount must be positive';
  END IF;

  SELECT balance, status INTO v_bal, v_status FROM account WHERE account_no = p_acc FOR UPDATE;
  IF v_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account not found';
  END IF;
  IF v_status <> 'ACTIVE' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account is not active';
  END IF;

  UPDATE account SET balance = balance + p_amt WHERE account_no = p_acc;
  INSERT INTO transactions(account_no, txn_type, amount, balance_after, remarks, done_by_emp)
  VALUES (p_acc, 'DEPOSIT', p_amt, v_bal + p_amt, 'Cash deposit', p_emp);

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Deposited ', p_amt, '. New balance ', v_bal + p_amt);
END$$

-- -----------------------------------------------------------------------------
-- 5. sp_withdraw
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_withdraw(
  IN p_acc BIGINT,
  IN p_amt DECIMAL(15,2),
  IN p_emp INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_bal DECIMAL(15,2);
  DECLARE v_status VARCHAR(10);
  DECLARE v_min_bal DECIMAL(12,2);

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF p_amt <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Amount must be positive';
  END IF;

  SELECT a.balance, a.status, t.min_balance
  INTO v_bal, v_status, v_min_bal
  FROM account a
  JOIN account_type t ON a.type_id = t.type_id
  WHERE a.account_no = p_acc FOR UPDATE;

  IF v_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account not found';
  END IF;
  IF v_status <> 'ACTIVE' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account is not active';
  END IF;

  IF (v_bal - p_amt) < v_min_bal THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient balance. Must maintain minimum balance';
  END IF;

  UPDATE account SET balance = balance - p_amt WHERE account_no = p_acc;
  INSERT INTO transactions(account_no, txn_type, amount, balance_after, remarks, done_by_emp)
  VALUES (p_acc, 'WITHDRAW', p_amt, v_bal - p_amt, 'Cash withdrawal', p_emp);

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Withdrawn ', p_amt, '. New balance ', v_bal - p_amt);
END$$

-- -----------------------------------------------------------------------------
-- 6. sp_transfer
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_transfer(
  IN p_from_acc BIGINT,
  IN p_to_acc BIGINT,
  IN p_amt DECIMAL(15,2),
  IN p_emp INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_from_bal DECIMAL(15,2);
  DECLARE v_from_status VARCHAR(10);
  DECLARE v_from_min_bal DECIMAL(12,2);

  DECLARE v_to_bal DECIMAL(15,2);
  DECLARE v_to_status VARCHAR(10);

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF p_amt <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Amount must be positive';
  END IF;

  IF p_from_acc = p_to_acc THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot transfer to the same account';
  END IF;

  -- Lock rows in ascending order to prevent deadlocks
  IF p_from_acc < p_to_acc THEN
    SELECT a.balance, a.status, t.min_balance
    INTO v_from_bal, v_from_status, v_from_min_bal
    FROM account a
    JOIN account_type t ON a.type_id = t.type_id
    WHERE a.account_no = p_from_acc FOR UPDATE;

    SELECT balance, status
    INTO v_to_bal, v_to_status
    FROM account
    WHERE account_no = p_to_acc FOR UPDATE;
  ELSE
    SELECT balance, status
    INTO v_to_bal, v_to_status
    FROM account
    WHERE account_no = p_to_acc FOR UPDATE;

    SELECT a.balance, a.status, t.min_balance
    INTO v_from_bal, v_from_status, v_from_min_bal
    FROM account a
    JOIN account_type t ON a.type_id = t.type_id
    WHERE a.account_no = p_from_acc FOR UPDATE;
  END IF;

  IF v_from_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Sender account not found';
  END IF;
  IF v_from_status <> 'ACTIVE' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Sender account is not active';
  END IF;

  IF v_to_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Receiver account not found';
  END IF;
  IF v_to_status <> 'ACTIVE' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Receiver account is not active';
  END IF;

  IF (v_from_bal - p_amt) < v_from_min_bal THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient balance in sender account';
  END IF;

  -- Deduct from sender
  UPDATE account SET balance = balance - p_amt WHERE account_no = p_from_acc;
  INSERT INTO transactions(account_no, txn_type, amount, balance_after, related_account, remarks, done_by_emp)
  VALUES (p_from_acc, 'TRANSFER_OUT', p_amt, v_from_bal - p_amt, p_to_acc, CONCAT('Transfer to ', p_to_acc), p_emp);

  -- Add to receiver
  UPDATE account SET balance = balance + p_amt WHERE account_no = p_to_acc;
  INSERT INTO transactions(account_no, txn_type, amount, balance_after, related_account, remarks, done_by_emp)
  VALUES (p_to_acc, 'TRANSFER_IN', p_amt, v_to_bal + p_amt, p_from_acc, CONCAT('Transfer from ', p_from_acc), p_emp);

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Transferred ', p_amt, ' from ', p_from_acc, ' to ', p_to_acc);
END$$

-- -----------------------------------------------------------------------------
-- 7. sp_apply_loan
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_apply_loan(
  IN p_customer_id INT,
  IN p_account_no BIGINT,
  IN p_principal DECIMAL(15,2),
  IN p_annual_rate DECIMAL(5,2),
  IN p_tenure_months INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_owner INT;
  DECLARE v_status VARCHAR(10);
  DECLARE v_kyc VARCHAR(20);
  DECLARE v_r DOUBLE;
  DECLARE v_pow DOUBLE;
  DECLARE v_emi DECIMAL(15,2);
  DECLARE v_outstanding DECIMAL(15,2);
  DECLARE v_loan_id INT;

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF p_principal <= 0 OR p_annual_rate <= 0 OR p_tenure_months <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Principal, rate, and tenure must be positive numbers';
  END IF;

  SELECT kyc_status INTO v_kyc FROM customer WHERE customer_id = p_customer_id;
  IF v_kyc IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Customer not found';
  END IF;
  IF v_kyc <> 'VERIFIED' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Customer KYC is not VERIFIED';
  END IF;

  SELECT customer_id, status INTO v_owner, v_status FROM account WHERE account_no = p_account_no;
  IF v_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account not found';
  END IF;
  IF v_owner <> p_customer_id THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account does not belong to customer';
  END IF;
  IF v_status <> 'ACTIVE' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account is not active';
  END IF;

  -- EMI calculation: r = annual_rate / 12 / 100
  SET v_r = (p_annual_rate / 12.0) / 100.0;
  SET v_pow = POW(1.0 + v_r, p_tenure_months);
  SET v_emi = ROUND((p_principal * v_r * v_pow) / (v_pow - 1.0), 2);
  SET v_outstanding = ROUND(v_emi * p_tenure_months, 2);

  INSERT INTO loan(customer_id, account_no, principal, annual_rate, tenure_months, emi, outstanding, status, applied_on)
  VALUES (p_customer_id, p_account_no, p_principal, p_annual_rate, p_tenure_months, v_emi, v_outstanding, 'PENDING', CURRENT_DATE);
  SET v_loan_id = LAST_INSERT_ID();

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Loan applied. Loan ID: ', v_loan_id, ', EMI: ', v_emi);
END$$

-- -----------------------------------------------------------------------------
-- 8. sp_approve_loan
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_approve_loan(
  IN p_loan_id INT,
  IN p_emp INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_role VARCHAR(30);
  DECLARE v_emp_active BOOLEAN;
  DECLARE v_status VARCHAR(20);
  DECLARE v_principal DECIMAL(15,2);
  DECLARE v_account_no BIGINT;
  DECLARE v_acc_status VARCHAR(10);
  DECLARE v_bal DECIMAL(15,2);

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  SELECT role, is_active INTO v_role, v_emp_active FROM employee WHERE emp_id = p_emp;
  IF v_role IS NULL OR v_emp_active IS FALSE THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Employee not found or inactive';
  END IF;
  IF v_role NOT IN ('MANAGER', 'LOAN_OFFICER') THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Only MANAGER or LOAN_OFFICER can approve loans';
  END IF;

  SELECT status, principal, account_no
  INTO v_status, v_principal, v_account_no
  FROM loan WHERE loan_id = p_loan_id FOR UPDATE;

  IF v_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Loan not found';
  END IF;
  IF v_status <> 'PENDING' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Loan is not in PENDING state';
  END IF;

  SELECT balance, status INTO v_bal, v_acc_status FROM account WHERE account_no = v_account_no FOR UPDATE;
  IF v_acc_status <> 'ACTIVE' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Disbursement account is not active';
  END IF;

  UPDATE loan
  SET status = 'APPROVED', approved_by = p_emp, approved_on = CURRENT_DATE
  WHERE loan_id = p_loan_id;

  UPDATE account SET balance = balance + v_principal WHERE account_no = v_account_no;

  INSERT INTO transactions(account_no, txn_type, amount, balance_after, remarks, done_by_emp)
  VALUES (v_account_no, 'LOAN_DISBURSE', v_principal, v_bal + v_principal, CONCAT('Disbursement for Loan #', p_loan_id), p_emp);

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Loan #', p_loan_id, ' approved and disbursed');
END$$

-- -----------------------------------------------------------------------------
-- 9. sp_reject_loan
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_reject_loan(
  IN p_loan_id INT,
  IN p_emp INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_role VARCHAR(30);
  DECLARE v_emp_active BOOLEAN;
  DECLARE v_status VARCHAR(20);

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  SELECT role, is_active INTO v_role, v_emp_active FROM employee WHERE emp_id = p_emp;
  IF v_role IS NULL OR v_emp_active IS FALSE THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Employee not found or inactive';
  END IF;
  IF v_role NOT IN ('MANAGER', 'LOAN_OFFICER') THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Only MANAGER or LOAN_OFFICER can reject loans';
  END IF;

  SELECT status INTO v_status FROM loan WHERE loan_id = p_loan_id FOR UPDATE;
  IF v_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Loan not found';
  END IF;
  IF v_status <> 'PENDING' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Loan is not in PENDING state';
  END IF;

  UPDATE loan
  SET status = 'REJECTED', approved_by = p_emp, approved_on = CURRENT_DATE
  WHERE loan_id = p_loan_id;

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Loan #', p_loan_id, ' rejected');
END$$

-- -----------------------------------------------------------------------------
-- 10. sp_pay_emi
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_pay_emi(
  IN p_loan_id INT,
  IN p_amount DECIMAL(15,2),
  IN p_emp INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_status VARCHAR(20);
  DECLARE v_outstanding DECIMAL(15,2);
  DECLARE v_account_no BIGINT;
  DECLARE v_bal DECIMAL(15,2);
  DECLARE v_acc_status VARCHAR(10);
  DECLARE v_min_bal DECIMAL(12,2);
  DECLARE v_new_outstanding DECIMAL(15,2);

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF p_amount <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Payment amount must be positive';
  END IF;

  SELECT status, outstanding, account_no
  INTO v_status, v_outstanding, v_account_no
  FROM loan WHERE loan_id = p_loan_id FOR UPDATE;

  IF v_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Loan not found';
  END IF;
  IF v_status <> 'APPROVED' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Loan is not APPROVED';
  END IF;
  IF p_amount > v_outstanding THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Payment amount exceeds total outstanding loan amount';
  END IF;

  SELECT a.balance, a.status, t.min_balance
  INTO v_bal, v_acc_status, v_min_bal
  FROM account a
  JOIN account_type t ON a.type_id = t.type_id
  WHERE a.account_no = v_account_no FOR UPDATE;

  IF v_acc_status <> 'ACTIVE' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Loan repayment account is not active';
  END IF;
  IF (v_bal - p_amount) < v_min_bal THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient balance in repayment account';
  END IF;

  -- Deduct EMI from account
  UPDATE account SET balance = balance - p_amount WHERE account_no = v_account_no;

  -- Record transaction
  INSERT INTO transactions(account_no, txn_type, amount, balance_after, remarks, done_by_emp)
  VALUES (v_account_no, 'LOAN_EMI', p_amount, v_bal - p_amount, CONCAT('EMI for Loan #', p_loan_id), p_emp);

  -- Record payment
  INSERT INTO loan_payment(loan_id, amount, paid_on)
  VALUES (p_loan_id, p_amount, CURRENT_TIMESTAMP);

  -- Update loan outstanding
  SET v_new_outstanding = v_outstanding - p_amount;
  UPDATE loan
  SET outstanding = v_new_outstanding,
      status = IF(v_new_outstanding <= 0, 'CLOSED', status)
  WHERE loan_id = p_loan_id;

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: EMI payment of ', p_amount, ' successful. Remaining: ', v_new_outstanding);
END$$

-- -----------------------------------------------------------------------------
-- 11. sp_apply_charge
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_apply_charge(
  IN p_acc BIGINT,
  IN p_amt DECIMAL(15,2),
  IN p_remarks VARCHAR(200),
  IN p_emp INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_bal DECIMAL(15,2);
  DECLARE v_status VARCHAR(10);

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF p_amt <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Charge amount must be positive';
  END IF;

  SELECT balance, status INTO v_bal, v_status FROM account WHERE account_no = p_acc FOR UPDATE;
  IF v_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account not found';
  END IF;
  IF v_status <> 'ACTIVE' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account is not active';
  END IF;
  IF v_bal < p_amt THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient balance to apply charge';
  END IF;

  UPDATE account SET balance = balance - p_amt WHERE account_no = p_acc;

  INSERT INTO transactions(account_no, txn_type, amount, balance_after, remarks, done_by_emp)
  VALUES (p_acc, 'CHARGE', p_amt, v_bal - p_amt, IFNULL(p_remarks, 'Service charge'), p_emp);

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Charge of ', p_amt, ' applied. New balance: ', v_bal - p_amt);
END$$

-- -----------------------------------------------------------------------------
-- 12. sp_credit_interest
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_credit_interest(
  IN p_emp INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_count INT DEFAULT 0;

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  -- Create temporary table to hold calculated interest for eligible accounts
  DROP TEMPORARY TABLE IF EXISTS tmp_interest;
  CREATE TEMPORARY TABLE tmp_interest AS
  SELECT
    a.account_no,
    a.balance,
    ROUND(a.balance * (t.interest_rate / 1200.0), 2) AS interest
  FROM account a
  JOIN account_type t ON a.type_id = t.type_id
  WHERE a.status = 'ACTIVE'
    AND t.interest_rate > 0
    AND ROUND(a.balance * (t.interest_rate / 1200.0), 2) > 0;

  SELECT COUNT(*) INTO v_count FROM tmp_interest;

  IF v_count > 0 THEN
    -- First: insert into transactions with balance_after = balance + interest
    INSERT INTO transactions(account_no, txn_type, amount, balance_after, remarks, done_by_emp)
    SELECT
      ti.account_no,
      'INTEREST',
      ti.interest,
      ti.balance + ti.interest,
      'Monthly interest credit',
      p_emp
    FROM tmp_interest ti;

    -- Second: update account balances
    UPDATE account a
    JOIN tmp_interest ti ON a.account_no = ti.account_no
    SET a.balance = a.balance + ti.interest;
  END IF;

  DROP TEMPORARY TABLE IF EXISTS tmp_interest;

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Interest credited to ', v_count, ' account(s)');
END$$

-- -----------------------------------------------------------------------------
-- 13. sp_issue_card
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_issue_card(
  IN p_acc BIGINT,
  IN p_card_type VARCHAR(10),
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_status VARCHAR(10);
  DECLARE v_card_num CHAR(16);
  DECLARE v_exists INT;

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF p_card_type NOT IN ('DEBIT', 'CREDIT') THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Card type must be DEBIT or CREDIT';
  END IF;

  SELECT status INTO v_status FROM account WHERE account_no = p_acc FOR UPDATE;
  IF v_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account not found';
  END IF;
  IF v_status <> 'ACTIVE' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Account is not active';
  END IF;

  -- Generate unique 16 digit card number
  REPEAT
    SET v_card_num = CONCAT(
      LPAD(FLOOR(RAND() * 100000000), 8, '0'),
      LPAD(FLOOR(RAND() * 100000000), 8, '0')
    );
    SELECT COUNT(*) INTO v_exists FROM card WHERE card_number = v_card_num;
  UNTIL v_exists = 0
  END REPEAT;

  INSERT INTO card(account_no, card_type, card_number, expiry, status)
  VALUES (p_acc, p_card_type, v_card_num, DATE_ADD(CURRENT_DATE, INTERVAL 5 YEAR), 'ACTIVE');

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Card issued successfully. Card No: ', v_card_num);
END$$

-- -----------------------------------------------------------------------------
-- 14. sp_set_card_status
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_set_card_status(
  IN p_card_id INT,
  IN p_new_status VARCHAR(10),
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_status VARCHAR(10);

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF p_new_status NOT IN ('ACTIVE', 'BLOCKED') THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Status must be ACTIVE or BLOCKED';
  END IF;

  SELECT status INTO v_status FROM card WHERE card_id = p_card_id FOR UPDATE;
  IF v_status IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Card not found';
  END IF;

  UPDATE card SET status = p_new_status WHERE card_id = p_card_id;

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Card status updated to ', p_new_status);
END$$

-- -----------------------------------------------------------------------------
-- 15. sp_add_employee
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_add_employee(
  IN p_name VARCHAR(80),
  IN p_role VARCHAR(20),
  IN p_salary DECIMAL(10,2),
  IN p_branch_id INT,
  IN p_manager_id INT,
  IN p_username VARCHAR(30),
  IN p_password VARCHAR(50),
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE v_emp_id INT;

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF p_role NOT IN ('MANAGER', 'TELLER', 'LOAN_OFFICER', 'CLERK') THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid employee role';
  END IF;
  IF p_salary <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Salary must be positive';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM branch WHERE branch_id = p_branch_id) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid branch ID';
  END IF;
  IF p_manager_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM employee WHERE emp_id = p_manager_id) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Manager does not exist';
  END IF;
  IF EXISTS (SELECT 1 FROM employee WHERE username = p_username) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username is already taken';
  END IF;

  INSERT INTO employee(name, role, salary, branch_id, manager_id, hire_date, username, password_hash, is_active)
  VALUES (p_name, p_role, p_salary, p_branch_id, p_manager_id, CURRENT_DATE, p_username, SHA2(p_password, 256), TRUE);
  SET v_emp_id = LAST_INSERT_ID();

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Employee added with ID: ', v_emp_id);
END$$

-- -----------------------------------------------------------------------------
-- 16. sp_transfer_employee
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_transfer_employee(
  IN p_emp_id INT,
  IN p_new_branch_id INT,
  OUT p_msg VARCHAR(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1 p_msg = MESSAGE_TEXT;
    SET p_msg = CONCAT('ERROR: ', p_msg);
    ROLLBACK;
  END;

  START TRANSACTION;

  IF NOT EXISTS (SELECT 1 FROM employee WHERE emp_id = p_emp_id) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Employee not found';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM branch WHERE branch_id = p_new_branch_id) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Branch not found';
  END IF;

  UPDATE employee SET branch_id = p_new_branch_id WHERE emp_id = p_emp_id;

  COMMIT;
  SET p_msg = CONCAT('SUCCESS: Employee ', p_emp_id, ' transferred to branch ', p_new_branch_id);
END$$

-- -----------------------------------------------------------------------------
-- 17. sp_mini_statement
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_mini_statement(
  IN p_acc BIGINT,
  IN p_n INT
)
BEGIN
  SELECT
    txn_id,
    txn_time,
    txn_type,
    amount,
    balance_after,
    related_account,
    remarks
  FROM transactions
  WHERE account_no = p_acc
  ORDER BY txn_time DESC, txn_id DESC
  LIMIT p_n;
END$$

DELIMITER ;
