"""
Enhanced Generator for the Bank Management System Software Engineering Presentation.
Features:
- Animated transitions on all 29 slides (fade, push, wipe, split, cover).
- Vibrant, executive color scheme (Sapphire, Electric Blue, Emerald Green, Amber Gold, Coral Red, Royal Violet).
- Balanced card layouts with zero awkward whitespace:
  - Header strips with category tags
  - Well-sized typography (12-14pt body, 15-18pt headings)
  - Bottom callout badges / metrics to fill cards naturally
  - Clean table formatting with alternating rows and colored status pills
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

def create_enhanced_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Vibrant Theme Palette
    C_NAVY_DARK    = RGBColor(11, 25, 44)       # Deep Obsidian Navy
    C_SLATE_BG     = RGBColor(241, 245, 249)    # Clean Light Slate
    C_WHITE        = RGBColor(255, 255, 255)
    C_TEXT_DARK    = RGBColor(15, 23, 42)       # Slate 900
    C_TEXT_MUTED   = RGBColor(100, 116, 139)    # Slate 500

    # Accent Colors
    C_SAPPHIRE     = RGBColor(30, 58, 138)      # Blue 900
    C_BLUE         = RGBColor(37, 99, 235)      # Blue 600
    C_EMERALD      = RGBColor(5, 150, 105)      # Emerald 600
    C_AMBER        = RGBColor(217, 119, 6)      # Amber 600
    C_CRIMSON      = RGBColor(220, 38, 38)      # Red 600
    C_PURPLE       = RGBColor(124, 58, 237)     # Violet 600
    C_TEAL         = RGBColor(13, 148, 136)     # Teal 600

    # Soft Pastel Card Backgrounds
    BG_BLUE        = RGBColor(239, 246, 255)    # Blue 50
    BG_GREEN       = RGBColor(236, 253, 245)    # Emerald 50
    BG_AMBER       = RGBColor(255, 251, 235)    # Amber 50
    BG_RED         = RGBColor(254, 242, 242)    # Red 50
    BG_PURPLE      = RGBColor(245, 243, 255)    # Violet 50
    BG_TEAL        = RGBColor(240, 253, 250)    # Teal 50
    BG_WHITE       = RGBColor(255, 255, 255)

    transitions = [
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="fast"><p:fade/></p:transition>',
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="fast"><p:push dir="l"/></p:transition>',
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="fast"><p:wipe dir="r"/></p:transition>',
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="fast"><p:split out="horz"/></p:transition>',
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="fast"><p:cover dir="l"/></p:transition>',
    ]

    def add_slide_with_transition(idx):
        slide = prs.slides.add_slide(blank_layout)
        trans_xml = transitions[idx % len(transitions)]
        slide._element.append(parse_xml(trans_xml))
        return slide

    def render_header(slide, title_text, category_tag="SOFTWARE ENGINEERING PROJECT", accent_color=C_BLUE):
        """Draws a crisp, vibrant header banner with category badge."""
        # Top color accent stripe
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = accent_color
        top_bar.line.fill.background()

        # Category Badge Pill
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.32), Inches(3.2), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = accent_color
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
        p_b = tf_b.paragraphs[0]
        p_b.text = category_tag.upper()
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = C_WHITE
        p_b.alignment = PP_ALIGN.CENTER

        # Slide Main Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.65))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_DARK

    def render_card(slide, left, top, width, height, title, items, 
                    accent_color=C_BLUE, bg_color=BG_WHITE, footer_badge=None, title_size=Pt(14), body_size=Pt(11)):
        """Renders an attractive, well-proportioned card with header, body items, and optional footer badge."""
        # Outer Card Container
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = accent_color
        card.line.width = Pt(1.5)

        # Header Strip inside card
        header_bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.55))
        header_bar.fill.solid()
        header_bar.fill.fore_color.rgb = accent_color
        header_bar.line.fill.background()
        tf_h = header_bar.text_frame
        tf_h.margin_left = Inches(0.2)
        tf_h.margin_top = Inches(0.08)
        p_h = tf_h.paragraphs[0]
        p_h.text = title
        p_h.font.size = title_size
        p_h.font.bold = True
        p_h.font.color.rgb = C_WHITE

        # Content Box - sized properly to eliminate empty void
        content_top = top + Inches(0.65)
        content_height = height - Inches(1.15) if footer_badge else height - Inches(0.75)
        tb_c = slide.shapes.add_textbox(left + Inches(0.2), content_top, width - Inches(0.4), content_height)
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

        for idx, itm in enumerate(items):
            p = tf_c.paragraphs[0] if idx == 0 else tf_c.add_paragraph()
            p.text = f"• {itm}"
            p.font.size = body_size
            p.font.color.rgb = C_TEXT_DARK
            p.space_before = Pt(5)
            p.line_spacing = 1.15

        # Footer Badge if provided
        if footer_badge:
            f_badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), top + height - Inches(0.45), width - Inches(0.4), Inches(0.35))
            f_badge.fill.solid()
            f_badge.fill.fore_color.rgb = accent_color
            f_badge.line.fill.background()
            tf_f = f_badge.text_frame
            tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
            pf = tf_f.paragraphs[0]
            pf.text = footer_badge.upper()
            pf.font.size = Pt(9.5)
            pf.font.bold = True
            pf.font.color.rgb = C_WHITE
            pf.alignment = PP_ALIGN.CENTER

    def render_table(slide, left, top, width, height, headers, rows_data, col_widths=None, header_bg=C_NAVY_DARK):
        """Renders high-contrast, professional tables with styled headers and status pills."""
        num_rows = len(rows_data) + 1
        num_cols = len(headers)
        tbl_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
        tbl = tbl_shape.table

        if col_widths and len(col_widths) == num_cols:
            for idx, w in enumerate(col_widths):
                tbl.columns[idx].width = w

        # Header Row
        for idx, text in enumerate(headers):
            cell = tbl.cell(0, idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = header_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.alignment = PP_ALIGN.CENTER
            p.font.bold = True
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_WHITE

        # Data Rows
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
                p.font.color.rgb = C_TEXT_DARK
                if c_idx == 0:
                    p.font.bold = True
                if val == "PASS":
                    p.font.color.rgb = C_EMERALD
                    p.font.bold = True
                    p.alignment = PP_ALIGN.CENTER
                elif val == "FAIL":
                    p.font.color.rgb = C_CRIMSON
                    p.font.bold = True
                    p.alignment = PP_ALIGN.CENTER
                elif "High" in str(val) or "Critical" in str(val):
                    p.font.color.rgb = C_CRIMSON
                    p.font.bold = True

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (LUXURY OBSIDIAN NAVY & CYAN GLOW)
    # =========================================================================
    s1 = add_slide_with_transition(0)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY_DARK
    bg1.line.fill.background()

    # Outer decorative glow frame
    frame = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    frame.fill.solid()
    frame.fill.fore_color.rgb = RGBColor(26, 44, 76)
    frame.line.color.rgb = RGBColor(56, 189, 248) # Sky blue
    frame.line.width = Pt(2)

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "VISHWAKARMA INSTITUTE OF TECHNOLOGY, PUNE"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(56, 189, 248)
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
    p2.space_before = Pt(18)

    p3 = tf.add_paragraph()
    p3.text = "Course Project in Software Engineering | End-to-End Analysis, Design, Testing & V&V"
    p3.font.size = Pt(15)
    p3.font.color.rgb = RGBColor(226, 232, 240)
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(8)

    p4 = tf.add_paragraph()
    p4.text = "Submitted by: Student Project Team | Class: TY B.Tech Computer Engineering\nUnder the Guidance of: Faculty Mentor, Department of Computer Engineering"
    p4.font.size = Pt(12)
    p4.font.color.rgb = RGBColor(203, 213, 225)
    p4.alignment = PP_ALIGN.CENTER
    p4.space_before = Pt(36)

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY (3 BALANCED VIBRANT CARDS)
    # =========================================================================
    s2 = add_slide_with_transition(1)
    render_header(s2, "Executive Summary & Architectural Mission", "PROJECT FOUNDATION", C_BLUE)

    render_card(s2, Inches(0.8), Inches(1.6), Inches(3.75), Inches(5.2),
                "Database-First Integrity",
                ["Critical business logic encapsulated strictly inside MySQL stored procedures.",
                 "Eliminates client-side bypass and guarantees 100% database-enforced invariants.",
                 "Declarative check constraints reject underage (age < 18) and negative balance records.",
                 "Every financial move is wrapped in START TRANSACTION, COMMIT, and ROLLBACK blocks.",
                 "Zero reliance on application ORM layers for monetary safety."],
                accent_color=C_SAPPHIRE, bg_color=BG_BLUE, footer_badge="17 Stored Procedures | 5 Triggers")

    render_card(s2, Inches(4.8), Inches(1.6), Inches(3.75), Inches(5.2),
                "ACID Concurrency Engine",
                ["Guarantees strict atomicity, consistency, isolation, and durability.",
                 "Enforces ascending row-locking order: min(id) locked before max(id).",
                 "Completely eliminates classic deadlocks during simultaneous reverse transfers.",
                 "SELECT ... FOR UPDATE prevents concurrent lost updates and phantom reads.",
                 "Zero ledger drift across millions of simulated transaction queries."],
                accent_color=C_EMERALD, bg_color=BG_GREEN, footer_badge="Deterministic Deadlock Prevention")

    render_card(s2, Inches(8.8), Inches(1.6), Inches(3.75), Inches(5.2),
                "Role-Based Banking Portals",
                ["4 Isolated operational personas: Manager, Teller, Loan Officer, and Clerk.",
                 "Streamlit multi-page dashboard protected by session authentication guards.",
                 "Trigger-based immutable audit trail logging all balance changes.",
                 "Live loan EMI calculation, automated disbursement, and card issuance.",
                 "Executive analytical reports with branch deposit distributions and CSV export."],
                accent_color=C_AMBER, bg_color=BG_AMBER, footer_badge="Streamlit UI + MySQL 8.0")

    # =========================================================================
    # SLIDE 3: ROADMAP & AGENDA (10 COLOR-CODED TILES)
    # =========================================================================
    s3 = add_slide_with_transition(2)
    render_header(s3, "Presentation Roadmap & Modules Covered", "TABLE OF CONTENTS", C_PURPLE)

    agenda = [
        ("01", "Problem Statement & Objectives", "Financial domain bottlenecks & software targets", C_BLUE, BG_BLUE),
        ("02", "Study of the Software Crisis", "Systemic causes & 2018 TSB Bank Case Study", C_CRIMSON, BG_RED),
        ("03", "SDLC Models & Methodology", "Comparative evaluation & Hybrid Agile-V life cycle", C_PURPLE, BG_PURPLE),
        ("04", "Requirement Engineering", "Stakeholder needs, FR Matrix (FR-01 to FR-11) & NFRs", C_TEAL, BG_TEAL),
        ("05", "SRS & User Stories", "IEEE 830 specification & Given-When-Then criteria", C_EMERALD, BG_GREEN),
        ("06", "UML Behavioral & Structural Models", "Use Case, Activity, Sequence & State Machine models", C_SAPPHIRE, BG_BLUE),
        ("07", "Software Testing Strategies", "Equivalence Partitioning, BVA & White-Box Basis Path", C_AMBER, BG_AMBER),
        ("08", "Software Maintenance & SLA", "Corrective, Adaptive, Perfective, Preventive routines", C_TEAL, BG_TEAL),
        ("09", "Risk Management & Git Control", "Quantitative 5x5 Risk Register & GitFlow release model", C_CRIMSON, BG_RED),
        ("10", "Verification, Validation & Conclusion", "Traceability Matrix (RTM), Defect Log & Project Summary", C_PURPLE, BG_PURPLE)
    ]
    for idx, (num, title, desc, acc, bg) in enumerate(agenda):
        col = idx // 5
        row = idx % 5
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.5 + row * 1.08)

        # Container
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.75), Inches(0.98))
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = acc
        card.line.width = Pt(1.5)

        # Number badge on left
        num_badge = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.12), top + Inches(0.14), Inches(0.7), Inches(0.7))
        num_badge.fill.solid()
        num_badge.fill.fore_color.rgb = acc
        num_badge.line.fill.background()
        tf_n = num_badge.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        pn = tf_n.paragraphs[0]
        pn.text = num
        pn.font.size = Pt(15)
        pn.font.bold = True
        pn.font.color.rgb = C_WHITE
        pn.alignment = PP_ALIGN.CENTER

        # Title & Subtitle text
        tb = s3.shapes.add_textbox(left + Inches(0.95), top + Inches(0.1), Inches(4.65), Inches(0.78))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_DARK
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 4: PROBLEM STATEMENT (4 BALANCED CARDS)
    # =========================================================================
    s4 = add_slide_with_transition(3)
    render_header(s4, "Problem Statement: Critical Challenges in Banking IT", "DOMAIN CHALLENGES", C_CRIMSON)

    render_card(s4, Inches(0.8), Inches(1.6), Inches(5.75), Inches(2.55),
                "Manual Overhead & Reconciliation Latency",
                ["Decentralized branch paperwork and manual ledger entries result in long queues.",
                 "High susceptibility to human bookkeeping errors during inter-account adjustments.",
                 "Difficulty synchronizing multi-branch customer transaction records in real time.",
                 "Absence of instant digital verification of customer KYC and identity credentials."],
                accent_color=C_CRIMSON, bg_color=BG_RED, footer_badge="Bottleneck: Operational Delay & High Error Rate")

    render_card(s4, Inches(6.75), Inches(1.6), Inches(5.75), Inches(2.55),
                "Concurrency Conflicts & Ledger Drift",
                ["Uncoordinated simultaneous teller transactions on the same account cause 'lost updates'.",
                 "Overdraft violations occur when concurrent withdrawals pass client balance checks together.",
                 "Ledger drift creates un-reconciled differences between assets and liabilities.",
                 "Requires database-level row locking with ACID transaction boundaries."],
                accent_color=C_AMBER, bg_color=BG_AMBER, footer_badge="Bottleneck: Data Inconsistency & Balance Drift")

    render_card(s4, Inches(0.8), Inches(4.35), Inches(5.75), Inches(2.55),
                "Deadlock Vulnerability in Inter-Account Transfers",
                ["Simultaneous reverse transfers (Acc 1 -> Acc 2 and Acc 2 -> Acc 1) lock rows out of order.",
                 "Creates cyclical wait dependencies inside database engines, freezing worker threads.",
                 "Causes transaction timeout aborts, customer frustration, and abandoned operations.",
                 "Requires deterministic ascending primary key lock ordering: min(id) then max(id)."],
                accent_color=C_PURPLE, bg_color=BG_PURPLE, footer_badge="Bottleneck: Concurrency Deadlocks")

    render_card(s4, Inches(6.75), Inches(4.35), Inches(5.75), Inches(2.55),
                "Audit Voids & Insider Fraud Susceptibility",
                ["Untracked administrative balance modifications leave no digital forensics footprint.",
                 "Lack of immutable database-level triggers permits unauthorized overdraft overrides.",
                 "Inability to prove non-repudiation during statutory central bank compliance audits.",
                 "Demands autonomous trigger-based logging into an append-only audit trail table."],
                accent_color=C_SAPPHIRE, bg_color=BG_BLUE, footer_badge="Bottleneck: Compliance & Fraud Risks")

    # =========================================================================
    # SLIDE 5: OBJECTIVES (7 HIGH-DENSITY TILES)
    # =========================================================================
    s5 = add_slide_with_transition(4)
    render_header(s5, "Software Engineering Course Project Objectives", "ENGINEERING GOALS", C_EMERALD)

    objs = [
        ("Study Financial Software Crises", "Analyze historical root causes of banking software failures and devise defensive architectural mitigations.", C_CRIMSON, BG_RED),
        ("Select & Justify Hybrid SDLC", "Design and validate a Hybrid Agile-V methodology pairing strict ledger verification with agile dashboard sprints.", C_PURPLE, BG_PURPLE),
        ("Multi-Stakeholder Elicitation", "Elicit and classify requirements across Managers, Tellers, Loan Officers, Clerks, and Compliance Auditors.", C_BLUE, BG_BLUE),
        ("Author IEEE 830 SRS & Stories", "Develop formal specifications, functional constraints, and user stories verified by Given-When-Then acceptance criteria.", C_TEAL, BG_TEAL),
        ("Formulate Complete UML Models", "Construct structural and dynamic models including Use Case, Activity, Sequence, and State Machine diagrams.", C_SAPPHIRE, BG_BLUE),
        ("Design Exhaustive Test Suites", "Implement Black-Box (EP & BVA) and White-Box (Basis Path & Cyclomatic Complexity) testing suites.", C_AMBER, BG_AMBER),
        ("Establish Maintenance & Risk SLA", "Formulate a 5x5 quantitative risk matrix, proactive maintenance SLA schedule, and GitFlow release pipeline.", C_EMERALD, BG_GREEN)
    ]
    for idx, (title, desc, acc, bg) in enumerate(objs):
        top = Inches(1.5 + idx * 0.78)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.733), Inches(0.70))
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = acc
        card.line.width = Pt(1.5)

        tb = s5.shapes.add_textbox(Inches(1.0), top + Inches(0.08), Inches(11.3), Inches(0.54))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run(f"🎯 Objective {idx+1}: {title} — ")
        r1.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = acc
        r2 = p.add_run(desc)
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 6: STUDY OF THE SOFTWARE CRISIS
    # =========================================================================
    s6 = add_slide_with_transition(0)
    render_header(s6, "Study of the Software Crisis in Financial Systems", "CRISIS ANALYSIS", C_CRIMSON)

    # Top Hero Card
    top_c = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.4))
    top_c.fill.solid()
    top_c.fill.fore_color.rgb = BG_RED
    top_c.line.color.rgb = C_CRIMSON
    top_c.line.width = Pt(1.5)
    tb_tc = s6.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(1.2))
    tf_tc = tb_tc.text_frame
    tf_tc.word_wrap = True
    tf_tc.margin_left = tf_tc.margin_top = tf_tc.margin_right = tf_tc.margin_bottom = 0
    pt1 = tf_tc.paragraphs[0]
    pt1.text = "WHAT IS THE SOFTWARE CRISIS IN BANKING?"
    pt1.font.size = Pt(13)
    pt1.font.bold = True
    pt1.font.color.rgb = C_CRIMSON
    pd1 = tf_tc.add_paragraph()
    pd1.text = "The software crisis refers to the persistent failure to deliver software within planned budgets, schedules, and quality requirements. In financial computing, software failures do not merely result in inconvenience—they trigger catastrophic balance drift, multi-million pound capital destruction, loss of customer trust, and severe regulatory fines."
    pd1.font.size = Pt(10.5)
    pd1.font.color.rgb = C_TEXT_DARK
    pd1.space_before = Pt(4)

    # 3 Bottom Pillars
    render_card(s6, Inches(0.8), Inches(3.05), Inches(3.75), Inches(3.8),
                "Complexity Explosion",
                ["Banking systems involve multi-layered regulatory logic, tax deductions, and multi-branch transactions.",
                 "Uncontrolled interdependencies between modules make system behavior unpredictable.",
                 "A bug fix in fee calculation can accidentally trigger illegal account closures.",
                 "Demands modular 3NF schema and isolated stored procedures."],
                accent_color=C_CRIMSON, bg_color=BG_RED, footer_badge="Root Cause: High Coupling")

    render_card(s6, Inches(4.8), Inches(3.05), Inches(3.75), Inches(3.8),
                "Concurrency Testing Void",
                ["Testing is frequently conducted on single-threaded, isolated happy paths.",
                 "Deadlocks and race conditions emerge only under peak concurrent load.",
                 "Lack of rigorous automated stress-testing leads to runtime crashes during live operations.",
                 "Requires automated multi-client concurrency test suites."],
                accent_color=C_AMBER, bg_color=BG_AMBER, footer_badge="Root Cause: Inadequate Testing")

    render_card(s6, Inches(8.8), Inches(3.05), Inches(3.75), Inches(3.8),
                "Incomplete Traceability",
                ["Informal, non-documented requirements lead to misalignment between developers and bank staff.",
                 "Changes introduced during maintenance lack backward regression verification.",
                 "Central bank compliance requirements get lost during UI upgrades.",
                 "Requires end-to-end Requirements Traceability (RTM)."],
                accent_color=C_SAPPHIRE, bg_color=BG_BLUE, footer_badge="Root Cause: Documentation Void")

    # =========================================================================
    # SLIDE 7: CASE STUDY: TSB BANK MIGRATION DISASTER
    # =========================================================================
    s7 = add_slide_with_transition(1)
    render_header(s7, "Real-World Case Study: 2018 TSB Bank Migration Collapse", "CASE STUDY", C_CRIMSON)

    render_card(s7, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.2),
                "The Catastrophe & Economic Fallout",
                ["In April 2018, UK-based TSB Bank migrated 5.2 million customer records and 1.3 billion records to its new core banking platform ('Proteo4UK').",
                 "System failed immediately upon going live: 1.9 million online banking customers were locked out of their accounts.",
                 "Severe data breaches: Customers could see other users' confidential balances, transaction histories, and credit card details.",
                 "Total direct financial damage exceeded £330 Million in compensation, remediation, and FCA regulatory fines.",
                 "TSB's Chief Executive was forced to resign amidst national public inquiry."],
                accent_color=C_CRIMSON, bg_color=BG_RED, footer_badge="Direct Loss: £330M+ | 1.9M Customers Affected")

    render_card(s7, Inches(6.75), Inches(1.6), Inches(5.75), Inches(5.2),
                "Critical Software Engineering Lessons",
                ["1. Never Skimp on End-to-End Load Testing:\nTSB tested modules in isolation but never stress-tested interconnected microservices under live transaction volumes.",
                 "2. Safe Cutover & Rollback Protocols:\nLack of an automated rollback mechanism left engineers unable to revert to the legacy system once corruption was flagged.",
                 "3. Database-Level Multi-Tenant Isolation:\nRecord crosstalk proved an absence of defensive primary key boundary checks at the query and storage layer.",
                 "4. Independent Verification & Validation:\nCrucial testing milestones were signed off despite known open defect logs."],
                accent_color=C_SAPPHIRE, bg_color=BG_BLUE, footer_badge="BMS Mitigation: Automated Regression & ACID Rollbacks")

    # =========================================================================
    # SLIDE 8: CRISIS CAUSES & REMEDIES MATRIX
    # =========================================================================
    s8 = add_slide_with_transition(2)
    render_header(s8, "Software Crisis: Root Causes & BMS Engineering Remedies", "CRISIS VS MITIGATION", C_SAPPHIRE)

    headers_s8 = ["Software Crisis Factor", "Banking Manifestation", "BMS Engineering Solution", "Verification Target"]
    rows_s8 = [
        ["Ambiguous Rules", "Uncertainty whether min balance applies before fees", "Explicit SQL constraints & Given-When-Then criteria", "SRS / User Stories"],
        ["Concurrency Races", "Simultaneous withdrawals causing negative balance", "InnoDB row locking & transaction boundaries (ACID)", "Acceptance Tests"],
        ["Deadlock Outages", "Reverse inter-account transfers locking worker threads", "Ascending lock ordering: min(id) then max(id)", "sp_transfer procedure"],
        ["Audit Void", "Untracked administrative balance modifications", "Automated DB triggers writing immutable snapshots", "5 Database Triggers"],
        ["Disjointed Logic", "Client-side validation bypassed via direct API calls", "Database-first stored procedures encapsulating all logic", "17 Stored Procedures"],
        ["Late Defect Discovery", "Bugs uncovered after deployment causing capital loss", "Continuous automated regression testing & V&V reviews", "Traceability Matrix"]
    ]
    render_table(s8, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2), headers_s8, rows_s8,
                 [Inches(2.1), Inches(3.7), Inches(3.7), Inches(2.233)], header_bg=C_SAPPHIRE)

    # =========================================================================
    # SLIDE 9: COMPARISON OF SDLC MODELS
    # =========================================================================
    s9 = add_slide_with_transition(3)
    render_header(s9, "Comparative Evaluation of Classic & Modern SDLC Models", "SDLC EVALUATION", C_PURPLE)

    headers_s9 = ["SDLC Model", "Core Strengths", "Critical Limitations", "Suitability for Banking Systems"]
    rows_s9 = [
        ["Waterfall", "Rigid phase gates; thorough upfront documentation", "Inflexible to changes; testing deferred to the end", "Poor for interactive modern banking UIs"],
        ["V-Model", "Verification planned alongside every development phase", "High cost of change; rigid requirements lock-in", "Excellent for safety-critical ledger core"],
        ["Incremental", "Delivers operational functional chunks progressively", "Requires early comprehensive architecture vision", "Good for staggered release of services"],
        ["Spiral", "Risk-driven iterations; prototypes detect vulnerabilities early", "High management overhead; requires risk experts", "Suited for multi-million core bank re-writes"],
        ["Agile (Scrum)", "Rapid feedback loops; adapts to evolving needs", "Risk of documentation neglect and scope creep", "Ideal for customer dashboards and reports"]
    ]
    render_table(s9, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2), headers_s9, rows_s9,
                 [Inches(1.8), Inches(3.6), Inches(3.6), Inches(2.733)], header_bg=C_PURPLE)

    # =========================================================================
    # SLIDE 10: SELECTED SDLC: HYBRID AGILE-V
    # =========================================================================
    s10 = add_slide_with_transition(4)
    render_header(s10, "Selected SDLC: Hybrid Agile-V Life Cycle Methodology", "SDLC JUSTIFICATION", C_TEAL)

    render_card(s10, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.2),
                "Core Ledger Layer: V-Model Rigor",
                ["Scope: 10-table 3NF relational schema, 17 transactional stored procedures, 5 audit triggers, and ACID fund movements.",
                 "Why V-Model? Financial ledger logic permits zero ambiguity. A defect in interest calculation or fund transfer destroys balance sheets.",
                 "Every procedure specification is directly paired with a corresponding automated verification test case before release.",
                 "Rigid signoff: Stored procedures cannot be altered without formal regression re-verification.",
                 "Outcome: A mathematically verified, deadlock-free database kernel that rejects all balance violations."],
                accent_color=C_SAPPHIRE, bg_color=BG_BLUE, footer_badge="Verification Method: V-Model Rigor")

    render_card(s10, Inches(6.75), Inches(1.6), Inches(5.75), Inches(5.2),
                "User Interface Layer: Agile Sprints",
                ["Scope: Streamlit multi-page portal, 4 RBAC role dashboards, interactive loan EMI calculators, Plotly visual charts, CSV reports.",
                 "Why Agile? Front-end workflows, form layouts, and teller usability benefit from rapid stakeholder reviews and 2-week iterations.",
                 "Rapid Prototyping: Teller and manager feedback gathered at the end of each sprint to optimize daily transaction speed.",
                 "Adaptability: Easily accommodates new reporting requirements or visual improvements without risking core ledger stability.",
                 "Outcome: Intuitive, responsive web interfaces delivered and refined through continuous feedback."],
                accent_color=C_AMBER, bg_color=BG_AMBER, footer_badge="Delivery Method: 2-Week Agile Sprints")

    # =========================================================================
    # SLIDE 11: 6-SPRINT DEVELOPMENT ROADMAP
    # =========================================================================
    s11 = add_slide_with_transition(0)
    render_header(s11, "6-Sprint Development Roadmap & Verified Deliverables", "SPRINT EXECUTION", C_BLUE)

    headers_s11 = ["Sprint", "Focus Domain", "Primary Engineering Activities", "Verified Deliverables"]
    rows_s11 = [
        ["Sprint 1", "Database Core", "Design 10-table 3NF schema, composite keys, checks", "sql/01_schema.sql (DDL Verified)"],
        ["Sprint 2", "Transaction Engine", "Build 17 stored procedures with ordered locking", "sql/02_procedures.sql (Deadlock-Free)"],
        ["Sprint 3", "Auditing & Analytics", "Implement 5 audit triggers & 6 relational views", "sql/03_triggers_views.sql & Seed Data"],
        ["Sprint 4", "Auth & Teller Portal", "Build Streamlit RBAC login & deposit/transfer screens", "app/main.py, app/auth.py, Pages 1-4"],
        ["Sprint 5", "Loans, Cards & Reports", "Origination, live EMI calculator, card management", "Pages 5-8, CSV exports, Plotly charts"],
        ["Sprint 6", "QA, Testing & Signoff", "Execute acceptance test harness & V&V matrix", "run_acceptance_tests.py & Final Report"]
    ]
    render_table(s11, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2), headers_s11, rows_s11,
                 [Inches(1.5), Inches(2.4), Inches(4.3), Inches(3.533)], header_bg=C_BLUE)

    # =========================================================================
    # SLIDE 12: STAKEHOLDER REQUIREMENTS ELICITATION
    # =========================================================================
    s12 = add_slide_with_transition(1)
    render_header(s12, "Stakeholder Requirements Elicitation & Analysis", "REQUIREMENT ENGINEERING", C_TEAL)

    headers_s12 = ["Stakeholder Persona", "Operational Responsibilities", "Core Needs & Technical Pain Points"]
    rows_s12 = [
        ["Bank Manager", "Branch supervision, staffing, fee runs, compliance", "Real-time liquidity visibility, audit trail review, staff transfer controls"],
        ["Bank Teller", "Daily cash deposits, withdrawals, fund transfers", "Rapid balance enquiry, zero transfer errors, instant receipt generation"],
        ["Loan Officer", "Credit origination, application risk evaluation", "Automated EMI calculator, debt-to-income checks, disbursement workflow"],
        ["Bank Clerk", "Customer onboarding, KYC compliance, card issuance", "Input validation (age >= 18), PAN/Aadhaar deduplication, card freeze tool"],
        ["Compliance Auditor", "Regulatory inspection & forensic trail tracking", "Immutable audit log table, tamper-proof trigger execution, dormant account lists"]
    ]
    render_table(s12, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2), headers_s12, rows_s12,
                 [Inches(2.2), Inches(4.2), Inches(5.333)], header_bg=C_TEAL)

    # =========================================================================
    # SLIDE 13: FUNCTIONAL REQUIREMENTS MATRIX
    # =========================================================================
    s13 = add_slide_with_transition(2)
    render_header(s13, "Functional Requirements (FR) Specification Matrix", "REQUIREMENT SPECIFICATION", C_SAPPHIRE)

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
    render_table(s13, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2), headers_s13, rows_s13,
                 [Inches(1.2), Inches(5.333), Inches(2.2), Inches(3.0)], header_bg=C_SAPPHIRE)

    # =========================================================================
    # SLIDE 14: NON-FUNCTIONAL REQUIREMENTS
    # =========================================================================
    s14 = add_slide_with_transition(3)
    render_header(s14, "Non-Functional Requirements & Quality Attributes", "QUALITY ATTRIBUTES", C_PURPLE)

    nfrs = [
        ("NFR-01: ACID Consistency", ["Zero financial drift.", "All balance changes enclosed in InnoDB transaction blocks.", "Guaranteed automatic rollback upon any query or constraint failure."], C_SAPPHIRE, BG_BLUE),
        ("NFR-02: Performance & Latency", ["Routine balance checks & deposits complete within < 500 ms.", "Complex branch analytics & Plotly reports render in < 2 seconds under peak load.", "Connection pool minimizes latency."], C_BLUE, BG_BLUE),
        ("NFR-03: Security & RBAC", ["Strict role separation across Manager, Teller, Loan Officer, Clerk.", "Zero plaintext passwords.", "Parameterized queries block 100% of SQL injection attempts."], C_CRIMSON, BG_RED),
        ("NFR-04: Data Integrity", ["Enforced at relational persistence layer.", "Foreign key cascading controls.", "Declarative check constraints reject negative balances and underage customers."], C_AMBER, BG_AMBER),
        ("NFR-05: High Availability", ["Database connection pool automatically recovers from transient network drops.", "Failover logging ensures uncommitted transactions are rolled back safely."], C_EMERALD, BG_GREEN),
        ("NFR-06: Full Auditability", ["Every balance adjustment creates an immutable audit row.", "Captures old balance, new balance, user ID, and timestamp.", "Users restricted from deleting audit logs."], C_PURPLE, BG_PURPLE)
    ]
    for idx, (title, items, acc, bg) in enumerate(nfrs):
        col = idx % 3
        row = idx // 3
        left = Inches(0.8 + col * 4.0)
        top = Inches(1.6 + row * 2.65)
        render_card(s14, left, top, Inches(3.75), Inches(2.55),
                    title, items, accent_color=acc, bg_color=bg, footer_badge=None, title_size=Pt(12), body_size=Pt(10))

    # =========================================================================
    # SLIDE 15: SRS ARCHITECTURE & DESIGN
    # =========================================================================
    s15 = add_slide_with_transition(4)
    render_header(s15, "Software Requirement Specification Architecture", "SYSTEM ARCHITECTURE", C_BLUE)

    render_card(s15, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.6),
                "1. Presentation Layer (Streamlit Multi-Page Web App)",
                ["Multi-page dashboard structure: app/main.py with 8 dedicated functional page controllers.",
                 "Session-state authentication guards redirect unauthorized URL visits immediately.",
                 "Rich user interface with dynamic form validation, Indian Rupee (₹) formatting, and Plotly Express visual charts.",
                 "Empowers 4 operational roles with clean, responsive, and specialized task screens."],
                accent_color=C_BLUE, bg_color=BG_BLUE, footer_badge="Frontend: Streamlit + Plotly Express")

    render_card(s15, Inches(0.8), Inches(3.4), Inches(11.733), Inches(1.6),
                "2. Data Access & Pool Layer (Python db.py)",
                ["Centralized MySQL connection pool managing active connections without socket starvation.",
                 "Exclusively executes parameterized queries (cursor.execute(sql, params)), eliminating SQL injection.",
                 "Captures authenticated staff session identity and passes user attribution to MySQL procedures for auditing.",
                 "Catches database exceptions gracefully and converts SQLSTATE errors into intuitive UI alerts."],
                accent_color=C_AMBER, bg_color=BG_AMBER, footer_badge="Connector: mysql-connector-python + Connection Pooling")

    render_card(s15, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.6),
                "3. Core Persistence & Business Logic (MySQL 8.0 InnoDB)",
                ["10 Fully normalized 3NF relational tables enforcing referential integrity and composite indexes.",
                 "17 Transactional stored procedures encapsulating all financial logic, fund movements, and interest runs.",
                 "5 Automated triggers enforcing immutable audit logging on balances, accounts, and loan transitions.",
                 "6 Relational analytical views serving executive reports without computationally heavy ad-hoc table joins."],
                accent_color=C_SAPPHIRE, bg_color=BG_BLUE, footer_badge="Core Engine: MySQL 8.0 Enterprise / Community Edition")

    # =========================================================================
    # SLIDE 16: USER STORIES: TRANSFER & ONBOARDING
    # =========================================================================
    s16 = add_slide_with_transition(0)
    render_header(s16, "User Stories & Acceptance Criteria: Core Flows", "USER STORIES", C_EMERALD)

    render_card(s16, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.2),
                "User Story 1: Atomic Fund Transfer",
                ["As a Bank Teller, I want to transfer funds between accounts atomically so that neither account experiences ledger drift.",
                 "Given a source account with balance >= (min_balance + amount), when submitted, debits source, credits destination, and commits.",
                 "Given an amount violating minimum balance, when submitted, transaction rolls back with error 'Insufficient balance'.",
                 "Given simultaneous reverse transfers, locks are acquired in ascending order (min ID first) to prevent deadlocks.",
                 "Given either account is in FROZEN or CLOSED state, the transaction is immediately aborted with a state alert."],
                accent_color=C_EMERALD, bg_color=BG_GREEN, footer_badge="Given-When-Then: Verified by TC-TXN-03")

    render_card(s16, Inches(6.75), Inches(1.6), Inches(5.75), Inches(5.2),
                "User Story 2: Customer Onboarding (18+)",
                ["As a Bank Clerk, I want to register customer profiles with mandatory KYC details so that accounts comply with statutory laws.",
                 "Given complete registration fields with DOB proving age >= 18, when submitted, customer created with status PENDING KYC.",
                 "Given date of birth indicating age < 18, when submitted, rejected with 'Customer must be at least 18 years old'.",
                 "Given a duplicate Aadhaar or PAN number, the unique database constraint blocks insertion and alerts the clerk.",
                 "Given missing email or phone, submission is rejected at both frontend and database layers."],
                accent_color=C_BLUE, bg_color=BG_BLUE, footer_badge="Given-When-Then: Verified by TC-CUST-01")

    # =========================================================================
    # SLIDE 17: USER STORIES: LOANS & AUDIT
    # =========================================================================
    s17 = add_slide_with_transition(1)
    render_header(s17, "User Stories & Acceptance Criteria: Loans & Audit", "USER STORIES", C_AMBER)

    render_card(s17, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.2),
                "User Story 3: Loan Origination & Live EMI",
                ["As a Loan Officer, I want to compute live amortized EMI and approve loans so that principal is credited securely.",
                 "Given requested principal P, annual rate r, tenure n, calculates monthly EMI via: [P * r * (1+r)^n] / [(1+r)^n - 1].",
                 "Given a loan in APPLIED status, Officer can evaluate credit risk and transition it to APPROVED or REJECTED.",
                 "Given an APPROVED loan, disbursement credits principal into customer savings account atomically and logs ledger row.",
                 "Given an applicant with defaulted loans or a frozen account, automated disbursement is strictly blocked."],
                accent_color=C_AMBER, bg_color=BG_AMBER, footer_badge="Given-When-Then: Verified by TC-LOAN-01")

    render_card(s17, Inches(6.75), Inches(1.6), Inches(5.75), Inches(5.2),
                "User Story 4: Immutable Audit Trails",
                ["As a Bank Manager / Auditor, I want an append-only audit trail so that all financial actions are verifiable.",
                 "Given any UPDATE to accounts.balance, database trigger trg_account_balance_audit fires automatically.",
                 "Log records old balance, new balance, changed_by employee ID, and UTC timestamp.",
                 "Application users are restricted from executing DELETE or UPDATE on audit_log table.",
                 "Manager reports display filterable audit records for regulatory compliance and forensic audit."],
                accent_color=C_PURPLE, bg_color=BG_PURPLE, footer_badge="Given-When-Then: Verified by TC-AUD-01")

    # =========================================================================
    # SLIDE 18: UML USE CASE DIAGRAM
    # =========================================================================
    s18 = add_slide_with_transition(2)
    render_header(s18, "UML Modeling: Use Case Architecture & RBAC", "UML STRUCTURAL MODEL", C_SAPPHIRE)

    headers_s18 = ["Actor Role", "Authorized Use Cases (Direct Responsibilities)", "Access Boundary Rationale"]
    rows_s18 = [
        ["Bank Clerk", "UC-01: Authenticate\nUC-02: Register Customer (Age >= 18)\nUC-03: Open Accounts\nUC-04: Issue / Block Cards", "Handles front-desk onboarding; isolated from loan approvals and money transfers."],
        ["Bank Teller", "UC-01: Authenticate\nUC-05: Deposit Cash\nUC-06: Withdraw Cash\nUC-07: Inter-Account Transfer\nUC-08: Balance Enquiry", "Executes ledger transactions; restricted from approving loans or changing staff roles."],
        ["Loan Officer", "UC-01: Authenticate\nUC-09: Originate Loan Application\nUC-10: Review / Approve Loan\nUC-11: Disburse Loan Principal", "Evaluates credit risk and disbursements; isolated from teller cash drawers."],
        ["Bank Manager", "Inherits ALL Use Cases (UC-01 through UC-11)\nUC-12: Employee Staff Hiring / Transfer\nUC-13: Execute Monthly Interest Run\nUC-14: Audit Trail Inspection", "Complete administrative supremacy across branch liquidity, staff, and regulatory auditing."]
    ]
    render_table(s18, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2), headers_s18, rows_s18,
                 [Inches(2.0), Inches(4.8), Inches(4.933)], header_bg=C_SAPPHIRE)

    # =========================================================================
    # SLIDE 19: UML ACTIVITY DIAGRAM: FUND TRANSFER
    # =========================================================================
    s19 = add_slide_with_transition(3)
    render_header(s19, "UML Activity Diagram: Atomic Transfer Logic", "UML BEHAVIORAL MODEL", C_BLUE)

    act_steps = [
        ("1. Input & Validation", ["Teller inputs from_acc, to_acc, amount.", "Checks: amount > 0 and from != to.", "Verifies teller authentication."], C_SAPPHIRE, BG_BLUE),
        ("2. Ordered Locking", ["Deterministic ascending row locking.", "Locks min(from_id, to_id) first.", "Prevents reverse transfer deadlocks."], C_BLUE, BG_BLUE),
        ("3. Account Status Check", ["Inspects status of both accounts.", "If either is FROZEN or CLOSED, aborts.", "Executes ROLLBACK transaction."], C_CRIMSON, BG_RED),
        ("4. Solvency Verification", ["Verifies: (Balance - Amount) >= Min Bal.", "Savings min: ₹1,000; Current min: ₹5,000.", "If violated, rolls back with error."], C_AMBER, BG_AMBER),
        ("5. Atomic Ledger Update", ["Debits sender: balance = balance - amount.", "Credits receiver: balance = balance + amount.", "Inserts transaction row into ledger."], C_EMERALD, BG_GREEN),
        ("6. Trigger Audit & Commit", ["Audit trigger records old & new balances.", "Executes COMMIT transaction.", "UI renders printable transfer receipt."], C_PURPLE, BG_PURPLE)
    ]
    for idx, (title, items, acc, bg) in enumerate(act_steps):
        col = idx % 3
        row = idx // 3
        left = Inches(0.8 + col * 4.0)
        top = Inches(1.6 + row * 2.65)
        render_card(s19, left, top, Inches(3.75), Inches(2.55),
                    title, items, accent_color=acc, bg_color=bg, footer_badge=None, title_size=Pt(12), body_size=Pt(10))

    # =========================================================================
    # SLIDE 20: UML SEQUENCE DIAGRAM: LOAN DISBURSEMENT
    # =========================================================================
    s20 = add_slide_with_transition(4)
    render_header(s20, "UML Sequence Diagram: Loan Disbursement Lifeline", "UML INTERACTION MODEL", C_AMBER)

    seq_steps = [
        ("Step 1: Loan Officer -> Streamlit UI", "Officer selects approved loan ID and clicks 'Disburse Principal to Customer Account'", C_BLUE, BG_BLUE),
        ("Step 2: Streamlit UI -> Database Pool", "Invokes db.execute_procedure('sp_disburse_loan', [loan_id, officer_id]) with auth token", C_PURPLE, BG_PURPLE),
        ("Step 3: DB Engine -> loans Table", "Executes START TRANSACTION and SELECT * FROM loans WHERE loan_id = ? FOR UPDATE", C_SAPPHIRE, BG_BLUE),
        ("Step 4: Stored Procedure Decision", "Checks if status == 'APPROVED'. If not, signals SQL exception 45000 and rolls back immediately", C_CRIMSON, BG_RED),
        ("Step 5: DB Engine -> accounts Table", "Executes UPDATE accounts SET balance = balance + principal WHERE account_id = target_account", C_EMERALD, BG_GREEN),
        ("Step 6: DB Engine -> audit_log", "Triggers fire automatically to record balance snapshot, loan status change, and user ID", C_AMBER, BG_AMBER),
        ("Step 7: DB Engine -> COMMIT", "Commits transaction atomically and returns 0 (Success) return code to connection pool", C_EMERALD, BG_GREEN),
        ("Step 8: UI -> Loan Officer", "Streamlit displays success confirmation badge and updated account ledger statement", C_TEAL, BG_TEAL)
    ]
    for idx, (actor_msg, detail, acc, bg) in enumerate(seq_steps):
        top = Inches(1.5 + idx * 0.68)
        card = s20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.733), Inches(0.62))
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = acc
        card.line.width = Pt(1.5)

        tb = s20.shapes.add_textbox(Inches(1.0), top + Inches(0.06), Inches(11.3), Inches(0.50))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run(f"{actor_msg} — ")
        r1.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = acc
        r2 = p.add_run(detail)
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 21: UML STATE MACHINE: ACCOUNT LIFECYCLE
    # =========================================================================
    s21 = add_slide_with_transition(0)
    render_header(s21, "UML State Machine: Bank Account Lifecycle", "UML STATE MODEL", C_TEAL)

    states = [
        ("PENDING_APPROVAL",
         ["Trigger: Customer profile submitted.",
          "Condition: Awaiting KYC verification by clerk.",
          "Allowed: Form edits, identity document re-upload.",
          "Blocked: All financial deposits, withdrawals, and card spends."],
         C_AMBER, BG_AMBER, "Initial State"),
        ("ACTIVE (Fully Operational)",
         ["Trigger: KYC verified & initial min deposit credited.",
          "Condition: Account is solvent and in good standing.",
          "Allowed: Cash deposits, withdrawals, transfers, interest runs.",
          "Sub-states: Idle -> Debited -> Credited -> Idle."],
         C_EMERALD, BG_GREEN, "Operational State"),
        ("FROZEN (Restricted)",
         ["Trigger: Suspicious fraud alert, court order, or 12M inactivity.",
          "Condition: Account locked by Bank Manager.",
          "Allowed: Balance enquiry and internal compliance review.",
          "Blocked: Outgoing transfers, card purchases, withdrawals."],
         C_CRIMSON, BG_RED, "Restricted State"),
        ("CLOSED (Terminal State)",
         ["Trigger: Customer formally requests account closure.",
          "Condition: Balance liquidated to exactly ₹0.00.",
          "Allowed: Historical audit and tax statement reporting only.",
          "Blocked: All financial operations permanently disabled."],
         C_NAVY_DARK, BG_BLUE, "Terminal State")
    ]
    for idx, (title, items, acc, bg, badge) in enumerate(states):
        left = Inches(0.8 + idx * 3.0)
        render_card(s21, left, Inches(1.6), Inches(2.75), Inches(5.2),
                    title, items, accent_color=acc, bg_color=bg, footer_badge=badge, title_size=Pt(12), body_size=Pt(10))

    # =========================================================================
    # SLIDE 22: TESTING: EQUIVALENCE PARTITIONING
    # =========================================================================
    s22 = add_slide_with_transition(1)
    render_header(s22, "Black-Box Testing: Equivalence Partitioning (EP)", "SOFTWARE TESTING", C_EMERALD)

    # Top Context Card
    top_c22 = s22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.8))
    top_c22.fill.solid()
    top_c22.fill.fore_color.rgb = BG_BLUE
    top_c22.line.color.rgb = C_BLUE
    top_c22.line.width = Pt(1.5)
    tb_c22 = s22.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.3), Inches(0.7))
    tf_c22 = tb_c22.text_frame
    tf_c22.word_wrap = True
    tf_c22.margin_left = tf_c22.margin_top = tf_c22.margin_right = tf_c22.margin_bottom = 0
    p22 = tf_c22.paragraphs[0]
    p22.text = "TEST SPECIFICATION — CASH WITHDRAWAL MODULE (SAVINGS ACCOUNT)"
    p22.font.size = Pt(11)
    p22.font.bold = True
    p22.font.color.rgb = C_NAVY_DARK
    p22d = tf_c22.add_paragraph()
    p22d.text = "Account Type: Savings Account | Current Balance: ₹10,000 | Mandatory Minimum Balance: ₹1,000 | Valid Withdrawal Range: ₹100 to ₹9,000"
    p22d.font.size = Pt(9.5)
    p22d.font.color.rgb = C_TEXT_DARK

    headers_s22 = ["Test ID", "Equivalence Partition Class", "Representative Input", "Expected System Action", "Actual Status"]
    rows_s22 = [
        ["EP-W01", "Valid Withdrawal Range (₹100 to ₹9,000)", "₹2,500", "Debits ₹2,500; New Balance ₹7,500; Transaction commits", "PASS"],
        ["EP-W02", "Zero or Negative Amount", "-₹500", "Reject with exception 'Withdrawal amount must be positive'", "PASS"],
        ["EP-W03", "Amount Violating Minimum Balance", "₹9,500 (Leaves ₹500)", "Reject with exception 'Insufficient funds below minimum balance'", "PASS"],
        ["EP-W04", "Amount Exceeding Entire Balance", "₹15,000", "Reject with exception 'Insufficient funds'", "PASS"],
        ["EP-W05", "Withdrawal from Non-Active Account", "₹1,000 (FROZEN)", "Reject with exception 'Account is FROZEN'", "PASS"]
    ]
    render_table(s22, Inches(0.8), Inches(2.45), Inches(11.733), Inches(4.35), headers_s22, rows_s22,
                 [Inches(1.4), Inches(3.2), Inches(2.0), Inches(4.133), Inches(1.0)], header_bg=C_EMERALD)

    # =========================================================================
    # SLIDE 23: TESTING: BOUNDARY VALUE ANALYSIS
    # =========================================================================
    s23 = add_slide_with_transition(2)
    render_header(s23, "Black-Box Testing: Boundary Value Analysis (BVA)", "SOFTWARE TESTING", C_PURPLE)

    headers_s23 = ["Test ID", "Boundary Condition Tested", "Input Value", "Expected Result & Balance Validation", "Status"]
    rows_s23 = [
        ["BVA-W01", "Just below minimum chunk (Min - 1)", "₹99", "Reject: Below minimum single transaction threshold", "PASS"],
        ["BVA-W02", "Exactly at minimum chunk (Min)", "₹100", "Accept: Balance debited to ₹9,900; Transaction commits", "PASS"],
        ["BVA-W03", "Just above minimum chunk (Min + 1)", "₹101", "Accept: Balance debited to ₹9,899; Transaction commits", "PASS"],
        ["BVA-W04", "Just below maximum limit (Max - 1)", "₹8,999", "Accept: Leaves ₹1,001 (Validly above ₹1,000 min balance)", "PASS"],
        ["BVA-W05", "Exactly at maximum limit (Max)", "₹9,000", "Accept: Leaves exactly ₹1,000 (Satisfies exact boundary)", "PASS"],
        ["BVA-W06", "Just above maximum limit (Max + 1)", "₹9,001", "Reject: Leaves ₹999 (Violates ₹1,000 minimum balance rule)", "PASS"]
    ]
    render_table(s23, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2), headers_s23, rows_s23,
                 [Inches(1.4), Inches(3.3), Inches(1.5), Inches(4.533), Inches(1.0)], header_bg=C_PURPLE)

    # =========================================================================
    # SLIDE 24: TESTING: WHITE-BOX BASIS PATH TESTING
    # =========================================================================
    s24 = add_slide_with_transition(3)
    render_header(s24, "White-Box Testing: Basis Path & Cyclomatic Complexity", "SOFTWARE TESTING", C_SAPPHIRE)

    render_card(s24, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2),
                "McCabe's Complexity Model",
                ["Formula: V(G) = P + 1 = E - N + 2",
                 "Decision 1 (Line 3): amount <= 0",
                 "Decision 2 (Line 7): from_id == to_id",
                 "Decision 3 (Line 12): from_status != 'ACTIVE' OR to_status != 'ACTIVE'",
                 "Decision 4 (Line 16): (balance - amount) < min_balance",
                 "Number of Binary Predicates: P = 4",
                 "Calculated Cyclomatic Complexity: V(G) = 4 + 1 = 5 Independent Basis Paths"],
                accent_color=C_SAPPHIRE, bg_color=BG_BLUE, footer_badge="V(G) = 5 Independent Basis Paths")

    headers_s24 = ["Basis Path", "Control Decisions Traversed", "Test Input Conditions", "Expected Outcome"]
    rows_s24 = [
        ["Path 1", "Decision 1 -> True", "amount = -500", "Rejects: Invalid negative amount"],
        ["Path 2", "Decision 1 -> False; Decision 2 -> True", "from_id = 101, to_id = 101", "Rejects: Self-transfer forbidden"],
        ["Path 3", "Dec 1, 2 -> False; Decision 3 -> True", "from_status = 'FROZEN'", "Rejects: Account not in active state"],
        ["Path 4", "Dec 1, 2, 3 -> False; Decision 4 -> True", "from_balance = 1200, amount = 500", "Rejects: Minimum balance breach"],
        ["Path 5", "All Decisions -> False (Happy Path)", "from_balance = 5000, amount = 1000", "Executes atomic transfer & commits"]
    ]
    render_table(s24, Inches(5.5), Inches(1.6), Inches(7.033), Inches(5.2), headers_s24, rows_s24,
                 [Inches(1.2), Inches(2.2), Inches(2.1), Inches(1.533)], header_bg=C_SAPPHIRE)

    # =========================================================================
    # SLIDE 25: SOFTWARE MAINTENANCE PLANNING
    # =========================================================================
    s25 = add_slide_with_transition(4)
    render_header(s25, "Software Maintenance Planning & SLA Schedule", "SOFTWARE MAINTENANCE", C_TEAL)

    headers_s25 = ["Maintenance Class", "Engineering Objective", "Practical BMS Application Scenario", "SLA Frequency"]
    rows_s25 = [
        ["Corrective Maintenance", "Diagnose and repair defects uncovered in runtime production", "Fixing fractional paisa rounding errors during interest runs", "Immediate / Hotfix"],
        ["Adaptive Maintenance", "Modify software to comply with changing external laws & OS", "Updating TDS withholding tax tables per revised Reserve Bank rules", "Monthly / Scheduled"],
        ["Perfective Maintenance", "Enhance performance, UI convenience, and query speeds", "Adding composite index on transactions(account_id, created_at)", "Quarterly Release"],
        ["Preventive Maintenance", "Refactor complex modules & patch libraries before failures", "Upgrading mysql-connector-python & archiving old audit logs", "Bi-Annual Review"]
    ]
    render_table(s25, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2), headers_s25, rows_s25,
                 [Inches(2.2), Inches(3.6), Inches(4.333), Inches(1.6)], header_bg=C_TEAL)

    # =========================================================================
    # SLIDE 26: RISK MANAGEMENT: 5X5 MATRIX
    # =========================================================================
    s26 = add_slide_with_transition(0)
    render_header(s26, "Risk Management: Quantitative 5x5 Risk Register", "RISK MANAGEMENT", C_CRIMSON)

    headers_s26 = ["Risk ID", "Risk Description", "Prob (1-5)", "Imp (1-5)", "Score", "Mitigation Strategy"]
    rows_s26 = [
        ["R-01", "Concurrent Transfer Deadlocks", "3", "5", "15 (High)", "Deterministic ascending primary-key row locking in SQL"],
        ["R-02", "Credential & Role Escalation", "2", "5", "10 (High)", "Strict session guards in app/auth.py & page-level checks"],
        ["R-03", "Ledger Inconsistency on Server Crash", "2", "5", "10 (High)", "InnoDB write-ahead redo logging & automatic rollback"],
        ["R-04", "SQL Injection Attacks", "2", "5", "10 (High)", "Exclusive parameterized queries; zero string concatenation"],
        ["R-05", "Underage Customer Onboarding", "3", "4", "12 (High)", "Dual validation: front-end calendar + MySQL CHECK (age >= 18)"],
        ["R-06", "Database Storage Corruption", "2", "5", "10 (High)", "Automated daily logical mysqldump to cold encrypted storage"]
    ]
    render_table(s26, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2), headers_s26, rows_s26,
                 [Inches(1.1), Inches(3.3), Inches(1.1), Inches(1.1), Inches(1.3), Inches(3.833)], header_bg=C_CRIMSON)

    # =========================================================================
    # SLIDE 27: VERSION CONTROL & GITFLOW
    # =========================================================================
    s27 = add_slide_with_transition(1)
    render_header(s27, "Configuration Management: GitFlow Strategy", "VERSION CONTROL", C_PURPLE)

    git_branches = [
        ("main (Production Releases)", ["Protected branch containing signed production-ready code.", "Direct pushes strictly prohibited.", "Tagged releases: v1.0.0 (Production BMS)."], C_NAVY_DARK, BG_BLUE),
        ("develop (Integration Branch)", ["Active staging trunk where verified feature branches merge.", "Subjected to automated Python test harness.", "Continuous regression validation."], C_BLUE, BG_BLUE),
        ("feature/sql-schema-3nf", ["Isolated branch for establishing normalized tables.", "Includes foreign keys and age/balance constraints.", "Verified via clean MySQL migrations."], C_EMERALD, BG_GREEN),
        ("feature/stored-procedures-acid", ["Branch for implementing 17 stored procedures.", "Incorporates ascending row-locking order.", "Tested under multi-client concurrency."], C_PURPLE, BG_PURPLE),
        ("feature/streamlit-rbac-ui", ["Sprint branch for developing multi-page role views.", "Adds session state auth guards and Plotly charts.", "Refined through branch user feedback."], C_AMBER, BG_AMBER),
        ("bugfix/deadlock-lock-order", ["Rapid-response hotfix branch to resolve race conditions.", "Applies ordered row-locking patch.", "Merged into develop and cherry-picked to main."], C_CRIMSON, BG_RED)
    ]
    for idx, (branch, items, acc, bg) in enumerate(git_branches):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.6 + row * 1.75)
        render_card(s27, left, top, Inches(5.75), Inches(1.65),
                    branch, items, accent_color=acc, bg_color=bg, footer_badge=None, title_size=Pt(12), body_size=Pt(10))

    # =========================================================================
    # SLIDE 28: VERIFICATION & VALIDATION (RTM & DEFECT LOG)
    # =========================================================================
    s28 = add_slide_with_transition(2)
    render_header(s28, "Verification & Validation: RTM & Defect Log", "QUALITY ASSURANCE", C_EMERALD)

    # Top: RTM Summary Card
    top_rtm = s28.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.2))
    top_rtm.fill.solid()
    top_rtm.fill.fore_color.rgb = BG_BLUE
    top_rtm.line.color.rgb = C_BLUE
    top_rtm.line.width = Pt(1.5)
    tb_rtm = s28.shapes.add_textbox(Inches(1.0), Inches(1.58), Inches(11.3), Inches(2.0))
    tf_rtm = tb_rtm.text_frame
    tf_rtm.word_wrap = True
    tf_rtm.margin_left = tf_rtm.margin_top = tf_rtm.margin_right = tf_rtm.margin_bottom = 0
    pt_r = tf_rtm.paragraphs[0]
    pt_r.text = "REQUIREMENTS TRACEABILITY MATRIX (RTM) VERIFICATION STATUS"
    pt_r.font.size = Pt(11.5)
    pt_r.font.bold = True
    pt_r.font.color.rgb = C_SAPPHIRE
    pd_r = tf_rtm.add_paragraph()
    pd_r.text = (
        "• FR-01 (Auth & RBAC) ────> Mapped to app/auth.py ─────────> Verified by TC-AUTH-01 & TC-AUTH-02  [STATUS: 100% VERIFIED]\n"
        "• FR-02 (Customer 18+) ───> Mapped to sql/01_schema.sql ────> Verified by TC-CUST-01 & TC-CUST-02  [STATUS: 100% VERIFIED]\n"
        "• FR-04 (Min Balance) ────> Mapped to sp_withdraw ──────────> Verified by TC-TXN-01 & TC-TXN-02    [STATUS: 100% VERIFIED]\n"
        "• FR-06 (Atomic Transfer) ─> Mapped to sp_transfer ──────────> Verified by TC-TXN-03 & TC-TXN-04    [STATUS: 100% VERIFIED]\n"
        "• FR-10 (Audit Triggers) ──> Mapped to sql/03_triggers ─────> Verified by TC-AUD-01 & TC-AUD-02    [STATUS: 100% VERIFIED]"
    )
    pd_r.font.size = Pt(9.5)
    pd_r.font.color.rgb = C_TEXT_DARK
    pd_r.space_before = Pt(4)

    # Bottom: Defect Log Table
    headers_s28 = ["Defect ID", "Severity", "Defect Description", "Root Cause", "Corrective Action Implemented"]
    rows_s28 = [
        ["DF-01", "Critical", "Concurrency deadlock under simultaneous reverse transfers", "Arbitrary row lock order in sp_transfer", "Enforced ascending primary key ordering: min(id) then max(id)"],
        ["DF-02", "Major", "Customer under 18 accepted if birth year entered wrong", "Missing database-level check constraint", "Added DB CHECK (TIMESTAMPDIFF(YEAR, dob, CURDATE()) >= 18)"],
        ["DF-03", "Moderate", "Division-by-zero error on empty branch analytics screen", "SQL view lacked COALESCE on aggregate sums", "Updated vw_branch_summary with COALESCE(SUM(balance), 0.00)"]
    ]
    render_table(s28, Inches(0.8), Inches(3.9), Inches(11.733), Inches(2.8), headers_s28, rows_s28,
                 [Inches(1.2), Inches(1.2), Inches(3.5), Inches(2.8), Inches(3.033)], header_bg=C_EMERALD)

    # =========================================================================
    # SLIDE 29: CONCLUSION & ENGINEERING SUMMARY
    # =========================================================================
    s29 = add_slide_with_transition(3)
    bg29 = s29.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg29.fill.solid()
    bg29.fill.fore_color.rgb = C_NAVY_DARK
    bg29.line.fill.background()

    frame29 = s29.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    frame29.fill.solid()
    frame29.fill.fore_color.rgb = RGBColor(26, 44, 76)
    frame29.line.color.rgb = RGBColor(56, 189, 248)
    frame29.line.width = Pt(2)

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
        "1. Rigorous Software Engineering Prevents Financial Catastrophe:\n"
        "Ambiguous specifications, untracked modifications, and uncoordinated concurrency destroy banking institutions. Applying formal requirements engineering and database-level invariants ensures zero financial drift.\n\n"
        "2. The Hybrid Agile-V Model Delivers Proven Engineering Balance:\n"
        "V-Model guarantees mathematical correctness and deadlock-free execution in the core relational procedures, while Agile iterations deliver an intuitive, responsive Streamlit dashboard for branch personnel.\n\n"
        "3. Multi-Tier Verification Validates Production Dependability:\n"
        "Equivalence Partitioning, Boundary Value Analysis, Basis Path Testing (V(G)=5), and a comprehensive Traceability Matrix prove that every banking invariant is verifiable before deployment."
    )
    p1.font.size = Pt(11)
    p1.font.color.rgb = RGBColor(226, 232, 240)
    p1.space_before = Pt(16)

    p2 = tf29.add_paragraph()
    p2.text = "THANK YOU! | QUESTIONS & DEMONSTRATION"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(56, 189, 248)
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(24)

    # Save
    out_file = os.path.abspath("Bank_Management_System_Software_Engineering_Presentation.pptx")
    prs.save(out_file)
    print(f"Enhanced presentation successfully saved at: {out_file}")

if __name__ == "__main__":
    create_enhanced_deck()
