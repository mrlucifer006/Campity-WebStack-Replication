#!/usr/bin/env python3
"""
generate_taskflow_presentation.py
Generates a professional 6-slide presentation for TaskFlow: Priority-Driven Campus Task Management & Posting System
Presenter: Sanjai M S
Reference: TaskFlow_Project_Report.docx / TaskFlow_Project_Report.pdf
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# --- Presentation Dimensions (16:9 Widescreen) ---
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# --- Theme Color Palette ---
COLOR_BG_DARK      = RGBColor(11, 17, 32)      # #0B1120 Very Deep Navy
COLOR_CARD_BG      = RGBColor(24, 33, 54)      # #182136 Slate-800 Card
COLOR_CARD_BORDER  = RGBColor(51, 65, 85)      # #334155 Slate-700
COLOR_PRIMARY_BLUE = RGBColor(59, 130, 246)    # #3B82F6 Primary Sapphire
COLOR_EMERALD      = RGBColor(16, 185, 129)    # #10B981 Emerald Green
COLOR_CYAN         = RGBColor(6, 182, 212)     # #06B6D4 Vibrant Cyan
COLOR_AMBER        = RGBColor(245, 158, 11)    # #F59E0B Amber
COLOR_ROSE         = RGBColor(239, 68, 68)     # #EF4444 Rose Red
COLOR_TEXT_WHITE   = RGBColor(248, 250, 252)   # #F8FAFC Pure Slate White
COLOR_TEXT_MUTED   = RGBColor(148, 163, 184)   # #94A3B8 Slate 400
COLOR_TEXT_LIGHT   = RGBColor(203, 213, 225)   # #CBD5E1 Slate 300
COLOR_PILL_BG      = RGBColor(30, 41, 59)      # #1E293B

FONT_FAMILY = "Arial"

def set_slide_background(slide):
    """Sets slide solid dark background."""
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = COLOR_BG_DARK
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, title_text, category_badge, subtitle_text=None):
    """Adds a standard executive header to content slides."""
    # Badge (Pill)
    badge = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(3.2), Inches(0.32)
    )
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(20, 35, 65)
    badge.line.color.rgb = COLOR_PRIMARY_BLUE
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    tf_b.word_wrap = True
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b = tf_b.paragraphs[0]
    p_b.text = category_badge.upper()
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_CYAN
    p_b.font.name = FONT_FAMILY
    p_b.alignment = PP_ALIGN.CENTER

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.7))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE
    p.font.name = FONT_FAMILY

    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.font.name = FONT_FAMILY

    # Top right author stamp
    author_box = slide.shapes.add_textbox(Inches(9.2), Inches(0.4), Inches(3.3), Inches(0.45))
    tf_a = author_box.text_frame
    p_a = tf_a.paragraphs[0]
    p_a.alignment = PP_ALIGN.RIGHT
    p_a.text = "Presenter: Sanjai M S (24CS181)"
    p_a.font.size = Pt(10)
    p_a.font.bold = True
    p_a.font.color.rgb = COLOR_EMERALD
    p_a.font.name = FONT_FAMILY

def add_card(slide, left, top, width, height, border_color=COLOR_CARD_BORDER, bg_color=COLOR_CARD_BG):
    """Draws a modern rounded card panel."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card

def build_presentation():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE & PROJECT OVERVIEW
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Decorative top bar
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
    bar.line.fill.background()

    # College Logo (if exists)
    logo_path = "template_logo.jpeg"
    if os.path.exists(logo_path):
        slide1.shapes.add_picture(logo_path, Inches(0.9), Inches(0.65), width=Inches(1.15))

    # College & Department Info Header
    col_box = slide1.shapes.add_textbox(Inches(2.2), Inches(0.65), Inches(10.2), Inches(1.0))
    tf_col = col_box.text_frame
    tf_col.word_wrap = True
    p_col1 = tf_col.paragraphs[0]
    p_col1.text = "KPR INSTITUTE OF ENGINEERING AND TECHNOLOGY (AUTONOMOUS)"
    p_col1.font.size = Pt(13)
    p_col1.font.bold = True
    p_col1.font.color.rgb = COLOR_TEXT_WHITE
    p_col1.font.name = FONT_FAMILY

    p_col2 = tf_col.add_paragraph()
    p_col2.text = "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING | U21CS504 — WEB TECHNOLOGIES LAB"
    p_col2.font.size = Pt(10)
    p_col2.font.color.rgb = COLOR_CYAN
    p_col2.font.name = FONT_FAMILY

    # Main Project Title Card
    main_card = add_card(slide1, Inches(0.9), Inches(1.9), Inches(11.53), Inches(3.2), border_color=COLOR_PRIMARY_BLUE)
    
    # Title badge inside main card
    tag = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(2.15), Inches(3.0), Inches(0.35))
    tag.fill.solid()
    tag.fill.fore_color.rgb = RGBColor(30, 58, 138)
    tag.line.color.rgb = COLOR_CYAN
    tf_tag = tag.text_frame
    p_t = tf_tag.paragraphs[0]
    p_t.text = "MINI PROJECT PRESENTATION"
    p_t.font.size = Pt(10)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_WHITE
    p_t.alignment = PP_ALIGN.CENTER

    title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(2.55), Inches(10.9), Inches(2.2))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    
    p1 = tf_t.paragraphs[0]
    p1.text = "TASKFLOW: Priority-Driven Campus Task\nManagement & Posting System"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_WHITE
    p1.font.name = FONT_FAMILY

    p2 = tf_t.add_paragraph()
    p2.text = "Full-Stack Web Architecture Replication Using HTML5, CSS3, PHP, and Java Servlets"
    p2.font.size = Pt(14)
    p2.font.color.rgb = COLOR_CYAN
    p2.font.name = FONT_FAMILY

    p3 = tf_t.add_paragraph()
    p3.text = "Benchmark Source: 'Campity' Repository | Transformed to Campus Productivity Ecosystem"
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_TEXT_MUTED
    p3.font.name = FONT_FAMILY

    # Bottom Metadata Panel (Presenter & Key Specs)
    pres_card = add_card(slide1, Inches(0.9), Inches(5.3), Inches(5.6), Inches(1.6), border_color=COLOR_EMERALD)
    pres_box = slide1.shapes.add_textbox(Inches(1.1), Inches(5.4), Inches(5.2), Inches(1.4))
    tf_p = pres_box.text_frame
    tf_p.word_wrap = True
    pp1 = tf_p.paragraphs[0]
    pp1.text = "PRESENTED BY:"
    pp1.font.size = Pt(10)
    pp1.font.bold = True
    pp1.font.color.rgb = COLOR_EMERALD
    
    pp2 = tf_p.add_paragraph()
    pp2.text = "SANJAI M S"
    pp2.font.size = Pt(18)
    pp2.font.bold = True
    pp2.font.color.rgb = COLOR_TEXT_WHITE

    pp3 = tf_p.add_paragraph()
    pp3.text = "Register No: 24CS181 | B.E. Computer Science and Engineering"
    pp3.font.size = Pt(10.5)
    pp3.font.color.rgb = COLOR_TEXT_LIGHT

    # Key Architectural Pillars Panel
    pillar_card = add_card(slide1, Inches(6.8), Inches(5.3), Inches(5.63), Inches(1.6))
    pil_box = slide1.shapes.add_textbox(Inches(7.0), Inches(5.4), Inches(5.2), Inches(1.4))
    tf_pil = pil_box.text_frame
    tf_pil.word_wrap = True
    
    pil1 = tf_pil.paragraphs[0]
    pil1.text = "CORE ARCHITECTURAL PILLARS"
    pil1.font.size = Pt(10)
    pil1.font.bold = True
    pil1.font.color.rgb = COLOR_CYAN

    bullet_items = [
        "⚡ Dual-Stack Engine: PHP 8.x (SQLite PDO) & Java EE 4.0 (HttpServer / Servlets)",
        "🎯 Algorithmic Dispatch: Dynamic Max-Heap Priority Queue (Urgency + Bounty + Deadline)",
        "🛡️ 10% Collateral Escrow: Requester deposit lock + helper stake accountability protocol"
    ]
    for b in bullet_items:
        p_b = tf_pil.add_paragraph()
        p_b.text = b
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = COLOR_TEXT_LIGHT

    # =========================================================================
    # SLIDE 2: MOTIVATION, PROBLEM STATEMENT & BENCHMARK SELECTION
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Motivation, Problem Statement & Benchmark Selection", 
               "TaskFlow Project Report — Chapters 1 & 2", 
               "Systematic analysis of 30+ workspace web applications and transformation into a production academic utility")

    # Column 1: Campus Problem Statement & Objectives
    col1_card = add_card(slide2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    c1_box = slide2.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.2), Inches(5.1))
    tf_c1 = c1_box.text_frame
    tf_c1.word_wrap = True

    h1 = tf_c1.paragraphs[0]
    h1.text = "🚨 Campus Errand Crisis & Problem Statement"
    h1.font.size = Pt(13)
    h1.font.bold = True
    h1.font.color.rgb = COLOR_AMBER

    p_body1 = tf_c1.add_paragraph()
    p_body1.text = (
        "In modern university environments, students and faculty face critical, time-sensitive micro-tasks:\n"
        "• Emergency lab hardware transfers & multimeter swaps\n"
        "• Immediate library textbook retrieval before cutoff hours\n"
        "• Peer code reviews, debugging, and academic note sharing\n"
        "• Prescription medicine deliveries during illness\n\n"
        "Current channels (WhatsApp / Telegram groups) suffer from critical failures:\n"
        "1. Feed Congestion: Urgent requests are buried under general chatter.\n"
        "2. Zero Commitment: No collateral, leading to frequent task abandonment.\n"
        "3. Financial Risk: Unprotected transfers with no escrow guarantees."
    )
    p_body1.font.size = Pt(10)
    p_body1.font.color.rgb = COLOR_TEXT_LIGHT

    h2 = tf_c1.add_paragraph()
    h2.text = "\n🎯 Core Engineering Objectives"
    h2.font.size = Pt(12)
    h2.font.bold = True
    h2.font.color.rgb = COLOR_EMERALD

    p_body2 = tf_c1.add_paragraph()
    p_body2.text = (
        "• Develop an Intelligent Priority Queue ensuring emergency errands appear first.\n"
        "• Establish a Dual-Sided Escrow Protocol protecting requester funds and helper effort.\n"
        "• Build dual-stack replication (PHP & Java Servlets) sharing a unified modern UI."
    )
    p_body2.font.size = Pt(10)
    p_body2.font.color.rgb = COLOR_TEXT_LIGHT

    # Column 2: Workspace Benchmarking & Domain Transformation
    col2_card = add_card(slide2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    c2_box = slide2.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.1))
    tf_c2 = c2_box.text_frame
    tf_c2.word_wrap = True

    h3 = tf_c2.paragraphs[0]
    h3.text = "📊 Workspace Web Benchmark (30+ Projects Surveyed)"
    h3.font.size = Pt(13)
    h3.font.bold = True
    h3.font.color.rgb = COLOR_CYAN

    p_body3 = tf_c2.add_paragraph()
    p_body3.text = (
        "Three architectural tiers were surveyed across the student workspace:\n"
        "• Tier 1 (Beginner): Digital-Checkpoint-System, quiet-scan, biosite. Minimal schemas, single-route Flask/HTML without algorithmic depth.\n"
        "• Tier 2 (Enterprise): SDC Castle Enigma, Irrigation AI, ATM IoT. Multi-repo distributed architectures with high operational overhead.\n"
        "• Tier 3 (Chosen Benchmark): Campity. Balanced mid-level architecture featuring complete relational models, priority queue scheduling, and economic mechanics."
    )
    p_body3.font.size = Pt(10)
    p_body3.font.color.rgb = COLOR_TEXT_LIGHT

    h4 = tf_c2.add_paragraph()
    h4.text = "\n🔄 Academic Domain Transformation"
    h4.font.size = Pt(12)
    h4.font.bold = True
    h4.font.color.rgb = COLOR_PRIMARY_BLUE

    p_body4 = tf_c2.add_paragraph()
    p_body4.text = (
        "Transformed fantasy RPG jargon into a professional campus task platform:\n"
        "• 'Quests / Bounties' ➔ Campus Micro-Tasks & Deliverables\n"
        "• 'Adventurers' ➔ Registered Student Taskers\n"
        "• 'Guild Ranks' ➔ Tasker Proficiency Tiers (Junior ➔ Lead Coordinator)\n"
        "• 'Mora / Gems' ➔ Campus Task Credits (Escrow held)"
    )
    p_body4.font.size = Pt(10)
    p_body4.font.color.rgb = COLOR_TEXT_LIGHT

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & DUAL-STACK IMPLEMENTATION
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "System Architecture & Dual-Stack Implementation", 
               "TaskFlow Project Report — Chapters 3 & 6", 
               "High-performance 3-tier dual-engine architecture sharing presentation assets and relational schema")

    # Left: Architecture Diagram
    diag_card = add_card(slide3, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.4))
    arch_img = "report_figures/fig3_1_architecture.png"
    if os.path.exists(arch_img):
        slide3.shapes.add_picture(arch_img, Inches(0.95), Inches(1.65), width=Inches(5.7))

    # Right: Stack Details & Relational Schema
    right_card = add_card(slide3, Inches(7.1), Inches(1.5), Inches(5.4), Inches(5.4))
    r_box = slide3.shapes.add_textbox(Inches(7.25), Inches(1.65), Inches(5.1), Inches(5.1))
    tf_r = r_box.text_frame
    tf_r.word_wrap = True

    rh1 = tf_r.paragraphs[0]
    rh1.text = "🏛️ 3-Tier Dual-Engine Stack Comparison"
    rh1.font.size = Pt(13)
    rh1.font.bold = True
    rh1.font.color.rgb = COLOR_CYAN

    rp1 = tf_r.add_paragraph()
    rp1.text = (
        "1. Shared Presentation Tier:\n"
        "   • CSS3 variables theme system (Dark Modern, Clean Light, Slate, Emerald)\n"
        "   • Modular SaaS cards, responsive grid, dynamic stake calculation via app.js\n\n"
        "2. PHP Application Tier (Port 8000):\n"
        "   • SQLite PDO persistence with auto-migration schema\n"
        "   • Bcrypt password hashing, session state, REST API endpoint\n\n"
        "3. Java Servlets Application Tier (Port 8080):\n"
        "   • Java EE 4.0 architecture with pure JDBC Data Access Objects (DAO)\n"
        "   • Standalone JDK EmbeddedServer (com.campity.server.EmbeddedServer)\n"
        "   • In-memory java.util.PriorityQueue Max-Heap algorithm"
    )
    rp1.font.size = Pt(9.5)
    rp1.font.color.rgb = COLOR_TEXT_LIGHT

    rh2 = tf_r.add_paragraph()
    rh2.text = "\n🗄️ Relational Schema (ACID Compliant)"
    rh2.font.size = Pt(12)
    rh2.font.bold = True
    rh2.font.color.rgb = COLOR_EMERALD

    rp2 = tf_r.add_paragraph()
    rp2.text = (
        "• USERS: id, username, email, password, credits, xp, rank, rating\n"
        "• QUESTS (Tasks): id, title, description, category, reward, priority,\n"
        "  deadline, status (OPEN, CLAIMED, SUBMITTED, COMPLETED), created_by, assigned_to\n"
        "• TRANSACTIONS: id, user_id, quest_id, amount, type, created_at\n"
        "Enforces strict foreign keys and atomic balance reconciliation."
    )
    rp2.font.size = Pt(9.5)
    rp2.font.color.rgb = COLOR_TEXT_LIGHT

    # =========================================================================
    # SLIDE 4: THE INTELLIGENT PRIORITY QUEUE SCHEDULING ALGORITHM
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Intelligent Priority Queue Scheduling Engine", 
               "TaskFlow Project Report — Chapter 4", 
               "Mathematical priority scoring model ensuring campus emergencies bypass general errand clutter")

    # Left: Mathematical Formulation & Weights Table
    left_card = add_card(slide4, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4))
    l_box = slide4.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.4), Inches(5.1))
    tf_l = l_box.text_frame
    tf_l.word_wrap = True

    lh1 = tf_l.paragraphs[0]
    lh1.text = "📐 Algorithmic Formulation & Scoring Model"
    lh1.font.size = Pt(13)
    lh1.font.bold = True
    lh1.font.color.rgb = COLOR_PRIMARY_BLUE

    lp1 = tf_l.add_paragraph()
    lp1.text = (
        "Every posted task is dynamically scored upon insertion and dispatch:\n\n"
        "Priority Score = (Category Weight × 10) + (Reward × 0.5) + Urgency Bonus\n\n"
        "Where Urgency Bonus scales as deadline approaches:\n"
        "• < 2 Hours remaining: +50 Points\n"
        "• < 6 Hours remaining: +30 Points\n"
        "• < 24 Hours remaining: +15 Points"
    )
    lp1.font.size = Pt(10)
    lp1.font.color.rgb = COLOR_TEXT_LIGHT

    lh2 = tf_l.add_paragraph()
    lh2.text = "\n🏷️ Category Urgency Weight Matrix"
    lh2.font.size = Pt(12)
    lh2.font.bold = True
    lh2.font.color.rgb = COLOR_CYAN

    lp2 = tf_l.add_paragraph()
    lp2.text = (
        "• Medical / Health: 100 pts (Emergency medications, first aid)\n"
        "• Urgent / Time-Sensitive: 90 pts (Expiring lab submissions, passes)\n"
        "• Tech & Hardware Support: 70 pts (Lab equipment troubleshooting)\n"
        "• Academics & Notes: 60 pts (Exam prep, peer tutoring assistance)\n"
        "• Campus Logistics & Delivery: 50 pts (Library book returns, parcels)\n"
        "• General Assistance & Labor: 40 pts (Campus event setup, cleaning)"
    )
    lp2.font.size = Pt(9.5)
    lp2.font.color.rgb = COLOR_TEXT_LIGHT

    # Right: Flowchart & Heap Complexity
    right_card4 = add_card(slide4, Inches(6.9), Inches(1.5), Inches(5.63), Inches(5.4))
    flow_img = "report_figures/fig4_1_algorithm_flowchart.png"
    if os.path.exists(flow_img):
        slide4.shapes.add_picture(flow_img, Inches(7.05), Inches(1.65), width=Inches(5.3))

    r4_box = slide4.shapes.add_textbox(Inches(7.1), Inches(4.35), Inches(5.2), Inches(2.3))
    tf_r4 = r4_box.text_frame
    tf_r4.word_wrap = True

    r4h = tf_r4.paragraphs[0]
    r4h.text = "⚡ Algorithmic Data Structures & Complexity"
    r4h.font.size = Pt(11.5)
    r4h.font.bold = True
    r4h.font.color.rgb = COLOR_EMERALD

    r4p = tf_r4.add_paragraph()
    r4p.text = (
        "• Java Servlets Engine: Binary Max-Heap via java.util.PriorityQueue\n"
        "  - Insertion: O(log N) | Priority Peek: O(1) | Poll: O(log N)\n"
        "• PHP Engine: In-memory dynamic quick-sort comparator\n"
        "  - O(N log N) sorting for dashboard priority feeds\n"
        "• REST API Endpoint: /api/quests/prioritized delivers pre-sorted JSON directly to client dashboards."
    )
    r4p.font.size = Pt(9)
    r4p.font.color.rgb = COLOR_TEXT_LIGHT

    # =========================================================================
    # SLIDE 5: CORE BUSINESS LOGIC & FINANCIAL ESCROW PROTOCOL
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Core Business Logic & Financial Escrow Protocol", 
               "TaskFlow Project Report — Chapter 5", 
               "Two-sided economic collateral protocol and multi-state task verification machine")

    # Left: State Machine Visual
    sm_card = add_card(slide5, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.4))
    sm_img = "report_figures/fig5_1_state_machine.png"
    if os.path.exists(sm_img):
        slide5.shapes.add_picture(sm_img, Inches(0.95), Inches(1.65), width=Inches(5.7))

    sm_box = slide5.shapes.add_textbox(Inches(1.0), Inches(4.6), Inches(5.6), Inches(2.1))
    tf_sm = sm_box.text_frame
    tf_sm.word_wrap = True
    smh = tf_sm.paragraphs[0]
    smh.text = "🔄 Lifecycle State Machine"
    smh.font.size = Pt(11.5)
    smh.font.bold = True
    smh.font.color.rgb = COLOR_AMBER
    smp = tf_sm.add_paragraph()
    smp.text = (
        "1. OPEN: Posted with full bounty locked in escrow.\n"
        "2. CLAIMED: Assigned helper locks 10% collateral stake.\n"
        "3. SUBMITTED: Deliverables uploaded; requester notified.\n"
        "4. COMPLETED: Payout released + stake refunded + XP granted."
    )
    smp.font.size = Pt(9.5)
    smp.font.color.rgb = COLOR_TEXT_LIGHT

    # Right: Escrow Protocol & Reputation Progression
    proto_card = add_card(slide5, Inches(7.1), Inches(1.5), Inches(5.4), Inches(5.4))
    p_box = slide5.shapes.add_textbox(Inches(7.25), Inches(1.65), Inches(5.1), Inches(5.1))
    tf_p5 = p_box.text_frame
    tf_p5.word_wrap = True

    ph1 = tf_p5.paragraphs[0]
    ph1.text = "🛡️ Two-Phase Escrow & Stake Protection"
    ph1.font.size = Pt(13)
    ph1.font.bold = True
    ph1.font.color.rgb = COLOR_EMERALD

    pp1 = tf_p5.add_paragraph()
    pp1.text = (
        "• Solvency Guarantee: Requester deposits reward upfront upon task creation. Avoids student non-payment disputes.\n"
        "• 10% Helper Accountability Stake: To claim an errand, the helper locks a 10% collateral stake. Eradicates task hoarding and frivolous acceptance.\n"
        "• Verified Settlement: Only when requester confirms delivery does escrow release to helper alongside their 10% stake refund."
    )
    pp1.font.size = Pt(9.5)
    pp1.font.color.rgb = COLOR_TEXT_LIGHT

    ph2 = tf_p5.add_paragraph()
    ph2.text = "\n🏆 Reputation & Tier Progression"
    ph2.font.size = Pt(12)
    ph2.font.bold = True
    ph2.font.color.rgb = COLOR_CYAN

    pp2 = tf_p5.add_paragraph()
    pp2.text = (
        "Completed tasks award +25 XP and peer star ratings (1-5):\n"
        "• Junior Tasker: 0 – 99 XP (Basic campus errands)\n"
        "• Associate Tasker: 100 – 299 XP (Higher reward limits)\n"
        "• Senior Tasker: 300 – 699 XP (Hardware & lab access)\n"
        "• Lead Coordinator: 700+ XP (Department-wide delegation)\n"
        "All transactions are logged to an immutable ledger."
    )
    pp2.font.size = Pt(9.5)
    pp2.font.color.rgb = COLOR_TEXT_LIGHT

    # =========================================================================
    # SLIDE 6: PERFORMANCE EVALUATION, DELIVERABLES & CONCLUSION
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Experimental Benchmarking & Project Conclusion", 
               "TaskFlow Project Report — Chapters 7 & 8", 
               "Empirical performance testing, production deliverables, and future academic extensions")

    # Left: Performance Graph
    bench_card = add_card(slide6, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4))
    bench_img = "report_figures/fig7_1_performance_benchmark.png"
    if os.path.exists(bench_img):
        slide6.shapes.add_picture(bench_img, Inches(0.95), Inches(1.65), width=Inches(5.5))

    b_box = slide6.shapes.add_textbox(Inches(1.0), Inches(4.35), Inches(5.4), Inches(2.3))
    tf_b6 = b_box.text_frame
    tf_b6.word_wrap = True
    bh = tf_b6.paragraphs[0]
    bh.text = "📈 Empirical Benchmarking Results"
    bh.font.size = Pt(11.5)
    bh.font.bold = True
    bh.font.color.rgb = COLOR_CYAN
    bp = tf_b6.add_paragraph()
    bp.text = (
        "• Java Servlets Stack: 9.2 ms avg response latency under 50 concurrent connections; in-memory Max-Heap delivers sub-millisecond priority peeking.\n"
        "• PHP Stack: 18.4 ms avg response latency; zero configuration, ultra-lightweight SQLite PDO connection footprint.\n"
        "• ACID Integrity: Zero transaction lockouts and 100% balance consistency across high-concurrency automated test harnesses."
    )
    bp.font.size = Pt(9)
    bp.font.color.rgb = COLOR_TEXT_LIGHT

    # Right: Deliverables, Impact & Future Scope
    deliv_card = add_card(slide6, Inches(6.9), Inches(1.5), Inches(5.63), Inches(5.4))
    d_box = slide6.shapes.add_textbox(Inches(7.1), Inches(1.65), Inches(5.2), Inches(5.1))
    tf_d = d_box.text_frame
    tf_d.word_wrap = True

    dh1 = tf_d.paragraphs[0]
    dh1.text = "📦 Production Deliverables Completed"
    dh1.font.size = Pt(13)
    dh1.font.bold = True
    dh1.font.color.rgb = COLOR_EMERALD

    dp1 = tf_d.add_paragraph()
    dp1.text = (
        "✅ Standalone Java Executable (com.campity.server.EmbeddedServer)\n"
        "✅ Production PHP 8.x Web Application with SQLite auto-migrations\n"
        "✅ Live GitHub IO Interactive Web Portal & Priority Queue Simulator\n"
        "✅ Comprehensive 8-Chapter Academic Project Report (.pdf & .docx)\n"
        "✅ Executive 6-Slide Presentation (.pptx) by Sanjai M S"
    )
    dp1.font.size = Pt(9.5)
    dp1.font.color.rgb = COLOR_TEXT_LIGHT

    dh2 = tf_d.add_paragraph()
    dh2.text = "\n🚀 Future Research & Enhancements"
    dh2.font.size = Pt(12)
    dh2.font.bold = True
    dh2.font.color.rgb = COLOR_AMBER

    dp2 = tf_d.add_paragraph()
    dp2.text = (
        "• Push Notifications: WebSockets / SSE for instant emergency alerts.\n"
        "• GPS Geofencing: Prioritizing tasks based on building proximity.\n"
        "• Cryptographic QR Verification: Handshake delivery confirmation.\n"
        "• Mobile Flutter Client: Connecting to the unified REST API backend."
    )
    dp2.font.size = Pt(9.5)
    dp2.font.color.rgb = COLOR_TEXT_LIGHT

    # Save presentation
    output_filename = "TaskFlow_Presentation.pptx"
    prs.save(output_filename)
    print(f"Successfully generated {output_filename}")
    return output_filename

if __name__ == "__main__":
    build_presentation()
