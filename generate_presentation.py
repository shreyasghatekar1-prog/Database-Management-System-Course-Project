"""
Script to generate a professional, 29-slide Software Engineering Presentation (.pptx)
for the Bank Management System (BMS) covering all report topics.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    # Theme Colors
    C_NAVY = RGBColor(31, 78, 156)       # Primary #1F4E9C
    C_DARK = RGBColor(30, 41, 59)        # Slate Dark #1E293B
    C_LIGHT_BG = RGBColor(248, 249, 250) # Light #F8F9FA
    C_WHITE = RGBColor(255, 255, 255)
    C_CARD_BG = RGBColor(255, 255, 255)
    C_BORDER = RGBColor(226, 232, 240)   # Slate 200
    C_ACCENT_BLUE = RGBColor(59, 130, 246) # Blue 500
    C_SUCCESS = RGBColor(16, 185, 129)   # Emerald 500
    C_DANGER = RGBColor(239, 68, 68)     # Red 500
    C_MUTED = RGBColor(100, 116, 139)    # Slate 500
    C_GOLD = RGBColor(217, 119, 6)       # Amber 600

    def add_slide_header(slide, title_text, category_text="SOFTWARE ENGINEERING COURSE PROJECT"):
        """Standard slide header banner."""
        # Top accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_NAVY
        bar.line.fill.background()

        # Header container
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(1.0))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_ACCENT_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY
        p_title.space_before = Pt(2)

    def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
        """Adds a clean card shape for content chunking."""
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    def add_table(slide, left, top, width, height, headers, rows_data, col_widths=None):
        """Generates a styled table on the slide."""
        num_rows = len(rows_data) + 1
        num_cols = len(headers)
        table_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
        tbl = table_shape.table

        if col_widths and len(col_widths) == num_cols:
            for idx, w in enumerate(col_widths):
                tbl.columns[idx].width = w

        # Headers
        for idx, text in enumerate(headers):
            cell = tbl.cell(0, idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_NAVY
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.alignment = PP_ALIGN.CENTER
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = C_WHITE

        # Rows
        for r_idx, row_values in enumerate(rows_data, start=1):
            row_bg = RGBColor(241, 245, 249) if r_idx % 2 == 1 else C_WHITE
            for c_idx, val in enumerate(row_values):
                cell = tbl.cell(r_idx, c_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = row_bg
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = cell.text_frame.paragraphs[0]
                p.text = str(val)
                p.font.size = Pt(10)
                p.font.color.rgb = C_DARK
                if c_idx == 0:
                    p.font.bold = True
                if val == "PASS":
                    p.font.color.rgb = C_SUCCESS
                    p.font.bold = True
                    p.alignment = PP_ALIGN.CENTER
                elif val == "FAIL":
                    p.font.color.rgb = C_DANGER
                    p.font.bold = True
                    p.alignment = PP_ALIGN.CENTER

        return tbl

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(15, 23, 42) # Slate 900
    bg1.line.fill.background()

    # Inner decorative border card
    inner_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    inner_card.fill.solid()
    inner_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    inner_card.line.color.rgb = C_ACCENT_BLUE
    inner_card.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "VISHWAKARMA INSTITUTE OF TECHNOLOGY, PUNE"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_ACCENT_BLUE
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf.add_paragraph()
    p1.text = "DEPARTMENT OF COMPUTER ENGINEERING | ACADEMIC YEAR 2026–2027"
    p1.font.size = Pt(11)
    p1.font.color.rgb = RGBColor(148, 163, 184)
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = "BANK MANAGEMENT SYSTEM (BMS)"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(20)

    p3 = tf.add_paragraph()
    p3.text = "Course Project in Software Engineering | End-to-End Analysis, Design, Testing & V&V"
    p3.font.size = Pt(15)
    p3.font.color.rgb = RGBColor(226, 232, 240)
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(8)

    p4 = tf.add_paragraph()
    p4.text = "Presented by: Student Team | TY B.Tech Computer Engineering\nGuided by: Faculty Mentor, Department of Computer Engineering"
    p4.font.size = Pt(12)
    p4.font.color.rgb = RGBColor(203, 213, 225)
    p4.alignment = PP_ALIGN.CENTER
    p4.space_before = Pt(36)

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & DOMAIN CONTEXT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "Executive Summary & Architectural Mission")
    
    # 3 Pillar Cards
    pillars = [
        ("Database-First Integrity", 
         "• Critical financial rules live inside MySQL 8.0 procedures & triggers.\n"
         "• Strict isolation of business logic from UI scripting.\n"
         "• Zero reliance on client-side validation alone.\n"
         "• Guaranteed rollback on constraint violations.", C_NAVY),
        ("ACID Concurrency Engine", 
         "• Strict InnoDB transaction isolation.\n"
         "• Ascending primary-key row locking (min ID, then max ID).\n"
         "• Zero deadlock vulnerabilities during reverse transfers.\n"
         "• Complete elimination of lost updates and race conditions.", C_ACCENT_BLUE),
        ("Role-Based Banking Portals", 
         "• 4 Isolated operational personas: Manager, Teller, Loan Officer, Clerk.\n"
         "• Streamlit dashboard with session authentication guards.\n"
         "• Immutable audit triggers tracking all financial movements.\n"
         "• Real-time analytical views and regulatory CSV export.", C_GOLD)
    ]
    for idx, (title, content, color) in enumerate(pillars):
        left = Inches(0.8 + idx * 4.0)
        card = add_card(s2, left, Inches(1.6), Inches(3.75), Inches(5.1))
        
        tb = s2.shapes.add_textbox(left + Inches(0.2), Inches(1.8), Inches(3.35), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = color
        
        p_c = tf.add_paragraph()
        p_c.text = content
        p_c.font.size = Pt(11)
        p_c.font.color.rgb = C_DARK
        p_c.space_before = Pt(12)

    # =========================================================================
    # SLIDE 3: ROADMAP & TABLE OF CONTENTS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "Presentation Roadmap & Topics Covered")

    agenda_items = [
        ("01", "Problem Statement & Objectives", "Financial domain bottlenecks & software engineering targets"),
        ("02", "Study of the Software Crisis", "Systemic causes, economic impact & TSB Bank Case Study"),
        ("03", "SDLC Models & Methodology", "Comparative analysis & justification of Hybrid Agile-V life cycle"),
        ("04", "Requirement Engineering", "Stakeholder elicitation, FR Matrix & NFR Quality Attributes"),
        ("05", "SRS & User Stories", "IEEE 830 specification & Given-When-Then acceptance criteria"),
        ("06", "UML Behavioral & Structural Models", "Use Case, Activity, Sequence & State Machine diagrams"),
        ("07", "Software Testing Strategies", "Equivalence Partitioning, BVA & White-Box Basis Path Testing"),
        ("08", "Software Maintenance & SLA", "Corrective, Adaptive, Perfective, Preventive & maintenance schedule"),
        ("09", "Risk Management & Git Control", "Quantitative 5x5 Risk Register & GitFlow release branch model"),
        ("10", "Verification, Validation & Wrap-Up", "Traceability Matrix (RTM), Defect Log, Project Roadmap & Conclusion")
    ]
    for idx, (num, title, desc) in enumerate(agenda_items):
        col = idx // 5
        row = idx % 5
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.6 + row * 1.05)
        
        add_card(s3, left, top, Inches(5.75), Inches(0.95))
        tb = s3.shapes.add_textbox(left + Inches(0.15), top + Inches(0.1), Inches(5.45), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{num}. {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 4: PROBLEM STATEMENT
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "Problem Statement: Challenges in Banking IT")

    problems = [
        ("Manual Overhead & Turnaround Latency", 
         "Paper slips and decentralized records slow down teller processing, resulting in queue congestion and human error in balances."),
        ("Concurrency Race Conditions & Lost Updates", 
         "Uncoordinated multi-teller withdrawals from identical accounts lead to ledger drift and unauthorized negative balances."),
        ("Deadlock Vulnerability in Reverse Transfers", 
         "Simultaneous transfers between Acc A and Acc B in opposing directions lock records out of order, freezing worker threads."),
        ("Audit Void & Insider Fraud Vulnerability", 
         "Lack of automated, immutable database-level logging prevents forensic non-repudiation when account balances are manipulated.")
    ]
    for idx, (title, desc) in enumerate(problems):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.6 + row * 2.6)
        
        add_card(s4, left, top, Inches(5.75), Inches(2.35))
        tb = s4.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.25), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_t = tf.paragraphs[0]
        p_t.text = f"❌ {title}"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = C_DANGER
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = C_DARK
        p_d.space_before = Pt(8)

    # =========================================================================
    # SLIDE 5: OBJECTIVES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "Software Engineering Objectives")

    objs = [
        ("Examine Financial Software Crises", "Analyze root causes of historical core banking outages and formulate defensive engineering controls."),
        ("Select & Justify Hybrid SDLC", "Design a life cycle pairing strict V-Model ledger verification with rapid Agile user interface sprints."),
        ("Elicit Multi-Stakeholder Requirements", "Structure functional and non-functional requirements across Managers, Tellers, Loan Officers, and Clerks."),
        ("Synthesize IEEE 830 SRS & Stories", "Author unambiguous specifications and testable Given-When-Then acceptance criteria."),
        ("Architect Complete UML Models", "Formalize system dynamics via Use Case, Activity, Sequence, and State Machine diagrams."),
        ("Design Exhaustive Test Suites", "Implement Black-Box (EP & BVA) and White-Box (Basis Path & Cyclomatic Complexity) suites."),
        ("Establish Maintenance & Risk Protocols", "Formulate proactive SLA plans, a 5x5 quantitative Risk Register, and a GitFlow release model.")
    ]
    for idx, (title, desc) in enumerate(objs):
        top = Inches(1.5 + idx * 0.78)
        add_card(s5, Inches(0.8), top, Inches(11.733), Inches(0.68))
        tb = s5.shapes.add_textbox(Inches(1.0), top + Inches(0.08), Inches(11.3), Inches(0.52))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        run_t = p.add_run()
        run_t.text = f"Objective {idx+1}: {title} — "
        run_t.bold = True
        run_t.font.size = Pt(11)
        run_t.font.color.rgb = C_NAVY
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.size = Pt(10.5)
        run_d.font.color.rgb = C_DARK

    # =========================================================================
    # SLIDE 6: STUDY OF THE SOFTWARE CRISIS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "Study of the Software Crisis in Financial Systems")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.5), bg_color=RGBColor(241, 245, 249))
    tb_def = s6.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.3), Inches(1.3))
    tf_def = tb_def.text_frame
    tf_def.word_wrap = True
    p_dt = tf_def.paragraphs[0]
    p_dt.text = "WHAT IS THE SOFTWARE CRISIS?"
    p_dt.font.size = Pt(13)
    p_dt.font.bold = True
    p_dt.font.color.rgb = C_NAVY
    p_dd = tf_def.add_paragraph()
    p_dd.text = "The software crisis refers to the chronic phenomenon where software projects exceed planned budgets and schedules, exhibit catastrophic runtime defects, fail user expectations, and resist maintainability. In banking, software crisis conditions lead to regulatory sanctions, institutional insolvency, and systemic contagion."
    p_dd.font.size = Pt(11)
    p_dd.space_before = Pt(4)

    # 3 manifestation cards
    manifestations = [
        ("Complexity Inversion", "Banking systems combine distributed ledgers, compliance constraints, and high concurrent workloads. Without modular decoupling, complexity spirals out of control.", C_DANGER),
        ("Testing Gaps Under Concurrency", "Verifying single-user happy paths fails to uncover deadlock traps and race conditions that emerge only during peak business transaction loads.", C_GOLD),
        ("Inadequate Traceability", "When regulatory rules are coded informally across disparate layers without traceability, bug fixes introduce cascading regressions.", C_NAVY)
    ]
    for idx, (t, d, c) in enumerate(manifestations):
        left = Inches(0.8 + idx * 4.0)
        add_card(s6, left, Inches(3.3), Inches(3.75), Inches(3.4))
        tb = s6.shapes.add_textbox(left + Inches(0.2), Inches(3.5), Inches(3.35), Inches(3.0))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = t
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = c
        pd = tf.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.space_before = Pt(8)

    # =========================================================================
    # SLIDE 7: CASE STUDY: TSB BANK OUTAGE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header(s7, "Case Study: The 2018 TSB Bank Migration Collapse")

    left_card = add_card(s7, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.1))
    tb_l = s7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.35), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p_lt = tf_l.paragraphs[0]
    p_lt.text = "INCIDENT SUMMARY & FALLOUT"
    p_lt.font.size = Pt(14)
    p_lt.font.bold = True
    p_lt.font.color.rgb = C_DANGER

    p_lc = tf_l.add_paragraph()
    p_lc.text = (
        "• Event: In April 2018, UK-based TSB Bank attempted to migrate 5.2 million customer records from its parent IT platform to 'Proteo4UK'.\n\n"
        "• Systemic Collapse: System failed immediately on cutover. 1.9M digital banking customers were locked out, accounts displayed other customers' financial records, and payroll transactions ground to a halt.\n\n"
        "• Economic Fallout: £330M+ in direct compensation, fraud remediation, and FCA regulatory fines. The bank Chief Executive was forced to resign."
    )
    p_lc.font.size = Pt(11)
    p_lc.space_before = Pt(8)

    right_card = add_card(s7, Inches(6.75), Inches(1.6), Inches(5.75), Inches(5.1))
    tb_r = s7.shapes.add_textbox(Inches(6.95), Inches(1.8), Inches(5.35), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_rt = tf_r.paragraphs[0]
    p_rt.text = "SOFTWARE ENGINEERING LESSONS"
    p_rt.font.size = Pt(14)
    p_rt.font.bold = True
    p_rt.font.color.rgb = C_NAVY

    p_rc = tf_r.add_paragraph()
    p_rc.text = (
        "1. Never Bypass Multi-User Concurrency Testing:\n"
        "TSB tested modules in isolation but failed to test end-to-end load concurrency across interconnected microservices.\n\n"
        "2. Strict Cutover & Rollback Protocols:\n"
        "Lack of an automated rollback mechanism left engineers unable to revert to the stable legacy ledger once anomalies were flagged.\n\n"
        "3. Database-Enforced Data Isolation:\n"
        "Customer record crosstalk demonstrated an absence of strict multi-tenant boundary checks in the query and persistence layer."
    )
    p_rc.font.size = Pt(11)
    p_rc.space_before = Pt(8)

    # =========================================================================
    # SLIDE 8: CAUSES & SOLUTIONS TABLE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header(s8, "Software Crisis: Causes & BMS Engineering Remedies")

    headers_s8 = ["Software Crisis Factor", "Banking Manifestation", "BMS Engineering Solution"]
    rows_s8 = [
        ["Ambiguous Business Rules", "Uncertainty whether min balance applies before fees", "Explicit SQL constraints & formal Given-When-Then criteria"],
        ["Concurrency Race Conditions", "Simultaneous withdrawals causing illegal negative balance", "InnoDB row locking & transactional boundaries (ACID)"],
        ["Deadlock Outages", "Reverse inter-account transfers locking worker threads", "Ascending primary-key lock ordering: min(id) then max(id)"],
        ["Audit Void", "Untracked administrative balance modifications", "Automated DB triggers writing immutable audit snapshots"],
        ["Disjointed Logic", "Client-side validation bypassed via direct API calls", "Database-first stored procedures encapsulating all moves"],
        ["Late Defect Discovery", "Bugs uncovered after deployment causing capital loss", "Continuous automated regression testing & V&V reviews"]
    ]
    add_table(s8, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), headers_s8, rows_s8,
              [Inches(2.6), Inches(4.5), Inches(4.633)])

    # =========================================================================
    # SLIDE 9: COMPARISON OF SDLC MODELS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_header(s9, "Comparative Analysis of SDLC Models")

    headers_s9 = ["SDLC Model", "Key Strengths", "Critical Limitations", "Suitability for Banking"]
    rows_s9 = [
        ["Waterfall", "Structured; clear stage gates & upfront documentation", "Inflexible to changes; testing deferred to the end", "Poor for interactive modern banking UIs"],
        ["V-Model", "Verification planned alongside every development phase", "High cost for change; rigid requirements lock-in", "Excellent for safety-critical ledger core"],
        ["Incremental", "Delivers operational functional chunks progressively", "Requires early comprehensive architecture vision", "Good for staggered release of services"],
        ["Spiral", "Risk-driven iterations; prototypes detect vulnerabilities early", "High management overhead; requires risk experts", "Suited for multi-million core bank re-writes"],
        ["Agile (Scrum)", "Rapid feedback loops; adapts to evolving needs", "Risk of documentation neglect and scope creep", "Ideal for customer dashboards and reports"]
    ]
    add_table(s9, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), headers_s9, rows_s9,
              [Inches(1.8), Inches(3.6), Inches(3.6), Inches(2.733)])

    # =========================================================================
    # SLIDE 10: SELECTED SDLC MODEL: HYBRID AGILE-V
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_header(s10, "Selected SDLC: Hybrid Agile-V Life Cycle")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.1), bg_color=RGBColor(241, 245, 249))
    tb_vl = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.35), Inches(4.7))
    tf_vl = tb_vl.text_frame
    tf_vl.word_wrap = True
    p_vt = tf_vl.paragraphs[0]
    p_vt.text = "CORE LEDGER LAYER: V-MODEL RIGOR"
    p_vt.font.size = Pt(14)
    p_vt.font.bold = True
    p_vt.font.color.rgb = C_NAVY

    p_vc = tf_vl.add_paragraph()
    p_vc.text = (
        "• Scope: 10-table 3NF relational schema, 17 transactional stored procedures, 5 audit triggers, and ACID fund movement.\n\n"
        "• Why V-Model? Financial ledger logic permits zero ambiguity. Every procedure requirement is directly mirrored by an automated verification acceptance test.\n\n"
        "• Deliverable: A mathematically verified, deadlock-free database kernel that rejects all balance violations."
    )
    p_vc.font.size = Pt(11)
    p_vc.space_before = Pt(8)

    add_card(s10, Inches(6.75), Inches(1.6), Inches(5.75), Inches(5.1), bg_color=RGBColor(254, 243, 199))
    tb_vr = s10.shapes.add_textbox(Inches(6.95), Inches(1.8), Inches(5.35), Inches(4.7))
    tf_vr = tb_vr.text_frame
    tf_vr.word_wrap = True
    p_at = tf_vr.paragraphs[0]
    p_at.text = "USER INTERFACE LAYER: AGILE SPRINTS"
    p_at.font.size = Pt(14)
    p_at.font.bold = True
    p_at.font.color.rgb = C_GOLD

    p_ac = tf_vr.add_paragraph()
    p_ac.text = (
        "• Scope: Streamlit multi-page portal, 4 RBAC role dashboards, interactive loan EMI calculators, Plotly visual charts, CSV reports.\n\n"
        "• Why Agile? Front-end workflows, form layouts, and teller usability benefit from rapid stakeholder reviews and 2-week iterations.\n\n"
        "• Deliverable: Intuitive, responsive web interfaces delivered and refined through continuous feedback."
    )
    p_ac.font.size = Pt(11)
    p_ac.space_before = Pt(8)

    # =========================================================================
    # SLIDE 11: 6-SPRINT DEVELOPMENT ROADMAP
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_slide_header(s11, "6-Sprint Iteration Plan & Milestones")

    headers_s11 = ["Sprint", "Focus Domain", "Primary Activities", "Verified Deliverables"]
    rows_s11 = [
        ["Sprint 1", "Database Core", "Design 10-table 3NF schema with constraints", "sql/01_schema.sql, DDL verified"],
        ["Sprint 2", "Transaction Engine", "Build 17 stored procedures with deadlock prevention", "sql/02_procedures.sql with lock ordering"],
        ["Sprint 3", "Auditing & Analytics", "Implement 5 audit triggers & 6 relational views", "sql/03_triggers_views.sql, seed data"],
        ["Sprint 4", "Auth & Teller Portal", "Build Streamlit RBAC login & deposit/transfer screens", "app/main.py, app/auth.py, Pages 1-4"],
        ["Sprint 5", "Loans, Cards & Reports", "Origination, live EMI calculator, card management", "Pages 5-8, CSV exports, Plotly charts"],
        ["Sprint 6", "QA, Testing & Signoff", "Execute acceptance test harness & V&V matrix", "run_acceptance_tests.py, Final Report"]
    ]
    add_table(s11, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), headers_s11, rows_s11,
              [Inches(1.5), Inches(2.4), Inches(4.3), Inches(3.533)])

    # =========================================================================
    # SLIDE 12: STAKEHOLDER REQUIREMENTS ELICITATION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_slide_header(s12, "Stakeholder Elicitation & Operational Needs")

    headers_s12 = ["Stakeholder Persona", "Operational Responsibilities", "Core Needs & Technical Pain Points"]
    rows_s12 = [
        ["Bank Manager", "Branch supervision, staffing, fee runs, compliance", "Real-time liquidity visibility, audit trail review, staff transfer controls"],
        ["Bank Teller", "Daily cash deposits, withdrawals, fund transfers", "Rapid balance enquiry, zero transfer errors, instant receipt generation"],
        ["Loan Officer", "Credit origination, application risk evaluation", "Automated EMI calculator, debt-to-income checks, disbursement workflow"],
        ["Bank Clerk", "Customer onboarding, KYC compliance, card issuance", "Input validation (age >= 18), PAN/Aadhaar deduplication, card freeze tool"],
        ["Compliance Auditor", "Regulatory inspection & forensic trail tracking", "Immutable audit log table, tamper-proof trigger execution, dormant account lists"]
    ]
    add_table(s12, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), headers_s12, rows_s12,
              [Inches(2.2), Inches(4.2), Inches(5.333)])

    # =========================================================================
    # SLIDE 13: FUNCTIONAL REQUIREMENTS MATRIX
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_slide_header(s13, "Functional Requirements (FR) Specification")

    headers_s13 = ["Req ID", "Functional Requirement Description", "Target Persona", "Implementation Engine"]
    rows_s13 = [
        ["FR-01", "Staff Authentication with salted hash & RBAC role assignment", "All Staff", "app/auth.py & session state"],
        ["FR-02", "Customer onboarding with mandatory KYC & age >= 18 check", "Clerk / Manager", "2_Customers.py & DB constraint"],
        ["FR-03", "Provision Savings, Current, and FD accounts with unique IDs", "Clerk / Teller", "sp_open_account procedure"],
        ["FR-04", "Enforce minimum balance rules (₹1,000 Savings; ₹5,000 Current)", "System Engine", "Stored procedure signal exception"],
        ["FR-05", "Execute atomic cash deposits & withdrawals adjusting balances", "Teller / Manager", "sp_deposit & sp_withdraw"],
        ["FR-06", "Atomic inter-account fund transfers with deadlock prevention", "Teller / Manager", "sp_transfer with ordered locks"],
        ["FR-07", "Loan application, amortization schedule & live EMI preview", "Loan Officer", "5_Loans.py & financial formulas"],
        ["FR-08", "Disburse approved loan principal directly to savings account", "Loan Officer", "sp_disburse_loan procedure"],
        ["FR-09", "Debit/Credit card issuance, monthly limits & instant freezing", "Clerk / Manager", "sp_issue_card & sp_block_card"],
        ["FR-10", "Trigger-based immutable audit trail for all balance modifications", "System Engine", "5 Database Triggers on tables"]
    ]
    add_table(s13, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), headers_s13, rows_s13,
              [Inches(1.2), Inches(5.333), Inches(2.2), Inches(3.0)])

    # =========================================================================
    # SLIDE 14: NON-FUNCTIONAL REQUIREMENTS
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_slide_header(s14, "Non-Functional Requirements & Quality Attributes")

    nfr_cards = [
        ("NFR-01: ACID Consistency", "Zero ledger drift. All fund movements enclosed in InnoDB transactions with rollback handlers on error.", C_NAVY),
        ("NFR-02: Performance & Latency", "Routine balance queries and deposits complete within < 500 ms; complex branch analytical reports within < 2 s.", C_ACCENT_BLUE),
        ("NFR-03: Security & RBAC", "Unauthorized URLs/pages redirect immediately; zero plaintext passwords; parameterized queries to block SQL injection.", C_DANGER),
        ("NFR-04: Data Integrity", "Enforced via foreign keys, unique national ID constraints, and DB-level CHECK (age >= 18).", C_GOLD),
        ("NFR-05: High Availability", "Connection pool automatically recovers from transient network drops without corrupting in-flight transactions.", C_SUCCESS),
        ("NFR-06: Full Auditability", "Every single balance modification generates an immutable, timestamped audit log row with user attribution.", C_DARK)
    ]
    for idx, (title, desc, color) in enumerate(nfr_cards):
        col = idx % 3
        row = idx // 3
        left = Inches(0.8 + col * 4.0)
        top = Inches(1.6 + row * 2.6)
        
        add_card(s14, left, top, Inches(3.75), Inches(2.35))
        tb = s14.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.35), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = color
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10.5)
        pd.space_before = Pt(8)

    # =========================================================================
    # SLIDE 15: SRS ARCHITECTURE & DESIGN
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_slide_header(s15, "Software Requirement Specification Architecture")

    arch_layers = [
        ("1. Presentation Layer (Streamlit)", 
         "• Multi-page application with role guards (app/main.py, app/pages/*.py)\n"
         "• Form validation, rupee formatting, and interactive Plotly visualization\n"
         "• Session state authentication preventing unauthenticated direct page access", C_ACCENT_BLUE),
        ("2. Data Access & Pool Layer (Python db.py)", 
         "• Connection pooling via mysql-connector-python\n"
         "• Exclusively executes parameterized queries (zero SQL injection vulnerabilities)\n"
         "• Passes user session identity to MySQL stored procedures for audit logging", C_GOLD),
        ("3. Core Persistence & Business Logic (MySQL 8.0 InnoDB)", 
         "• 10 normalized 3NF tables with strict primary/foreign key cascading rules\n"
         "• 17 Stored procedures handling atomic transfers, loan disbursements, and charges\n"
         "• 5 Triggers enforcing append-only immutable audit logging\n"
         "• 6 Analytical views driving executive reports without expensive ad-hoc joins", C_NAVY)
    ]
    for idx, (title, content, color) in enumerate(arch_layers):
        top = Inches(1.6 + idx * 1.7)
        add_card(s15, Inches(0.8), top, Inches(11.733), Inches(1.5))
        tb = s15.shapes.add_textbox(Inches(1.1), top + Inches(0.15), Inches(11.2), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = color
        pd = tf.add_paragraph()
        pd.text = content
        pd.font.size = Pt(10.5)
        pd.space_before = Pt(4)

    # =========================================================================
    # SLIDE 16: USER STORIES: TRANSFER & ONBOARDING
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_slide_header(s16, "User Stories & Acceptance Criteria: Core Flows")

    # Left: Transfer
    add_card(s16, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.1))
    tb_u1 = s16.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.35), Inches(4.7))
    tf_u1 = tb_u1.text_frame
    tf_u1.word_wrap = True
    p_u1t = tf_u1.paragraphs[0]
    p_u1t.text = "USER STORY 1: ATOMIC FUND TRANSFER"
    p_u1t.font.size = Pt(13)
    p_u1t.font.bold = True
    p_u1t.font.color.rgb = C_NAVY
    p_u1n = tf_u1.add_paragraph()
    p_u1n.text = "As a Teller, I want to transfer funds between accounts atomically so that neither account experiences ledger drift."
    p_u1n.font.size = Pt(10.5)
    p_u1n.font.italic = True
    p_u1n.space_before = Pt(4)

    p_u1c = tf_u1.add_paragraph()
    p_u1c.text = (
        "Acceptance Criteria:\n"
        "• Given valid source balance >= (min_bal + amount), when submitted, debits source, credits destination, and commits.\n"
        "• Given transfer amount violating min balance, when submitted, transaction rolls back with error 'Insufficient balance'.\n"
        "• Given simultaneous reverse transfers, locks are acquired in ascending order (min ID first) to prevent deadlocks.\n"
        "• Given frozen source or receiver, aborts immediately."
    )
    p_u1c.font.size = Pt(10)
    p_u1c.space_before = Pt(8)

    # Right: Onboarding
    add_card(s16, Inches(6.75), Inches(1.6), Inches(5.75), Inches(5.1))
    tb_u2 = s16.shapes.add_textbox(Inches(6.95), Inches(1.8), Inches(5.35), Inches(4.7))
    tf_u2 = tb_u2.text_frame
    tf_u2.word_wrap = True
    p_u2t = tf_u2.paragraphs[0]
    p_u2t.text = "USER STORY 2: CUSTOMER ONBOARDING"
    p_u2t.font.size = Pt(13)
    p_u2t.font.bold = True
    p_u2t.font.color.rgb = C_ACCENT_BLUE
    p_u2n = tf_u2.add_paragraph()
    p_u2n.text = "As a Clerk, I want to register customer profiles with mandatory KYC details so that accounts comply with statutory laws."
    p_u2n.font.size = Pt(10.5)
    p_u2n.font.italic = True
    p_u2n.space_before = Pt(4)

    p_u2c = tf_u2.add_paragraph()
    p_u2c.text = (
        "Acceptance Criteria:\n"
        "• Given valid inputs and DOB proving age >= 18, when submitted, customer created with status PENDING KYC.\n"
        "• Given date of birth showing age < 18, when submitted, rejected with 'Customer must be at least 18 years old'.\n"
        "• Given duplicate Aadhaar/PAN, unique DB constraint blocks insertion and raises an alert.\n"
        "• Given missing email or phone, submission blocked."
    )
    p_u2c.font.size = Pt(10)
    p_u2c.space_before = Pt(8)

    # =========================================================================
    # SLIDE 17: USER STORIES: LOANS & AUDIT
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_slide_header(s17, "User Stories & Acceptance Criteria: Loans & Audit")

    # Left: Loans
    add_card(s17, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.1))
    tb_u3 = s17.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.35), Inches(4.7))
    tf_u3 = tb_u3.text_frame
    tf_u3.word_wrap = True
    p_u3t = tf_u3.paragraphs[0]
    p_u3t.text = "USER STORY 3: LOAN ORIGINATION & EMI"
    p_u3t.font.size = Pt(13)
    p_u3t.font.bold = True
    p_u3t.font.color.rgb = C_GOLD
    p_u3n = tf_u3.add_paragraph()
    p_u3n.text = "As a Loan Officer, I want to compute live amortized EMI and approve loans so that principal is credited securely."
    p_u3n.font.size = Pt(10.5)
    p_u3n.font.italic = True
    p_u3n.space_before = Pt(4)

    p_u3c = tf_u3.add_paragraph()
    p_u3c.text = (
        "Acceptance Criteria:\n"
        "• Given principal P, interest r, tenure n, calculates monthly EMI via: [P * r * (1+r)^n] / [(1+r)^n - 1].\n"
        "• Given loan in APPLIED status, Officer can transition it to APPROVED or REJECTED with notes.\n"
        "• Given APPROVED loan, disbursement credits principal into the customer savings account and logs ledger transaction.\n"
        "• Rejects disbursement if customer account is closed/frozen."
    )
    p_u3c.font.size = Pt(10)
    p_u3c.space_before = Pt(8)

    # Right: Audit
    add_card(s17, Inches(6.75), Inches(1.6), Inches(5.75), Inches(5.1))
    tb_u4 = s17.shapes.add_textbox(Inches(6.95), Inches(1.8), Inches(5.35), Inches(4.7))
    tf_u4 = tb_u4.text_frame
    tf_u4.word_wrap = True
    p_u4t = tf_u4.paragraphs[0]
    p_u4t.text = "USER STORY 4: IMMUTABLE AUDIT TRAILS"
    p_u4t.font.size = Pt(13)
    p_u4t.font.bold = True
    p_u4t.font.color.rgb = C_DARK
    p_u4n = tf_u4.add_paragraph()
    p_u4n.text = "As a Manager / Compliance Auditor, I want an append-only audit trail so that all financial actions are verifiable."
    p_u4n.font.size = Pt(10.5)
    p_u4n.font.italic = True
    p_u4n.space_before = Pt(4)

    p_u4c = tf_u4.add_paragraph()
    p_u4c.text = (
        "Acceptance Criteria:\n"
        "• Given any UPDATE to accounts.balance, database trigger trg_account_balance_audit fires automatically.\n"
        "• Log records old balance, new balance, changed_by employee ID, and UTC timestamp.\n"
        "• Application users are restricted from executing DELETE or UPDATE on audit_log.\n"
        "• Manager reports display filterable audit records."
    )
    p_u4c.font.size = Pt(10)
    p_u4c.space_before = Pt(8)

    # =========================================================================
    # SLIDE 18: UML USE CASE DIAGRAM
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_slide_header(s18, "UML Modeling: Use Case Architecture & RBAC")

    headers_s18 = ["Actor Role", "Authorized Use Cases (Direct Responsibilities)", "Access Boundary Rationale"]
    rows_s18 = [
        ["Bank Clerk", "UC-01: Authenticate\nUC-02: Register Customer (Age >= 18)\nUC-03: Open Accounts\nUC-04: Issue / Block Cards", "Handles front-desk onboarding; isolated from loan approvals and money transfers."],
        ["Bank Teller", "UC-01: Authenticate\nUC-05: Deposit Cash\nUC-06: Withdraw Cash\nUC-07: Inter-Account Transfer\nUC-08: Balance Enquiry", "Executes ledger transactions; restricted from approving loans or changing staff roles."],
        ["Loan Officer", "UC-01: Authenticate\nUC-09: Originate Loan Application\nUC-10: Review / Approve Loan\nUC-11: Disburse Loan Principal", "Evaluates credit risk and disbursements; isolated from teller cash drawers."],
        ["Bank Manager", "Inherits ALL Use Cases (UC-01 through UC-11)\nUC-12: Employee Staff Hiring / Transfer\nUC-13: Execute Monthly Interest Run\nUC-14: Audit Trail Inspection", "Complete administrative supremacy across branch liquidity, staff, and regulatory auditing."]
    ]
    add_table(s18, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), headers_s18, rows_s18,
              [Inches(2.0), Inches(4.8), Inches(4.933)])

    # =========================================================================
    # SLIDE 19: UML ACTIVITY DIAGRAM: FUND TRANSFER
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_slide_header(s19, "UML Activity Diagram: Atomic Transfer Logic")

    steps = [
        ("1. Input & Validation", "Teller submits from_acc, to_acc, and transfer amount. Checks amount > 0 and from != to.", C_NAVY),
        ("2. Ordered Locking", "Deterministic row locking: locks min(from_id, to_id) first, preventing reverse transfer deadlocks.", C_ACCENT_BLUE),
        ("3. Account Health Check", "Inspects status of both accounts. If either is FROZEN or CLOSED, rolls back transaction.", C_DANGER),
        ("4. Solvency Verification", "Verifies: (Sender Balance - Amount) >= Minimum Balance. If violated, executes ROLLBACK.", C_GOLD),
        ("5. Atomic Ledger Update", "Debits sender balance, credits receiver balance, inserts transaction row, and triggers write audit log.", C_SUCCESS),
        ("6. Commit & Receipt", "Executes COMMIT transaction; UI renders formatted transfer confirmation receipt with transaction ID.", C_DARK)
    ]
    for idx, (title, desc, color) in enumerate(steps):
        col = idx % 3
        row = idx // 3
        left = Inches(0.8 + col * 4.0)
        top = Inches(1.6 + row * 2.6)
        
        add_card(s19, left, top, Inches(3.75), Inches(2.35))
        tb = s19.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.35), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = color
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10.5)
        pd.space_before = Pt(8)

    # =========================================================================
    # SLIDE 20: UML SEQUENCE DIAGRAM: LOAN DISBURSEMENT
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_slide_header(s20, "UML Sequence Diagram: Loan Disbursement Flow")

    seq_steps = [
        ("1. Loan Officer -> Streamlit UI", "Selects approved loan ID and clicks 'Disburse Principal to Customer'"),
        ("2. Streamlit UI -> Database Pool", "Invokes db.execute_procedure('sp_disburse_loan', [loan_id, officer_id])"),
        ("3. DB Engine -> loans Table", "Starts transaction: SELECT * FROM loans WHERE loan_id = ? FOR UPDATE"),
        ("4. Stored Procedure Decision", "Checks if status == 'APPROVED'. If not, signals SQL exception 45000 and rolls back"),
        ("5. DB Engine -> accounts Table", "Executes: UPDATE accounts SET balance = balance + principal WHERE account_id = ?"),
        ("6. DB Engine -> audit_log", "Triggers fire automatically to record balance snapshot and loan status transition"),
        ("7. DB Engine -> COMMIT", "Commits transaction atomically and returns success status code"),
        ("8. UI -> Loan Officer", "Streamlit displays success confirmation badge and updated ledger statement")
    ]
    for idx, (actor_msg, detail) in enumerate(seq_steps):
        top = Inches(1.5 + idx * 0.68)
        add_card(s20, Inches(0.8), top, Inches(11.733), Inches(0.6))
        tb = s20.shapes.add_textbox(Inches(1.0), top + Inches(0.06), Inches(11.3), Inches(0.48))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"Step {idx+1}: {actor_msg} — "
        r1.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = detail
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_DARK

    # =========================================================================
    # SLIDE 21: UML STATE MACHINE: ACCOUNT LIFECYCLE
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_slide_header(s21, "UML State Machine: Bank Account Lifecycle")

    states = [
        ("PENDING_APPROVAL", "Trigger: Customer registers profile.\nCondition: Awaiting KYC verification.\nAllowed: Form edit, document upload.\nBlocked: All financial withdrawals/deposits.", C_GOLD),
        ("ACTIVE (Fully Operational)", "Trigger: KYC verified & initial min deposit paid.\nCondition: Account is solvent.\nAllowed: Deposits, withdrawals, transfers, interest.\nSub-states: Idle, Debited, Credited.", C_SUCCESS),
        ("FROZEN (Restricted)", "Trigger: Suspicious fraud, court order, or 12M inactivity.\nCondition: Account locked by Manager.\nAllowed: Balance enquiry, incoming court review.\nBlocked: Outgoing transfers, card spends.", C_DANGER),
        ("CLOSED (Terminal State)", "Trigger: Customer requests closure.\nCondition: Balance liquidated to exactly ₹0.00.\nAllowed: Archival reporting only.\nBlocked: All operations permanently disabled.", C_DARK)
    ]
    for idx, (title, content, color) in enumerate(states):
        left = Inches(0.8 + idx * 3.0)
        add_card(s21, left, Inches(1.6), Inches(2.75), Inches(5.1))
        tb = s21.shapes.add_textbox(left + Inches(0.15), Inches(1.8), Inches(2.45), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = color
        pd = tf.add_paragraph()
        pd.text = content
        pd.font.size = Pt(10)
        pd.space_before = Pt(10)

    # =========================================================================
    # SLIDE 22: TESTING: EQUIVALENCE PARTITIONING
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_slide_header(s22, "Black-Box Testing: Equivalence Partitioning (EP)")

    add_card(s22, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.8), bg_color=RGBColor(241, 245, 249))
    tb_rule = s22.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.3), Inches(0.7))
    tf_rule = tb_rule.text_frame
    tf_rule.word_wrap = True
    pr = tf_rule.paragraphs[0]
    pr.text = "TEST SPECIFICATION — CASH WITHDRAWAL MODULE"
    pr.font.size = Pt(11)
    pr.font.bold = True
    pr.font.color.rgb = C_NAVY
    prd = tf_rule.add_paragraph()
    prd.text = "Account Type: Savings Account | Current Balance: ₹10,000 | Mandatory Minimum Balance: ₹1,000 | Valid Range: ₹100 to ₹9,000"
    prd.font.size = Pt(10)

    headers_s22 = ["Test ID", "Equivalence Partition Class", "Representative Input", "Expected System Action", "Actual Status"]
    rows_s22 = [
        ["EP-W01", "Valid Withdrawal Range (₹100 to ₹9,000)", "₹2,500", "Debits ₹2,500; New Balance ₹7,500; Transaction commits", "PASS"],
        ["EP-W02", "Zero or Negative Amount", "-₹500", "Reject with exception 'Withdrawal amount must be positive'", "PASS"],
        ["EP-W03", "Amount Violating Minimum Balance", "₹9,500 (Leaves ₹500)", "Reject with exception 'Insufficient funds below minimum balance'", "PASS"],
        ["EP-W04", "Amount Exceeding Entire Balance", "₹15,000", "Reject with exception 'Insufficient funds'", "PASS"],
        ["EP-W05", "Withdrawal from Non-Active Account", "₹1,000 (FROZEN)", "Reject with exception 'Account is FROZEN'", "PASS"]
    ]
    add_table(s22, Inches(0.8), Inches(2.5), Inches(11.733), Inches(4.3), headers_s22, rows_s22,
              [Inches(1.4), Inches(3.2), Inches(2.0), Inches(4.133), Inches(1.0)])

    # =========================================================================
    # SLIDE 23: TESTING: BOUNDARY VALUE ANALYSIS
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_slide_header(s23, "Black-Box Testing: Boundary Value Analysis (BVA)")

    headers_s23 = ["Test ID", "Boundary Condition Tested", "Input Value", "Expected Result & Balance Validation", "Status"]
    rows_s23 = [
        ["BVA-W01", "Just below minimum chunk (Min - 1)", "₹99", "Reject: Below minimum single transaction threshold", "PASS"],
        ["BVA-W02", "Exactly at minimum chunk (Min)", "₹100", "Accept: Balance debited to ₹9,900; Transaction commits", "PASS"],
        ["BVA-W03", "Just above minimum chunk (Min + 1)", "₹101", "Accept: Balance debited to ₹9,899; Transaction commits", "PASS"],
        ["BVA-W04", "Just below maximum limit (Max - 1)", "₹8,999", "Accept: Leaves ₹1,001 (Validly above ₹1,000 min balance)", "PASS"],
        ["BVA-W05", "Exactly at maximum limit (Max)", "₹9,000", "Accept: Leaves exactly ₹1,000 (Satisfies exact boundary)", "PASS"],
        ["BVA-W06", "Just above maximum limit (Max + 1)", "₹9,001", "Reject: Leaves ₹999 (Violates ₹1,000 minimum balance rule)", "PASS"]
    ]
    add_table(s23, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), headers_s23, rows_s23,
              [Inches(1.4), Inches(3.3), Inches(1.5), Inches(4.533), Inches(1.0)])

    # =========================================================================
    # SLIDE 24: TESTING: WHITE-BOX BASIS PATH TESTING
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_slide_header(s24, "White-Box Testing: Basis Path & Cyclomatic Complexity")

    # Left: Formula & CFG
    add_card(s24, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.1))
    tb_cfg = s24.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.1), Inches(4.7))
    tf_cfg = tb_cfg.text_frame
    tf_cfg.word_wrap = True
    pt = tf_cfg.paragraphs[0]
    pt.text = "CYCLOMATIC COMPLEXITY"
    pt.font.size = Pt(13)
    pt.font.bold = True
    pt.font.color.rgb = C_NAVY

    pd = tf_cfg.add_paragraph()
    pd.text = (
        "McCabe's Formula:\n"
        "V(G) = P + 1 = E - N + 2\n\n"
        "Predicate Nodes (P = 4):\n"
        "1. amount <= 0\n"
        "2. from_id == to_id\n"
        "3. from_status != 'ACTIVE' OR to_status != 'ACTIVE'\n"
        "4. (balance - amount) < min_balance\n\n"
        "Calculated Complexity:\n"
        "V(G) = 4 + 1 = 5 Independent Paths"
    )
    pd.font.size = Pt(10.5)
    pd.space_before = Pt(8)

    # Right: Paths table
    headers_s24 = ["Basis Path", "Control Decisions Traversed", "Test Input Conditions", "Expected Outcome"]
    rows_s24 = [
        ["Path 1", "Decision 1 -> True", "amount = -500", "Rejects: Invalid negative amount"],
        ["Path 2", "Decision 1 -> False; Decision 2 -> True", "from_id = 101, to_id = 101", "Rejects: Self-transfer forbidden"],
        ["Path 3", "Dec 1, 2 -> False; Decision 3 -> True", "from_status = 'FROZEN'", "Rejects: Account not in active state"],
        ["Path 4", "Dec 1, 2, 3 -> False; Decision 4 -> True", "from_balance = 1200, amount = 500", "Rejects: Minimum balance breach"],
        ["Path 5", "All Decisions -> False (Happy Path)", "from_balance = 5000, amount = 1000", "Executes atomic transfer & commits"]
    ]
    add_table(s24, Inches(5.5), Inches(1.6), Inches(7.033), Inches(5.1), headers_s24, rows_s24,
              [Inches(1.2), Inches(2.2), Inches(2.1), Inches(1.533)])

    # =========================================================================
    # SLIDE 25: SOFTWARE MAINTENANCE
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_slide_header(s25, "Software Maintenance Planning & SLA Schedule")

    headers_s25 = ["Maintenance Class", "Engineering Objective", "Practical BMS Application Scenario", "SLA Frequency"]
    rows_s25 = [
        ["Corrective Maintenance", "Diagnose and repair defects uncovered in runtime production", "Fixing fractional paisa rounding errors during interest runs", "Immediate / Hotfix"],
        ["Adaptive Maintenance", "Modify software to comply with changing external laws & OS", "Updating TDS withholding tax tables per revised Reserve Bank rules", "Monthly / Scheduled"],
        ["Perfective Maintenance", "Enhance performance, UI convenience, and query speeds", "Adding composite index on transactions(account_id, created_at)", "Quarterly Release"],
        ["Preventive Maintenance", "Refactor complex modules & patch libraries before failures", "Upgrading mysql-connector-python & archiving old audit logs", "Bi-Annual Review"]
    ]
    add_table(s25, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), headers_s25, rows_s25,
              [Inches(2.2), Inches(3.6), Inches(4.333), Inches(1.6)])

    # =========================================================================
    # SLIDE 26: RISK MANAGEMENT: 5X5 MATRIX
    # =========================================================================
    s26 = prs.slides.add_slide(blank_layout)
    add_slide_header(s26, "Risk Management: Quantitative 5x5 Risk Register")

    headers_s26 = ["Risk ID", "Risk Description", "Prob (1-5)", "Imp (1-5)", "Score", "Mitigation Strategy"]
    rows_s26 = [
        ["R-01", "Concurrent Transfer Deadlocks", "3", "5", "15 (High)", "Deterministic ascending primary-key row locking in SQL"],
        ["R-02", "Credential & Role Escalation", "2", "5", "10 (High)", "Strict session guards in app/auth.py & page-level checks"],
        ["R-03", "Ledger Inconsistency on Server Crash", "2", "5", "10 (High)", "InnoDB write-ahead redo logging & automatic rollback"],
        ["R-04", "SQL Injection Attacks", "2", "5", "10 (High)", "Exclusive parameterized queries; zero string concatenation"],
        ["R-05", "Underage Customer Onboarding", "3", "4", "12 (High)", "Dual validation: front-end calendar + MySQL CHECK (age >= 18)"],
        ["R-06", "Database Storage Corruption", "2", "5", "10 (High)", "Automated daily logical mysqldump to cold encrypted storage"]
    ]
    add_table(s26, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), headers_s26, rows_s26,
              [Inches(1.1), Inches(3.3), Inches(1.1), Inches(1.1), Inches(1.3), Inches(3.833)])

    # =========================================================================
    # SLIDE 27: VERSION CONTROL & GITFLOW
    # =========================================================================
    s27 = prs.slides.add_slide(blank_layout)
    add_slide_header(s27, "Configuration Management: GitFlow Strategy")

    git_steps = [
        ("main (Production Releases)", "Protected branch containing only signed, production-ready code (e.g. tag v1.0.0). Direct pushes strictly prohibited.", C_NAVY),
        ("develop (Integration Branch)", "Staging trunk where verified feature branches merge. Subjected to automated test harness before release.", C_ACCENT_BLUE),
        ("feature/sql-schema-3nf", "Isolated branch for establishing normalized tables, foreign keys, and age/balance constraints.", C_GOLD),
        ("feature/stored-procedures-acid", "Isolated branch for developing 17 stored procedures with deadlock-prevention lock ordering.", C_SUCCESS),
        ("feature/streamlit-rbac-ui", "Sprint branch for developing multi-page role views, auth guards, and Plotly dashboards.", C_DARK),
        ("bugfix/deadlock-lock-order", "Rapid-response hotfix branch to resolve race conditions identified during concurrent load testing.", C_DANGER)
    ]
    for idx, (branch, desc, color) in enumerate(git_steps):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.6 + row * 1.7)
        
        add_card(s27, left, top, Inches(5.75), Inches(1.5))
        tb = s27.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.35), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = branch
        pt.font.size = Pt(12.5)
        pt.font.bold = True
        pt.font.color.rgb = color
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.space_before = Pt(4)

    # =========================================================================
    # SLIDE 28: VERIFICATION & VALIDATION (RTM & DEFECT LOG)
    # =========================================================================
    s28 = prs.slides.add_slide(blank_layout)
    add_slide_header(s28, "Verification & Validation: RTM & Defect Log")

    # Top: RTM Summary
    add_card(s28, Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.4))
    tb_rtm = s28.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(2.1))
    tf_rtm = tb_rtm.text_frame
    tf_rtm.word_wrap = True
    pt = tf_rtm.paragraphs[0]
    pt.text = "REQUIREMENTS TRACEABILITY MATRIX (RTM) SUMMARY"
    pt.font.size = Pt(12)
    pt.font.bold = True
    pt.font.color.rgb = C_NAVY
    pd = tf_rtm.add_paragraph()
    pd.text = (
        "• FR-01 (Auth & RBAC) -> Mapped to app/auth.py -> Verified by TC-AUTH-01 & TC-AUTH-02 [STATUS: VERIFIED]\n"
        "• FR-02 (Customer 18+) -> Mapped to sql/01_schema.sql -> Verified by TC-CUST-01 [STATUS: VERIFIED]\n"
        "• FR-04 (Min Balance) -> Mapped to sp_withdraw -> Verified by TC-TXN-01 & TC-TXN-02 [STATUS: VERIFIED]\n"
        "• FR-06 (Atomic Transfer) -> Mapped to sp_transfer -> Verified by TC-TXN-03 & TC-TXN-04 [STATUS: VERIFIED]\n"
        "• FR-10 (Audit Triggers) -> Mapped to sql/03_triggers_views.sql -> Verified by TC-AUD-01 [STATUS: VERIFIED]"
    )
    pd.font.size = Pt(10)
    pd.space_before = Pt(4)

    # Bottom: Defect Log
    headers_s28 = ["Defect ID", "Severity", "Defect Description", "Root Cause", "Corrective Action Implemented"]
    rows_s28 = [
        ["DF-01", "Critical", "Concurrency deadlock under simultaneous reverse transfers", "Arbitrary row lock order in sp_transfer", "Enforced ascending primary key ordering: min(id) then max(id)"],
        ["DF-02", "Major", "Customer under 18 accepted if birth year entered wrong", "Missing database-level check constraint", "Added DB CHECK (TIMESTAMPDIFF(YEAR, dob, CURDATE()) >= 18)"],
        ["DF-03", "Moderate", "Division-by-zero error on empty branch analytics screen", "SQL view lacked COALESCE on aggregate sums", "Updated vw_branch_summary with COALESCE(SUM(balance), 0.00)"]
    ]
    add_table(s28, Inches(0.8), Inches(4.1), Inches(11.733), Inches(2.6), headers_s28, rows_s28,
              [Inches(1.2), Inches(1.2), Inches(3.5), Inches(2.8), Inches(3.033)])

    # =========================================================================
    # SLIDE 29: CONCLUSION & KEY TAKEAWAYS
    # =========================================================================
    s29 = prs.slides.add_slide(blank_layout)
    bg29 = s29.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg29.fill.solid()
    bg29.fill.fore_color.rgb = RGBColor(15, 23, 42)
    bg29.line.fill.background()

    inner29 = s29.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    inner29.fill.solid()
    inner29.fill.fore_color.rgb = RGBColor(30, 41, 59)
    inner29.line.color.rgb = C_ACCENT_BLUE
    inner29.line.width = Pt(1.5)

    tb29 = s29.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(11), Inches(5.2))
    tf29 = tb29.text_frame
    tf29.word_wrap = True

    p0 = tf29.paragraphs[0]
    p0.text = "CONCLUSION & ENGINEERING SUMMARY"
    p0.font.size = Pt(22)
    p0.font.bold = True
    p0.font.color.rgb = C_WHITE
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf29.add_paragraph()
    p1.text = (
        "1. Rigorous Software Engineering Prevents Financial Crisis:\n"
        "Ambiguous rules and unverified concurrency are catastrophic in banking. Upfront formal specifications and systematic testing eliminate systemic risks.\n\n"
        "2. The Hybrid Agile-V Model Delivers Optimal Balance:\n"
        "V-Model guarantees zero ledger drift and mathematical correctness in the core database procedures, while Agile sprints provide high usability and rapid refinement for the Streamlit web portals.\n\n"
        "3. Multi-Tier Verification Ensures Production Dependability:\n"
        "Equivalence Partitioning, Boundary Value Analysis, Basis Path Testing (V(G)=5), and automated Requirements Traceability (RTM) confirm that every banking invariant is fully verified."
    )
    p1.font.size = Pt(11)
    p1.font.color.rgb = RGBColor(226, 232, 240)
    p1.space_before = Pt(16)

    p2 = tf29.add_paragraph()
    p2.text = "THANK YOU! | QUESTIONS & DEMONSTRATION"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = C_ACCENT_BLUE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(24)

    # Save Presentation
    output_path = os.path.abspath("Bank_Management_System_Software_Engineering_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_deck()
