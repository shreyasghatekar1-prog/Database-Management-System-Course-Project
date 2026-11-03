# ER Diagram – Bank Management System (Chen Notation)

- **High-Resolution A3 PNG (`4200 × 2970` px)**: `docs/ER_Diagram_Chen_A3.png` (and `ER_Diagram_Chen_A3.png` in project root)
- **Scalable Vector SVG (`420mm × 297mm`)**: `docs/ER_Diagram_Chen_A3.svg`

---

## 1. Entities, Primary Keys & Attribute Types (Chen Notation)

| # | Entity Name | Entity Type (Shape) | Primary / Partial Key | Composite Attributes | Derived / Multivalued Attributes | Other Simple Attributes |
| :- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **BRANCH** | Strong Entity (Rectangle) | `Branch_ID` *(solid underline)* | `Address` → (`Street`, `City`, `State`, `Pincode`) | — | `Branch_Name`, `IFSC_Code`, `Phone` |
| 2 | **CUSTOMER** | Strong Entity (Rectangle) | `Customer_ID` *(solid underline)* | `Name` → (`First_Name`, `Last_Name`)<br>`Address` → (`Street`, `City`, `State`, `Pincode`) | `Age` *(Derived — dashed ellipse)*<br>`Phone` *(Multivalued — double ellipse)* | `DOB`, `Gender`, `Email`, `Aadhaar/PAN` |
| 3 | **ACCOUNT** | Strong Entity (Rectangle) | `Account_No` *(solid underline)* | — | — | `Account_Type`, `Balance`, `Open_Date`, `Status` |
| 4 | **TRANSACTION** | Strong Entity (Rectangle) | `Transaction_ID` *(solid underline)* | — | — | `Type`, `Amount`, `Date_Time`, `Description` |
| 5 | **EMPLOYEE** | Strong Entity (Rectangle) | `Employee_ID` *(solid underline)* | `Name` → (`First_Name`, `Last_Name`) | — | `Designation`, `Salary`, `Phone`, `Email`, `Join_Date` |
| 6 | **LOAN** | Strong Entity (Rectangle) | `Loan_ID` *(solid underline)* | — | — | `Loan_Type`, `Principal_Amount`, `Interest_Rate`, `Start_Date`, `Duration`, `Status` |
| 7 | **LOAN_PAYMENT** | **Weak Entity (Double Rectangle)**<br>*(Owner: `LOAN`)* | `Installment_No` *(Partial Key — dashed underline)* | — | — | `Payment_Date`, `Amount_Paid` |
| 8 | **CARD** | Strong Entity (Rectangle) | `Card_No` *(solid underline)* | — | — | `Card_Type`, `Expiry_Date`, `CVV`, `Status` |
| 9 | **NOMINEE** | Strong Entity (Rectangle) | `Nominee_ID` *(solid underline)* | — | — | `Name`, `Relation` |

---

## 2. Relationships, Cardinalities & Participation Constraints

| # | Relationship Name | Diamond Type | Entity 1 (Left / Top) | Participation (Entity 1) | Cardinality | Entity 2 (Right / Bottom) | Participation (Entity 2) | Notes / Role Labels |
| :- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| 1 | **Owns / Holds** | Single Diamond | `CUSTOMER` | Partial *(Single line)* | **1 : N** | `ACCOUNT` | **Total** *(Double line)* | Every account must belong to a customer |
| 2 | **Maintains** | Single Diamond | `BRANCH` | Partial *(Single line)* | **1 : N** | `ACCOUNT` | **Total** *(Double line)* | Every account is maintained at a branch |
| 3 | **Employs** | Single Diamond | `BRANCH` | Partial *(Single line)* | **1 : N** | `EMPLOYEE` | **Total** *(Double line)* | Every employee is assigned to a branch |
| 4 | **Manages** | Single Diamond *(Recursive)* | `EMPLOYEE` | Partial *(Single line)* | **1 : N** | `EMPLOYEE` | Partial *(Single line)* | Roles: `(Manager)` [**1**] supervises `(Subordinate)` [**N**] |
| 5 | **Performs** | Single Diamond | `ACCOUNT` | Partial *(Single line)* | **1 : N** | `TRANSACTION` | **Total** *(Double line)* | Every transaction must be linked to an account |
| 6 | **Transfer** | Single Diamond *(Recursive)* | `ACCOUNT` | Partial *(Single line)* | **1 : N** | `ACCOUNT` | Partial *(Single line)* | Roles: `(Sender)` [**1**] transfers funds to `(Receiver)` [**N**] |
| 7 | **Has Nominee** | Single Diamond | `ACCOUNT` | Partial *(Single line)* | **1 : N** | `NOMINEE` | **Total** *(Double line)* | Beneficiaries/nominees registered on an account |
| 8 | **Issued** | Single Diamond | `ACCOUNT` | Partial *(Single line)* | **1 : N** | `CARD` | **Total** *(Double line)* | Debit/Credit cards issued against an account |
| 9 | **Applies for** | Single Diamond | `CUSTOMER` | Partial *(Single line)* | **1 : N** | `LOAN` | **Total** *(Double line)* | Every loan is applied for by a customer |
| 10 | **Sanctions** | Single Diamond | `BRANCH` | Partial *(Single line)* | **1 : N** | `LOAN` | **Total** *(Double line)* | Every loan is sanctioned by a branch |
| 11 | **Approves** | Single Diamond | `EMPLOYEE` | Partial *(Single line)* | **1 : N** | `LOAN` | Partial *(Single line)* | Loan officer / manager approves sanctioned loans |
| 12 | **Has Installments** | **Double Diamond** *(Identifying)* | `LOAN` | Partial *(Single line)* | **1 : N** | `LOAN_PAYMENT` | **Total** *(Double line)* | Identifies weak entity `LOAN_PAYMENT` via `(Loan_ID, Installment_No)` |

