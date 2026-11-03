"""
Script to generate the Software Engineering Course Project Report (.docx)
for the Bank Management System (BMS).
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, hex_color):
    """Set the background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set padding/margins for a table cell in twentieths of a point (dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    """Set subtle, professional borders for a table."""
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), val)
        border.set(qn('w:sz'), sz)
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), color)
        tblBorders.append(border)
    insideV = OxmlElement('w:insideV')
    insideV.set(qn('w:val'), 'none')
    tblBorders.append(insideV)
    tblPr.append(tblBorders)

def format_table(table, header_bg="1F4E9C", alt_bg="F4F6F9"):
    """Format table with header styling and alternating row background."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    
    # Format Header Row
    header_tr = table.rows[0]
    trPr = header_tr._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))
    
    for cell in header_tr.cells:
        set_cell_background(cell, header_bg)
        set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(9.5)
                run.font.name = "Calibri"
                
    # Format Data Rows
    for i, row in enumerate(table.rows[1:], start=1):
        bg = alt_bg if i % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            if bg != "FFFFFF":
                set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9.0)
                    run.font.name = "Calibri"

def add_callout(doc, text, title=None):
    """Add a stylized callout box with a colored left border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4FA")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border only
    tc_pr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '24') # 3pt
    left.set(qn('w:space'), '0')
    left.set(qn('w:color'), '1F4E9C')
    tcBorders.append(left)
    
    for b in ['top', 'bottom', 'right']:
        node = OxmlElement(f'w:{b}')
        node.set(qn('w:val'), 'none')
        tcBorders.append(node)
    tc_pr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    if title:
        run_t = p.add_run(f"{title}\n")
        run_t.bold = True
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(10.5)
        run_t.font.color.rgb = RGBColor(31, 78, 156)
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(9.5)
    run.font.italic = True
    run.font.color.rgb = RGBColor(40, 50, 70)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_code_block(doc, code_text):
    """Add a shaded monospace code / pseudocode block."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tc_pr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for b in ['top', 'bottom', 'left', 'right']:
        node = OxmlElement(f'w:{b}')
        node.set(qn('w:val'), 'single')
        node.set(qn('w:sz'), '4')
        node.set(qn('w:color'), 'D0D7DE')
        tcBorders.append(node)
    tc_pr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(36, 41, 47)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_report():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles Setup
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 30, 30)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # COVER / HEADER PAGE
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("VISHWAKARMA INSTITUTE OF TECHNOLOGY, PUNE\n")
    r_inst.bold = True
    r_inst.font.size = Pt(15)
    r_inst.font.color.rgb = RGBColor(31, 78, 156)
    
    r_dept = p_inst.add_run("DEPARTMENT OF COMPUTER ENGINEERING\n")
    r_dept.bold = True
    r_dept.font.size = Pt(12)
    r_dept.font.color.rgb = RGBColor(80, 80, 80)
    
    r_ay = p_inst.add_run("Academic Year 2026–2027\n\n")
    r_ay.font.size = Pt(10.5)
    r_ay.font.color.rgb = RGBColor(120, 120, 120)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tag = p_proj.add_run("COURSE PROJECT MINI REPORT\n")
    r_tag.bold = True
    r_tag.font.size = Pt(13)
    r_tag.font.color.rgb = RGBColor(180, 40, 40)
    
    r_title = p_proj.add_run("BANK MANAGEMENT SYSTEM (BMS)\n")
    r_title.bold = True
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = RGBColor(31, 78, 156)
    
    r_sub = p_proj.add_run("An Enterprise-Grade, Database-First Financial Core with ACID Integrity and Role-Based Portals\n\n")
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(90, 90, 90)

    # Submission Meta Table
    tbl_meta = doc.add_table(rows=6, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Course Name:", "Software Engineering (Computer Engineering)"),
        ("Project Type:", "Course Mini Project / Laboratory Comprehensive Report"),
        ("Class & Division:", "TY B.Tech Computer Engineering / Division: _____"),
        ("Submitted By:", "1. Roll No: _________ | Name: _____________________\n"
                         "2. Roll No: _________ | Name: _____________________\n"
                         "3. Roll No: _________ | Name: _____________________\n"
                         "4. Roll No: _________ | Name: _____________________"),
        ("Guide / Evaluator:", "Prof. __________________________________"),
        ("Submission Date:", "November 2026")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = tbl_meta.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.2)
        cell_val.width = Inches(4.3)
        
        p0 = cell_lbl.paragraphs[0]
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.size = Pt(10)
        r0.font.color.rgb = RGBColor(31, 78, 156)
        
        p1 = cell_val.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(10)
        set_cell_background(cell_lbl, "F0F4FA")
        set_cell_background(cell_val, "FAFAFA")
        set_cell_margins(cell_lbl, 80, 80, 100, 100)
        set_cell_margins(cell_val, 80, 80, 100, 100)
    
    set_table_borders(tbl_meta, color="CCCCCC")
    doc.add_page_break()

    # -------------------------------------------------------------
    # ABSTRACT & TOC
    # -------------------------------------------------------------
    h_abs = doc.add_heading("ABSTRACT", level=1)
    h_abs.paragraph_format.space_before = Pt(12)
    
    p_abs = doc.add_paragraph(
        "Software engineering provides a disciplined, quantifiable, and systematic approach to the development, "
        "operation, and maintenance of high-integrity software applications. In enterprise and financial domains, "
        "software systems must strictly guarantee transactional consistency (ACID properties), zero financial drift, "
        "tamper-evident auditability, robust role-based security, and strict regulatory compliance.\n\n"
        "This mini project presents a comprehensive software engineering study centered on a production-grade Bank Management System (BMS). "
        "The report integrates key software engineering concepts across the life cycle: analyzing the causes and catastrophic consequences "
        "of the software crisis in banking; comparative evaluation of Software Development Life Cycle (SDLC) models justifying an iterative/hybrid "
        "Agile-V methodology; rigorous requirement elicitation and categorization into functional and non-functional requirements; a formal "
        "IEEE 830-compliant Software Requirement Specification (SRS) with acceptance-criteria-backed user stories; behavior and architectural "
        "modeling via Unified Modeling Language (UML) use case, activity, sequence, and state machine diagrams; exhaustive black-box and white-box "
        "test design (Equivalence Partitioning, Boundary Value Analysis, and Cyclomatic Complexity Basis Path Testing); software maintenance "
        "categorization and planning; risk management and Git branch workflow strategies; and formal verification and validation (V&V) procedures "
        "with an end-to-end Requirements Traceability Matrix (RTM).\n\n"
        "The resulting system models a 10-table normalized relational core with 17 transactional stored procedures, 5 automated audit triggers, "
        "6 analytical views, and an interactive Streamlit role-based dashboard supporting four operational personas (MANAGER, TELLER, LOAN_OFFICER, and CLERK). "
        "This report validates that rigorous software engineering planning, verification, and testing are vital to preventing critical financial discrepancies "
        "and building dependable financial systems."
    )
    p_kw = doc.add_paragraph()
    r_kwt = p_kw.add_run("Keywords: ")
    r_kwt.bold = True
    r_kwt.font.color.rgb = RGBColor(31, 78, 156)
    p_kw.add_run("Software Engineering, Bank Management System, ACID Transactions, SDLC, SRS, UML, Equivalence Partitioning, Basis Path Testing, Risk Register, Git Version Control, Verification and Validation.")

    # Table of Contents
    doc.add_heading("TABLE OF CONTENTS", level=1)
    toc_items = [
        ("1. Introduction & Project Scope", "Page 3"),
        ("2. Problem Statement", "Page 4"),
        ("3. Project Objectives", "Page 4"),
        ("4. Study of the Software Crisis", "Page 5"),
        ("5. Comparison of SDLC Models & Justification", "Page 7"),
        ("6. Requirement Elicitation & Classification", "Page 9"),
        ("7. SRS & Acceptance-Criteria User Stories", "Page 11"),
        ("8. UML Behavioral & Structural Modeling", "Page 13"),
        ("9. Software Testing (Black-Box & White-Box)", "Page 16"),
        ("10. Software Maintenance Planning & SLA", "Page 19"),
        ("11. Risk Management & Git Version Control", "Page 21"),
        ("12. Verification & Validation (RTM & Defect Log)", "Page 24"),
        ("13. Integrated Project Development Plan", "Page 26"),
        ("14. Conclusion", "Page 27"),
        ("15. References", "Page 28"),
    ]
    tbl_toc = doc.add_table(rows=len(toc_items), cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (sec_title, page_no) in enumerate(toc_items):
        r = tbl_toc.rows[idx]
        c0, c1 = r.cells[0], r.cells[1]
        c0.width = Inches(5.5)
        c1.width = Inches(1.0)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(sec_title)
        r0.font.size = Pt(10)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(page_no)
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(100, 100, 100)
        set_cell_margins(c0, 40, 40, 60, 60)
        set_cell_margins(c1, 40, 40, 60, 60)
    set_table_borders(tbl_toc, color="E0E0E0")
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 1: INTRODUCTION
    # -------------------------------------------------------------
    doc.add_heading("1. INTRODUCTION", level=1)
    doc.add_paragraph(
        "Software engineering is the systematic application of engineering principles, methods, and management techniques to software development. "
        "Unlike non-critical consumer applications, financial software applications operate under zero-tolerance thresholds for data corruption, "
        "transaction non-repudiation, and unauthorized access."
    )
    doc.add_paragraph(
        "A Bank Management System (BMS) is a mission-critical platform designed to administer core banking operations: customer onboarding, "
        "KYC compliance, multi-tier account lifecycle management (Savings, Current, Fixed Deposit), transactional ledger execution (deposits, "
        "cash withdrawals, inter-account transfers, maintenance fees), loan origination with amortization scheduling, debit/credit card issuance, "
        "and automated regulatory reporting."
    )
    doc.add_paragraph(
        "Developing such a system requires more than writing basic database queries or interface scripts. The development lifecycle requires formal "
        "requirements engineering to prevent ambiguous banking rules, selection of an appropriate life cycle model, rigorous architectural and behavioral "
        "modeling, systematic verification of deadlock-free transactional routines, and multi-tier testing."
    )

    doc.add_heading("1.1 Scope of the Project", level=2)
    doc.add_paragraph("The Bank Management System encapsulates the following core functional modules:")
    modules = [
        ("Authentication & Role-Based Access Control (RBAC):", " Multi-persona access boundary enforcing distinct access privileges for MANAGER, TELLER, LOAN_OFFICER, and CLERK."),
        ("Customer Relationship & KYC Management:", " Customer profile onboarding, national ID / PAN deduplication, age validation (18+), and KYC verification state tracking."),
        ("Account Portfolio Administration:", " Account provisioning across Savings, Current, and Fixed Deposit accounts with minimum balance constraints and operational status switches (ACTIVE, FROZEN, CLOSED)."),
        ("Atomic Transactional Processing:", " Fund transfer, deposit, withdrawal, and service charge execution enforced via MySQL InnoDB stored procedures using strict row-locking (SELECT ... FOR UPDATE in ascending account ID order) to eliminate concurrency race conditions and deadlocks."),
        ("Loan Origination & Amortization:", " Loan application submission, credit approval/rejection workflows, live Equated Monthly Installment (EMI) calculation, disbursement, and automated EMI deduction."),
        ("Card Management:", " Card issuance (Debit/Credit), monthly spending limits, CVV encryption, and immediate freeze/unblock controls."),
        ("Automated Audit Trails & Analytical Intelligence:", " Autonomous trigger-based logging of all balance adjustments, status changes, and administrative actions, accompanied by visual business intelligence reports (branch liquidity distributions, high-net-worth rankings, dormant account detection).")
    ]
    for title, desc in modules:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(title)
        r_b.bold = True
        p.add_run(desc)

    # -------------------------------------------------------------
    # SECTION 2: PROBLEM STATEMENT
    # -------------------------------------------------------------
    doc.add_heading("2. PROBLEM STATEMENT", level=1)
    doc.add_paragraph(
        "Traditional banking workflows and poorly architected legacy banking software suffer from significant operational and computational bottlenecks:"
    )
    problems = [
        ("Manual Overhead and Latency:", " Paper-based or uncoordinated electronic customer onboarding and physical ledger maintenance increase transaction turnaround times and human bookkeeping errors."),
        ("Concurrency Conflicts and Ledger Inconsistencies:", " Concurrent access by multiple teller terminals or automated processes can lead to the classic 'lost update' problem, overdraft violations, or phantom reads if concurrency controls and transaction boundaries are absent."),
        ("Deadlock Vulnerabilities:", " When two transfers between the same two accounts happen in reverse order simultaneously, improper locking order locks both accounts indefinitely, leading to system hangs and aborted customer transactions."),
        ("Insufficient Auditability & Fraud Vulnerability:", " Lack of automated, tamper-proof audit trails leaves banking institutions vulnerable to insider fraud, unauthorized overdrafts, or untracked state modifications."),
        ("Disjointed Business Logic:", " Implementing critical financial balance checks solely within the client UI layer rather than at the database persistence layer invites bypass risks and data corruption during API integration.")
    ]
    for p_title, p_desc in problems:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(p_title)
        r_b.bold = True
        p.add_run(p_desc)
    doc.add_paragraph(
        "Therefore, a database-first, robustly engineered Bank Management System must be designed using software engineering principles "
        "to enforce strict ACID properties, deterministic locking, automated audit triggers, and secure role-based portals."
    )

    # -------------------------------------------------------------
    # SECTION 3: OBJECTIVES
    # -------------------------------------------------------------
    doc.add_heading("3. OBJECTIVES", level=1)
    doc.add_paragraph("The primary software engineering objectives of this project are:")
    objectives = [
        "To study the causes and catastrophic consequences of the software crisis within the financial and banking sector.",
        "To comparatively analyze different SDLC models and justify an iterative Hybrid Agile-V methodology suited for banking.",
        "To execute structured requirement elicitation across banking stakeholders and classify functional and non-functional requirements.",
        "To prepare an IEEE-standard Software Requirement Specification (SRS) and define acceptance-criteria-backed user stories.",
        "To model system behavior and architectural relationships using UML Use Case, Activity, Sequence, and State Machine diagrams.",
        "To formulate black-box test suites (Equivalence Partitioning, Boundary Value Analysis) and white-box Basis Path Testing with Cyclomatic Complexity.",
        "To categorize software maintenance routines (Corrective, Adaptive, Perfective, Preventive) and formulate a maintenance SLA plan.",
        "To build a quantitative 5x5 risk management register with actionable mitigation strategies and define a Git version control release model.",
        "To perform systematic Verification and Validation (V&V) through structured reviews, an end-to-end Traceability Matrix, and formal Defect Logging."
    ]
    for obj in objectives:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(obj)

    # -------------------------------------------------------------
    # SECTION 4: STUDY OF THE SOFTWARE CRISIS
    # -------------------------------------------------------------
    doc.add_heading("4. STUDY OF THE SOFTWARE CRISIS", level=1)
    doc.add_heading("4.1 Aim", level=2)
    doc.add_paragraph("To investigate the causes, systemic risks, and consequences of the software crisis within the financial and banking sector, and formulate engineering mitigations.")
    
    doc.add_heading("4.2 Introduction", level=2)
    doc.add_paragraph(
        "The Software Crisis refers to the persistent phenomenon where software projects exceed budgetary allocations, run significantly "
        "past deadlines, display severe unreliability, fail user requirements, and become unmaintainable. In financial systems, the software crisis "
        "can directly destroy institutional liquidity, disrupt national payment networks, and trigger legal penalties."
    )

    doc.add_heading("4.3 Real-World Case Study: The TSB Bank IT Migration Disaster (2018)", level=2)
    add_callout(
        doc,
        "In April 2018, UK-based TSB Bank attempted to migrate 5.2 million customer records and 1.3 billion records from its former "
        "parent company's (Lloyds Banking Group) legacy core banking system to a new proprietary platform called Proteo4UK.\n\n"
        "• The Catastrophe: Upon going live, the system experienced catastrophic failure. Customers were locked out of their accounts, "
        "could see other customers' confidential financial balances and transactions, unauthorized payments failed, and businesses could not run payroll.\n"
        "• The Consequences: TSB incurred direct losses exceeding £330 million in customer compensation, fraud remediation, and regulatory fines "
        "by the Financial Conduct Authority (FCA). The Chief Executive resigned, and the bank suffered immense reputational damage.\n"
        "• Engineering Root Causes: Independent post-mortems revealed severe testing shortcuts, inadequate integration testing under concurrent loads, "
        "poorly verified cutover procedures, and insufficient documentation.",
        title="CASE STUDY: TSB BANK CORE MIGRATION COLLAPSE"
    )

    doc.add_heading("4.4 Causes of the Software Crisis in Banking Systems", level=2)
    t_crisis = doc.add_table(rows=7, cols=3)
    crisis_headers = ["Cause Factor", "Description in Banking Context", "Concrete Project Example"]
    for c_idx, h in enumerate(crisis_headers):
        t_crisis.rows[0].cells[c_idx].paragraphs[0].text = h
    
    crisis_rows = [
        ("Ambiguous Business Rules", "Financial policies and edge conditions are not rigorously specified.", "Failure to specify whether minimum balance checks apply before or after charging transaction fees."),
        ("Concurrency & Race Conditions", "Multi-user access without deterministic locking orders causes balance drift.", "Two concurrent withdrawals from the same account causing an illegal negative balance."),
        ("Inadequate Testing Under Load", "Systems are tested only on single-user, happy-path flows.", "Simultaneous inter-account transfers deadlocking MySQL InnoDB threads."),
        ("Incomplete Audit Logging", "Changes occur in volatile memory without immutable database triggers.", "Inability to identify which teller authorized an illegal overdraft override."),
        ("Poor Interface Boundaries", "Business logic is scattered across UI scripts rather than encapsulated in DB procedures.", "UI bypass allowing direct database inserts of non-compliant customer records."),
        ("Scope Creep & Changing Regulations", "Central bank statutory changes (e.g., KYC mandates, tax deductions) injected without change control.", "Uncontrolled ad-hoc additions of fee waivers destabilizing the core ledger.")
    ]
    for r_idx, (col0, col1, col2) in enumerate(crisis_rows, start=1):
        row = t_crisis.rows[r_idx]
        row.cells[0].paragraphs[0].text = col0
        row.cells[1].paragraphs[0].text = col1
        row.cells[2].paragraphs[0].text = col2
    format_table(t_crisis)

    doc.add_heading("4.5 Recommended Solutions & Outcome", level=2)
    doc.add_paragraph(
        "To mitigate software crisis conditions, the Bank Management System adopts database-first invariant enforcement "
        "(stored procedures and triggers), defensive ascending row-locking to guarantee deadlock prevention, role-based access control, "
        "and automated regression test suites verifying zero ledger drift."
    )

    # -------------------------------------------------------------
    # SECTION 5: COMPARISON OF SDLC MODELS
    # -------------------------------------------------------------
    doc.add_heading("5. COMPARISON OF SDLC MODELS", level=1)
    doc.add_heading("5.1 Aim", level=2)
    doc.add_paragraph("To comparatively analyze classical and modern SDLC models and justify the most suitable development methodology for a robust Bank Management System.")

    doc.add_heading("5.2 Comparative Analysis Matrix", level=2)
    t_sdlc = doc.add_table(rows=6, cols=4)
    sdlc_headers = ["SDLC Model", "Key Strengths", "Critical Limitations", "Suitability for Banking Systems"]
    for c_idx, h in enumerate(sdlc_headers):
        t_sdlc.rows[0].cells[c_idx].paragraphs[0].text = h
    
    sdlc_rows = [
        ("Waterfall", "Highly structured; thorough upfront documentation; clear milestones.", "Inflexible; cannot accommodate changing financial regulations; testing occurs only at the end.", "Unsuitable for modern full-stack platforms; high risk of late-stage integration failure."),
        ("V-Model (V&V)", "Emphasizes verification at each development stage; high reliability and test-driven rigor.", "Inflexible to changes once specifications are approved; costly overhead for small prototype changes.", "Highly suitable for safety-critical and core ledger modules where verification cannot be deferred."),
        ("Incremental", "Delivers functional partitions in increments; reduces initial deployment wait time.", "Requires comprehensive early architectural vision to avoid downstream integration friction.", "Good for releasing core accounts first, followed by loans and credit cards."),
        ("Spiral", "Explicit focus on risk analysis; iterative prototyping allows early vulnerability detection.", "Complex project management; high cost; requires specialized risk assessment expertise.", "Well suited for high-risk, multi-million dollar core banking modernizations."),
        ("Agile (Scrum)", "High flexibility; continuous stakeholder collaboration; rapid feedback loops through 2-week sprints.", "Requires high discipline; risk of scope creep; documentation can be neglected if not enforced.", "Excellent for building responsive web dashboards, customer management, and analytics.")
    ]
    for r_idx, rdata in enumerate(sdlc_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_sdlc.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_sdlc)

    doc.add_heading("5.3 Selected Methodology: Hybrid Agile-V Life Cycle", level=2)
    doc.add_paragraph(
        "For the Bank Management System, a Hybrid Agile-V Model is selected:\n"
        "• Core Ledger Layer (V-Model Rigor): The relational schema, stored procedures, audit triggers, and ACID fund movement routines "
        "are managed with strict V-Model verification (formal specifications paired with automated integration test suites) because transactional errors cannot be tolerated.\n"
        "• Application & Dashboard Layer (Agile Iterations): The multi-page Streamlit portal, role-based dashboards, loan calculators, and analytical reports "
        "are developed in 2-week Agile sprints with rapid customer and branch staff feedback."
    )

    doc.add_heading("5.4 Proposed Development Sprints", level=2)
    t_sprints = doc.add_table(rows=7, cols=3)
    sp_headers = ["Iteration", "Focus Area", "Deliverables & Milestones"]
    for c_idx, h in enumerate(sp_headers):
        t_sprints.rows[0].cells[c_idx].paragraphs[0].text = h
    sp_rows = [
        ("Sprint 1", "Requirements & Database Core", "10-table 3NF relational schema, primary/foreign keys, check constraints (sql/01_schema.sql)."),
        ("Sprint 2", "Transaction Engine & Procedures", "17 Stored procedures with exception handlers, START TRANSACTION, COMMIT, ROLLBACK (sql/02_procedures.sql)."),
        ("Sprint 3", "Triggers, Views & Audit System", "5 automated audit triggers, 6 analytical views, and seed test data (sql/03_triggers_views.sql, sql/04_sample_data.sql)."),
        ("Sprint 4", "Authentication & Core Workflows", "Streamlit RBAC login, Teller customer onboarding, and account deposit/withdrawal screens (app/main.py, app/auth.py)."),
        ("Sprint 5", "Loans, Cards & System Reports", "Loan origination, EMI calculator, card management, branch analytics, and CSV exports (app/pages/*.py)."),
        ("Sprint 6", "System Testing & Final Acceptance", "Automated Python test harness (run_acceptance_tests.py), security review, and documentation.")
    ]
    for r_idx, rdata in enumerate(sp_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_sprints.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_sprints)

    # -------------------------------------------------------------
    # SECTION 6: REQUIREMENT ELICITATION
    # -------------------------------------------------------------
    doc.add_heading("6. REQUIREMENT ELICITATION", level=1)
    doc.add_heading("6.1 Stakeholder Analysis", level=2)
    t_stakeholders = doc.add_table(rows=6, cols=3)
    sh_headers = ["Stakeholder Role", "Responsibilities in System", "Primary Needs & Pain Points"]
    for c_idx, h in enumerate(sh_headers):
        t_stakeholders.rows[0].cells[c_idx].paragraphs[0].text = h
    sh_rows = [
        ("Bank Manager", "Oversees branch operations, staffing, risk health, and compliance.", "Requires branch liquidity views, audit logs, employee hiring/transfer tools, and fee-run execution."),
        ("Teller", "Executes daily cash and account ledger operations.", "Needs rapid account balance verification, instant deposit/withdrawal, and error-free inter-account transfers."),
        ("Loan Officer", "Manages loan origination and risk evaluation.", "Needs automated EMI calculation, debt-to-income checks, and loan approval/rejection workflows."),
        ("Clerk", "Handles customer onboarding and administrative service requests.", "Needs form validation for customer registration, age verification (18+), KYC updates, and card issuance."),
        ("Auditor / Compliance Officer", "Audits transaction legality and financial integrity.", "Requires tamper-proof, immutable audit trail logs and dormant account inspection.")
    ]
    for r_idx, rdata in enumerate(sh_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_stakeholders.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_stakeholders)

    doc.add_heading("6.2 Functional Requirements (FR)", level=2)
    t_fr = doc.add_table(rows=12, cols=3)
    fr_headers = ["ID", "Requirement Description", "Target Actor"]
    for c_idx, h in enumerate(fr_headers):
        t_fr.rows[0].cells[c_idx].paragraphs[0].text = h
    fr_rows = [
        ("FR-01", "The system shall authenticate staff members via username and salted/hashed passwords and assign session roles.", "All Staff"),
        ("FR-02", "The system shall register new customers with mandatory national ID (Aadhaar/PAN), email, phone, and verify that date-of-birth confirms age >= 18.", "Clerk, Manager"),
        ("FR-03", "The system shall provision Savings, Current, and Fixed Deposit accounts with system-generated unique account numbers.", "Clerk, Teller, Manager"),
        ("FR-04", "The system shall enforce minimum balance thresholds (e.g., ₹1,000 for Savings; ₹5,000 for Current) and reject violations via SQL exceptions.", "System Core"),
        ("FR-05", "The system shall execute atomic fund deposits and cash withdrawals, adjusting account balances and recording ledger transactions.", "Teller, Manager"),
        ("FR-06", "The system shall execute inter-account transfers atomically, debiting the source and crediting the destination within a single rollback-safe transaction block.", "Teller, Manager"),
        ("FR-07", "The system shall originate loan applications, compute standard amortized monthly EMI, and record loan tenure and interest rates.", "Loan Officer"),
        ("FR-08", "The system shall allow authorized Loan Officers/Managers to approve or reject loans and disburse approved loan principals directly into customer savings accounts.", "Loan Officer, Manager"),
        ("FR-09", "The system shall issue Debit and Credit cards, manage CVV security, set spending limits, and allow immediate freezing/unblocking.", "Clerk, Manager"),
        ("FR-10", "The system shall automatically record all balance updates, account status changes, and employee actions in an append-only audit_log table via triggers.", "System (Automated)"),
        ("FR-11", "The system shall generate branch performance analytics, high-net-worth rankings, and exportable financial reports.", "Manager")
    ]
    for r_idx, rdata in enumerate(fr_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_fr.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_fr)

    doc.add_heading("6.3 Non-Functional Requirements (NFR)", level=2)
    t_nfr = doc.add_table(rows=7, cols=4)
    nfr_headers = ["ID", "Category", "Metric / Specification", "Acceptance Criterion"]
    for c_idx, h in enumerate(nfr_headers):
        t_nfr.rows[0].cells[c_idx].paragraphs[0].text = h
    nfr_rows = [
        ("NFR-01", "Transactional Consistency (ACID)", "Zero ledger drift; 100% atomic operations.", "All balance changes executed within InnoDB transactions with rollback handlers."),
        ("NFR-02", "Performance & Latency", "Query execution time under normal operational workload.", "Routine balance queries and deposits complete within < 500 ms; complex reports within < 2 s."),
        ("NFR-03", "Security & Access Control", "Role-Based Access Control (RBAC) enforcement.", "Unauthorized page visits redirected immediately; zero direct password exposure in plain text."),
        ("NFR-04", "Data Integrity", "Foreign key constraints and check validations.", "MySQL engine rejects negative balances, orphan loan records, and underage customer entries at DB level."),
        ("NFR-05", "Availability & Reliability", "System uptime during business operating hours.", "Database connection pool automatically reconnects upon transient connection drops."),
        ("NFR-06", "Auditability", "Non-repudiation of financial operations.", "System writes an immutable timestamped log row for every single financial update.")
    ]
    for r_idx, rdata in enumerate(nfr_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_nfr.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_nfr)

    # -------------------------------------------------------------
    # SECTION 7: SRS AND USER STORIES
    # -------------------------------------------------------------
    doc.add_heading("7. SRS AND USER STORIES", level=1)
    doc.add_paragraph(
        "The Software Requirement Specification establishes the functional boundaries, database relational invariants, "
        "and client interfaces. User stories translate these formal requirements into user-centric operational behaviors accompanied "
        "by testable Given-When-Then acceptance criteria."
    )

    user_stories = [
        ("User Story 1: Inter-Account Fund Transfer (Atomic Execution)",
         "As a Bank Teller,\nI want to transfer funds from a source account to a destination account upon customer request,\nSo that funds are securely and instantly remitted without any risk of double-spending or partial debits.",
         "1. Given a source account with sufficient balance above the minimum required balance (₹1,000 for Savings), when a valid transfer amount is submitted, then the system debits the source, credits the destination, creates a TRANSFER transaction record, and commits.\n"
         "2. Given an transfer amount greater than (source_balance - minimum_balance), when transfer is initiated, then the transaction is rolled back and an explicit error message 'Insufficient balance' is displayed.\n"
         "3. Given two concurrent transfers between Account A and Account B in opposing directions, then the system locks records in ascending order of Account ID (min(from_id, to_id) first), avoiding database deadlocks.\n"
         "4. Given either account is in FROZEN or CLOSED state, then the transaction is immediately aborted."),
        
        ("User Story 2: Customer Onboarding with Age & KYC Validation",
         "As a Bank Clerk,\nI want to register a new customer profile with personal, contact, and identity details,\nSo that the customer can open financial accounts while complying with statutory KYC norms.",
         "1. Given complete registration fields with date-of-birth proving age >= 18 years, when submitted, then a new customer record is created with KYC_STATUS = 'PENDING'.\n"
         "2. Given a date of birth indicating age < 18 years, when submitted, then the system rejects creation with a 'Customer must be at least 18 years old' validation error.\n"
         "3. Given a duplicate Aadhaar or PAN number already present in the database, then the unique constraint aborts the insert and alerts the clerk."),
        
        ("User Story 3: Loan Origination, Live EMI Preview and Disbursement",
         "As a Loan Officer,\nI want to evaluate loan applications, preview live amortization EMI, and approve credit disbursements,\nSo that the bank can safely disburse capital while ensuring prompt interest returns.",
         "1. Given requested loan principal, annual interest rate, and tenure in months, when evaluated in the portal, then the system calculates monthly EMI using standard amortization formula: EMI = [P * r * (1+r)^n] / [(1+r)^n - 1].\n"
         "2. Given a loan in APPLIED state, when the Loan Officer clicks Approve, then the status transitions to APPROVED, and upon disbursement, the principal amount is atomically credited to the customer's savings account.\n"
         "3. Given an applicant with an active REJECTED or default status, then the system prevents automated disbursement."),

        ("User Story 4: Automated Trigger-Based Audit Trails",
         "As a Bank Manager / Internal Auditor,\nI want to review an immutable system audit trail,\nSo that all balance alterations, status modifications, and teller actions are verifiable.",
         "1. Given any update to accounts.balance, when committed, then the trg_account_balance_audit trigger immediately inserts a row into audit_log detailing old balance, new balance, user ID, and timestamp.\n"
         "2. Given an attempt by any application user to delete rows from audit_log, then the database permissions prevent DELETE operations, preserving log immutability.")
    ]

    for us_title, narrative, criteria in user_stories:
        doc.add_heading(us_title, level=2)
        p_narr = doc.add_paragraph()
        r_n = p_narr.add_run(narrative)
        r_n.italic = True
        
        add_callout(doc, criteria, title="ACCEPTANCE CRITERIA (GIVEN-WHEN-THEN)")

    # -------------------------------------------------------------
    # SECTION 8: UML MODELING
    # -------------------------------------------------------------
    doc.add_heading("8. UML MODELING", level=1)
    doc.add_paragraph(
        "Unified Modeling Language (UML) models formalize the structural relationships and dynamic behavior of the Bank Management System. "
        "The following diagrams document the use cases, transactional workflows, sequence interactions, and entity lifecycles."
    )

    doc.add_heading("8.1 Use Case Model", level=2)
    doc.add_paragraph(
        "The Use Case diagram identifies the boundaries of the Bank Management System across four operational actors:\n"
        "• Clerk: Onboards customers (18+), manages basic accounts, and issues debit/credit cards.\n"
        "• Teller: Performs cash deposits, withdrawals, and atomic inter-account fund transfers.\n"
        "• Loan Officer: Evaluates credit applications, computes EMIs, and processes loan disbursements.\n"
        "• Manager: Full administrative authority; oversees staff hiring/transfers, fee runs, interest runs, and audit reports."
    )
    add_code_block(
        doc,
        "USE CASE ACTOR & SCENARIO INTERACTION SUMMARY:\n"
        "-----------------------------------------------------------------------------------\n"
        "Clerk         --> [UC-1: Authenticate]  --> [UC-2: Register Customer (Age >= 18)]\n"
        "              --> [UC-3: Open Account]  --> [UC-4: Issue/Freeze Card]\n"
        "Teller        --> [UC-1: Authenticate]  --> [UC-5: Deposit / Withdraw Cash]\n"
        "              --> [UC-6: Transfer Funds] --> [UC-7: Balance Enquiry]\n"
        "Loan Officer  --> [UC-1: Authenticate]  --> [UC-8: Originate Loan]\n"
        "              --> [UC-9: Compute EMI]   --> [UC-10: Disburse Principal]\n"
        "Manager       --> Inherits all Use Cases UC-1 to UC-10\n"
        "              --> [UC-11: Employee Staff Transfers] --> [UC-12: Run Monthly Interest]\n"
        "              --> [UC-13: Audit Trail Review]       --> [UC-14: Branch Analytics]"
    )

    doc.add_heading("8.2 Activity Diagram: Atomic Inter-Account Fund Transfer", level=2)
    doc.add_paragraph(
        "The Activity Diagram specifies the sequential steps, decisions, and rollback branches during money movement:"
    )
    add_code_block(
        doc,
        "[Start: Teller initiates transfer]\n"
        "       │\n"
        "       ▼\n"
        "[Input: from_acc_id, to_acc_id, amount]\n"
        "       │\n"
        "       ▼\n"
        "<Is Teller/Manager Authenticated?> ──No──> [Display Auth Error] ──> [Terminate]\n"
        "       │ Yes\n"
        "       ▼\n"
        "[Sort Account IDs: Lock min(ID) first, then max(ID) to prevent deadlocks]\n"
        "       │\n"
        "       ▼\n"
        "[Execute: START TRANSACTION]\n"
        "       │\n"
        "       ▼\n"
        "<Are Both Accounts ACTIVE?> ──No──> [ROLLBACK] ──> [Error: Account Frozen/Closed] ──> [End]\n"
        "       │ Yes\n"
        "       ▼\n"
        "<Sender Balance - Amount >= Min Balance?> ──No──> [ROLLBACK] ──> [Error: Insufficient Bal] ──> [End]\n"
        "       │ Yes\n"
        "       ▼\n"
        "[Debit Sender: balance = balance - amount]\n"
        "       │\n"
        "       ▼\n"
        "[Credit Receiver: balance = balance + amount]\n"
        "       │\n"
        "       ▼\n"
        "[Insert Ledger Row into 'transactions']\n"
        "       │\n"
        "       ▼\n"
        "[Triggers automatically log audit entries to 'audit_log']\n"
        "       │\n"
        "       ▼\n"
        "[Execute: COMMIT Transaction]\n"
        "       │\n"
        "       ▼\n"
        "[Display Transfer Receipt] ──> [End: Transaction Complete]"
    )

    doc.add_heading("8.3 Sequence Diagram: Loan Approval and Disbursement", level=2)
    doc.add_paragraph("The Sequence Diagram details message exchange between UI components, database connection pools, and MySQL stored procedures:")
    add_code_block(
        doc,
        "Loan Officer          Streamlit UI             Database Pool            MySQL Stored Proc Engine\n"
        "     │                     │                         │                              │\n"
        "     │── Click Disburse ──>│                         │                              │\n"
        "     │                     │── sp_disburse_loan() ──>│                              │\n"
        "     │                     │                         │── START TRANSACTION ────────>│\n"
        "     │                     │                         │                              │── SELECT FOR UPDATE\n"
        "     │                     │                         │                              │── Check status == APPROVED\n"
        "     │                     │                         │                              │── Credit Customer Balance\n"
        "     │                     │                         │                              │── Insert Transaction Row\n"
        "     │                     │                         │                              │── Fire Audit Triggers\n"
        "     │                     │                         │                              │── COMMIT\n"
        "     │                     │                         │<── Success Return Code ──────│\n"
        "     │                     │<── JSON Response ───────│\n"
        "     │<── Show Success ────│"
    )

    doc.add_heading("8.4 State Machine Diagram: Bank Account Lifecycle", level=2)
    doc.add_paragraph("The State Machine diagram models the finite operational states of a bank account:")
    add_code_block(
        doc,
        "[*] ──> [PENDING_APPROVAL: KYC documents submitted]\n"
        "           │\n"
        "           ├─ KYC Verified & Initial Deposit ──> [ACTIVE: Fully Operational]\n"
        "           │                                         │\n"
        "           │                                         ├─ Court Order / 12M Inactive ─> [FROZEN]\n"
        "           │                                         │                                    │\n"
        "           │                                         │<── Identity Re-verified ───────────┘\n"
        "           │                                         │\n"
        "           │                                         └─ Customer Requests Closure ──> [CLOSED]\n"
        "           │\n"
        "           └─ KYC Rejected ──> [REJECTED] ──> [*]\n"
        "[CLOSED] ──> [*]"
    )

    # -------------------------------------------------------------
    # SECTION 9: SOFTWARE TESTING
    # -------------------------------------------------------------
    doc.add_heading("9. SOFTWARE TESTING", level=1)
    doc.add_heading("9.1 Black-Box Testing", level=2)
    doc.add_paragraph(
        "Black-box testing validates the system against requirements without inspecting the underlying source code. "
        "The Cash Withdrawal module is tested under the business rule: Savings Account Minimum Balance = ₹1,000; Initial Balance = ₹10,000."
    )

    doc.add_heading("9.1.1 Equivalence Partitioning (EP)", level=3)
    t_ep = doc.add_table(rows=6, cols=6)
    ep_headers = ["Test ID", "Equivalence Class", "Input Value", "Expected Outcome", "Actual Result", "Status"]
    for c_idx, h in enumerate(ep_headers):
        t_ep.rows[0].cells[c_idx].paragraphs[0].text = h
    ep_rows = [
        ("EP-W01", "Valid Withdrawal Amount", "₹2,500", "Balance debited to ₹7,500; Committed", "Balance debited to ₹7,500", "PASS"),
        ("EP-W02", "Zero or Negative Amount", "-₹500", "Reject: 'Amount must be positive'", "Rejected with SQLState 45000", "PASS"),
        ("EP-W03", "Violating Minimum Balance", "₹9,500", "Reject: 'Insufficient funds below minimum'", "Transaction rolled back", "PASS"),
        ("EP-W04", "Exceeds Total Balance", "₹15,000", "Reject: 'Insufficient balance'", "Transaction rolled back", "PASS"),
        ("EP-W05", "Frozen Account Withdrawal", "₹1,000 (Frozen)", "Reject: 'Account is FROZEN'", "Transaction rejected", "PASS")
    ]
    for r_idx, rdata in enumerate(ep_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_ep.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_ep)

    doc.add_heading("9.1.2 Boundary Value Analysis (BVA)", level=3)
    doc.add_paragraph("Boundary limits for withdrawal from ₹10,000 balance: Min = ₹100, Max = ₹9,000 (leaves ₹1,000 min balance).")
    t_bva = doc.add_table(rows=7, cols=5)
    bva_headers = ["Test ID", "Boundary Tested", "Input Value", "Expected Result", "Status"]
    for c_idx, h in enumerate(bva_headers):
        t_bva.rows[0].cells[c_idx].paragraphs[0].text = h
    bva_rows = [
        ("BVA-W01", "Just below minimum (Min - 1)", "₹99", "Reject: Below minimum withdrawal chunk", "PASS"),
        ("BVA-W02", "Exactly at minimum (Min)", "₹100", "Accept: Debits ₹100, New Balance ₹9,900", "PASS"),
        ("BVA-W03", "Just above minimum (Min + 1)", "₹101", "Accept: Debits ₹101, New Balance ₹9,899", "PASS"),
        ("BVA-W04", "Just below maximum (Max - 1)", "₹8,999", "Accept: Debits ₹8,999, New Balance ₹1,001", "PASS"),
        ("BVA-W05", "Exactly at maximum (Max)", "₹9,000", "Accept: Debits ₹9,000, New Balance ₹1,000", "PASS"),
        ("BVA-W06", "Just above maximum (Max + 1)", "₹9,001", "Reject: Breaches ₹1,000 Minimum Balance", "PASS")
    ]
    for r_idx, rdata in enumerate(bva_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_bva.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_bva)

    doc.add_heading("9.2 White-Box Testing: Basis Path Testing", level=2)
    doc.add_paragraph(
        "White-box testing inspects internal program control logic. The atomic fund transfer procedure is evaluated "
        "using McCabe's Cyclomatic Complexity on its Control Flow Graph (CFG)."
    )
    
    add_code_block(
        doc,
        "ALGORITHM PSEUDOCODE: ATOMIC FUND TRANSFER ROUTINE\n"
        "1:  START\n"
        "2:  READ from_acc_id, to_acc_id, amount\n"
        "3:  IF amount <= 0 THEN\n"
        "4:      DISPLAY 'Error: Amount must be positive'\n"
        "5:      STOP\n"
        "6:  ENDIF\n"
        "7:  IF from_acc_id = to_acc_id THEN\n"
        "8:      DISPLAY 'Error: Cannot transfer to same account'\n"
        "9:      STOP\n"
        "10: ENDIF\n"
        "11: FETCH from_account_status, from_balance, to_account_status\n"
        "12: IF from_account_status != 'ACTIVE' OR to_account_status != 'ACTIVE' THEN\n"
        "13:     DISPLAY 'Error: Account not active'\n"
        "14:     STOP\n"
        "15: ENDIF\n"
        "16: IF (from_balance - amount) < min_balance THEN\n"
        "17:     DISPLAY 'Error: Insufficient balance'\n"
        "18:     STOP\n"
        "19: ELSE\n"
        "20:     EXECUTE atomic_debit_credit_and_commit()\n"
        "21:     DISPLAY 'Transfer Successful'\n"
        "22: ENDIF\n"
        "23: STOP"
    )

    doc.add_paragraph(
        "Cyclomatic Complexity Calculation:\n"
        "Using McCabe's formula V(G) = P + 1, where P is the count of predicate decision nodes:\n"
        "• Decision 1 (Line 3): amount <= 0\n"
        "• Decision 2 (Line 7): from_acc_id == to_acc_id\n"
        "• Decision 3 (Line 12): from_status != 'ACTIVE' OR to_status != 'ACTIVE'\n"
        "• Decision 4 (Line 16): (from_balance - amount) < min_balance\n\n"
        "V(G) = 4 + 1 = 5 independent basis paths."
    )

    t_paths = doc.add_table(rows=6, cols=4)
    path_headers = ["Path", "Decision Sequence", "Input Conditions", "Expected Outcome"]
    for c_idx, h in enumerate(path_headers):
        t_paths.rows[0].cells[c_idx].paragraphs[0].text = h
    path_rows = [
        ("Path 1", "1 -> 3 -> 4 -> 5", "amount = -500", "Rejects: Invalid negative amount"),
        ("Path 2", "1 -> 3 -> 7 -> 8 -> 9", "from_id = 101, to_id = 101, amount = 500", "Rejects: Self-transfer invalid"),
        ("Path 3", "1 -> 3 -> 7 -> 11 -> 12 -> 13 -> 14", "from_status = 'FROZEN', amount = 500", "Rejects: Account not active"),
        ("Path 4", "1 -> 3 -> 7 -> 11 -> 12 -> 16 -> 17 -> 18", "from_balance = 1200, amount = 500, min = 1000", "Rejects: Minimum balance breach"),
        ("Path 5", "1 -> 3 -> 7 -> 11 -> 12 -> 16 -> 20 -> 21 -> 23", "from_balance = 5000, amount = 1000, min = 1000", "Executes transfer & commits")
    ]
    for r_idx, rdata in enumerate(path_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_paths.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_paths)

    # -------------------------------------------------------------
    # SECTION 10: SOFTWARE MAINTENANCE
    # -------------------------------------------------------------
    doc.add_heading("10. SOFTWARE MAINTENANCE", level=1)
    doc.add_heading("10.1 Maintenance Categories", level=2)
    t_maint = doc.add_table(rows=5, cols=3)
    m_headers = ["Maintenance Type", "Objective", "Practical Banking System Scenario"]
    for c_idx, h in enumerate(m_headers):
        t_maint.rows[0].cells[c_idx].paragraphs[0].text = h
    m_rows = [
        ("Corrective Maintenance", "Diagnose and rectify runtime defects and data inconsistencies discovered post-deployment.", "Remedying an edge-case rounding error occurring in fractional paisa calculations during interest compounding."),
        ("Adaptive Maintenance", "Modify software to adapt to shifts in external regulations, infrastructure, or platform dependencies.", "Updating tax deduction tables to align with newly notified Reserve Bank / Income Tax TDS statutory rate changes."),
        ("Perfective Maintenance", "Enhance existing features, user experience, and query efficiency based on operational feedback.", "Adding multi-column filtering to the teller ledger screen and creating a composite index on transactions(account_id, created_at) to accelerate statement generation."),
        ("Preventive Maintenance", "Refactor code, patch vulnerabilities, and rotate database connection secrets before failures occur.", "Upgrading mysql-connector-python and Streamlit dependencies to patch CVEs, and archiving 3-year-old audit logs.")
    ]
    for r_idx, rdata in enumerate(m_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_maint.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_maint)

    doc.add_heading("10.2 Proposed Maintenance SLA Schedule", level=2)
    t_sla = doc.add_table(rows=5, cols=3)
    sla_headers = ["Frequency", "Activity Type", "Operational Action Plan"]
    for c_idx, h in enumerate(sla_headers):
        t_sla.rows[0].cells[c_idx].paragraphs[0].text = h
    sla_rows = [
        ("Daily", "Monitoring", "Inspect automated database error logs for transaction deadlock spikes and failed login anomalies."),
        ("Weekly", "Corrective & Preventive", "Review unresolved ticket logs, verify automated database backups (mysqldump), and test disaster recovery restores."),
        ("Monthly", "Adaptive & Perfective", "Optimize database query performance with EXPLAIN ANALYZE, review index fragmentation, and verify regulatory interest runs."),
        ("Quarterly", "Security & Compliance", "Rotate database root credentials, conduct simulated penetration audits, and execute archival of dormant account records.")
    ]
    for r_idx, rdata in enumerate(sla_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_sla.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_sla)

    # -------------------------------------------------------------
    # SECTION 11: RISK MANAGEMENT AND VERSION CONTROL
    # -------------------------------------------------------------
    doc.add_heading("11. RISK MANAGEMENT AND VERSION CONTROL", level=1)
    doc.add_heading("11.1 Quantitative Risk Assessment Matrix", level=2)
    doc.add_paragraph("Risk Score = Probability (1 to 5) x Impact (1 to 5). Low: 1-4 | Medium: 5-9 | High: 10-16 | Critical: 17-25.")
    
    t_risk = doc.add_table(rows=7, cols=6)
    risk_headers = ["Risk ID", "Risk Description", "Prob (1-5)", "Imp (1-5)", "Score", "Mitigation Strategy"]
    for c_idx, h in enumerate(risk_headers):
        t_risk.rows[0].cells[c_idx].paragraphs[0].text = h
    risk_rows = [
        ("R-01", "Concurrent Transfer Deadlocks: Simultaneous reverse transfers lock identical rows.", "3", "5", "15 (High)", "Enforce deterministic ascending primary-key locking (min(id) then max(id)) in SQL procedures."),
        ("R-02", "Credential & Role Escalation: Unauthorized clerk accessing manager-level tools.", "2", "5", "10 (High)", "Strict session authentication checking (app/auth.py) and UI component guards at page load."),
        ("R-03", "Ledger Inconsistency During Crash: Power loss during mid-transfer leaving money in limbo.", "2", "5", "10 (High)", "Strict MySQL InnoDB ACID engine transactions with write-ahead redo logs and automatic rollback."),
        ("R-04", "Unencrypted Passwords / SQL Injection: Malicious input strings compromising database.", "2", "5", "10 (High)", "Use parameterized queries exclusively (cursor.execute(sql, params)); salted password hashing."),
        ("R-05", "Underage Customer Onboarding: Non-compliant accounts opened violating central banking laws.", "3", "4", "12 (High)", "Dual-layer age verification: Streamlit front-end validation and MySQL database CHECK constraint."),
        ("R-06", "Database Drift / Missing Backup: Hard-drive failure corrupting local database state.", "2", "5", "10 (High)", "Automated daily logical dump scripts (mysqldump) stored on separate encrypted cold storage.")
    ]
    for r_idx, rdata in enumerate(risk_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_risk.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_risk)

    doc.add_heading("11.2 Git Version Control Strategy (GitFlow)", level=2)
    doc.add_paragraph(
        "A structured Git branching model (GitFlow) separates development, feature branches, and stable release tags:"
    )
    add_code_block(
        doc,
        "# Initialize and commit core database architecture\n"
        "git init\n"
        "git add sql/ app/ requirements.txt README.md\n"
        "git commit -m 'feat: initial commit of BMS architecture and database scripts'\n\n"
        "# Create feature branch for ACID stored procedures\n"
        "git switch -c feature/stored-procedures-acid\n"
        "git add sql/02_procedures.sql\n"
        "git commit -m 'feat(sql): implement 17 stored procedures with atomic transaction blocks'\n\n"
        "# Merge feature branch into develop\n"
        "git switch develop\n"
        "git merge --no-ff feature/stored-procedures-acid -m 'merge: integrate stored procedures into develop'\n\n"
        "# Release production version 1.0.0\n"
        "git switch main\n"
        "git merge --no-ff develop -m 'release: v1.0.0 production ready Bank Management System'\n"
        "git tag -a v1.0.0 -m 'Release v1.0.0: Full ACID Bank Management System'"
    )

    # -------------------------------------------------------------
    # SECTION 12: VERIFICATION AND VALIDATION
    # -------------------------------------------------------------
    doc.add_heading("12. VERIFICATION AND VALIDATION", level=1)
    doc.add_heading("12.1 Requirements Traceability Matrix (RTM)", level=2)
    t_rtm = doc.add_table(rows=9, cols=6)
    rtm_headers = ["Req ID", "Requirement Summary", "Design Spec", "Implementation File", "Verification Test", "Status"]
    for c_idx, h in enumerate(rtm_headers):
        t_rtm.rows[0].cells[c_idx].paragraphs[0].text = h
    rtm_rows = [
        ("FR-01", "Staff Authentication & RBAC", "UI Sequence & Session Model", "app/auth.py, app/main.py", "TC-AUTH-01, TC-AUTH-02", "VERIFIED"),
        ("FR-02", "Customer Onboarding (18+)", "Customer Entity & Constraint", "sql/01_schema.sql, 2_Customers.py", "TC-CUST-01, TC-CUST-02", "VERIFIED"),
        ("FR-03", "Account Lifecycle (Active/Freeze)", "Account State Machine", "sql/02_procedures.sql, 3_Accounts.py", "TC-ACC-01, TC-ACC-02", "VERIFIED"),
        ("FR-04", "Minimum Balance Enforcement", "Business Rule Constraint", "sql/02_procedures.sql (sp_withdraw)", "TC-TXN-01, TC-TXN-02", "VERIFIED"),
        ("FR-05", "Atomic Fund Transfer", "Deadlock-Free Transfer Sequence", "sql/02_procedures.sql (sp_transfer)", "TC-TXN-03, TC-TXN-04", "VERIFIED"),
        ("FR-06", "Loan Amortization & Approval", "Loan Workflow Activity Diagram", "sql/02_procedures.sql, 5_Loans.py", "TC-LOAN-01, TC-LOAN-02", "VERIFIED"),
        ("FR-07", "Automated Audit Trail Logging", "Audit Trigger Model", "sql/03_triggers_views.sql", "TC-AUD-01, TC-AUD-02", "VERIFIED"),
        ("FR-08", "Executive Analytical Reporting", "Relational Analytical Views", "sql/03_triggers_views.sql, 8_Reports.py", "TC-REP-01, TC-REP-02", "VERIFIED")
    ]
    for r_idx, rdata in enumerate(rtm_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_rtm.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_rtm)

    doc.add_heading("12.2 Formal Defect Log (Static Analysis & Code Reviews)", level=2)
    t_df = doc.add_table(rows=5, cols=5)
    df_headers = ["Defect ID", "Severity", "Defect Description", "Root Cause", "Corrective Action Implemented"]
    for c_idx, h in enumerate(df_headers):
        t_df.rows[0].cells[c_idx].paragraphs[0].text = h
    df_rows = [
        ("DF-01", "Critical", "Concurrency test caused deadlock when Account 1 and Account 2 transferred to each other simultaneously.", "Arbitrary row locking order in sp_transfer.", "Replaced arbitrary locking with ascending lock ordering: SELECT ... FOR UPDATE sorting by Account ID."),
        ("DF-02", "Major", "Customer registration allowed entering an age under 18 if the clerk typed the year incorrectly.", "Missing database-level date-of-birth check constraint.", "Added database constraint: CHECK (TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) >= 18)."),
        ("DF-03", "Moderate", "Streamlit report page raised zero-division error when an empty branch with no deposits was selected.", "SQL view query lacked COALESCE on aggregated balance sums.", "Updated vw_branch_summary view to wrap aggregate sums with COALESCE(SUM(balance), 0.00)."),
        ("DF-04", "Minor", "Plaintext password exposed in .env.example template.", "Inadvertent hardcoding of local testing string.", "Replaced value with blank placeholder DB_PASSWORD=your_password in .env.example.")
    ]
    for r_idx, rdata in enumerate(df_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_df.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_df)

    # -------------------------------------------------------------
    # SECTION 13: INTEGRATED PROJECT DEVELOPMENT PLAN
    # -------------------------------------------------------------
    doc.add_heading("13. INTEGRATED PROJECT DEVELOPMENT PLAN", level=1)
    doc.add_heading("13.1 Phased Engineering Roadmap", level=2)
    t_plan = doc.add_table(rows=10, cols=3)
    p_headers = ["Phase", "Main Activities", "Deliverables"]
    for c_idx, h in enumerate(p_headers):
        t_plan.rows[0].cells[c_idx].paragraphs[0].text = h
    p_rows = [
        ("1. Problem Analysis", "Study software crisis in banking; identify concurrency and consistency challenges.", "Problem Statement & System Domain Model"),
        ("2. Planning & SDLC", "Comparative analysis of SDLC models; select Hybrid Agile-V life cycle.", "SDLC Justification & Sprint Schedule"),
        ("3. Requirement Engineering", "Stakeholder elicitation; classify FRs and NFRs.", "Formal IEEE SRS & Acceptance User Stories"),
        ("4. System Architecture", "Model static and dynamic system behavior.", "UML Use Case, Activity, Sequence & State Diagrams"),
        ("5. Database Construction", "Construct 10-table 3NF schema, 17 procedures, and 5 triggers.", "SQL scripts (01_schema, 02_procedures, 03_triggers)"),
        ("6. UI Construction", "Develop role-based Streamlit application with auth guards.", "Streamlit multi-page app (app/main.py, pages/*.py)"),
        ("7. Testing & Verification", "Execute Black-Box (EP/BVA) and White-Box Basis Path suites.", "Test execution logs and Python test runner"),
        ("8. Risk & Maintenance", "Formulate 5x5 risk register and long-term maintenance SLA.", "Risk Register, Git repository, Maintenance Plan"),
        ("9. Quality Assurance Signoff", "RTM verification, defect remediation, and final report signoff.", "Comprehensive Course Project Report (.docx)")
    ]
    for r_idx, rdata in enumerate(p_rows, start=1):
        for c_idx, val in enumerate(rdata):
            t_plan.rows[r_idx].cells[c_idx].paragraphs[0].text = val
    format_table(t_plan)

    doc.add_heading("13.2 Technical Boundaries & Assumptions", level=2)
    doc.add_paragraph(
        "While the Bank Management System implements end-to-end relational and transactional rigor, the academic project prototype notes the following boundaries:\n"
        "1. Simulated Payment Gateway: External real-time payment interfaces (SWIFT, NEFT/RTGS, UPI switch networks) are simulated via internal transaction procedures.\n"
        "2. Multi-Factor Authentication (MFA): Authentication utilizes hashed database credentials and role session guards; physical biometric scanners and SMS OTP delivery services are omitted from this phase.\n"
        "3. Multi-Currency Support: All balances and calculations operate in single-currency denomination (Indian Rupee, INR ₹)."
    )

    # -------------------------------------------------------------
    # SECTION 14: CONCLUSION
    # -------------------------------------------------------------
    doc.add_heading("14. CONCLUSION", level=1)
    doc.add_paragraph(
        "This mini project report demonstrates the systematic application of core software engineering methodologies to the specification, "
        "design, construction, and verification of an enterprise-grade Bank Management System (BMS).\n\n"
        "By analyzing the software crisis in banking, the report established that financial software demands zero tolerance for ambiguous requirements, "
        "race conditions, and unverified data operations. The selection of a hybrid Agile-V life cycle model effectively balanced the rigid verification "
        "required for the core ledger engine with the rapid, user-centric iterations needed for the Streamlit dashboard interface.\n\n"
        "Requirement elicitation and formal IEEE-compliant SRS authoring translated complex banking regulations into testable user stories with explicit "
        "acceptance criteria. Behavioral and structural UML diagrams provided unambiguous blueprints for concurrency-safe execution and lifecycle state changes. "
        "Systematic testing—integrating Equivalence Partitioning, Boundary Value Analysis, and Cyclomatic Complexity Basis Path Testing—proved that financial "
        "operations can be exhaustively validated before deployment. Finally, formal risk registers, Git branching protocols, and a comprehensive Requirements "
        "Traceability Matrix demonstrated that quality assurance and verification and validation must accompany every phase of the software engineering lifecycle.\n\n"
        "In conclusion, this project illustrates that building dependable financial software is not simply a coding task, but the disciplined culmination "
        "of rigorous software engineering planning, formal modeling, robust database design, and exhaustive test-driven verification."
    )

    # -------------------------------------------------------------
    # SECTION 15: REFERENCES
    # -------------------------------------------------------------
    doc.add_heading("15. REFERENCES", level=1)
    refs = [
        "Pressman, R. S., & Maxim, B. R. Software Engineering: A Practitioner's Approach. 9th Edition, McGraw-Hill Education.",
        "Sommerville, I. Software Engineering. 10th Edition, Pearson Education.",
        "IEEE Computer Society. IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications.",
        "Object Management Group (OMG). Unified Modeling Language (UML) Specification Version 2.5.1. https://www.omg.org/spec/UML/",
        "MySQL Documentation Team. MySQL 8.0 Reference Manual: InnoDB Storage Engine & Transaction Model. Oracle Corporation.",
        "International Software Testing Qualifications Board (ISTQB). Certified Tester Foundation Level (CTFL) Syllabus. https://www.istqb.org/",
        "Financial Conduct Authority (FCA). Report into the IT Migration and System Failure at TSB Bank plc. HM Treasury / FCA UK."
    ]
    for r in refs:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(r)

    # Output file
    output_path = os.path.abspath("Bank_Management_System_Software_Engineering_Project_Report.docx")
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    build_report()

