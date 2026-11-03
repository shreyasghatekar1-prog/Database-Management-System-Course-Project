-- =============================================================================
-- Bank Management System - Schema Definition
-- File: sql/01_schema.sql
-- =============================================================================

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
