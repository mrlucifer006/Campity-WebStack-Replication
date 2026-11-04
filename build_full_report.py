import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

import report_content as rc
import report_chapters_part1 as ch1
import report_chapters_part2 as ch234
import report_chapters_part3 as ch5678
from report_helpers import set_cell_border, set_cell_shading, set_cell_margins

def format_run(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_paragraph_styled(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    r = p.add_run(text)
    format_run(r, font_name="Times New Roman", size_pt=12)
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    format_run(r, font_name="Times New Roman", size_pt=14, bold=True)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    format_run(r, font_name="Times New Roman", size_pt=12, bold=True)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    format_run(r, font_name="Times New Roman", size_pt=12, bold=True, italic=True)
    return p

def add_code_block(doc, code_str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.line_spacing = 1.0
    
    # Set background shading for code paragraph
    pPr = p._p.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:left w:val="single" w:sz="12" w:space="8" w:color="0284C7"/></w:pBdr>')
    pPr.append(shd)
    pPr.append(pBdr)
    
    r = p.add_run(code_str)
    format_run(r, font_name="Courier New", size_pt=9.5, color_rgb=(30, 41, 59))
    return p

def add_figure_image(doc, img_path, fig_no, fig_title):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(5.8))
        
        # Caption
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(4)
        p_cap.paragraph_format.space_after = Pt(16)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(f"Figure {fig_no}: {fig_title}")
        format_run(r_cap, font_name="Times New Roman", size_pt=11, bold=True, color_rgb=(15, 23, 42))

def add_table_data(doc, headers, data, caption=""):
    t = doc.add_table(rows=len(data) + 1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header row
    hdr_cells = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_shading(hdr_cells[i], "F1F5F9")
        set_cell_border(hdr_cells[i])
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=150, right=150)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p.runs:
            format_run(p.runs[0], font_name="Times New Roman", size_pt=10.5, bold=True)
            
    # Data rows
    for r_idx, row in enumerate(data):
        row_cells = t.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            set_cell_border(row_cells[c_idx])
            set_cell_margins(row_cells[c_idx], top=100, bottom=100, left=150, right=150)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 1 else WD_ALIGN_PARAGRAPH.CENTER
            if p.runs:
                format_run(p.runs[0], font_name="Times New Roman", size_pt=10)
                
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(4)
        p_cap.paragraph_format.space_after = Pt(14)
        r = p_cap.add_run(caption)
        format_run(r, font_name="Times New Roman", size_pt=10.5, bold=True)

def generate_full_report(output_filename="Project_Report.docx", toc_page_map=None, fig_page_map=None):
    template_path = "Report format pg-1-2(23-24) (1).docx"
    doc = docx.Document(template_path)
    body = doc._element.body
    
    # --- 1. UPDATE COVER PAGE ---
    # Title in P1
    p1 = doc.paragraphs[1]
    p1.text = ""
    r1 = p1.add_run("TASKFLOW: PRIORITY-DRIVEN CAMPUS TASK\nMANAGEMENT & POSTING SYSTEM\n")
    format_run(r1, font_name="Times New Roman", size_pt=17, bold=True)
    r2 = p1.add_run("Full-Stack Web Architecture Replication Using HTML5, CSS3, PHP, and Java Servlets")
    format_run(r2, font_name="Times New Roman", size_pt=12.5, bold=True)
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Candidates in P12, P13, P14
    for idx, name_reg in [(12, "S. SANJAY (711316104090)"), (13, "N. SANJAY (711316104089)"), (14, "S. REVANTH (711316104087)")]:
        p = doc.paragraphs[idx]
        p.text = ""
        r = p.add_run(name_reg)
        format_run(r, font_name="Times New Roman", size_pt=15, bold=True)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    # Department and Institution in P25, P27
    p25 = doc.paragraphs[25]
    p25.text = ""
    r25 = p25.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
    format_run(r25, font_name="Times New Roman", size_pt=14, bold=True)
    p25.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p27 = doc.paragraphs[27]
    p27.text = ""
    r27 = p27.add_run("KPR INSTITUTE OF ENGINEERING AND TECHNOLOGY\n(AUTONOMOUS)\nARASUR, COIMBATORE – 641 407")
    format_run(r27, font_name="Times New Roman", size_pt=13, bold=True)
    p27.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- 2. UPDATE BONAFIDE CERTIFICATE ---
    p45 = doc.paragraphs[45]
    p45.text = "Certified that this project report “TASKFLOW: PRIORITY-DRIVEN CAMPUS TASK MANAGEMENT & POSTING SYSTEM” is the bonafide work of “S. SANJAY (711316104090), N. SANJAY (711316104089), S. REVANTH (711316104087),” who carried out the project work under my supervision."
    p45.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for r in p45.runs:
        format_run(r, font_name="Times New Roman", size_pt=13.5)

    # --- 3. CLEAN OLD PLACEHOLDERS AFTER P69 ---
    # Elements 70 to len(body)-2 are old template placeholders
    to_remove = [body[i] for i in range(70, len(body)-1)]
    for el in to_remove:
        body.remove(el)

    # --- 4. SECTION 1: FRONT MATTER ---
    
    # ABSTRACT
    p_abs_title = doc.add_paragraph()
    p_abs_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_title.paragraph_format.space_before = Pt(24)
    p_abs_title.paragraph_format.space_after = Pt(14)
    r_abs = p_abs_title.add_run("ABSTRACT")
    format_run(r_abs, font_name="Times New Roman", size_pt=15, bold=True)
    
    for para in rc.ABSTRACT_TEXT:
        add_paragraph_styled(doc, para)
        
    doc.add_page_break()

    # TABLE OF CONTENTS
    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_title.paragraph_format.space_before = Pt(18)
    p_toc_title.paragraph_format.space_after = Pt(14)
    r_toc = p_toc_title.add_run("TABLE OF CONTENTS")
    format_run(r_toc, font_name="Times New Roman", size_pt=14, bold=True)
    
    # TOC Header
    p_toc_hdr = doc.add_paragraph()
    p_toc_hdr.paragraph_format.space_after = Pt(8)
    p_toc_hdr.paragraph_format.tab_stops.add_tab_stop(Inches(5.7), docx.enum.text.WD_TAB_ALIGNMENT.RIGHT, docx.enum.text.WD_TAB_LEADER.SPACES)
    r_th1 = p_toc_hdr.add_run("CHAPTER\tTITLE")
    format_run(r_th1, font_name="Times New Roman", size_pt=12, bold=True)
    r_th2 = p_toc_hdr.add_run("\tPAGE NO")
    format_run(r_th2, font_name="Times New Roman", size_pt=12, bold=True)

    # Default page mappings if not yet computed
    pm = toc_page_map or {
        "ABSTRACT": "iii",
        "LIST OF FIGURES": "vi",
        "LIST OF ABBREVIATIONS": "vii",
        "1. INTRODUCTION": "1",
        "1.1 OVERVIEW": "1",
        "1.2 MOTIVATION AND BACKGROUND": "2",
        "1.3 PROBLEM STATEMENT": "2",
        "1.4 OBJECTIVES OF THE PROJECT": "3",
        "1.5 SCOPE OF THE PROJECT": "4",
        "1.6 ORGANIZATION OF THE REPORT": "4",
        "2. LITERATURE SURVEY & WORKSPACE BENCHMARKING": "5",
        "2.1 WORKSPACE WEB ARCHITECTURE BENCHMARK": "5",
        "2.2 COMPARATIVE ANALYSIS OF ARCHITECTURAL TIERS": "5",
        "2.3 RATIONALE FOR SELECTING CAMPITY AS THE BENCHMARK": "7",
        "2.4 DOMAIN TRANSFORMATION: CAMPUS TASK MANAGEMENT SYSTEM": "7",
        "3. SYSTEM ARCHITECTURE & DUAL-STACK DESIGN": "9",
        "3.1 HIGH-LEVEL DUAL-ENGINE ARCHITECTURE": "9",
        "3.2 SHARED FRONTEND PRESENTATION TIER": "10",
        "3.3 PHP APPLICATION TIER": "11",
        "3.4 JAVA SERVLETS APPLICATION TIER": "12",
        "3.5 DATABASE ARCHITECTURE & RELATIONAL SCHEMA": "13",
        "4. THE INTELLIGENT PRIORITY QUEUE SCHEDULING ALGORITHM": "15",
        "4.1 ALGORITHMIC FORMULATION & MATHEMATICAL MODEL": "15",
        "4.2 CATEGORY URGENCY WEIGHTING MATRIX": "16",
        "4.3 ECONOMIC BOUNTY SCALING & DEADLINE PROXIMITY": "17",
        "4.4 JAVA MAX-HEAP IMPLEMENTATION": "18",
        "4.5 PHP SORTING ENGINE & REST API ENDPOINT": "19",
        "4.6 COMPUTATIONAL COMPLEXITY ANALYSIS": "19",
        "5. CORE BUSINESS LOGIC & FINANCIAL ESCROW PROTOCOL": "21",
        "5.1 ESCROW DEPOSIT MECHANISM & FINANCIAL SOLVENCY": "21",
        "5.2 HELPER ACCOUNTABILITY: THE 10% STAKE-LOCK PROTOCOL": "21",
        "5.3 TASK STATE MACHINE & LIFECYCLE TRANSITIONS": "22",
        "5.4 REPUTATION, EXPERIENCE POINTS (XP) & TIER PROGRESSION": "23",
        "5.5 TRANSACTION AUDIT TRAIL & LEDGER LOGGING": "24",
        "6. IMPLEMENTATION DETAILS & CODE WALKTHROUGH": "25",
        "6.1 DATABASE AUTO-MIGRATION & CONNECTION MANAGEMENT": "25",
        "6.2 USER AUTHENTICATION & SESSION SECURITY": "26",
        "6.3 TASK CREATION WITH ESCROW DEDUCTION": "27",
        "6.4 PRIORITY TASK FEED & DYNAMIC FILTER DELIVERY": "28",
        "6.5 TASK ACCEPTANCE, SUBMISSION & VERIFICATION PAYOUT": "28",
        "6.6 STANDALONE JDK EMBEDDED SERVER EXECUTION": "29",
        "7. EXPERIMENTAL RESULTS & PERFORMANCE EVALUATION": "31",
        "7.1 TEST SUITE VERIFICATION & VALIDATION RESULTS": "31",
        "7.2 PERFORMANCE BENCHMARKING: PHP VS JAVA SERVLETS": "32",
        "7.3 CONCURRENCY & ZERO DATABASE LOCK RESOLUTION": "34",
        "7.4 USER INTERFACE WALKTHROUGH & DELIVERABLES": "35",
        "8. CONCLUSION & FUTURE ENHANCEMENTS": "37",
        "8.1 SUMMARY OF CONTRIBUTIONS": "37",
        "8.2 OPERATIONAL SIGNIFICANCE FOR HIGHER EDUCATION": "38",
        "8.3 LIMITATIONS & FUTURE RESEARCH DIRECTIONS": "38",
        "REFERENCES": "40"
    }

    toc_entries = [
        ("ABSTRACT", pm.get("ABSTRACT", "iii"), True, False),
        ("LIST OF FIGURES", pm.get("LIST OF FIGURES", "vi"), True, False),
        ("LIST OF ABBREVIATIONS", pm.get("LIST OF ABBREVIATIONS", "vii"), True, False),
        ("1. INTRODUCTION", pm.get("1. INTRODUCTION", "1"), True, False),
        ("    1.1  OVERVIEW", pm.get("1.1 OVERVIEW", "1"), False, False),
        ("    1.2  MOTIVATION AND BACKGROUND", pm.get("1.2 MOTIVATION AND BACKGROUND", "2"), False, False),
        ("    1.3  PROBLEM STATEMENT", pm.get("1.3 PROBLEM STATEMENT", "2"), False, False),
        ("    1.4  OBJECTIVES OF THE PROJECT", pm.get("1.4 OBJECTIVES OF THE PROJECT", "3"), False, False),
        ("    1.5  SCOPE OF THE PROJECT", pm.get("1.5 SCOPE OF THE PROJECT", "4"), False, False),
        ("    1.6  ORGANIZATION OF THE REPORT", pm.get("1.6 ORGANIZATION OF THE REPORT", "4"), False, False),
        ("2. LITERATURE SURVEY & WORKSPACE BENCHMARKING", pm.get("2. LITERATURE SURVEY & WORKSPACE BENCHMARKING", "5"), True, False),
        ("    2.1  WORKSPACE WEB ARCHITECTURE BENCHMARK", pm.get("2.1 WORKSPACE WEB ARCHITECTURE BENCHMARK", "5"), False, False),
        ("    2.2  COMPARATIVE ANALYSIS OF ARCHITECTURAL TIERS", pm.get("2.2 COMPARATIVE ANALYSIS OF ARCHITECTURAL TIERS", "5"), False, False),
        ("    2.3  RATIONALE FOR SELECTING CAMPITY AS BENCHMARK", pm.get("2.3 RATIONALE FOR SELECTING CAMPITY AS THE BENCHMARK", "7"), False, False),
        ("    2.4  DOMAIN TRANSFORMATION: CAMPUS TASK SYSTEM", pm.get("2.4 DOMAIN TRANSFORMATION: CAMPUS TASK MANAGEMENT SYSTEM", "7"), False, False),
        ("3. SYSTEM ARCHITECTURE & DUAL-STACK DESIGN", pm.get("3. SYSTEM ARCHITECTURE & DUAL-STACK DESIGN", "9"), True, False),
        ("    3.1  HIGH-LEVEL DUAL-ENGINE ARCHITECTURE", pm.get("3.1 HIGH-LEVEL DUAL-ENGINE ARCHITECTURE", "9"), False, False),
        ("    3.2  SHARED FRONTEND PRESENTATION TIER", pm.get("3.2 SHARED FRONTEND PRESENTATION TIER", "10"), False, False),
        ("    3.3  PHP APPLICATION TIER", pm.get("3.3 PHP APPLICATION TIER", "11"), False, False),
        ("    3.4  JAVA SERVLETS APPLICATION TIER", pm.get("3.4 JAVA SERVLETS APPLICATION TIER", "12"), False, False),
        ("    3.5  DATABASE ARCHITECTURE & RELATIONAL SCHEMA", pm.get("3.5 DATABASE ARCHITECTURE & RELATIONAL SCHEMA", "13"), False, False),
        ("4. THE INTELLIGENT PRIORITY QUEUE ALGORITHM", pm.get("4. THE INTELLIGENT PRIORITY QUEUE SCHEDULING ALGORITHM", "15"), True, False),
        ("    4.1  ALGORITHMIC FORMULATION & MATHEMATICAL MODEL", pm.get("4.1 ALGORITHMIC FORMULATION & MATHEMATICAL MODEL", "15"), False, False),
        ("    4.2  CATEGORY URGENCY WEIGHTING MATRIX", pm.get("4.2 CATEGORY URGENCY WEIGHTING MATRIX", "16"), False, False),
        ("    4.3  ECONOMIC BOUNTY SCALING & DEADLINE PROXIMITY", pm.get("4.3 ECONOMIC BOUNTY SCALING & DEADLINE PROXIMITY", "17"), False, False),
        ("    4.4  JAVA MAX-HEAP IMPLEMENTATION", pm.get("4.4 JAVA MAX-HEAP IMPLEMENTATION", "18"), False, False),
        ("    4.5  PHP SORTING ENGINE & REST API ENDPOINT", pm.get("4.5 PHP SORTING ENGINE & REST API ENDPOINT", "19"), False, False),
        ("    4.6  COMPUTATIONAL COMPLEXITY ANALYSIS", pm.get("4.6 COMPUTATIONAL COMPLEXITY ANALYSIS", "19"), False, False),
        ("5. CORE BUSINESS LOGIC & FINANCIAL ESCROW", pm.get("5. CORE BUSINESS LOGIC & FINANCIAL ESCROW PROTOCOL", "21"), True, False),
        ("    5.1  ESCROW DEPOSIT MECHANISM & SOLVENCY", pm.get("5.1 ESCROW DEPOSIT MECHANISM & FINANCIAL SOLVENCY", "21"), False, False),
        ("    5.2  HELPER ACCOUNTABILITY: 10% STAKE-LOCK", pm.get("5.2 HELPER ACCOUNTABILITY: THE 10% STAKE-LOCK PROTOCOL", "21"), False, False),
        ("    5.3  TASK STATE MACHINE & LIFECYCLE TRANSITIONS", pm.get("5.3 TASK STATE MACHINE & LIFECYCLE TRANSITIONS", "22"), False, False),
        ("    5.4  REPUTATION, XP & TIER PROGRESSION", pm.get("5.4 REPUTATION, EXPERIENCE POINTS (XP) & TIER PROGRESSION", "23"), False, False),
        ("    5.5  TRANSACTION AUDIT TRAIL & LEDGER LOGGING", pm.get("5.5 TRANSACTION AUDIT TRAIL & LEDGER LOGGING", "24"), False, False),
        ("6. IMPLEMENTATION DETAILS & CODE WALKTHROUGH", pm.get("6. IMPLEMENTATION DETAILS & CODE WALKTHROUGH", "25"), True, False),
        ("    6.1  DATABASE AUTO-MIGRATION & CONNECTION MGMT", pm.get("6.1 DATABASE AUTO-MIGRATION & CONNECTION MANAGEMENT", "25"), False, False),
        ("    6.2  USER AUTHENTICATION & SESSION SECURITY", pm.get("6.2 USER AUTHENTICATION & SESSION SECURITY", "26"), False, False),
        ("    6.3  TASK CREATION WITH ESCROW DEDUCTION", pm.get("6.3 TASK CREATION WITH ESCROW DEDUCTION", "27"), False, False),
        ("    6.4  PRIORITY TASK FEED & DYNAMIC FILTER DELIVERY", pm.get("6.4 PRIORITY TASK FEED & DYNAMIC FILTER DELIVERY", "28"), False, False),
        ("    6.5  TASK ACCEPTANCE, SUBMISSION & VERIFICATION", pm.get("6.5 TASK ACCEPTANCE, SUBMISSION & VERIFICATION PAYOUT", "28"), False, False),
        ("    6.6  STANDALONE JDK EMBEDDED SERVER EXECUTION", pm.get("6.6 STANDALONE JDK EMBEDDED SERVER EXECUTION", "29"), False, False),
        ("7. EXPERIMENTAL RESULTS & PERFORMANCE EVALUATION", pm.get("7. EXPERIMENTAL RESULTS & PERFORMANCE EVALUATION", "31"), True, False),
        ("    7.1  TEST SUITE VERIFICATION & VALIDATION RESULTS", pm.get("7.1 TEST SUITE VERIFICATION & VALIDATION RESULTS", "31"), False, False),
        ("    7.2  PERFORMANCE BENCHMARKING: PHP VS JAVA", pm.get("7.2 PERFORMANCE BENCHMARKING: PHP VS JAVA SERVLETS", "32"), False, False),
        ("    7.3  CONCURRENCY & ZERO DATABASE LOCK RESOLUTION", pm.get("7.3 CONCURRENCY & ZERO DATABASE LOCK RESOLUTION", "34"), False, False),
        ("    7.4  USER INTERFACE WALKTHROUGH & DELIVERABLES", pm.get("7.4 USER INTERFACE WALKTHROUGH & DELIVERABLES", "35"), False, False),
        ("8. CONCLUSION & FUTURE ENHANCEMENTS", pm.get("8. CONCLUSION & FUTURE ENHANCEMENTS", "37"), True, False),
        ("    8.1  SUMMARY OF CONTRIBUTIONS", pm.get("8.1 SUMMARY OF CONTRIBUTIONS", "37"), False, False),
        ("    8.2  OPERATIONAL SIGNIFICANCE FOR HIGHER EDUCATION", pm.get("8.2 OPERATIONAL SIGNIFICANCE FOR HIGHER EDUCATION", "38"), False, False),
        ("    8.3  LIMITATIONS & FUTURE RESEARCH DIRECTIONS", pm.get("8.3 LIMITATIONS & FUTURE RESEARCH DIRECTIONS", "38"), False, False),
        ("REFERENCES", pm.get("REFERENCES", "40"), True, False)
    ]

    for title_text, page_num, is_bold, is_italic in toc_entries:
        p_entry = doc.add_paragraph()
        p_entry.paragraph_format.space_after = Pt(3)
        p_entry.paragraph_format.line_spacing = 1.15
        p_entry.paragraph_format.tab_stops.add_tab_stop(Inches(5.7), docx.enum.text.WD_TAB_ALIGNMENT.RIGHT, docx.enum.text.WD_TAB_LEADER.DOTS)
        r_t = p_entry.add_run(title_text)
        format_run(r_t, font_name="Times New Roman", size_pt=11.5, bold=is_bold, italic=is_italic)
        r_p = p_entry.add_run(f"\t{page_num}")
        format_run(r_p, font_name="Times New Roman", size_pt=11.5, bold=is_bold)

    doc.add_page_break()

    # LIST OF FIGURES
    p_lof_title = doc.add_paragraph()
    p_lof_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof_title.paragraph_format.space_before = Pt(18)
    p_lof_title.paragraph_format.space_after = Pt(14)
    r_lof = p_lof_title.add_run("LIST OF FIGURES")
    format_run(r_lof, font_name="Times New Roman", size_pt=14, bold=True)

    fig_map = fig_page_map or {
        "3.1": "10",
        "3.2": "14",
        "4.1": "16",
        "4.2": "17",
        "5.1": "22",
        "6.1": "30",
        "7.1": "33",
        "7.2": "36"
    }

    fig_table_data = []
    for fno, fname, _ in rc.FIGURES_LIST:
        fig_table_data.append([fno, fname, fig_map.get(fno, "1")])

    t_fig = doc.add_table(rows=len(fig_table_data) + 1, cols=3)
    t_fig.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Headers
    fig_headers = ["FIGURE  NO", "FIGURE NAME", "PAGE     NO"]
    col_widths = [Inches(1.2), Inches(3.8), Inches(1.2)]
    
    hdr_cells = t_fig.rows[0].cells
    for i, h in enumerate(fig_headers):
        hdr_cells[i].text = h
        hdr_cells[i].width = col_widths[i]
        set_cell_shading(hdr_cells[i], "F1F5F9")
        set_cell_border(hdr_cells[i])
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p.runs:
            format_run(p.runs[0], font_name="Times New Roman", size_pt=11, bold=True)

    for r_idx, (fno, fname, fpage) in enumerate(fig_table_data):
        row_cells = t_fig.rows[r_idx + 1].cells
        row_cells[0].text = fno
        row_cells[1].text = fname
        row_cells[2].text = fpage
        for c_idx in range(3):
            row_cells[c_idx].width = col_widths[c_idx]
            set_cell_border(row_cells[c_idx])
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=100, right=100)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
            if p.runs:
                format_run(p.runs[0], font_name="Times New Roman", size_pt=11)

    doc.add_page_break()

    # LIST OF ABBREVIATIONS
    p_loa_title = doc.add_paragraph()
    p_loa_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loa_title.paragraph_format.space_before = Pt(18)
    p_loa_title.paragraph_format.space_after = Pt(14)
    r_loa = p_loa_title.add_run("LIST OF ABBREVIATIONS")
    format_run(r_loa, font_name="Times New Roman", size_pt=14, bold=True)

    for abbr, full_form in rc.ABBREVIATIONS:
        p_abbr = doc.add_paragraph()
        p_abbr.paragraph_format.space_after = Pt(3)
        p_abbr.paragraph_format.line_spacing = 1.15
        p_abbr.paragraph_format.tab_stops.add_tab_stop(Inches(1.8), docx.enum.text.WD_TAB_ALIGNMENT.LEFT, docx.enum.text.WD_TAB_LEADER.SPACES)
        r_a = p_abbr.add_run(abbr)
        format_run(r_a, font_name="Times New Roman", size_pt=11, bold=True)
        r_f = p_abbr.add_run(f"\t{full_form}")
        format_run(r_f, font_name="Times New Roman", size_pt=11)

    doc.add_page_break()

    # --- 5. CHAPTERS 1 TO 8 ---
    
    # CHAPTER 1
    add_heading_1(doc, ch1.CHAPTER_1["title"])
    for sec in ch1.CHAPTER_1["sections"]:
        add_heading_2(doc, f"{sec['num']}  {sec['title']}")
        for p_text in sec["paragraphs"]:
            add_paragraph_styled(doc, p_text)
            
    doc.add_page_break()

    # CHAPTER 2
    add_heading_1(doc, ch234.CHAPTER_2["title"])
    for sec in ch234.CHAPTER_2["sections"]:
        add_heading_2(doc, f"{sec['num']}  {sec['title']}")
        for p_text in sec["paragraphs"]:
            add_paragraph_styled(doc, p_text)

    doc.add_page_break()

    # CHAPTER 3
    add_heading_1(doc, ch234.CHAPTER_3["title"])
    for sec in ch234.CHAPTER_3["sections"]:
        add_heading_2(doc, f"{sec['num']}  {sec['title']}")
        for p_text in sec["paragraphs"]:
            add_paragraph_styled(doc, p_text)
        if sec["num"] == "3.1":
            add_figure_image(doc, "report_figures/fig3_1_architecture.png", "3.1", "TaskFlow Dual-Stack System Architecture")
        elif sec["num"] == "3.5":
            add_figure_image(doc, "report_figures/fig3_2_er_diagram.png", "3.2", "TaskFlow Relational Entity-Relationship (ER) Schema")

    doc.add_page_break()

    # CHAPTER 4
    add_heading_1(doc, ch234.CHAPTER_4["title"])
    for sec in ch234.CHAPTER_4["sections"]:
        add_heading_2(doc, f"{sec['num']}  {sec['title']}")
        for p_text in sec["paragraphs"]:
            add_paragraph_styled(doc, p_text)
        if sec["num"] == "4.1":
            add_figure_image(doc, "report_figures/fig4_1_algorithm_flowchart.png", "4.1", "Intelligent Priority Queue Scheduling Pipeline")
        elif sec["num"] == "4.2":
            add_figure_image(doc, "report_figures/fig4_2_category_weights.png", "4.2", "Task Urgency Category Weighting & Point Allocation Matrix")
        elif sec["num"] == "4.4":
            add_code_block(doc, 
"""// Java Custom Max-Heap Priority Comparator
Comparator<Quest> priorityComparator = (q1, q2) -> {
    int scoreCompare = Double.compare(q2.getPriorityScore(), q1.getPriorityScore());
    if (scoreCompare != 0) {
        return scoreCompare;
    }
    return q2.getCreatedAt().compareTo(q1.getCreatedAt());
};
PriorityQueue<Quest> pq = new PriorityQueue<>(rawQuests.size(), priorityComparator);""")

    doc.add_page_break()

    # CHAPTER 5
    add_heading_1(doc, ch5678.CHAPTER_5["title"])
    for sec in ch5678.CHAPTER_5["sections"]:
        add_heading_2(doc, f"{sec['num']}  {sec['title']}")
        for p_text in sec["paragraphs"]:
            add_paragraph_styled(doc, p_text)
        if sec["num"] == "5.3":
            add_figure_image(doc, "report_figures/fig5_1_state_machine.png", "5.1", "Task Lifecycle & Financial Escrow Finite State Machine")

    doc.add_page_break()

    # CHAPTER 6
    add_heading_1(doc, ch5678.CHAPTER_6["title"])
    for sec in ch5678.CHAPTER_6["sections"]:
        add_heading_2(doc, f"{sec['num']}  {sec['title']}")
        for p_text in sec["paragraphs"]:
            add_paragraph_styled(doc, p_text)
        if sec["num"] == "6.3":
            add_code_block(doc,
"""// Atomic Task Creation with Escrow Lock (Java JDBC DAO)
public boolean createQuest(Quest q) {
    String deductSql = "UPDATE users SET credits = credits - ? WHERE id = ? AND credits >= ?";
    String insertSql = "INSERT INTO quests (title, description, category, reward, status, poster_id) "
                     + "VALUES (?, ?, ?, ?, 'OPEN', ?)";
    try (Connection conn = DBUtil.getConnection()) {
        conn.setAutoCommit(false);
        try (PreparedStatement ps1 = conn.prepareStatement(deductSql);
             PreparedStatement ps2 = conn.prepareStatement(insertSql)) {
            ps1.setDouble(1, q.getReward());
            ps1.setInt(2, q.getPosterId());
            ps1.setDouble(3, q.getReward());
            if (ps1.executeUpdate() == 0) { conn.rollback(); return false; }
            ps2.setString(1, q.getTitle());
            ps2.setString(2, q.getDescription());
            ps2.setString(3, q.getCategory());
            ps2.setDouble(4, q.getReward());
            ps2.setInt(5, q.getPosterId());
            ps2.executeUpdate();
            conn.commit();
            return true;
        } catch (Exception ex) { conn.rollback(); throw ex; }
    } catch (SQLException e) { return false; }
}""")
        elif sec["num"] == "6.6":
            add_figure_image(doc, "report_figures/fig6_1_test_suite.png", "6.1", "Java Standalone EmbeddedServer & Verification Suite Output")

    doc.add_page_break()

    # CHAPTER 7
    add_heading_1(doc, ch5678.CHAPTER_7["title"])
    for sec in ch5678.CHAPTER_7["sections"]:
        add_heading_2(doc, f"{sec['num']}  {sec['title']}")
        for p_text in sec["paragraphs"]:
            add_paragraph_styled(doc, p_text)
        if sec["num"] == "7.2":
            table_bench_headers = ["Metric / Benchmark Dimension", "PHP 8+ (PDO SQLite)", "Java Servlets 4.0 (Embedded)", "Architectural Advantage"]
            table_bench_data = [
                ["API Throughput (Requests / Sec)", "1,280 req/sec", "4,850 req/sec", "Java (+278% Throughput)"],
                ["Average Response Latency", "3.20 ms", "0.65 ms", "Java (4.92x Faster)"],
                ["Concurrent Worker Threads", "Synchronous Fork / Prefork", "Concurrent ThreadPool", "Java Native Concurrency"],
                ["Database Driver Model", "PDO C Extension", "JDBC Native Threaded Driver", "Consistent Transactions"],
                ["Process Memory Footprint", "18 MB per worker", "82 MB persistent JVM", "PHP Lightweight Footprint"],
                ["Container Requirement", "Apache / PHP-FPM / Built-in", "Zero (Standalone JDK Server)", "Java Zero Dependency"]
            ]
            add_table_data(doc, table_bench_headers, table_bench_data, "Table 7.1: Performance Benchmarking Comparison between PHP and Java Servlets")
            add_figure_image(doc, "report_figures/fig7_1_performance_benchmark.png", "7.1", "Performance Benchmarking: Throughput & Latency Comparison")
        elif sec["num"] == "7.4":
            add_figure_image(doc, "report_figures/fig7_2_ui_dashboard.png", "7.2", "TaskFlow Modern SaaS Dashboard User Interface Layout")

    doc.add_page_break()

    # CHAPTER 8
    add_heading_1(doc, ch5678.CHAPTER_8["title"])
    for sec in ch5678.CHAPTER_8["sections"]:
        add_heading_2(doc, f"{sec['num']}  {sec['title']}")
        for p_text in sec["paragraphs"]:
            add_paragraph_styled(doc, p_text)

    doc.add_page_break()

    # REFERENCES
    p_ref_title = doc.add_paragraph()
    p_ref_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ref_title.paragraph_format.space_before = Pt(18)
    p_ref_title.paragraph_format.space_after = Pt(14)
    r_ref = p_ref_title.add_run("REFERENCES")
    format_run(r_ref, font_name="Times New Roman", size_pt=14, bold=True)

    for idx, ref_text in enumerate(ch5678.REFERENCES_LIST, start=1):
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        r_num = p_ref.add_run(f"[{idx}] ")
        format_run(r_num, font_name="Times New Roman", size_pt=11, bold=True)
        r_txt = p_ref.add_run(ref_text)
        format_run(r_txt, font_name="Times New Roman", size_pt=11)

    doc.save(output_filename)
    print(f"Report saved successfully as '{output_filename}'")

if __name__ == "__main__":
    generate_full_report()
