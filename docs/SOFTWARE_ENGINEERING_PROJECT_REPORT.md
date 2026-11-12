# MINI PROJECT REPORT
Project Title : Bank Management System
Course: Software Engineering
Project Type: Course Project
Submitted by
Roll Number and Name
__________________________
__________________________
__________________________
__________________________
Class/Division: __________________________
Department: Computer Engineering (Software Engineering)
Institute: Vishwakarma Institute of Technology
Academic Year: 2026–2027

## TABLE OF CONTENTS
1. Introduction
2. Problem Statement
3. Objectives
4. Study of Software Crisis
5. Comparison of SDLC Models
6. Requirement Elicitation
7. SRS and User Stories
8. UML Modeling
9. Software Testing
10. Software Maintenance
11. Risk Management and Version Control
12. Verification and Validation
13. Integrated Project Development Plan
14. Conclusion
15. References

## ABSTRACT
Software engineering provides a systematic approach to developing, testing, deploying, and maintaining reliable software applications. Modern banking software systems must satisfy user requirements, maintain transactional integrity, manage operational risks, and adapt to changing financial regulations.

This mini project presents a comprehensive software engineering study based on a Bank Management System. It integrates nine laboratory assignments covering the causes and consequences of the software crisis, comparison of Software Development Life Cycle (SDLC) models, requirement elicitation, Software Requirement Specification (SRS), user stories, UML modeling, software testing, software maintenance, risk management, version control, verification, and validation.

The proposed Bank Management System enables bank staff to onboard customers, verify KYC details, open and manage bank accounts, process cash deposits, withdrawals, and inter-account fund transfers, originate and approve loans with automated EMI calculation, issue and manage debit/credit cards, and track audit logs. Bank managers can manage branch employees, run monthly savings interest batches, and generate compliance and financial reports.

The report demonstrates how software engineering principles can be applied throughout the software development life cycle. It also presents sample test cases, risk assessment tables, maintenance recommendations, and review procedures. The expected outcome is a structured project document that demonstrates the importance of planning, documentation, testing, quality assurance, and controlled software development.

Keywords: Software Engineering, SDLC, SRS, UML, Software Testing, Risk Management, Git, Verification and Validation.

## 1. INTRODUCTION
Software engineering is the systematic application of engineering principles, methods, and tools to software development and maintenance. It helps developers build software that is reliable, efficient, maintainable, secure, and capable of satisfying user requirements.

A Bank Management System is a software application that allows bank personnel to manage retail banking operations across multiple branches. It provides facilities for customer registration and KYC verification, account opening and management, deposit and withdrawal processing, inter-account fund transfers, loan origination and EMI collection, card issuance, and audit reporting.

Developing such a system requires more than programming. The development team must understand banking requirements, select an appropriate SDLC model, prepare design documents, identify concurrency and security risks, perform software testing, and plan future maintenance.

This mini project applies the concepts covered in nine Software Engineering laboratory assignments to a common project scenario centered on the Bank Management System.

### 1.1 Scope of the Project
The proposed Bank Management System includes the following modules:
- Staff authentication and Role-Based Access Control (Manager, Teller, Loan Officer, Clerk).
- Customer registration (18+ age validation) and KYC verification.
- Bank account opening and lifecycle management (Savings, Current, Fixed Deposit).
- Cash deposit and withdrawal processing with minimum balance checks.
- Atomic inter-account fund transfers with deadlock prevention.
- Loan application, reducing-balance EMI calculation, approval, and repayment.
- Debit and credit card issuance, masking, and block/unblock management.
- Manager administration of branches, employees, service charges, and monthly interest runs.
- Generation of branch summaries, dormant account reports, and automated audit logs.

The project focuses on software engineering analysis, documentation, design, testing, risk management, and maintenance alongside a MySQL 8.0 and Streamlit prototype.

## 2. PROBLEM STATEMENT
Traditional or poorly integrated banking record systems require manual ledger checks, disconnected spreadsheets, or application scripts that lack database-level transaction guarantees. This process consumes time, limits multi-branch coordination, and introduces risks of financial inconsistency.

A centralized Bank Management System addresses these problems by providing an integrated relational database and staff portal for customer onboarding, account operations, fund transfers, loan servicing, and compliance auditing.

However, developing a banking application introduces several software engineering challenges, including:
- Incomplete or changing banking and regulatory requirements.
- Transaction failures and partial balance updates during fund transfers.
- Concurrent access issues and database deadlocks during simultaneous transfers.
- Inaccurate interest, fee, or loan EMI calculations due to rounding errors.
- Enforcement of role-based permissions across different bank staff designations.
- Software defects and long-term maintenance difficulties.
- Risks associated with unauthorized access, unverified KYC records, and data loss.

Therefore, a systematic software engineering approach is required to develop and maintain the proposed application.

## 3. OBJECTIVES
The main objectives of this mini project are:
- To study the causes and consequences of the software crisis in a real-world banking software project.
- To compare different SDLC models and justify a suitable model for a Bank Management System.
- To perform requirement elicitation and classify functional and non-functional requirements.
- To prepare an SRS document and develop user stories with acceptance criteria.
- To model system behavior using UML use case, activity, sequence, and state machine diagrams.
- To design test cases using black-box and white-box testing techniques.
- To identify software maintenance types and propose a maintenance plan.
- To prepare a risk register, develop mitigation strategies, and manage project versions using Git.
- To conduct verification and validation activities and document identified defects.

## 4. STUDY OF THE SOFTWARE CRISIS

### 4.1 Aim
To study a real-world software project and analyze the causes and consequences of the software crisis.

### 4.2 Introduction
The software crisis refers to difficulties encountered in developing and maintaining software systems within planned budgets and schedules while meeting the required quality standards.

As software systems become larger and more complex, poorly defined requirements, inadequate testing, weak project management, and insufficient documentation can result in software failures.

### 4.3 Case Study: Core Banking and Multi-Branch Ledger Information System
A core banking information system manages customer registration, KYC verification, savings and current accounts, inter-account fund transfers, loan disbursements, EMI collections, and branch audit logs.

Consider a hypothetical regional bank implementing a new centralized account and transaction management system. During implementation, the project experiences delays, inconsistent account balances after interrupted transfers, deadlocks during peak banking hours, duplicate transaction records, and missing role checks between tellers and loan officers.

These problems illustrate how inadequate software engineering practices can lead to software crisis conditions.

Note: This is an illustrative case study demonstrating software engineering challenges in financial systems.

### 4.4 Causes of the Software Crisis
| Cause | Description | Example |
| :--- | :--- | :--- |
| Unclear requirements | Banking rules are not completely understood. | Minimum balance rules for Savings and Current accounts are not defined. |
| Increasing complexity | Many modules must exchange information atomically. | Account balances and transaction ledger records become inconsistent. |
| Poor estimation | Time and cost requirements are underestimated. | Stored procedure and concurrency testing time is insufficient. |
| Inadequate testing | Defects remain undetected before release. | Negative deposit amounts or underage customer profiles are accepted. |
| Poor communication | Stakeholders and developers have different expectations. | Bank managers request dormant account detection late in development. |
| Lack of documentation | Database constraints and design decisions are not recorded. | New developers struggle to maintain stored procedures and triggers. |
| Changing requirements | New features are introduced without proper change control. | Credit card limit management is added late without schema review. |
| Security weaknesses | Access controls and data protection are inadequate. | Unauthorized staff roles access loan approval or employee transfer screens. |

### 4.5 Consequences of the Software Crisis
- Cost overruns: Additional development and corrective work increase the project budget.
- Schedule delays: The project takes longer than planned.
- Poor software quality: Ledger defects reduce financial reliability and usability.
- User dissatisfaction: Bank staff and customers lose confidence in the system.
- Operational disruption: Inconsistent account balances affect daily branch operations.
- Security and privacy risks: Sensitive customer KYC and card information may be exposed.
- Increased maintenance costs: Poorly designed software becomes difficult to modify.
- Project failure: The system may not satisfy its intended banking objectives.

### 4.6 Recommended Solutions
- Conduct structured requirement elicitation with banking stakeholders.
- Prepare an SRS before implementation.
- Use an appropriate iterative SDLC model.
- Apply modular 3NF database design, ACID transactions, and coding standards.
- Perform regular code reviews and automated testing.
- Maintain source code and SQL scripts using version control.
- Conduct risk analysis throughout development.
- Implement Role-Based Access Control (RBAC), password hashing, backups, and audit triggers.
- Involve users in acceptance testing.

### 4.7 Outcome
The study demonstrates that the software crisis can be reduced through systematic requirement engineering, realistic planning, transactional database design, quality assurance, risk management, and continuous maintenance.

## 5. COMPARISON OF SDLC MODELS

### 5.1 Aim
To compare different SDLC models for a Bank Management System and justify the selection of the most appropriate development model.

### 5.2 Overview of SDLC Models
The Software Development Life Cycle defines the stages involved in developing software, from requirement analysis to deployment and maintenance.

The major SDLC models considered are Waterfall, V-Model, Incremental, Spiral, and Agile.

### 5.3 Comparison of SDLC Models
| SDLC Model | Advantages | Limitations | Suitability |
| :--- | :--- | :--- | :--- |
| Waterfall | Simple, structured, and documentation-oriented. | Changes are difficult to accommodate after a phase is completed. | Suitable when banking requirements are completely static. |
| V-Model | Testing activities are planned alongside development activities. | Less flexible when UI or reporting requirements change frequently. | Suitable for projects with strict verification requirements. |
| Incremental | Delivers software in smaller functional releases. | Requires careful planning of database and module integration. | Suitable for phased delivery of banking modules. |
| Spiral | Emphasizes risk identification and risk reduction. | Can be expensive and complex to manage for small teams. | Suitable for large, high-budget enterprise banking projects. |
| Agile | Supports frequent feedback, iterative development, and changing requirements. | Requires continuous stakeholder participation and disciplined team coordination. | Suitable for modular banking applications and interactive dashboards. |

### 5.4 Selected Model: Agile Development
The Agile model is selected for the Bank Management System because banking modules (customers, accounts, transactions, loans, cards, and reports), user interface workflows, and analytical requirements can be developed and verified incrementally.

The project is divided into short iterations, with each iteration delivering a testable set of banking features.

#### Proposed Development Iterations
| Iteration | Main Activities | Expected Deliverable |
| :--- | :--- | :--- |
| Iteration 1 | Requirement analysis, 3NF database schema, staff roles, and login. | Database schema and authentication module. |
| Iteration 2 | Customer onboarding (18+ check), KYC status workflow, and account opening. | Customer and account management modules. |
| Iteration 3 | Cash deposits, withdrawals, deadlock-safe transfers, and audit triggers. | Transactional ledger and statement module. |
| Iteration 4 | Loan application, EMI calculation, loan approval/disbursement, and cards. | Loan servicing and card management modules. |
| Iteration 5 | Employee administration, analytical views, security testing, and final validation. | Complete release candidate and acceptance test suite. |

### 5.5 Justification for Selecting Agile
Agile is appropriate because:
- Requirements can be refined through stakeholder and faculty feedback.
- Features can be prioritized according to core banking dependencies.
- Database procedures and UI pages can be tested during each iteration.
- Ledger and validation defects can be identified and corrected early.
- Analytical views and compliance reports can be evaluated incrementally.
- The system can be delivered in functional stages rather than waiting for the final phase.

However, Agile does not eliminate the need for documentation. The project still maintains an SRS, ER and UML design diagrams, test cases, a risk register, and version history.

### 5.6 Outcome
Agile development is recommended for the Bank Management System because it supports incremental delivery, continuous testing, stakeholder feedback, and controlled adaptation to evolving requirements.

## 6. REQUIREMENT ELICITATION

### 6.1 Aim
To conduct requirement elicitation for the Bank Management System and prepare functional and non-functional requirements.

### 6.2 Case Study
A multi-branch bank wants to computerize customer onboarding, KYC verification, savings/current/fixed-deposit account management, deposits, withdrawals, inter-account transfers, loan origination, card issuance, employee management, and audit reporting.

The system should reduce manual ledger errors, enforce transactional consistency in MySQL, and enable authorized bank staff to access role-appropriate modules efficiently.

### 6.3 Stakeholders
| Stakeholder | Requirements and Responsibilities |
| :--- | :--- |
| Bank Manager | Oversee branch analytics, manage employees, approve loans, run monthly interest, and review audit logs. |
| Bank Teller | Process cash deposits, withdrawals, inter-account transfers, account status updates, and EMI collections. |
| Loan Officer | Review customer KYC status, submit loan applications, preview EMIs, and approve or reject loans. |
| Bank Clerk | Register new customers (18+ years), update KYC verification status, open accounts, and issue/block cards. |
| Customer | Hold bank accounts, perform deposits/transfers via branch staff, apply for loans, and receive statements. |
| Internal Auditor | Inspect high-value transaction alerts, dormant accounts, branch summaries, and immutable audit logs. |

### 6.4 Requirement Elicitation Techniques
The following techniques can be used to collect requirements:
- Interviews: Discuss operational workflows and validation rules with branch managers, tellers, and loan officers.
- Questionnaires: Collect feedback from bank staff regarding common transaction bottlenecks and reporting needs.
- Observation: Study existing counter deposit, transfer, account opening, and loan approval workflows.
- Document analysis: Examine account opening forms, KYC norms (PAN/Aadhaar), minimum balance rules, and EMI formulas.
- Prototyping: Present sample Streamlit dashboard and transaction screens to stakeholders and collect feedback.

### 6.5 Functional Requirements
Functional requirements describe what the system must do.

| ID | Functional Requirement |
| :--- | :--- |
| FR-01 | The system shall allow authorized staff to register new customers aged 18 years or older with unique PAN and Aadhaar numbers. |
| FR-02 | The system shall allow staff to update customer KYC status (PENDING, VERIFIED, REJECTED). |
| FR-03 | The system shall allow opening of SAVINGS, CURRENT, and FD accounts with minimum balance validation. |
| FR-04 | The system shall process atomic cash deposits and withdrawals on ACTIVE accounts without breaching minimum balances. |
| FR-05 | The system shall execute atomic inter-account fund transfers using ordered row locks to prevent deadlocks. |
| FR-06 | The system shall allow Loan Officers to submit loan applications for KYC-VERIFIED customers and auto-calculate monthly EMI. |
| FR-07 | The system shall allow Loan Officers and Managers to approve or reject pending loans and auto-disburse principal upon approval. |
| FR-08 | The system shall process loan EMI repayments and update the remaining principal balance. |
| FR-09 | The system shall allow issuing and blocking/unblocking of masked Debit and Credit cards linked to active accounts. |
| FR-10 | The system shall automatically log sensitive operations and high-value transactions (> Rs. 50,000) into an audit log. |

### 6.6 Non-Functional Requirements
Non-functional requirements specify quality attributes and operating constraints.

| ID | Requirement | Proposed Acceptance Criterion |
| :--- | :--- | :--- |
| NFR-01 | Performance | At least 95% of routine banking requests should complete within 2 seconds under the agreed test workload. |
| NFR-02 | Security | Access to portal pages shall require SHA-256 password authentication and role-based authorization (RBAC). |
| NFR-03 | Reliability | All balance-modifying operations shall execute inside ACID transactions and roll back completely on error. |
| NFR-04 | Concurrency | Simultaneous transfers between the same pair of accounts shall acquire locks in ascending account ID order to prevent deadlocks. |
| NFR-05 | Usability | Staff users shall be able to complete tasks through clearly labeled Streamlit forms, Rupee formatting, and validation messages. |
| NFR-06 | Maintainability | The application shall separate SQL schema/procedures, database pooling, authentication, and UI modules cleanly. |
| NFR-07 | Data integrity | Monetary values shall use exact DECIMAL(15,2) types, and account balances shall reconcile with ledger transactions. |
| NFR-08 | Privacy | Customer card numbers shall be masked (XXXX-XXXX-XXXX-1234) in analytical views and UI directories. |

### 6.7 Outcome
Requirement elicitation identifies the expectations of bank managers, tellers, loan officers, clerks, customers, and auditors. The resulting functional and non-functional requirements provide a foundation for system design and testing.

## 7. SRS AND USER STORIES

### 7.1 Aim
To prepare an SRS document and write user stories with acceptance criteria for the Bank Management System.

### 7.2 Purpose of the SRS
The Software Requirement Specification defines the system's scope, features, interfaces, constraints, and quality requirements. It provides a common reference for developers, testers, stakeholders, and project managers.

### 7.3 SRS Document

#### 7.3.1 Product Overview
The Bank Management System is a database-first web application through which authenticated bank staff can onboard customers, manage accounts, process deposits, withdrawals, and transfers, originate and service loans, manage cards, and view real-time branch and audit reports.

#### 7.3.2 Product Functions
- Staff login and Role-Based Access Control (RBAC).
- Customer onboarding (18+ validation) and KYC status management.
- Account opening, freezing/unfreezing, and zero-balance account closure.
- Cash deposits, cash withdrawals, and inter-account fund transfers.
- Batch monthly savings interest crediting and service charge deduction.
- Loan application, reducing-balance EMI calculation, approval/disbursement, and EMI repayment.
- Debit and credit card issuance and status toggling.
- Branch employee hiring and inter-branch transfers.
- Analytical dashboards, dormant account detection, CSV statement export, and trigger-based audit logging.

#### 7.3.3 User Classes
- Manager: Full administrative access to all modules, employee management, interest batch runs, loan approvals, and audit reports.
- Teller: Access to accounts, cash deposits, withdrawals, transfers, account statements, and EMI payments.
- Loan Officer: Access to customer KYC verification, loan origination, EMI preview, loan approvals/rejections, and EMI payments.
- Clerk: Access to customer registration, KYC updates, account opening, and debit/credit card management.

#### 7.3.4 Operating Environment
- Client: Modern web browser on desktop or laptop.
- Application: Python 3.10+ multi-page Streamlit web application.
- Database: MySQL 8.0+ relational database using the InnoDB storage engine.
- Database Connector: mysql-connector-python with connection pooling and python-dotenv configuration.
- Network: Localhost or authorized branch network connection over TCP/IP.

#### 7.3.5 Functional Requirements
| ID | Requirement |
| :--- | :--- |
| FR-01 | Staff users shall be able to log in securely using role-assigned credentials. |
| FR-02 | Authorized staff shall be able to register adult customers (18+ years) and update KYC status. |
| FR-03 | Authorized staff shall be able to open Savings, Current, and FD accounts meeting minimum balance rules. |
| FR-04 | Tellers shall be able to record cash deposits and withdrawals on ACTIVE accounts. |
| FR-05 | The system shall validate minimum balance retention before confirming any withdrawal or transfer. |
| FR-06 | The system shall execute inter-account transfers atomically and record paired ledger entries. |
| FR-07 | Managers shall be able to credit monthly interest to active savings accounts and apply service charges. |
| FR-08 | Tellers and Managers shall be able to freeze, unfreeze, and close zero-balance accounts. |
| FR-09 | Loan Officers shall be able to submit loan applications for KYC-verified customers with automatic EMI calculation. |
| FR-10 | Loan Officers and Managers shall be able to approve or reject pending loans, triggering principal disbursement on approval. |
| FR-11 | Staff shall be able to record loan EMI repayments, issue/block bank cards, and manage branch employees. |
| FR-12 | The system shall maintain an automated audit log of account openings, status changes, loan updates, and high-value transactions. |

#### 7.3.6 Non-Functional Requirements
- Performance: Under the agreed test workload, at least 95% of database and portal requests should complete within 2 seconds.
- Security: Passwords must be stored as SHA-256 hashes; role-based access controls must be enforced on every page.
- Usability: The interface must provide understandable navigation, Rupee formatting, validation, and error messages.
- Reliability: All stored procedures must use explicit transactions with automatic rollback on SQL exceptions.
- Scalability: The schema should support additional branches, accounts, and transactions through composite indexing.
- Maintainability: SQL scripts, database helpers, authentication guards, and UI pages must be modular and documented.
- Compatibility: The web interface should work across modern desktop browsers supporting Streamlit.
- Data integrity: Account, transaction, customer, loan, and audit records must remain mathematically consistent in 3NF.

#### 7.3.7 External Interface Requirements
- User interface: Login, Dashboard, Customers, Accounts, Transactions, Loans, Cards, Employees, and Reports screens.
- Software interfaces: MySQL 8.0 database engine accessed via pooled connections in `app/db.py`, Pandas DataFrames, and Plotly charts.
- Communication interfaces: Local or branch network TCP connection to MySQL Server (port 3306) and HTTP/WebSocket connection to Streamlit (port 8501).

#### 7.3.8 Constraints and Assumptions
- MySQL Server 8.0+ must be running with the InnoDB engine enabled to support transactions and foreign keys.
- Customers must be at least 18 years old to be registered in the system.
- Only customers with `VERIFIED` KYC status are eligible to apply for loans.
- An account can only be transitioned to `CLOSED` status when its balance is exactly Rs. 0.00.
- Full 16-digit card numbers are masked in reporting views to protect sensitive financial data.

### 7.4 User Stories with Acceptance Criteria

#### User Story 1: Customer Registration
- User story: As a bank clerk, I want to register a new customer with personal and KYC details so that they can open bank accounts.
- Acceptance criteria:
  - Given valid required details and age >= 18 years, when the clerk submits the registration form, the system creates a customer record.
  - Given an applicant under 18 years of age, when registration is submitted, the database trigger rejects the insertion with an age validation error.
  - Given a duplicate email, PAN, or Aadhaar number, the system rejects the submission and identifies the conflict.
  - Newly registered customers are assigned an initial KYC status of `PENDING`.

#### User Story 2: Staff Login and Role Access
- User story: As a bank staff member, I want to log in securely so that I can access modules permitted for my role.
- Acceptance criteria:
  - Given valid username and password credentials, the system authenticates the user and loads their assigned role.
  - Given an incorrect password or inactive user, the system denies access and displays an authentication error.
  - Unauthenticated users cannot access protected banking pages.
  - Users attempting to access restricted pages outside their role (such as a Teller accessing Employee Management) are blocked.

#### User Story 3: Open and Manage Bank Accounts
- User story: As a teller or clerk, I want to open and manage customer accounts so that customers can safely hold funds.
- Acceptance criteria:
  - Given an initial deposit meeting the product minimum balance (Rs. 1,000 for Savings, Rs. 5,000 for Current, Rs. 10,000 for FD), the system opens an `ACTIVE` account.
  - Given an initial deposit below the required minimum balance, the system rejects account creation with a descriptive error.
  - Authorized staff can freeze or unfreeze an account and view real-time account balances.
  - Account closure is permitted only when the current balance is exactly Rs. 0.00.

#### User Story 4: Perform Deposit, Withdrawal, and Transfer
- User story: As a bank teller, I want to process deposits, withdrawals, and inter-account transfers so that customer transactions are settled accurately.
- Acceptance criteria:
  - A teller can deposit a positive amount into any `ACTIVE` account and immediately view the updated balance.
  - A withdrawal or transfer that would reduce the source account balance below its `min_balance` is rejected and rolled back.
  - An inter-account transfer locks both accounts in ascending primary-key order, updates both balances atomically, and records `TRANSFER_OUT` and `TRANSFER_IN` entries.
  - Transactions on `FROZEN` or `CLOSED` accounts are rejected.
  - Any single transaction exceeding Rs. 50,000 is automatically recorded in `audit_log`.

#### User Story 5: Apply and Approve Loan
- User story: As a loan officer, I want to submit and process loan applications so that eligible customers receive credit with accurate EMI schedules.
- Acceptance criteria:
  - The system validates that the customer's KYC status is `VERIFIED` before accepting a loan application.
  - The system calculates the monthly EMI using the reducing-balance formula based on principal, annual interest rate, and tenure in months.
  - When a pending loan is approved by a Loan Officer or Manager, the system transitions the loan to `ACTIVE` and automatically credits the principal amount into the customer's disbursement account.
  - EMI repayments deduct the installment from the customer's account, split principal and interest components, and close the loan when remaining principal reaches zero.

#### User Story 6: Manage Cards and Employees
- User story: As an authorized staff member or manager, I want to manage bank cards and branch employees so that card services and branch staffing remain updated.
- Acceptance criteria:
  - Clerks and Managers can issue Debit or Credit cards linked to active accounts and toggle card status between `ACTIVE` and `BLOCKED`.
  - Card numbers are displayed in masked format (`XXXX-XXXX-XXXX-1234`) in the card directory.
  - Authorized Managers can add new employees and transfer employees between branches.
  - Non-manager roles cannot access employee hiring or branch transfer functions.

### 7.5 Outcome
The SRS establishes a clear specification for the Bank Management System. User stories and acceptance criteria translate banking rules into testable conditions for development and validation.

## 8. UML MODELING

### 8.1 Aim
To model the behavior of the Bank Management System using use case, activity, sequence, and state machine diagrams.

### 8.2 System Description
The Bank Management System manages customers, KYC verification, bank accounts, deposits, withdrawals, inter-account transfers, loans, EMI payments, bank cards, employees, and audit logs.

The system supports four staff roles (Clerk, Teller, Loan Officer, and Manager) interacting with the Streamlit interface and MySQL InnoDB stored procedures and triggers.

### 8.3 Use Case Diagram

#### Actors
- Bank Clerk
- Bank Teller
- Loan Officer
- Bank Manager

#### Use Cases
- Log in with RBAC.
- Register customer (18+ age check) and update KYC status.
- Open bank account.
- Deposit and withdraw cash.
- Transfer funds between accounts.
- Freeze, unfreeze, and close account.
- Apply for loan and calculate EMI.
- Approve or reject loan with auto-disbursement.
- Pay loan EMI.
- Issue and block/unblock bank card.
- Manage employees and run monthly savings interest.
- View branch analytics and audit logs.

#### Use Case Diagram Representation
```text
+-------------------------------------------------------------------------+
|                      BANK MANAGEMENT SYSTEM (BMS)                       |
|                                                                         |
|  [Clerk] --------> (Log In)                                             |
|            ------> (Register Customer & Update KYC)                     |
|            ------> (Open Bank Account)                                  |
|            ------> (Issue / Block Bank Card)                            |
|                                                                         |
|  [Teller] -------> (Log In)                                             |
|            ------> (Deposit / Withdraw Cash)                            |
|            ------> (Inter-Account Fund Transfer)                        |
|            ------> (Freeze / Close Zero-Balance Account)                |
|            ------> (Collect Loan EMI Payment)                           |
|                                                                         |
|  [Loan Officer] -> (Log In)                                             |
|                 -> (Verify Customer KYC)                                |
|                 -> (Apply for Loan & Calculate Reducing-Balance EMI)    |
|                 -> (Approve / Reject Loan & Auto-Disburse Principal)    |
|                                                                         |
|  [Manager] ------> (All Operational Use Cases Above)                    |
|            ------> (Run Monthly Savings Interest & Apply Charges)       |
|            ------> (Hire & Transfer Branch Employees)                   |
|            ------> (View Branch Analytics, Dormant Accounts & Audit)    |
+-------------------------------------------------------------------------+
```

### 8.4 Activity Diagram: Inter-Account Fund Transfer Process
```text
                    ([Start Fund Transfer Request])
                                  |
                                  v
          [Validate Input: Amount > 0 AND Source != Destination]
                     /                         \
                (Invalid)                    (Valid)
                   /                             \
                  v                               v
     [Display Validation Error]        [START TRANSACTION (InnoDB)]
                  |                               |
                  v                               v
           ([Stop Process])          [Lock Accounts in Ascending ID Order:
                                      LEAST(from, to) then GREATEST(from, to)]
                                                  |
                                                  v
                                    <Both Accounts Exist & ACTIVE?>
                                       /                       \
                                    (No)                      (Yes)
                                     /                           \
                                    v                             v
                        [ROLLBACK & Signal Error]   <(Source Bal - Amount) >= Min Bal?>
                                    |                      /                 \
                                    v                   (No)                (Yes)
                             ([Stop Process])            /                     \
                                                        v                       v
                                            [ROLLBACK & Signal Error]  [Debit Source & Credit Dest;
                                                        |               Insert TRANSFER_OUT & IN]
                                                        v                       |
                                                 ([Stop Process])               v
                                                                      <Amount > Rs. 50,000?>
                                                                         /              \
                                                                      (Yes)             (No)
                                                                       /                  \
                                                                      v                    v
                                                           [Trigger Logs High-Value   [COMMIT Transaction]
                                                            Entry in audit_log]            |
                                                                      \                   /
                                                                       v                 v
                                                                    ([End: Transfer Complete])
```

Explanation: The activity begins when a teller initiates an inter-account transfer. The system validates that the transfer amount is positive and the accounts are distinct, locks both rows in ascending primary-key order to prevent deadlocks, checks that both accounts are `ACTIVE` and that the source account retains its minimum balance, updates the balances, records paired transaction ledger rows, triggers high-value audit logging if applicable, and commits the transaction.

### 8.5 Sequence Diagram: Loan Application and Approval Process
```text
Loan Officer        Streamlit UI (5_Loans.py)        DB Pool (app/db.py)        MySQL Stored Procs & Triggers
     |                         |                              |                               |
     |--- 1. Enter Loan Form ->|                              |                               |
     |<-- 2. Show EMI Preview -|                              |                               |
     |--- 3. Submit Loan ----->|                              |                               |
     |                         |--- 4. call sp_apply_loan --->|                               |
     |                         |                              |--- 5. Check KYC & Account --->|
     |                         |                              |    [If KYC = VERIFIED]:       |
     |                         |                              |    Compute EMI & Insert Loan  |
     |                         |                              |<-- 6. Return loan_id & EMI ---|
     |<-- 7. Display Success --|<-----------------------------|                               |
     |                                                                                        |
     |--- 8. Click Approve --->|                              |                               |
     |                         |--- 9. call sp_approve_loan ->|                               |
     |                         |                              |--- 10. Lock Loan & Account -->|
     |                         |                              |--- 11. Set Loan = ACTIVE ---->|
     |                         |                              |--- 12. Fire Audit Trigger --->|
     |                         |                              |--- 13. Credit Principal & --->|
     |                         |                              |        Log LOAN_DISBURSEMENT  |
     |                         |                              |<-- 14. COMMIT Transaction ----|
     |<-- 15. Confirm Credit --|<-----------------------------|                               |
```

Explanation: The sequence shows how the Loan Officer interface, database connection pool, MySQL stored procedures (`sp_apply_loan`, `sp_approve_loan`), and database triggers interact during loan origination and approval. Loan status updates, principal disbursement into the customer account, transaction logging, and audit trail insertion occur atomically within a single database transaction.

### 8.6 State Machine Diagram: Bank Account State
```text
                           sp_open_account (Deposit >= Min Balance)
                    [*] ---------------------------------------------> [ ACTIVE ]
                                                                        |  ^  |
                     +--------------------------------------------------+  |  |
                     | sp_update_account_status('FROZEN')                  |  | Inactivity >= 180 Days
                     v                                                     |  v
                [ FROZEN ] ------------------------------------------------+  [ DORMANT ]
                     |     sp_update_account_status('ACTIVE')                    |
                     |                                                           | Re-KYC & Reactivation
                     +----------------------------+------------------------------+
                                                  |
                                                  | Withdraw Balance to Rs. 0.00
                                                  | & Call sp_close_account
                                                  v
                                             [ CLOSED ] -----> [*]
```

Explanation: A bank account starts in the `ACTIVE` state upon opening with the required minimum deposit. It can transition to `FROZEN` due to administrative/security holds, be flagged as `DORMANT` after 180 days of inactivity, return to `ACTIVE` upon unfreezing or reactivation, and transition permanently to `CLOSED` once its balance is reduced to Rs. 0.00.

### 8.7 UML Modeling Tools
The diagrams can be created or refined using:
- StarUML.
- Visual Paradigm.
- diagrams.net (draw.io).
- PlantUML / Mermaid.

### 8.8 Outcome
The UML diagrams represent the functional behavior, transactional workflow, object interactions, and state transitions of the Bank Management System. They provide a foundation for implementation and testing.

## 9. SOFTWARE TESTING

### 9.1 Aim
To develop test cases for the Login and Transactional Banking modules using black-box techniques, including Boundary Value Analysis and Equivalence Partitioning, and white-box Basis Path Testing.

### 9.2 Module Description
The Login module (`app/auth.py`) accepts a staff username and password, verifies the SHA-256 credential hash against the `users` table, and grants role-based access only to active staff accounts. The Withdrawal/Onboarding modules validate username/password lengths, customer minimum age (18 years), and account minimum balance constraints.

For length validation in the authentication module, consider:
- Username length: 5–20 characters.
- Password length: 6–16 characters.
- The staff account exists and `is_active = 1` for positive authentication tests.

### 9.3 Black-Box Testing
Black-box testing checks system behavior using inputs and expected outputs without examining internal program logic.

#### 9.3.1 Equivalence Partitioning
Equivalence Partitioning divides input values into classes expected to behave similarly.

| Test ID | Input Class | Example Input | Expected Result |
| :--- | :--- | :--- | :--- |
| EP-01 | Valid staff username and password | `admin` / `admin123` | Login successful (Role: MANAGER) |
| EP-02 | Invalid username | `unknown_staff` / `pass123` | Access denied |
| EP-03 | Invalid password | `teller1` / `wrongpass` | Access denied |
| EP-04 | Adult customer registration (age >= 18) | DOB `1998-05-15` | Customer registered successfully |
| EP-05 | Minor customer registration (age < 18) | DOB `2014-08-20` | Trigger validation error (18+ required) |
| EP-06 | Empty username | Blank username | Required-field error |
| EP-07 | Empty password | Blank password | Required-field error |
| EP-08 | Withdrawal breaching minimum balance | Withdraw Rs. 4,500 from Rs. 5,000 Savings (Min Rs. 1,000) | Transaction rejected and rolled back |

#### 9.3.2 Boundary Value Analysis
Boundary Value Analysis tests values at and around the limits of accepted input ranges.

Username boundaries: Minimum = 5 characters; maximum = 20 characters.

| Test ID | Input Length | Expected Result |
| :--- | :--- | :--- |
| BVA-01 | 4 | Reject |
| BVA-02 | 5 | Accept length validation |
| BVA-03 | 6 | Accept length validation |
| BVA-04 | 19 | Accept length validation |
| BVA-05 | 20 | Accept length validation |
| BVA-06 | 21 | Reject |

Password boundaries: Minimum = 6 characters; maximum = 16 characters.

| Test ID | Input Length | Expected Result |
| :--- | :--- | :--- |
| BVA-07 | 5 | Reject |
| BVA-08 | 6 | Accept length validation |
| BVA-09 | 7 | Accept length validation |
| BVA-10 | 15 | Accept length validation |
| BVA-11 | 16 | Accept length validation |
| BVA-12 | 17 | Reject |

Passing a length-validation test does not guarantee successful login. The submitted credentials must also match the SHA-256 hash stored in `users`.

### 9.4 White-Box Testing: Basis Path Testing
White-box testing examines the internal control flow of a program. Basis Path Testing identifies independent execution paths using a control-flow graph.

Consider the following simplified pseudocode for the Login and Account Verification flow:
```text
START
  Read username and password
  IF username is empty
      Display username error
      STOP
  ENDIF
  IF password is empty
      Display password error
      STOP
  ENDIF
  IF SHA-256 credentials match active user in users table
      Load user role and display login success
  ELSE
      Display login failure
  ENDIF
STOP
```

#### 9.4.1 Control-Flow Graph
The control flow contains three decision points:
- Is the username empty?
- Is the password empty?
- Are the credentials valid for an active staff user?

Cyclomatic complexity is calculated as:
V(G) = D + 1
where D is the number of binary decision points.

For this example:
V(G) = 3 + 1 = 4

Therefore, four independent basis paths are required to cover the decision structure.

#### 9.4.2 Independent Paths
| Path | Conditions | Expected Result |
| :--- | :--- | :--- |
| P1 | Username is empty | Username error |
| P2 | Username present, password empty | Password error |
| P3 | Both fields present, credentials valid | Login success and role loaded |
| P4 | Both fields present, credentials invalid | Login failure |

### 9.5 Test Execution Record
The following table records the execution status of the test cases verified against the Bank Management System (`run_acceptance_tests.py`).

| Test ID | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- |
| EP-01 | Login successful (`admin` / `admin123`) | Authenticated as MANAGER | Executed - PASS |
| EP-02 | Access denied for unknown username | Rejected (`None` returned) | Executed - PASS |
| EP-05 | Reject customer age below 18 | Blocked by `trg_before_customer_insert_age_check` | Executed - PASS |
| EP-08 | Reject withdrawal below Rs. 1,000 min balance | Blocked by `sp_withdraw` (`SQLSTATE '45000'`) | Executed - PASS |
| BVA-01 | Reject username length 4 | Validation error | Executed - PASS |
| BVA-02 | Accept username length 5 (`admin`, `loan1`) | Accepted and authenticated | Executed - PASS |
| P1 | Username error when blank | Warning displayed in `app/main.py` | Executed - PASS |
| P2 | Password error when blank | Warning displayed in `app/main.py` | Executed - PASS |
| P3 | Login success with valid credentials | Session populated and redirected | Executed - PASS |
| P4 | Login failure with invalid password | Error banner `"Invalid username or password"` | Executed - PASS |

### 9.6 Additional Security Tests
- Verify that protected Streamlit pages cannot be accessed without authentication (`require_auth()`).
- Verify that role-restricted pages (such as `7_Employees.py`) block non-Manager roles.
- Check session state cleanup on logout.
- Verify that full 16-digit card numbers are masked (`XXXX-XXXX-XXXX-1234`) in views.
- Check that all SQL calls use parameterized queries or stored procedures to prevent SQL injection.
- Verify that passwords are stored using SHA-256 cryptographic hashes in the `users` table.

### 9.7 Outcome
The test plan demonstrates how equivalence partitioning, boundary value analysis, and basis path testing are used to evaluate the Login and Banking modules, confirmed by automated execution in `run_acceptance_tests.py`.

## 10. SOFTWARE MAINTENANCE

### 10.1 Aim
To analyze software maintenance activities, classify maintenance types, and recommend an appropriate maintenance plan for the Bank Management System.

### 10.2 Case Study: Existing Bank Management Application
Consider an operational Bank Management System that requires updates because of reported defects, revised central bank interest rates, new Python/MySQL versions, branch manager reporting requests, and security improvements.

Software maintenance begins after deployment and continues throughout the banking system's operational life.

### 10.3 Types of Software Maintenance
| Maintenance Type | Description | Example |
| :--- | :--- | :--- |
| Corrective | Fixes defects discovered after release. | Resolving unbuffered cursor errors or formatting raw MySQL exception strings. |
| Adaptive | Modifies software to accommodate environmental or regulatory changes. | Updating savings/FD interest rates or adapting to a newer Streamlit/MySQL version. |
| Perfective | Improves performance, functionality, or usability. | Adding branch deposit vs. loan Plotly charts and CSV statement exports. |
| Preventive | Reduces the likelihood of future failures. | Adding composite database indexes and deterministic lock ordering in `sp_transfer`. |

### 10.4 Maintenance History Analysis
| Scenario | Maintenance Type | Recommended Action |
| :--- | :--- | :--- |
| Sequential queries on pooled connections raise `Unread result found` | Corrective | Enable `buffered=True` on MySQL cursors in `app/db.py` and run regression tests. |
| Regulatory change in default Savings or FD interest rates | Adaptive | Update rate defaults in `sp_open_account` and verify new account creation. |
| Account statement search slows down as ledger rows grow | Perfective | Optimize queries using composite index `idx_txn_account_date`. |
| Outdated Python package contains a known vulnerability | Preventive | Update `requirements.txt` inside `.venv` and run acceptance tests. |
| Bank managers request dormant account identification | Perfective | Add `vw_dormant_accounts` view and Dormant Accounts tab in `8_Reports.py`. |
| Simultaneous bidirectional transfers risk database deadlock | Preventive | Enforce ascending primary-key lock ordering (`LEAST`/`GREATEST`) in `sp_transfer`. |

### 10.5 Proposed Maintenance Plan

#### Corrective Maintenance
- Record defects in an issue tracker.
- Reproduce the problem using `run_acceptance_tests.py`.
- Identify the root cause in the stored procedure or UI script.
- Apply a controlled fix and verify ledger reconciliation.
- Run regression tests before release.

#### Adaptive Maintenance
- Monitor changes to banking regulations, Python libraries, and MySQL Server releases.
- Review database connector and Streamlit compatibility notes.
- Test environment updates in a local staging database (`bank_db`).
- Deploy approved updates with a database backup and rollback plan.

#### Perfective Maintenance
- Collect feedback from branch managers, tellers, loan officers, and clerks.
- Analyze query execution plans and dashboard usability.
- Prioritize enhancements according to banking value.
- Update SRS requirements and acceptance criteria.

#### Preventive Maintenance
- Review SQL stored procedure and Python code quality.
- Update dependencies regularly in `requirements.txt`.
- Verify composite indexes and remove redundant queries.
- Maintain daily `mysqldump` backups and test recovery procedures.
- Perform periodic RBAC security and `audit_log` reviews.

### 10.6 Maintenance Schedule
| Frequency | Activity |
| :--- | :--- |
| Continuous | Monitor `audit_log` triggers, high-value transactions (> Rs. 50,000), and runtime errors. |
| Weekly | Review open support issues, failed login attempts, and pending loan queues. |
| Monthly | Run monthly savings interest batch (`sp_credit_interest`), review dormant accounts, and check backups. |
| Quarterly | Conduct index optimization, ledger reconciliation audits, and dependency reviews. |
| Before each release | Execute `run_acceptance_tests.py`, approve changes, and verify database backup restoration. |

### 10.7 Outcome
The maintenance study shows that corrective, adaptive, perfective, and preventive maintenance serve distinct purposes in banking software. A documented maintenance process improves ledger reliability, security, performance, and long-term maintainability.

## 11. RISK MANAGEMENT AND VERSION CONTROL

### 11.1 Aim
To prepare a risk register, assess software project risks, propose mitigation strategies, and maintain project versions using Git.

### 11.2 Risk Management Overview
Software project risks are uncertain events that may negatively affect project scope, schedule, cost, quality, security, or banking operations.

Risk management involves identifying risks, estimating their probability and impact, prioritizing them, planning responses, and monitoring them throughout development.

### 11.3 Risk Assessment Method
Probability and impact are scored on a scale from 1 to 5.

Risk Score = Probability × Impact

| Score | Risk Level |
| :--- | :--- |
| 1–4 | Low |
| 5–9 | Medium |
| 10–16 | High |
| 17–25 | Critical |

### 11.4 Risk Register
| Risk ID | Risk Description | Probability | Impact | Score | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R-01 | Concurrent bidirectional fund transfers cause a database deadlock. | 4 | 5 | 20 | Lock accounts in ascending primary-key order (`LEAST` then `GREATEST`) using `SELECT ... FOR UPDATE`. |
| R-02 | Mid-transaction failure leaves account balances inconsistent. | 3 | 5 | 15 | Wrap all stored procedures in InnoDB `START TRANSACTION` blocks with `EXIT HANDLER FOR SQLEXCEPTION ROLLBACK`. |
| R-03 | Unauthorized staff role accesses restricted banking operations. | 3 | 5 | 15 | Enforce `require_auth()` RBAC guards on every Streamlit page and procedure check. |
| R-04 | Floating-point rounding errors corrupt Rupee balances or EMIs. | 3 | 4 | 12 | Use exact `DECIMAL(15,2)` and `DECIMAL(5,2)` fixed-point types across all tables and procedures. |
| R-05 | Project schedule is delayed due to integration issues. | 4 | 4 | 16 | Divide development into 5 Agile iterations and test database procedures early. |
| R-06 | Database connection pool exhausts during rapid UI interactions. | 3 | 4 | 12 | Use a cached `MySQLConnectionPool` with `buffered=True` cursors and `try...finally` cleanup. |
| R-07 | Sensitive customer card numbers or passwords are exposed. | 2 | 5 | 10 | Store SHA-256 password hashes and mask card numbers (`XXXX-XXXX-XXXX-1234`) in views. |
| R-08 | Database data is lost because of a system failure. | 2 | 5 | 10 | Maintain regular SQL schema/seed scripts (`setup_db.py`) and scheduled database backups. |

### 11.5 Risk Prioritization
The highest-scoring risk is concurrent transfer deadlock (`R-01`, score 20), followed by project schedule delay (`R-05`, score 16), mid-transaction failure (`R-02`, score 15), and unauthorized access (`R-03`, score 15).

These high-priority risks are mitigated directly through deterministic InnoDB row locking, ACID transaction handlers, RBAC session guards, and iterative testing.

### 11.6 Git Version Control
Git is a distributed version control system used to track source code and SQL schema changes, collaborate across team members, maintain project history, and recover earlier versions.

#### Proposed Repository Structure
```text
BankManagementSystem/
├── sql/
│   ├── 01_schema.sql
│   ├── 02_procedures.sql
│   ├── 03_triggers_views.sql
│   ├── 04_sample_data.sql
│   └── 05_test_queries.sql
├── app/
│   ├── main.py
│   ├── db.py
│   ├── auth.py
│   ├── ui.py
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
│   ├── ER_diagram.md
│   └── SOFTWARE_ENGINEERING_PROJECT_REPORT.md
├── setup_db.py
├── run_acceptance_tests.py
├── requirements.txt
├── README.md
└── .gitignore
```

#### Git Commands
Initialize the repository:
```text
git init
```
Check file changes:
```text
git status
```
Add files:
```text
git add .
```
Commit the first version:
```text
git commit -m "Initial project structure, 3NF SQL schema, and documentation"
```
Create a feature branch:
```text
git switch -c feature/transactions-module
```
Record a feature change:
```text
git add sql/02_procedures.sql app/pages/4_Transactions.py
git commit -m "Add atomic deposit, withdrawal, and deadlock-safe transfer procedures"
```
Return to the main branch:
```text
git switch main
```
Review commit history:
```text
git log --oneline
```
Merge an approved feature branch:
```text
git merge feature/transactions-module
```

### 11.7 Proposed Version History
| Version | Description |
| :--- | :--- |
| v0.1 | Initial project plan, scope, and requirement elicitation. |
| v0.2 | 3NF database schema (`01_schema.sql`) and ER diagram documentation. |
| v0.3 | Stored procedures (`02_procedures.sql`), triggers, views, and UML design. |
| v0.4 | Streamlit multi-page portal (`app/`) and RBAC authentication implementation. |
| v0.5 | Seed data generation (`04_sample_data.sql`) and acceptance testing (`run_acceptance_tests.py`). |
| v1.0 | Approved final release of the Bank Management System. |

### 11.8 Outcome
The risk register identifies major technical and operational threats to the banking project and provides concrete mitigation strategies. Git supports controlled development, collaboration, change tracking, and recovery of earlier versions.

## 12. VERIFICATION AND VALIDATION

### 12.1 Aim
To perform verification and validation activities on the SRS, database design, and implementation, record defects identified during reviews, and prepare a validation report.

### 12.2 Verification and Validation
Verification determines whether work products conform to their specified requirements and design rules.

Validation determines whether the resulting Bank Management System satisfies stakeholder needs and intended banking operations.

A common distinction is:
- Verification: Are we building the product correctly?
- Validation: Are we building the correct product?

### 12.3 Verification Activities
Verification activities for the Bank Management System include:
- Reviewing the SRS for completeness and consistency across all banking modules.
- Checking whether functional and non-functional requirements are uniquely identified.
- Confirming that all 17 stored procedures enforce ACID transaction boundaries.
- Checking that non-functional requirements have measurable acceptance criteria.
- Reviewing UML and ER diagrams for consistency with `01_schema.sql` and `02_procedures.sql`.
- Checking traceability between requirements, database procedures, UI pages, and test cases.
- Executing `run_acceptance_tests.py` to verify zero ledger mismatch across all accounts.

### 12.4 SRS Review Checklist
| Review ID | Review Item | Expected Condition |
| :--- | :--- | :--- |
| VR-01 | Requirements completeness | All essential banking functions (Accounts, Transactions, Loans, Cards, Audit) are covered. |
| VR-02 | Requirement clarity | Each requirement has an unambiguous domain rule (e.g., 18+ age, min balance). |
| VR-03 | Requirement testability | Acceptance conditions can be evaluated via SQL and UI tests. |
| VR-04 | Requirement consistency | Status enumerations and constraints do not contradict one another. |
| VR-05 | Requirement traceability | Requirements can be linked to stored procedures, UI pages, and tests. |
| VR-06 | Security requirements | SHA-256 authentication, RBAC roles, and card masking are specified. |
| VR-07 | Interface requirements | Streamlit UI, MySQL connection pool, and environment variables are identified. |
| VR-08 | Quality requirements | Performance, ACID reliability, and precision targets are measurable. |

### 12.5 Design Review Checklist
| Review ID | Review Item | Expected Condition |
| :--- | :--- | :--- |
| DR-01 | Use case coverage | Interactions for Clerk, Teller, Loan Officer, and Manager are represented. |
| DR-02 | Activity flow | Validations, row locking, and rollback paths are shown in transfer workflows. |
| DR-03 | Sequence consistency | UI, DB pool, stored procedures, and triggers follow a valid interaction sequence. |
| DR-04 | State transitions | Valid account states (`ACTIVE`, `FROZEN`, `DORMANT`, `CLOSED`) and guards are defined. |
| DR-05 | Error handling | Custom `SIGNAL SQLSTATE '45000'` rejection scenarios and rollbacks are addressed. |
| DR-06 | Data consistency | Every account balance equals the net sum of its ledger transactions. |
| DR-07 | Security | Protected pages and operations enforce `require_auth()` role authorization. |

### 12.6 Illustrative Defect Log
The following table logs defects identified during design and code reviews along with the corrective actions implemented.

| Defect ID | Potential Defect | Severity | Recommended Corrective Action |
| :--- | :--- | :--- | :--- |
| D-01 | Simultaneous opposite transfers (`A->B` and `B->A`) risk deadlock. | Major | Lock accounts in ascending ID order (`LEAST` then `GREATEST`) in `sp_transfer`. |
| D-02 | Closing an account with positive balance could orphan customer funds. | Major | Enforce `balance = 0.00` check in `sp_close_account` before setting status to `CLOSED`. |
| D-03 | Sequential queries on pooled MySQL connections raise `Unread result found`. | Moderate | Configure `cursor(dictionary=True, buffered=True)` in `app/db.py`. |
| D-04 | Raw MySQL driver error prefixes (`1644 (45000):`) appear in UI alerts. | Moderate | Strip driver error codes in `app/db.py` so clean error messages display in Streamlit. |
| D-05 | Full 16-digit card numbers appear unmasked in card tables. | Major | Mask card numbers as `XXXX-XXXX-XXXX-1234` in `vw_active_cards`. |
| D-06 | Loan applications could be submitted for customers with unverified KYC. | Major | Add `kyc_status = 'VERIFIED'` guard inside `sp_apply_loan`. |

### 12.7 Requirement Traceability Matrix
| Requirement ID | Design Reference | Test Reference | Verification Method |
| :--- | :--- | :--- | :--- |
| FR-01: Staff Login & RBAC | `users` table, `app/auth.py` | EP-01, EP-02, BVA-01 | Code review and functional test |
| FR-02: Customer Onboarding (18+) | `sp_register_customer`, `2_Customers.py` | EP-04, EP-05 | Trigger review and functional test |
| FR-03: Account Opening & Min Bal | `sp_open_account`, `3_Accounts.py` | AT-06 | Procedure review and integration test |
| FR-04/05: Deposit & Withdrawal | `sp_deposit`, `sp_withdraw`, `4_Transactions.py` | EP-08 | Basis path and boundary test |
| FR-06: Deadlock-Safe Transfer | `sp_transfer`, Activity Diagram | AT-07 | Concurrency review and integration test |
| FR-09/10: Loan Apply & Approve | `sp_apply_loan`, `sp_approve_loan`, Sequence Diagram | AT-09 | Interface review and integration test |
| FR-12: Automated Audit Trail | `audit_log`, 5 Triggers, `8_Reports.py` | AT-08 | Trigger test and audit log inspection |
| NFR-07: Ledger Data Integrity | 3NF Schema (`01_schema.sql`), `DECIMAL(15,2)` | AT-02 | Automated ledger reconciliation query |

### 12.8 Validation Report
Project: Bank Management System

Documents under review: SRS, 3NF ER & UML design, SQL schema/procedures, test plan, and risk register.

Review objectives:
- Confirm that the documented requirements reflect core retail banking functions.
- Check that UML and ER diagrams represent the specified transactional workflows.
- Verify that requirements can be traced to stored procedures, UI pages, and test cases.
- Identify ambiguity, omissions, and concurrency inconsistencies.
- Confirm that all automated acceptance tests pass prior to final submission.

Review procedure:
- Distribute the current document and code versions to reviewers.
- Examine the documents using the SRS and Design review checklists.
- Record each identified defect with a unique identifier and severity.
- Apply corrective fixes to SQL procedures, triggers, and Streamlit pages.
- Execute `run_acceptance_tests.py` to verify all positive and negative test cases.
- Record final approval.

Validation status: Verified against the implemented MySQL 8.0 database and Streamlit portal (`run_acceptance_tests.py` passing with 0 ledger mismatches).

Approval: __________________________

Reviewer: __________________________

Date: __________________________

### 12.9 Outcome
Verification and validation provide a systematic way to identify requirement, concurrency, and design defects early. A traceability matrix, defect log, and automated acceptance test suite ensure high software quality and financial accuracy.

## 13. INTEGRATED PROJECT DEVELOPMENT PLAN

### 13.1 Project Phases
| Phase | Main Activities | Deliverables |
| :--- | :--- | :--- |
| 1. Problem analysis | Study the software crisis in banking systems and identify project challenges. | Problem statement and crisis analysis. |
| 2. Planning | Compare SDLC models and select an Agile iterative approach. | SDLC justification and 5-iteration plan. |
| 3. Requirement engineering | Identify banking stakeholders and collect functional/non-functional requirements. | Requirement list, SRS, and user stories. |
| 4. System design | Design 3NF relational schema and model behavior using UML diagrams. | ER diagram, `01_schema.sql`, and UML diagrams. |
| 5. Core implementation | Implement 17 stored procedures, 5 triggers, 6 views, and 8 Streamlit pages. | `sql/02`–`04` scripts and `app/` portal. |
| 6. Testing & verification | Prepare black-box/white-box test cases and run automated acceptance tests. | Test plan and `run_acceptance_tests.py`. |
| 7. Maintenance planning | Identify corrective, adaptive, perfective, and preventive maintenance needs. | Maintenance plan and schedule. |
| 8. Risk and configuration management | Assess banking project risks and manage versions using Git. | Risk register and Git repository structure. |
| 9. Quality assurance & evaluation | Review requirements/design, trace requirements, and finalize report. | Defect log, traceability matrix, and final report. |

### 13.4 Project Limitations
This project implements a complete local multi-branch Bank Management System backed by MySQL 8.0 and Streamlit for academic demonstration. Integration with external real-time payment networks (such as NPCI/UPI/SWIFT), hardware ATM switches, SMS/email OTP gateways, and production cloud deployment are outside the scope of this course project.

## 14. CONCLUSION
This mini project report demonstrates the application of software engineering principles to the analysis, design, implementation, testing, and maintenance planning of a Bank Management System.

The study of the software crisis highlights the consequences of unclear banking rules, concurrency race conditions, inadequate testing, and weak access control. The SDLC comparison supports the selection of Agile iterative development for delivering modular banking capabilities with continuous verification.

Requirement elicitation and SRS preparation establish the functional and non-functional expectations of the system across four bank roles (Manager, Teller, Loan Officer, and Clerk). User stories and acceptance criteria translate these rules into testable conditions. UML use case, activity, sequence, and state machine diagrams model key banking workflows, including deadlock-free fund transfers and automated loan disbursement.

The testing section illustrates how equivalence partitioning, boundary value analysis, and basis path testing are combined with an automated test suite (`run_acceptance_tests.py`) to verify validation rules and ledger consistency. The maintenance plan addresses corrective, adaptive, perfective, and preventive activities, while the risk register and Git workflow support controlled change management.

Finally, verification and validation ensure that requirements, database procedures, and design documents are complete, consistent, and aligned with stakeholder expectations.

Overall, the project demonstrates that building reliable financial software depends not only on programming but also on systematic planning, database-first transactional design, documentation, testing, risk management, and continuous quality assurance.

## 15. REFERENCES
1. Pressman, R. S., & Maxim, B. R. Software Engineering: A Practitioner's Approach. McGraw Hill.
2. Sommerville, I. Software Engineering. Pearson.
3. IEEE. ISO/IEC/IEEE 29148:2018 — Systems and Software Engineering: Life Cycle Processes — Requirements Engineering.
4. Object Management Group. Unified Modeling Language (UML) Specification. https://www.omg.org/spec/UML/
5. Git Documentation. Git Reference and User Manual. https://git-scm.com/doc
6. ISTQB. Certified Tester Foundation Level Syllabus. https://www.istqb.org/

END OF REPORT
