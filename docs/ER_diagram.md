# Bank Management System - Entity Relationship (ER) Diagram

This document models the relational database schema of the **Bank Management System (BMS)** in **Third Normal Form (3NF)**.

```mermaid
erDiagram
    BRANCH ||--o{ EMPLOYEE : "employs"
    EMPLOYEE ||--o{ EMPLOYEE : "manages"
    BRANCH ||--o{ ACCOUNT : "maintains"
    ACCOUNT_TYPE ||--o{ ACCOUNT : "classifies"
    CUSTOMER ||--o{ ACCOUNT : "holds"
    ACCOUNT ||--o{ TRANSACTIONS : "records"
    EMPLOYEE ||--o{ TRANSACTIONS : "processes"
    CUSTOMER ||--o{ LOAN : "borrows"
    ACCOUNT ||--o{ LOAN : "linked_for_disbursement"
    EMPLOYEE ||--o{ LOAN : "approves"
    LOAN ||--o{ LOAN_PAYMENT : "receives"
    ACCOUNT ||--o{ CARD : "issued_for"

    BRANCH {
        int branch_id PK
        varchar name
        varchar city
        varchar ifsc UK
    }

    EMPLOYEE {
        int emp_id PK
        varchar name
        enum role "MANAGER,TELLER,LOAN_OFFICER,CLERK"
        decimal salary
        int branch_id FK
        int manager_id FK
        date hire_date
        varchar username UK
        char password_hash
        boolean is_active
    }

    CUSTOMER {
        int customer_id PK
        varchar name
        date dob
        varchar phone UK
        varchar email UK
        varchar address
        enum kyc_status "PENDING,VERIFIED,REJECTED"
        datetime created_at
    }

    ACCOUNT_TYPE {
        int type_id PK
        enum name "SAVINGS,CURRENT,FIXED_DEPOSIT" UK
        decimal min_balance
        decimal interest_rate
    }

    ACCOUNT {
        bigint account_no PK
        int customer_id FK
        int type_id FK
        int branch_id FK
        decimal balance
        enum status "ACTIVE,FROZEN,CLOSED"
        date opened_on
    }

    TRANSACTIONS {
        bigint txn_id PK
        bigint account_no FK
        enum txn_type "DEPOSIT,WITHDRAW,TRANSFER_OUT,TRANSFER_IN,LOAN_DISBURSE,LOAN_EMI,INTEREST,CHARGE"
        decimal amount
        decimal balance_after
        bigint related_account
        datetime txn_time
        varchar remarks
        int done_by_emp FK
    }

    LOAN {
        int loan_id PK
        int customer_id FK
        bigint account_no FK
        decimal principal
        decimal annual_rate
        int tenure_months
        decimal emi
        decimal outstanding
        enum status "PENDING,APPROVED,REJECTED,CLOSED"
        date applied_on
        int approved_by FK
        date approved_on
    }

    LOAN_PAYMENT {
        int payment_id PK
        int loan_id FK
        decimal amount
        datetime paid_on
    }

    CARD {
        int card_id PK
        bigint account_no FK
        enum card_type "DEBIT,CREDIT"
        char card_number UK
        date expiry
        enum status "ACTIVE,BLOCKED,EXPIRED"
    }

    AUDIT_LOG {
        bigint log_id PK
        varchar table_name
        varchar action
        varchar record_id
        varchar details
        datetime logged_at
    }
```

## Normalization Details (3NF)

1. **First Normal Form (1NF):**
   - All attributes are atomic (no repeating groups, multi-valued fields, or comma-separated lists).
   - Every table possesses an explicit primary key (`branch_id`, `emp_id`, `customer_id`, `type_id`, `account_no`, `txn_id`, `loan_id`, `payment_id`, `card_id`, `log_id`).

2. **Second Normal Form (2NF):**
   - The schema is in 1NF and contains no composite candidate keys whose non-prime attributes depend on a proper subset of the key. All non-key attributes are fully functionally dependent on the entire primary key.

3. **Third Normal Form (3NF):**
   - The schema is in 2NF and contains no transitive dependencies ($X \to Y \to Z$).
   - For example, account type configuration (`min_balance`, `interest_rate`) is isolated into `account_type` rather than repeated across individual `account` records.
   - Branch city and IFSC details live in `branch`, eliminating transitive dependencies from `account` or `employee`.
