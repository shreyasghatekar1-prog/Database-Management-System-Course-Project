-- =============================================================================
-- Bank Management System - Sample Seed Data
-- File: sql/04_sample_data.sql
-- =============================================================================
USE bank_db;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE audit_log;
TRUNCATE TABLE loan_payment;
TRUNCATE TABLE loan;
TRUNCATE TABLE card;
TRUNCATE TABLE transactions;
TRUNCATE TABLE account;
TRUNCATE TABLE customer;
TRUNCATE TABLE employee;
TRUNCATE TABLE account_type;
TRUNCATE TABLE branch;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. Branches
INSERT INTO branch (branch_id, name, city, ifsc) VALUES (1, 'Pune Main Branch', 'Pune', 'BMSB0001001');
INSERT INTO branch (branch_id, name, city, ifsc) VALUES (2, 'Mumbai Central Branch', 'Mumbai', 'BMSB0002002');
INSERT INTO branch (branch_id, name, city, ifsc) VALUES (3, 'Nashik City Branch', 'Nashik', 'BMSB0003003');

-- 2. Account Types
INSERT INTO account_type (type_id, name, min_balance, interest_rate) VALUES (1, 'SAVINGS', 1000.0, 4.0);
INSERT INTO account_type (type_id, name, min_balance, interest_rate) VALUES (2, 'CURRENT', 5000.0, 0.0);
INSERT INTO account_type (type_id, name, min_balance, interest_rate) VALUES (3, 'FIXED_DEPOSIT', 10000.0, 6.5);

-- 3. Employees
INSERT INTO employee (emp_id, name, role, salary, branch_id, manager_id, hire_date, username, password_hash, is_active) VALUES (1, 'Aditya Deshmukh', 'MANAGER', 95000.0, 1, NULL, '2023-01-15', 'admin', SHA2('admin123', 256), TRUE);
INSERT INTO employee (emp_id, name, role, salary, branch_id, manager_id, hire_date, username, password_hash, is_active) VALUES (2, 'Sneha Joshi', 'TELLER', 45000.0, 1, 1, '2023-01-15', 'teller1', SHA2('pass123', 256), TRUE);
INSERT INTO employee (emp_id, name, role, salary, branch_id, manager_id, hire_date, username, password_hash, is_active) VALUES (3, 'Rohan Kulkarni', 'LOAN_OFFICER', 60000.0, 1, 1, '2023-01-15', 'loan1', SHA2('pass123', 256), TRUE);
INSERT INTO employee (emp_id, name, role, salary, branch_id, manager_id, hire_date, username, password_hash, is_active) VALUES (4, 'Pooja Patil', 'CLERK', 35000.0, 1, 1, '2023-01-15', 'clerk1', SHA2('pass123', 256), TRUE);
INSERT INTO employee (emp_id, name, role, salary, branch_id, manager_id, hire_date, username, password_hash, is_active) VALUES (5, 'Vikram Shinde', 'MANAGER', 92000.0, 2, NULL, '2023-01-15', 'manager2', SHA2('pass123', 256), TRUE);
INSERT INTO employee (emp_id, name, role, salary, branch_id, manager_id, hire_date, username, password_hash, is_active) VALUES (6, 'Neha More', 'TELLER', 44000.0, 2, 5, '2023-01-15', 'teller2', SHA2('pass123', 256), TRUE);
INSERT INTO employee (emp_id, name, role, salary, branch_id, manager_id, hire_date, username, password_hash, is_active) VALUES (7, 'Suresh Gaikwad', 'MANAGER', 90000.0, 3, NULL, '2023-01-15', 'manager3', SHA2('pass123', 256), TRUE);
INSERT INTO employee (emp_id, name, role, salary, branch_id, manager_id, hire_date, username, password_hash, is_active) VALUES (8, 'Kavita Pawar', 'TELLER', 43000.0, 3, 7, '2023-01-15', 'teller3', SHA2('pass123', 256), TRUE);

-- 4. Customers
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (1, 'Rahul Patil', '1990-05-14', '9822011001', 'rahul.patil@example.com', 'FC Road, Shivajinagar, Pune', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (2, 'Priya Sharma', '1994-08-22', '9822011002', 'priya.sharma@example.com', 'Bandra West, Mumbai', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (3, 'Amitabh Kulkarni', '1985-11-03', '9822011003', 'amit.kulkarni@example.com', 'College Road, Nashik', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (4, 'Ananya Deshpande', '1998-02-19', '9822011004', 'ananya.d@example.com', 'Kothrud, Pune', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (5, 'Sachin Tendulkar', '1988-04-24', '9822011005', 'sachin.t@example.com', 'Dadar East, Mumbai', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (6, 'Dipika Ranade', '1992-09-30', '9822011006', 'dipika.r@example.com', 'Indira Nagar, Nashik', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (7, 'Manish Shinde', '1987-07-12', '9822011007', 'manish.shinde@example.com', 'Viman Nagar, Pune', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (8, 'Tanvi Chitnis', '1996-12-05', '9822011008', 'tanvi.c@example.com', 'Andheri East, Mumbai', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (9, 'Rajesh Varma', '1983-03-17', '9822011009', 'rajesh.varma@example.com', 'Panchavati, Nashik', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (10, 'Pooja Nair', '1995-06-25', '9822011010', 'pooja.nair@example.com', 'Aundh, Pune', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (11, 'Gaurav Jadhav', '1991-01-11', '9822011011', 'gaurav.j@example.com', 'Thane West, Mumbai', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (12, 'Swati Bhosle', '1993-10-14', '9822011012', 'swati.b@example.com', 'Gangapur Road, Nashik', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (13, 'Nikhil Gokhale', '1989-04-09', '9822011013', 'nikhil.g@example.com', 'Baner, Pune', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (14, 'Meera Sen', '1997-07-08', '9822011014', 'meera.sen@example.com', 'Powai, Mumbai', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (15, 'Kishore Kumar', '1982-12-21', '9822011015', 'kishore.k@example.com', 'Satpur, Nashik', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (16, 'Radhika Merchant', '1994-03-01', '9822011016', 'radhika.m@example.com', 'Koregaon Park, Pune', 'VERIFIED', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (17, 'Omkar Phadke', '2000-09-18', '9822011017', 'omkar.p@example.com', 'Warje, Pune', 'PENDING', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (18, 'Sonali Kadam', '1999-11-27', '9822011018', 'sonali.k@example.com', 'Borivali, Mumbai', 'PENDING', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (19, 'Vinay Thorat', '2001-05-15', '9822011019', 'vinay.t@example.com', 'CIDCO, Nashik', 'PENDING', '2024-01-10 10:00:00');
INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) VALUES (20, 'Deepak Sawant', '1986-08-10', '9822011020', 'deepak.s@example.com', 'Kurla, Mumbai', 'REJECTED', '2024-01-10 10:00:00');

-- 5. Accounts
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100001, 1, 1, 1, 24000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100002, 2, 1, 2, 19000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100003, 3, 1, 3, 12850.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100004, 4, 1, 1, 13850.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100005, 5, 1, 2, 9850.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100006, 6, 1, 3, 15000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100007, 7, 1, 1, 38900.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100008, 8, 1, 2, 31500.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100009, 9, 1, 3, 11000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100010, 10, 1, 1, 15000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100011, 11, 1, 2, 15000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100012, 12, 1, 3, 17000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100013, 13, 1, 1, 33000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100014, 14, 1, 2, 11000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100015, 15, 1, 3, 14000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100016, 16, 1, 1, 14000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100017, 1, 2, 1, 54000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100018, 2, 2, 2, 79000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100019, 3, 3, 3, 105000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100020, 4, 3, 1, 65000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100021, 5, 2, 2, 49000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100022, 6, 1, 3, 18000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100023, 7, 3, 1, 118000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100024, 8, 2, 2, 76000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100025, 9, 1, 3, 18000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100026, 10, 3, 1, 90000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100027, 11, 2, 2, 30950.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100028, 12, 1, 3, 22000.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100029, 13, 3, 1, 153750.00, 'ACTIVE', '2024-08-01');
INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) VALUES (1000100030, 14, 2, 2, 62000.00, 'ACTIVE', '2024-08-01');

-- 6. Transactions (Total: 93)
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (1, 1000100001, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (2, 1000100002, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (3, 1000100003, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (4, 1000100004, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (5, 1000100005, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (6, 1000100006, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (7, 1000100007, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (8, 1000100008, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (9, 1000100009, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (10, 1000100010, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (11, 1000100011, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (12, 1000100012, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (13, 1000100013, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (14, 1000100014, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (15, 1000100015, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (16, 1000100016, 'DEPOSIT', 15000.00, 15000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (17, 1000100017, 'DEPOSIT', 50000.00, 50000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (18, 1000100018, 'DEPOSIT', 75000.00, 75000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (19, 1000100019, 'DEPOSIT', 100000.00, 100000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (20, 1000100020, 'DEPOSIT', 60000.00, 60000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (21, 1000100021, 'DEPOSIT', 45000.00, 45000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (22, 1000100022, 'DEPOSIT', 20000.00, 20000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (23, 1000100023, 'DEPOSIT', 120000.00, 120000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (24, 1000100024, 'DEPOSIT', 80000.00, 80000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (25, 1000100025, 'DEPOSIT', 25000.00, 25000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (26, 1000100026, 'DEPOSIT', 90000.00, 90000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (27, 1000100027, 'DEPOSIT', 35000.00, 35000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (28, 1000100028, 'DEPOSIT', 18000.00, 18000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (29, 1000100029, 'DEPOSIT', 150000.00, 150000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (30, 1000100030, 'DEPOSIT', 65000.00, 65000.00, NULL, '2024-08-01 10:00:00', 'Initial account opening deposit', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (31, 1000100001, 'DEPOSIT', 8000.00, 23000.00, NULL, '2024-08-03 18:00:00', 'Cash deposit at counter', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (32, 1000100024, 'WITHDRAW', 1000.00, 79000.00, NULL, '2024-08-04 13:00:00', 'ATM / Branch cash withdrawal', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (33, 1000100019, 'DEPOSIT', 10000.00, 110000.00, NULL, '2024-08-06 00:00:00', 'Cash deposit at counter', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (34, 1000100007, 'DEPOSIT', 5000.00, 20000.00, NULL, '2024-08-06 12:00:00', 'Cash deposit at counter', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (35, 1000100018, 'DEPOSIT', 5000.00, 80000.00, NULL, '2024-08-07 19:00:00', 'Cash deposit at counter', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (36, 1000100008, 'CHARGE', 250.00, 14750.00, NULL, '2024-08-09 03:00:00', 'Quarterly SMS and maintenance charge', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (37, 1000100026, 'TRANSFER_OUT', 1000.00, 89000.00, 1000100028, '2024-08-10 09:00:00', 'Fund transfer to 1000100028', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (38, 1000100028, 'TRANSFER_IN', 1000.00, 19000.00, 1000100026, '2024-08-10 09:00:00', 'Fund transfer from 1000100026', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (39, 1000100009, 'TRANSFER_OUT', 1000.00, 14000.00, 1000100005, '2024-08-11 10:00:00', 'Fund transfer to 1000100005', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (40, 1000100005, 'TRANSFER_IN', 1000.00, 16000.00, 1000100009, '2024-08-11 10:00:00', 'Fund transfer from 1000100009', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (41, 1000100004, 'CHARGE', 150.00, 14850.00, NULL, '2024-08-12 00:00:00', 'Quarterly SMS and maintenance charge', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (42, 1000100026, 'TRANSFER_OUT', 4000.00, 85000.00, 1000100002, '2024-08-12 23:00:00', 'Fund transfer to 1000100002', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (43, 1000100002, 'TRANSFER_IN', 4000.00, 19000.00, 1000100026, '2024-08-12 23:00:00', 'Fund transfer from 1000100026', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (44, 1000100003, 'CHARGE', 150.00, 14850.00, NULL, '2024-08-13 14:00:00', 'Quarterly SMS and maintenance charge', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (45, 1000100019, 'TRANSFER_OUT', 4000.00, 106000.00, 1000100007, '2024-08-14 22:00:00', 'Fund transfer to 1000100007', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (46, 1000100007, 'TRANSFER_IN', 4000.00, 24000.00, 1000100019, '2024-08-14 22:00:00', 'Fund transfer from 1000100019', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (47, 1000100025, 'WITHDRAW', 2000.00, 23000.00, NULL, '2024-08-16 07:00:00', 'ATM / Branch cash withdrawal', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (48, 1000100013, 'DEPOSIT', 8000.00, 23000.00, NULL, '2024-08-17 02:00:00', 'Cash deposit at counter', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (49, 1000100006, 'TRANSFER_OUT', 2000.00, 13000.00, 1000100012, '2024-08-18 10:00:00', 'Fund transfer to 1000100012', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (50, 1000100012, 'TRANSFER_IN', 2000.00, 17000.00, 1000100006, '2024-08-18 10:00:00', 'Fund transfer from 1000100006', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (51, 1000100020, 'DEPOSIT', 5000.00, 65000.00, NULL, '2024-08-19 06:00:00', 'Cash deposit at counter', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (52, 1000100006, 'WITHDRAW', 2000.00, 11000.00, NULL, '2024-08-20 17:00:00', 'ATM / Branch cash withdrawal', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (53, 1000100022, 'WITHDRAW', 2000.00, 18000.00, NULL, '2024-08-21 13:00:00', 'ATM / Branch cash withdrawal', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (54, 1000100026, 'DEPOSIT', 8000.00, 93000.00, NULL, '2024-08-22 08:00:00', 'Cash deposit at counter', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (55, 1000100007, 'DEPOSIT', 15000.00, 39000.00, NULL, '2024-08-23 04:00:00', 'Cash deposit at counter', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (56, 1000100021, 'WITHDRAW', 2000.00, 43000.00, NULL, '2024-08-24 02:00:00', 'ATM / Branch cash withdrawal', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (57, 1000100005, 'CHARGE', 150.00, 15850.00, NULL, '2024-08-25 10:00:00', 'Quarterly SMS and maintenance charge', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (58, 1000100024, 'WITHDRAW', 3000.00, 76000.00, NULL, '2024-08-26 02:00:00', 'ATM / Branch cash withdrawal', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (59, 1000100029, 'CHARGE', 250.00, 149750.00, NULL, '2024-08-26 22:00:00', 'Quarterly SMS and maintenance charge', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (60, 1000100005, 'WITHDRAW', 3000.00, 12850.00, NULL, '2024-08-27 21:00:00', 'ATM / Branch cash withdrawal', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (61, 1000100028, 'DEPOSIT', 2000.00, 21000.00, NULL, '2024-08-28 11:00:00', 'Cash deposit at counter', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (62, 1000100026, 'WITHDRAW', 3000.00, 90000.00, NULL, '2024-08-29 19:00:00', 'ATM / Branch cash withdrawal', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (63, 1000100013, 'DEPOSIT', 10000.00, 33000.00, NULL, '2024-08-31 02:00:00', 'Cash deposit at counter', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (64, 1000100018, 'TRANSFER_OUT', 1000.00, 79000.00, 1000100028, '2024-09-01 04:00:00', 'Fund transfer to 1000100028', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (65, 1000100028, 'TRANSFER_IN', 1000.00, 22000.00, 1000100018, '2024-09-01 04:00:00', 'Fund transfer from 1000100018', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (66, 1000100025, 'TRANSFER_OUT', 2000.00, 21000.00, 1000100021, '2024-09-01 19:00:00', 'Fund transfer to 1000100021', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (67, 1000100021, 'TRANSFER_IN', 2000.00, 45000.00, 1000100025, '2024-09-01 19:00:00', 'Fund transfer from 1000100025', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (68, 1000100015, 'WITHDRAW', 1000.00, 14000.00, NULL, '2024-09-02 20:00:00', 'ATM / Branch cash withdrawal', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (69, 1000100017, 'TRANSFER_OUT', 1000.00, 49000.00, 1000100025, '2024-09-04 07:00:00', 'Fund transfer to 1000100025', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (70, 1000100025, 'TRANSFER_IN', 1000.00, 22000.00, 1000100017, '2024-09-04 07:00:00', 'Fund transfer from 1000100017', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (71, 1000100027, 'TRANSFER_OUT', 4000.00, 31000.00, 1000100021, '2024-09-05 15:00:00', 'Fund transfer to 1000100021', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (72, 1000100021, 'TRANSFER_IN', 4000.00, 49000.00, 1000100027, '2024-09-05 15:00:00', 'Fund transfer from 1000100027', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (73, 1000100025, 'TRANSFER_OUT', 4000.00, 18000.00, 1000100006, '2024-09-06 07:00:00', 'Fund transfer to 1000100006', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (74, 1000100006, 'TRANSFER_IN', 4000.00, 15000.00, 1000100025, '2024-09-06 07:00:00', 'Fund transfer from 1000100025', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (75, 1000100016, 'TRANSFER_OUT', 1000.00, 14000.00, 1000100001, '2024-09-07 14:00:00', 'Fund transfer to 1000100001', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (76, 1000100001, 'TRANSFER_IN', 1000.00, 24000.00, 1000100016, '2024-09-07 14:00:00', 'Fund transfer from 1000100016', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (77, 1000100008, 'DEPOSIT', 15000.00, 29750.00, NULL, '2024-09-08 09:00:00', 'Cash deposit at counter', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (78, 1000100027, 'CHARGE', 50.00, 30950.00, NULL, '2024-09-08 23:00:00', 'Quarterly SMS and maintenance charge', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (79, 1000100005, 'WITHDRAW', 3000.00, 9850.00, NULL, '2024-09-10 11:00:00', 'ATM / Branch cash withdrawal', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (80, 1000100009, 'WITHDRAW', 3000.00, 11000.00, NULL, '2024-09-11 16:00:00', 'ATM / Branch cash withdrawal', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (81, 1000100030, 'WITHDRAW', 3000.00, 62000.00, NULL, '2024-09-12 17:00:00', 'ATM / Branch cash withdrawal', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (82, 1000100023, 'WITHDRAW', 2000.00, 118000.00, NULL, '2024-09-14 03:00:00', 'ATM / Branch cash withdrawal', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (83, 1000100015, 'TRANSFER_OUT', 4000.00, 10000.00, 1000100029, '2024-09-15 12:00:00', 'Fund transfer to 1000100029', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (84, 1000100029, 'TRANSFER_IN', 4000.00, 153750.00, 1000100015, '2024-09-15 12:00:00', 'Fund transfer from 1000100015', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (85, 1000100003, 'WITHDRAW', 2000.00, 12850.00, NULL, '2024-09-16 07:00:00', 'ATM / Branch cash withdrawal', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (86, 1000100019, 'WITHDRAW', 1000.00, 105000.00, NULL, '2024-09-17 13:00:00', 'ATM / Branch cash withdrawal', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (87, 1000100008, 'DEPOSIT', 2000.00, 31750.00, NULL, '2024-09-18 03:00:00', 'Cash deposit at counter', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (88, 1000100017, 'DEPOSIT', 5000.00, 54000.00, NULL, '2024-09-19 01:00:00', 'Cash deposit at counter', 6);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (89, 1000100007, 'CHARGE', 100.00, 38900.00, NULL, '2024-09-20 10:00:00', 'Quarterly SMS and maintenance charge', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (90, 1000100008, 'CHARGE', 250.00, 31500.00, NULL, '2024-09-21 21:00:00', 'Quarterly SMS and maintenance charge', 1);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (91, 1000100004, 'WITHDRAW', 1000.00, 13850.00, NULL, '2024-09-22 22:00:00', 'ATM / Branch cash withdrawal', 8);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (92, 1000100014, 'TRANSFER_OUT', 4000.00, 11000.00, 1000100015, '2024-09-23 23:00:00', 'Fund transfer to 1000100015', 2);
INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) VALUES (93, 1000100015, 'TRANSFER_IN', 4000.00, 14000.00, 1000100014, '2024-09-23 23:00:00', 'Fund transfer from 1000100014', 8);

-- 7. Loans and Loan Payments
INSERT INTO loan (loan_id, customer_id, account_no, principal, annual_rate, tenure_months, emi, outstanding, status, applied_on, approved_by, approved_on) VALUES (1, 1, 1000100001, 100000.00, 10.50, 12, 8814.86, 88148.60, 'APPROVED', '2024-05-10', 3, '2024-05-12');
INSERT INTO loan (loan_id, customer_id, account_no, principal, annual_rate, tenure_months, emi, outstanding, status, applied_on, approved_by, approved_on) VALUES (2, 2, 1000100002, 250000.00, 9.50, 24, 11480.20, 252564.40, 'APPROVED', '2024-06-01', 3, '2024-06-03');
INSERT INTO loan (loan_id, customer_id, account_no, principal, annual_rate, tenure_months, emi, outstanding, status, applied_on, approved_by, approved_on) VALUES (3, 4, 1000100004, 50000.00, 11.00, 6, 8603.95, 34415.80, 'APPROVED', '2024-07-01', 3, '2024-07-02');
INSERT INTO loan (loan_id, customer_id, account_no, principal, annual_rate, tenure_months, emi, outstanding, status, applied_on, approved_by, approved_on) VALUES (4, 5, 1000100005, 300000.00, 9.00, 36, 9540.00, 343440.00, 'PENDING', '2024-09-01', NULL, NULL);
INSERT INTO loan (loan_id, customer_id, account_no, principal, annual_rate, tenure_months, emi, outstanding, status, applied_on, approved_by, approved_on) VALUES (5, 7, 1000100007, 150000.00, 10.00, 12, 13187.00, 158244.00, 'PENDING', '2024-09-10', NULL, NULL);
INSERT INTO loan (loan_id, customer_id, account_no, principal, annual_rate, tenure_months, emi, outstanding, status, applied_on, approved_by, approved_on) VALUES (6, 9, 1000100009, 80000.00, 12.00, 12, 7108.00, 85296.00, 'REJECTED', '2024-04-15', 3, '2024-04-16');

-- Loan Payments
INSERT INTO loan_payment (payment_id, loan_id, amount, paid_on) VALUES (1, 1, 8814.86, '2024-06-12 11:30:00');
INSERT INTO loan_payment (payment_id, loan_id, amount, paid_on) VALUES (2, 1, 8814.86, '2024-07-12 14:15:00');
INSERT INTO loan_payment (payment_id, loan_id, amount, paid_on) VALUES (3, 2, 11480.20, '2024-07-03 10:20:00');
INSERT INTO loan_payment (payment_id, loan_id, amount, paid_on) VALUES (4, 2, 11480.20, '2024-08-03 16:45:00');
INSERT INTO loan_payment (payment_id, loan_id, amount, paid_on) VALUES (5, 3, 8603.95, '2024-08-02 12:00:00');
INSERT INTO loan_payment (payment_id, loan_id, amount, paid_on) VALUES (6, 3, 8603.95, '2024-09-02 15:30:00');

-- 8. Cards
INSERT INTO card (card_id, account_no, card_type, card_number, expiry, status) VALUES (1, 1000100001, 'DEBIT', '4532789123456701', '2029-08-01', 'ACTIVE');
INSERT INTO card (card_id, account_no, card_type, card_number, expiry, status) VALUES (2, 1000100002, 'DEBIT', '4532789123456702', '2029-08-01', 'ACTIVE');
INSERT INTO card (card_id, account_no, card_type, card_number, expiry, status) VALUES (3, 1000100003, 'CREDIT', '5421890123456703', '2029-08-01', 'ACTIVE');
INSERT INTO card (card_id, account_no, card_type, card_number, expiry, status) VALUES (4, 1000100004, 'DEBIT', '4532789123456704', '2029-08-01', 'BLOCKED');
INSERT INTO card (card_id, account_no, card_type, card_number, expiry, status) VALUES (5, 1000100005, 'CREDIT', '5421890123456705', '2029-08-01', 'ACTIVE');
INSERT INTO card (card_id, account_no, card_type, card_number, expiry, status) VALUES (6, 1000100006, 'DEBIT', '4532789123456706', '2029-08-01', 'ACTIVE');
INSERT INTO card (card_id, account_no, card_type, card_number, expiry, status) VALUES (7, 1000100007, 'DEBIT', '4532789123456707', '2029-08-01', 'ACTIVE');
INSERT INTO card (card_id, account_no, card_type, card_number, expiry, status) VALUES (8, 1000100008, 'CREDIT', '5421890123456708', '2029-08-01', 'BLOCKED');
INSERT INTO card (card_id, account_no, card_type, card_number, expiry, status) VALUES (9, 1000100009, 'DEBIT', '4532789123456709', '2029-08-01', 'ACTIVE');
INSERT INTO card (card_id, account_no, card_type, card_number, expiry, status) VALUES (10, 1000100010, 'DEBIT', '4532789123456710', '2029-08-01', 'ACTIVE');
