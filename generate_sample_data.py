import random
import datetime

# Seed for reproducibility
random.seed(42)

def generate_sql():
    sql = []
    sql.append("-- =============================================================================")
    sql.append("-- Bank Management System - Sample Seed Data")
    sql.append("-- File: sql/04_sample_data.sql")
    sql.append("-- =============================================================================")
    sql.append("USE bank_db;\n")
    sql.append("SET FOREIGN_KEY_CHECKS = 0;")
    sql.append("TRUNCATE TABLE audit_log;")
    sql.append("TRUNCATE TABLE loan_payment;")
    sql.append("TRUNCATE TABLE loan;")
    sql.append("TRUNCATE TABLE card;")
    sql.append("TRUNCATE TABLE transactions;")
    sql.append("TRUNCATE TABLE account;")
    sql.append("TRUNCATE TABLE customer;")
    sql.append("TRUNCATE TABLE employee;")
    sql.append("TRUNCATE TABLE account_type;")
    sql.append("TRUNCATE TABLE branch;")
    sql.append("SET FOREIGN_KEY_CHECKS = 1;\n")

    # 1. Branches (3 branches)
    sql.append("-- 1. Branches")
    branches = [
        (1, "Pune Main Branch", "Pune", "BMSB0001001"),
        (2, "Mumbai Central Branch", "Mumbai", "BMSB0002002"),
        (3, "Nashik City Branch", "Nashik", "BMSB0003003")
    ]
    for b in branches:
        sql.append(f"INSERT INTO branch (branch_id, name, city, ifsc) VALUES ({b[0]}, '{b[1]}', '{b[2]}', '{b[3]}');")
    sql.append("")

    # 2. Account Types (3 types)
    sql.append("-- 2. Account Types")
    types = [
        (1, "SAVINGS", 1000.00, 4.00),
        (2, "CURRENT", 5000.00, 0.00),
        (3, "FIXED_DEPOSIT", 10000.00, 6.50)
    ]
    for t in types:
        sql.append(f"INSERT INTO account_type (type_id, name, min_balance, interest_rate) VALUES ({t[0]}, '{t[1]}', {t[2]}, {t[3]});")
    sql.append("")

    # 3. Employees (8 employees, required logins: admin, teller1, loan1, clerk1)
    sql.append("-- 3. Employees")
    employees = [
        # id, name, role, salary, branch_id, manager_id, username, password_plain
        (1, "Aditya Deshmukh", "MANAGER", 95000.00, 1, "NULL", "admin", "admin123"),
        (2, "Sneha Joshi", "TELLER", 45000.00, 1, 1, "teller1", "pass123"),
        (3, "Rohan Kulkarni", "LOAN_OFFICER", 60000.00, 1, 1, "loan1", "pass123"),
        (4, "Pooja Patil", "CLERK", 35000.00, 1, 1, "clerk1", "pass123"),
        (5, "Vikram Shinde", "MANAGER", 92000.00, 2, "NULL", "manager2", "pass123"),
        (6, "Neha More", "TELLER", 44000.00, 2, 5, "teller2", "pass123"),
        (7, "Suresh Gaikwad", "MANAGER", 90000.00, 3, "NULL", "manager3", "pass123"),
        (8, "Kavita Pawar", "TELLER", 43000.00, 3, 7, "teller3", "pass123")
    ]
    for e in employees:
        mgr = e[5] if e[5] == "NULL" else str(e[5])
        sql.append(f"INSERT INTO employee (emp_id, name, role, salary, branch_id, manager_id, hire_date, username, password_hash, is_active) "
                   f"VALUES ({e[0]}, '{e[1]}', '{e[2]}', {e[3]}, {e[4]}, {mgr}, '2023-01-15', '{e[6]}', SHA2('{e[7]}', 256), TRUE);")
    sql.append("")

    # 4. Customers (20 customers: 16 VERIFIED, 3 PENDING, 1 REJECTED)
    sql.append("-- 4. Customers")
    customer_data = [
        ("Rahul Patil", "1990-05-14", "9822011001", "rahul.patil@example.com", "FC Road, Shivajinagar, Pune", "VERIFIED"),
        ("Priya Sharma", "1994-08-22", "9822011002", "priya.sharma@example.com", "Bandra West, Mumbai", "VERIFIED"),
        ("Amitabh Kulkarni", "1985-11-03", "9822011003", "amit.kulkarni@example.com", "College Road, Nashik", "VERIFIED"),
        ("Ananya Deshpande", "1998-02-19", "9822011004", "ananya.d@example.com", "Kothrud, Pune", "VERIFIED"),
        ("Sachin Tendulkar", "1988-04-24", "9822011005", "sachin.t@example.com", "Dadar East, Mumbai", "VERIFIED"),
        ("Dipika Ranade", "1992-09-30", "9822011006", "dipika.r@example.com", "Indira Nagar, Nashik", "VERIFIED"),
        ("Manish Shinde", "1987-07-12", "9822011007", "manish.shinde@example.com", "Viman Nagar, Pune", "VERIFIED"),
        ("Tanvi Chitnis", "1996-12-05", "9822011008", "tanvi.c@example.com", "Andheri East, Mumbai", "VERIFIED"),
        ("Rajesh Varma", "1983-03-17", "9822011009", "rajesh.varma@example.com", "Panchavati, Nashik", "VERIFIED"),
        ("Pooja Nair", "1995-06-25", "9822011010", "pooja.nair@example.com", "Aundh, Pune", "VERIFIED"),
        ("Gaurav Jadhav", "1991-01-11", "9822011011", "gaurav.j@example.com", "Thane West, Mumbai", "VERIFIED"),
        ("Swati Bhosle", "1993-10-14", "9822011012", "swati.b@example.com", "Gangapur Road, Nashik", "VERIFIED"),
        ("Nikhil Gokhale", "1989-04-09", "9822011013", "nikhil.g@example.com", "Baner, Pune", "VERIFIED"),
        ("Meera Sen", "1997-07-08", "9822011014", "meera.sen@example.com", "Powai, Mumbai", "VERIFIED"),
        ("Kishore Kumar", "1982-12-21", "9822011015", "kishore.k@example.com", "Satpur, Nashik", "VERIFIED"),
        ("Radhika Merchant", "1994-03-01", "9822011016", "radhika.m@example.com", "Koregaon Park, Pune", "VERIFIED"),
        # 3 PENDING
        ("Omkar Phadke", "2000-09-18", "9822011017", "omkar.p@example.com", "Warje, Pune", "PENDING"),
        ("Sonali Kadam", "1999-11-27", "9822011018", "sonali.k@example.com", "Borivali, Mumbai", "PENDING"),
        ("Vinay Thorat", "2001-05-15", "9822011019", "vinay.t@example.com", "CIDCO, Nashik", "PENDING"),
        # 1 REJECTED
        ("Deepak Sawant", "1986-08-10", "9822011020", "deepak.s@example.com", "Kurla, Mumbai", "REJECTED")
    ]
    for cid, c in enumerate(customer_data, 1):
        sql.append(f"INSERT INTO customer (customer_id, name, dob, phone, email, address, kyc_status, created_at) "
                   f"VALUES ({cid}, '{c[0]}', '{c[1]}', '{c[2]}', '{c[3]}', '{c[4]}', '{c[5]}', '2024-01-10 10:00:00');")
    sql.append("")

    # 5. Accounts (30 accounts for verified customers 1-16)
    # Start auto increment at 1000100001
    sql.append("-- 5. Accounts")
    # Define initial opening deposits
    account_defs = []
    # (acc_no, customer_id, type_id, branch_id, opening_deposit)
    acc_id = 1000100001
    for c_id in range(1, 17):
        # Every verified customer gets at least 1 SAVINGS account
        branch = ((c_id - 1) % 3) + 1
        account_defs.append((acc_id, c_id, 1, branch, 15000.00))
        acc_id += 1
    # Additional accounts (CURRENT, FIXED_DEPOSIT, extra SAVINGS) up to 30 accounts
    extra_types = [
        (1, 2, 1, 50000.00), # c1 CURRENT
        (2, 2, 2, 75000.00), # c2 CURRENT
        (3, 3, 3, 100000.00),# c3 FD
        (4, 3, 1, 60000.00), # c4 FD
        (5, 2, 2, 45000.00), # c5 CURRENT
        (6, 1, 3, 20000.00), # c6 SAVINGS
        (7, 3, 1, 120000.00),# c7 FD
        (8, 2, 2, 80000.00), # c8 CURRENT
        (9, 1, 3, 25000.00), # c9 SAVINGS
        (10, 3, 1, 90000.00),# c10 FD
        (11, 2, 2, 35000.00),# c11 CURRENT
        (12, 1, 3, 18000.00),# c12 SAVINGS
        (13, 3, 1, 150000.00),# c13 FD
        (14, 2, 2, 65000.00) # c14 CURRENT
    ]
    for ext in extra_types:
        account_defs.append((acc_id, ext[0], ext[1], ext[2], ext[3]))
        acc_id += 1

    # Ledger tracking: acc_no -> { 'balance': current_bal, 'history': [] }
    ledger = {}
    txns = [] # (txn_id, account_no, txn_type, amount, balance_after, related_acc, txn_time, remarks, emp_id)
    txn_counter = 1

    base_time = datetime.datetime(2024, 8, 1, 10, 0, 0)

    # Initial deposit transaction for each account
    for a in account_defs:
        acc_no, cid, tid, bid, op_bal = a
        ledger[acc_no] = {
            'cid': cid,
            'tid': tid,
            'bid': bid,
            'bal': op_bal,
            'op_bal': op_bal
        }
        # Opening deposit transaction
        txns.append({
            'txn_id': txn_counter,
            'account_no': acc_no,
            'txn_type': 'DEPOSIT',
            'amount': op_bal,
            'balance_after': op_bal,
            'related_account': 'NULL',
            'txn_time': base_time.strftime('%Y-%m-%d %H:%M:%S'),
            'remarks': 'Initial account opening deposit',
            'emp_id': 1
        })
        txn_counter += 1

    # Now generate ~70-80 additional transactions across the last 60 days to reach ~100 total transactions
    # Types: DEPOSIT, WITHDRAW, TRANSFER pairs, CHARGE
    cur_time = base_time + datetime.timedelta(days=1)
    acc_list = [a[0] for a in account_defs]

    # Generate varied transactions
    for step in range(50):
        cur_time += datetime.timedelta(hours=random.randint(12, 36))
        time_str = cur_time.strftime('%Y-%m-%d %H:%M:%S')

        action = random.choice(['DEPOSIT', 'WITHDRAW', 'TRANSFER', 'CHARGE'])
        if action == 'DEPOSIT':
            acc = random.choice(acc_list)
            amt = random.choice([2000.0, 5000.0, 8000.0, 10000.0, 15000.0])
            ledger[acc]['bal'] += amt
            txns.append({
                'txn_id': txn_counter,
                'account_no': acc,
                'txn_type': 'DEPOSIT',
                'amount': amt,
                'balance_after': ledger[acc]['bal'],
                'related_account': 'NULL',
                'txn_time': time_str,
                'remarks': 'Cash deposit at counter',
                'emp_id': random.choice([2, 6, 8])
            })
            txn_counter += 1

        elif action == 'WITHDRAW':
            # Pick account with enough balance above min_balance
            acc = random.choice(acc_list)
            min_bal = 1000.0 if ledger[acc]['tid'] == 1 else (5000.0 if ledger[acc]['tid'] == 2 else 10000.0)
            avail = ledger[acc]['bal'] - min_bal
            if avail > 3000.0:
                amt = float(random.choice([1000, 2000, 3000]))
                ledger[acc]['bal'] -= amt
                txns.append({
                    'txn_id': txn_counter,
                    'account_no': acc,
                    'txn_type': 'WITHDRAW',
                    'amount': amt,
                    'balance_after': ledger[acc]['bal'],
                    'related_account': 'NULL',
                    'txn_time': time_str,
                    'remarks': 'ATM / Branch cash withdrawal',
                    'emp_id': random.choice([2, 6, 8])
                })
                txn_counter += 1

        elif action == 'CHARGE':
            acc = random.choice(acc_list)
            if ledger[acc]['bal'] > 1000.0:
                amt = float(random.choice([50, 100, 150, 250]))
                ledger[acc]['bal'] -= amt
                txns.append({
                    'txn_id': txn_counter,
                    'account_no': acc,
                    'txn_type': 'CHARGE',
                    'amount': amt,
                    'balance_after': ledger[acc]['bal'],
                    'related_account': 'NULL',
                    'txn_time': time_str,
                    'remarks': 'Quarterly SMS and maintenance charge',
                    'emp_id': 1
                })
                txn_counter += 1

        elif action == 'TRANSFER':
            # Pick two distinct accounts
            acc1, acc2 = random.sample(acc_list, 2)
            min_bal1 = 1000.0 if ledger[acc1]['tid'] == 1 else (5000.0 if ledger[acc1]['tid'] == 2 else 10000.0)
            avail1 = ledger[acc1]['bal'] - min_bal1
            if avail1 > 2000.0:
                amt = float(random.choice([1000, 2000, 4000]))
                ledger[acc1]['bal'] -= amt
                ledger[acc2]['bal'] += amt

                # Out txn
                txns.append({
                    'txn_id': txn_counter,
                    'account_no': acc1,
                    'txn_type': 'TRANSFER_OUT',
                    'amount': amt,
                    'balance_after': ledger[acc1]['bal'],
                    'related_account': acc2,
                    'txn_time': time_str,
                    'remarks': f'Fund transfer to {acc2}',
                    'emp_id': random.choice([2, 6, 8])
                })
                txn_counter += 1

                # In txn
                txns.append({
                    'txn_id': txn_counter,
                    'account_no': acc2,
                    'txn_type': 'TRANSFER_IN',
                    'amount': amt,
                    'balance_after': ledger[acc2]['bal'],
                    'related_account': acc1,
                    'txn_time': time_str,
                    'remarks': f'Fund transfer from {acc1}',
                    'emp_id': random.choice([2, 6, 8])
                })
                txn_counter += 1

    # Write accounts with their final balances!
    for a in account_defs:
        acc_no = a[0]
        cid = ledger[acc_no]['cid']
        tid = ledger[acc_no]['tid']
        bid = ledger[acc_no]['bid']
        final_bal = ledger[acc_no]['bal']
        sql.append(f"INSERT INTO account (account_no, customer_id, type_id, branch_id, balance, status, opened_on) "
                   f"VALUES ({acc_no}, {cid}, {tid}, {bid}, {final_bal:.2f}, 'ACTIVE', '2024-08-01');")
    sql.append("")

    # Write transactions
    sql.append("-- 6. Transactions (Total: " + str(len(txns)) + ")")
    for tx in txns:
        rel = tx['related_account'] if tx['related_account'] != 'NULL' else "NULL"
        emp = tx['emp_id'] if tx['emp_id'] else "NULL"
        sql.append(f"INSERT INTO transactions (txn_id, account_no, txn_type, amount, balance_after, related_account, txn_time, remarks, done_by_emp) "
                   f"VALUES ({tx['txn_id']}, {tx['account_no']}, '{tx['txn_type']}', {tx['amount']:.2f}, {tx['balance_after']:.2f}, {rel}, '{tx['txn_time']}', '{tx['remarks']}', {emp});")
    sql.append("")

    # 7. Loans (6 loans: 3 APPROVED with payments, 2 PENDING, 1 REJECTED)
    sql.append("-- 7. Loans and Loan Payments")
    loans = [
        # loan_id, customer_id, account_no, principal, rate, tenure, emi, outstanding, status, applied_on, approved_by, approved_on
        (1, 1, 1000100001, 100000.00, 10.50, 12, 8814.86, 88148.60, 'APPROVED', '2024-05-10', 3, '2024-05-12'),
        (2, 2, 1000100002, 250000.00, 9.50, 24, 11480.20, 252564.40, 'APPROVED', '2024-06-01', 3, '2024-06-03'),
        (3, 4, 1000100004, 50000.00, 11.00, 6, 8603.95, 34415.80, 'APPROVED', '2024-07-01', 3, '2024-07-02'),
        (4, 5, 1000100005, 300000.00, 9.00, 36, 9540.00, 343440.00, 'PENDING', '2024-09-01', 'NULL', 'NULL'),
        (5, 7, 1000100007, 150000.00, 10.00, 12, 13187.00, 158244.00, 'PENDING', '2024-09-10', 'NULL', 'NULL'),
        (6, 9, 1000100009, 80000.00, 12.00, 12, 7108.00, 85296.00, 'REJECTED', '2024-04-15', 3, '2024-04-16')
    ]
    for l in loans:
        app_by = l[10] if l[10] != 'NULL' else "NULL"
        app_on = f"'{l[11]}'" if l[11] != 'NULL' else "NULL"
        sql.append(f"INSERT INTO loan (loan_id, customer_id, account_no, principal, annual_rate, tenure_months, emi, outstanding, status, applied_on, approved_by, approved_on) "
                   f"VALUES ({l[0]}, {l[1]}, {l[2]}, {l[3]:.2f}, {l[4]:.2f}, {l[5]}, {l[6]:.2f}, {l[7]:.2f}, '{l[8]}', '{l[9]}', {app_by}, {app_on});")
    sql.append("")

    # Loan payments for the 3 approved loans
    sql.append("-- Loan Payments")
    loan_payments = [
        # payment_id, loan_id, amount, paid_on
        (1, 1, 8814.86, '2024-06-12 11:30:00'),
        (2, 1, 8814.86, '2024-07-12 14:15:00'),
        (3, 2, 11480.20, '2024-07-03 10:20:00'),
        (4, 2, 11480.20, '2024-08-03 16:45:00'),
        (5, 3, 8603.95, '2024-08-02 12:00:00'),
        (6, 3, 8603.95, '2024-09-02 15:30:00')
    ]
    for lp in loan_payments:
        sql.append(f"INSERT INTO loan_payment (payment_id, loan_id, amount, paid_on) VALUES ({lp[0]}, {lp[1]}, {lp[2]:.2f}, '{lp[3]}');")
    sql.append("")

    # 8. Cards (10 cards: mix of DEBIT/CREDIT, 2 BLOCKED)
    sql.append("-- 8. Cards")
    cards = [
        # card_id, account_no, card_type, card_number, expiry, status
        (1, 1000100001, 'DEBIT', '4532789123456701', '2029-08-01', 'ACTIVE'),
        (2, 1000100002, 'DEBIT', '4532789123456702', '2029-08-01', 'ACTIVE'),
        (3, 1000100003, 'CREDIT', '5421890123456703', '2029-08-01', 'ACTIVE'),
        (4, 1000100004, 'DEBIT', '4532789123456704', '2029-08-01', 'BLOCKED'),
        (5, 1000100005, 'CREDIT', '5421890123456705', '2029-08-01', 'ACTIVE'),
        (6, 1000100006, 'DEBIT', '4532789123456706', '2029-08-01', 'ACTIVE'),
        (7, 1000100007, 'DEBIT', '4532789123456707', '2029-08-01', 'ACTIVE'),
        (8, 1000100008, 'CREDIT', '5421890123456708', '2029-08-01', 'BLOCKED'),
        (9, 1000100009, 'DEBIT', '4532789123456709', '2029-08-01', 'ACTIVE'),
        (10, 1000100010, 'DEBIT', '4532789123456710', '2029-08-01', 'ACTIVE')
    ]
    for c in cards:
        sql.append(f"INSERT INTO card (card_id, account_no, card_type, card_number, expiry, status) "
                   f"VALUES ({c[0]}, {c[1]}, '{c[2]}', '{c[3]}', '{c[4]}', '{c[5]}');")
    sql.append("")

    # Verify ledger consistency
    print(f"Total accounts generated: {len(account_defs)}")
    print(f"Total transactions generated: {len(txns)}")
    for acc_no in ledger:
        acc_bal = ledger[acc_no]['bal']
        # Calculate signed sum of transactions
        calc_bal = 0.0
        for tx in txns:
            if tx['account_no'] == acc_no:
                if tx['txn_type'] in ('DEPOSIT', 'TRANSFER_IN', 'INTEREST', 'LOAN_DISBURSE'):
                    calc_bal += tx['amount']
                elif tx['txn_type'] in ('WITHDRAW', 'TRANSFER_OUT', 'LOAN_EMI', 'CHARGE'):
                    calc_bal -= tx['amount']
        assert round(calc_bal, 2) == round(acc_bal, 2), f"Ledger mismatch for account {acc_no}: {calc_bal} != {acc_bal}"
    print("Ledger consistency verified! All 30 accounts match their transaction ledgers perfectly.")

    with open("sql/04_sample_data.sql", "w", encoding="utf-8") as f:
        f.write("\n".join(sql))
    print("Wrote sql/04_sample_data.sql successfully.")

if __name__ == "__main__":
    generate_sql()
