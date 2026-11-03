# Bank Management System (BMS)

A robust, enterprise-grade Bank Management System built for the Database Management Systems (DBMS) Course Project. The system enforces all core business logic and transactional integrity strictly within MySQL 8.0 (stored procedures, triggers, declarative constraints, and views), complemented by an intuitive Streamlit dashboard.

---

## 1. Key Features

- **Relational Integrity & 3NF Design**: Fully normalized 10-table schema with foreign keys, composite indexes, and integrity checks.
- **Database-First Business Logic**: All fund operations, account opening/closures, loan disbursements, and interest credits are performed via stored procedures with explicit `START TRANSACTION`, `COMMIT`, and `ROLLBACK` blocks.
- **ACID Deadlock Prevention**: Inter-account transfers sort and lock rows in ascending primary key order (`SELECT ... FOR UPDATE`).
- **Comprehensive Audit Trail**: Database triggers automatically log insertions and status transitions across accounts, transactions, and loans into `audit_log`.
- **Role-Based Access Control (RBAC)**: Enforces access restrictions for 4 bank roles: `MANAGER`, `TELLER`, `LOAN_OFFICER`, and `CLERK`.
- **Analytical & Compliance Reports**: Visualizes branch deposit distributions, high-net-worth customer ranks, monthly inflow trajectories, dormant account detection, and full CSV exports.

---

## 2. Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Database** | MySQL 8.0+ (InnoDB Engine) |
| **DB Connector** | `mysql-connector-python` |
| **User Interface** | Streamlit (Multi-page App) |
| **Data Processing** | pandas |
| **Visualizations** | Plotly Express |
| **Environment Configuration** | `python-dotenv` (`.env`) |
| **Python Runtime** | Python 3.10+ |

---

## 3. Demonstration Credentials

All accounts are pre-seeded in `sql/04_sample_data.sql`:

| Username | Password | Role | Permissions |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | **MANAGER** | Full access to all modules, staff management, charges, interest run, reports |
| `teller1` | `pass123` | **TELLER** | Deposits, cash withdrawals, transfers, account operations |
| `loan1` | `pass123` | **LOAN_OFFICER** | Loan origination, application approvals/rejections, loan analytics |
| `clerk1` | `pass123` | **CLERK** | Customer onboarding (18+), KYC status updates, card issuance |

---

## 4. Setup & Installation Instructions

### Prerequisites
1. **MySQL Server 8.0+** running locally on port 3306.
2. **Python 3.10+** installed.

### Step-by-Step Setup

```bash
# 1. Clone repository / navigate to project root
cd "Database Management System Course Project"

# 2. Set up virtual environment
python -m venv .venv

# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On Linux / macOS:
# source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
# Copy .env.example to .env and set your MySQL root password:
cp .env.example .env
# Edit .env:
# DB_HOST=localhost
# DB_PORT=3306
# DB_USER=root
# DB_PASSWORD=your_mysql_password
# DB_NAME=bank_db

# 5. Initialize Database and Seed Data
mysql -u root -p < sql/01_schema.sql
mysql -u root -p bank_db < sql/02_procedures.sql
mysql -u root -p bank_db < sql/03_triggers_views.sql
mysql -u root -p bank_db < sql/04_sample_data.sql

# 6. Launch the Streamlit Portal
streamlit run app/main.py
```

Open your browser at `http://localhost:8501` and sign in with `admin` / `admin123`.

---

## 5. Folder Structure

```
Database Management System Course Project/
├── sql/
│   ├── 01_schema.sql          # Tables, constraints, and indexes
│   ├── 02_procedures.sql      # 17 Stored procedures with exception handlers
│   ├── 03_triggers_views.sql  # 5 Triggers and 6 Relational Views
│   ├── 04_sample_data.sql     # Seed data with mathematically verified ledger
│   └── 05_test_queries.sql    # 13 SQL queries for viva & concept demos
├── app/
│   ├── main.py                # Entry portal with login & quick links
│   ├── db.py                  # MySQL connection pool, procedures & query helpers
│   ├── auth.py                # Session authentication & role guards
│   ├── ui.py                  # Page headers, rupee formatter, custom styles
│   └── pages/
│       ├── 1_Dashboard.py     # High-level metrics, Plotly charts, recent ledger
│       ├── 2_Customers.py     # Customer list, onboarding (18+), KYC updates, 360 view
│       ├── 3_Accounts.py      # Account list, opening, freeze/close, balance enquiry
│       ├── 4_Transactions.py  # Deposit, withdraw, transfer, charges, interest, statements
│       ├── 5_Loans.py         # Loan application, live EMI preview, approvals, EMI payment
│       ├── 6_Cards.py         # Masked card directory, card issuance, block/unblock
│       ├── 7_Employees.py     # Staff hierarchy, hiring, branch transfers (Manager only)
│       └── 8_Reports.py       # Branch analytics, top 5, dormant accounts, audit log
├── docs/
│   ├── ER_diagram.md          # Complete Mermaid ER diagram and 3NF notes
│   └── screenshots/           # UI screenshots
├── .streamlit/
│   └── config.toml            # Primary color theme (#1f4e9c)
├── .env.example               # Database configuration template
├── .gitignore                 # Python and environment ignores
├── requirements.txt           # Project dependencies
└── README.md                  # System documentation
```

---

## 6. Database Normalization (3NF)

- **1NF**: Atomic scalar values in all columns; explicit primary keys on all tables.
- **2NF**: No partial dependencies; all non-key columns fully depend on table primary keys.
- **3NF**: Elimination of transitive dependencies. Product parameters (`min_balance`, `interest_rate`) reside in `account_type`. Branch location attributes (`city`, `ifsc`) reside in `branch`. Customer contact info is maintained strictly in `customer`.

---

## 7. Feature to Transaction Type Mapping

| Operation | Triggering Procedure | Transaction Type | Balance Effect |
| :--- | :--- | :--- | :--- |
| Initial Account Deposit | `sp_open_account` | `DEPOSIT` | `+amount` |
| Counter Cash Deposit | `sp_deposit` | `DEPOSIT` | `+amount` |
| Counter Cash Withdrawal | `sp_withdraw` | `WITHDRAW` | `-amount` |
| Inter-Account Transfer (Debit) | `sp_transfer` | `TRANSFER_OUT` | `-amount` |
| Inter-Account Transfer (Credit) | `sp_transfer` | `TRANSFER_IN` | `+amount` |
| Loan Disbursement | `sp_approve_loan` | `LOAN_DISBURSE` | `+principal` |
| Loan EMI Repayment | `sp_pay_emi` | `LOAN_EMI` | `-amount` |
| Monthly Interest Run | `sp_credit_interest` | `INTEREST` | `+interest` |
| Service / Penalty Charge | `sp_apply_charge` | `CHARGE` | `-amount` |

---

## 8. Assumptions & Design Decisions

1. **Currency**: All monetary values are processed in Indian Rupees (INR) and formatted with ₹ symbol and 2 decimal places.
2. **Masked Card Security**: To adhere to PCI-DSS standards, card numbers are stored securely and masked (`**** **** **** 1234`) on view tables.
3. **Ledger Consistency Rule**: Every account's current balance strictly equals its opening deposit plus the sum of all credit transactions minus debit transactions.
