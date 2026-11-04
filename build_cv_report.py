import os, sys, subprocess, re, shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

import cv_report_data as rd
from report_helpers import set_cell_border, set_cell_shading, set_cell_margins

def format_run(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_paragraph_styled(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=5, line_spacing=1.15):
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
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    format_run(r, font_name="Times New Roman", size_pt=14, bold=True)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    format_run(r, font_name="Times New Roman", size_pt=12.5, bold=True)
    return p

def add_bullet_point(doc, text, space_after=3):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    r_bullet = p.add_run("•  ")
    format_run(r_bullet, font_name="Times New Roman", size_pt=12, bold=True)
    r_text = p.add_run(text)
    format_run(r_text, font_name="Times New Roman", size_pt=12)
    return p

def add_code_block(doc, title, code_str):
    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_t.paragraph_format.space_before = Pt(10)
    p_t.paragraph_format.space_after = Pt(3)
    p_t.paragraph_format.keep_with_next = True
    r_t = p_t.add_run(title)
    format_run(r_t, font_name="Times New Roman", size_pt=11, bold=True, color_rgb=(15, 23, 42))

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.right_indent = Inches(0.2)
    p.paragraph_format.line_spacing = 1.0
    pPr = p._p.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:left w:val="single" w:sz="16" w:space="8" w:color="0284C7"/><w:top w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/><w:right w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/><w:bottom w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/></w:pBdr>')
    pPr.append(shd)
    pPr.append(pBdr)
    r = p.add_run(code_str)
    format_run(r, font_name="Courier New", size_pt=9.0, color_rgb=(30, 41, 59))
    return p

def add_figure_image(doc, img_path, fig_no, fig_title, width_in=5.4):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(3)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(3)
        p_cap.paragraph_format.space_after = Pt(12)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(f"Figure {fig_no}: {fig_title}")
        format_run(r_cap, font_name="Times New Roman", size_pt=10.5, bold=True, color_rgb=(15, 23, 42))

def add_table_data(doc, table_id, t_info):
    caption = t_info["caption"]
    headers = t_info["headers"]
    data = t_info["rows"]
    widths = t_info.get("widths", [1.0] * len(headers))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(10)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.keep_with_next = True
    r_cap = p_cap.add_run(caption)
    format_run(r_cap, font_name="Times New Roman", size_pt=10.5, bold=True, color_rgb=(15, 23, 42))

    t = doc.add_table(rows=len(data) + 1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_shading(hdr_cells[i], "F1F5F9")
        set_cell_border(hdr_cells[i], color="94A3B8")
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p.runs:
            format_run(p.runs[0], font_name="Times New Roman", size_pt=9.5, bold=True, color_rgb=(15, 23, 42))
            
    for r_idx, row in enumerate(data):
        row_cells = t.rows[r_idx + 1].cells
        bg_col = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            set_cell_shading(row_cells[c_idx], bg_col)
            set_cell_border(row_cells[c_idx], color="CBD5E1")
            set_cell_margins(row_cells[c_idx], top=65, bottom=65, left=100, right=100)
            p = row_cells[c_idx].paragraphs[0]
            if len(str(val)) < 15 and not (" " in str(val) and len(str(val)) > 8):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if p.runs:
                format_run(p.runs[0], font_name="Times New Roman", size_pt=9.0)
                
    for row in t.rows:
        for idx, w in enumerate(widths):
            row.cells[idx].width = Inches(w)
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(5)

def build_docx(output_path, toc_map, table_map, fig_map):
    template_path = "Report format pg-1-2(23-24) (1).docx"
    doc = docx.Document(template_path)
    body = doc._element.body
    
    # -------------------------------------------------------------
    # 1. UPDATE TITLE PAGE (PAGE 1)
    # -------------------------------------------------------------
    p1 = doc.paragraphs[1]
    p1.text = ""
    r1 = p1.add_run(rd.PROJECT_TITLE + "\n")
    format_run(r1, font_name="Times New Roman", size_pt=17, bold=True)
    r2 = p1.add_run(rd.PROJECT_SUBTITLE)
    format_run(r2, font_name="Times New Roman", size_pt=11.5, bold=True)
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER

    cand_strs = [f"{s['name']} ({s['reg']})" for s in rd.STUDENTS]
    doc.paragraphs[12].text = ""
    r = doc.paragraphs[12].add_run(cand_strs[0])
    format_run(r, font_name="Times New Roman", size_pt=14, bold=True)
    doc.paragraphs[12].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.paragraphs[13].text = ""
    r = doc.paragraphs[13].add_run(cand_strs[1])
    format_run(r, font_name="Times New Roman", size_pt=14, bold=True)
    doc.paragraphs[13].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.paragraphs[14].text = ""
    r = doc.paragraphs[14].add_run(f"{cand_strs[2]}\n{cand_strs[3]}\n{cand_strs[4]}")
    format_run(r, font_name="Times New Roman", size_pt=14, bold=True)
    doc.paragraphs[14].alignment = WD_ALIGN_PARAGRAPH.CENTER

    p20 = doc.paragraphs[20]
    p20.text = ""
    r20 = p20.add_run(rd.COURSE)
    format_run(r20, font_name="Times New Roman", size_pt=15, bold=True)
    p20.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p25 = doc.paragraphs[25]
    p25.text = ""
    r25 = p25.add_run(rd.BRANCH)
    format_run(r25, font_name="Times New Roman", size_pt=14, bold=True)
    p25.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p27 = doc.paragraphs[27]
    p27.text = ""
    r27 = p27.add_run(f"{rd.COLLEGE_NAME}\n{rd.COLLEGE_AUTONOMOUS}\n{rd.COLLEGE_LOCATION}\n{rd.UNIVERSITY}\n{rd.MONTH_YEAR}")
    format_run(r27, font_name="Times New Roman", size_pt=12.5, bold=True)
    p27.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Delete 14 empty paragraphs between P27 and P42 so Page 1 fits cleanly
    for idx in range(41, 27, -1):
        body.remove(doc.paragraphs[idx]._element)

    # -------------------------------------------------------------
    # 2. UPDATE BONAFIDE CERTIFICATE (PAGE 2)
    # -------------------------------------------------------------
    doc.paragraphs[28].paragraph_format.page_break_before = True

    p_cert = doc.paragraphs[31]
    all_cand_str = ", ".join([f"{s['name']} ({s['reg']})" for s in rd.STUDENTS])
    p_cert.text = f"Certified that this project report “{rd.PROJECT_TITLE}” is the bonafide work of “{all_cand_str},” who carried out the project work under my supervision."
    p_cert.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for r in p_cert.runs:
        format_run(r, font_name="Times New Roman", size_pt=13)

    # Supervisor & HOD info
    doc.paragraphs[38].text = f"{rd.HOD_NAME}\t{rd.SUPERVISOR_NAME}"
    doc.paragraphs[40].text = f"{rd.HOD_DESIG}\t\t{rd.SUPERVISOR_DESIG}"
    doc.paragraphs[41].text = f"{rd.HOD_TITLE}\t\t{rd.SUPERVISOR_TITLE}"
    doc.paragraphs[42].text = "Computer Science and Engineering        Computer Science and Engineering"
    doc.paragraphs[43].text = "KPR Institute of Engineering and\t KPR Institute of Engineering and"
    doc.paragraphs[44].text = "Technology\tTechnology"
    doc.paragraphs[45].text = "Arasur, Coimbatore – 641407\tArasur, Coimbatore – 641407"

    # Delete empty paragraphs on page 2 so it fits on exactly Page 2
    to_del_p2 = [54, 53, 52, 48, 47, 39, 37, 36, 35, 34, 33, 30]
    for idx in sorted(to_del_p2, reverse=True):
        body.remove(doc.paragraphs[idx]._element)

    p_exam_idx = 55 - len(to_del_p2)

    # Remove template placeholders after the examiner line
    for el in list(body)[body.index(doc.paragraphs[p_exam_idx]._element) + 1 : -1]:
        body.remove(el)

    # -------------------------------------------------------------
    # 3. ACKNOWLEDGEMENT (PAGE 3)
    # -------------------------------------------------------------
    p_ack_title = doc.add_paragraph()
    p_ack_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack_title.paragraph_format.space_before = Pt(20)
    p_ack_title.paragraph_format.space_after = Pt(12)
    r_ack = p_ack_title.add_run("ACKNOWLEDGEMENT")
    format_run(r_ack, font_name="Times New Roman", size_pt=15, bold=True)

    for p_txt in rd.ACKNOWLEDGEMENT_PARAS:
        add_paragraph_styled(doc, p_txt, space_after=4)

    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(14)
    p_sign.paragraph_format.space_after = Pt(8)
    for s in rd.STUDENTS:
        r_s = p_sign.add_run(f"{s['name']} ({s['reg']})\n")
        format_run(r_s, font_name="Times New Roman", size_pt=11, bold=True)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. ABSTRACT (PAGE 4)
    # -------------------------------------------------------------
    p_abs_title = doc.add_paragraph()
    p_abs_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_title.paragraph_format.space_before = Pt(20)
    p_abs_title.paragraph_format.space_after = Pt(12)
    r_abs = p_abs_title.add_run("ABSTRACT")
    format_run(r_abs, font_name="Times New Roman", size_pt=15, bold=True)

    for p_txt in rd.ABSTRACT_PARAS:
        add_paragraph_styled(doc, p_txt, space_after=5)

    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.space_before = Pt(8)
    p_kw.paragraph_format.space_after = Pt(10)
    r_kw_lbl = p_kw.add_run("Keywords: ")
    format_run(r_kw_lbl, font_name="Times New Roman", size_pt=11, bold=True, italic=True)
    r_kw_val = p_kw.add_run(rd.KEYWORDS)
    format_run(r_kw_val, font_name="Times New Roman", size_pt=11)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. TABLE OF CONTENTS (PAGE 5)
    # -------------------------------------------------------------
    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_title.paragraph_format.space_before = Pt(10)
    p_toc_title.paragraph_format.space_after = Pt(4)
    r_toc = p_toc_title.add_run("TABLE OF CONTENTS")
    format_run(r_toc, font_name="Times New Roman", size_pt=13.5, bold=True)

    p_toc_hdr = doc.add_paragraph()
    p_toc_hdr.paragraph_format.space_after = Pt(4)
    p_toc_hdr.paragraph_format.tab_stops.add_tab_stop(Inches(5.7), docx.enum.text.WD_TAB_ALIGNMENT.RIGHT, docx.enum.text.WD_TAB_LEADER.SPACES)
    r_th1 = p_toc_hdr.add_run("CHAPTER\tTITLE")
    format_run(r_th1, font_name="Times New Roman", size_pt=11, bold=True)
    r_th2 = p_toc_hdr.add_run("\tPAGE NO")
    format_run(r_th2, font_name="Times New Roman", size_pt=11, bold=True)

    toc_entries = [
        ("ABSTRACT", toc_map.get("ABSTRACT", "iv"), True),
        ("LIST OF TABLES", toc_map.get("LIST OF TABLES", "vi"), True),
        ("LIST OF FIGURES", toc_map.get("LIST OF FIGURES", "vii"), True),
        ("LIST OF ABBREVIATIONS", toc_map.get("LIST OF ABBREVIATIONS", "viii"), True),
        ("1. INTRODUCTION", toc_map.get("1. INTRODUCTION", "1"), True),
        ("    1.1  Objective of the Research Investigation", toc_map.get("1.1", "1"), False),
        ("    1.2  Computer Vision & Feature Hierarchies", toc_map.get("1.2", "1"), False),
        ("    1.3  Theoretical Foundations of Visual Transfer Learning", toc_map.get("1.3", "2"), False),
        ("    1.4  Inductive Biases in Convolutional Architectures", toc_map.get("1.4", "2"), False),
        ("    1.5  Statistical Divergence Across Visual Domain Manifolds", toc_map.get("1.5", "2"), False),
        ("    1.6  Problem Scope, Delimitations, & Operational Assumptions", toc_map.get("1.6", "3"), False),
        ("    1.7  Organization of the Project Report", toc_map.get("1.7", "3"), False),
        ("2. LITERATURE SURVEY", toc_map.get("2. LITERATURE SURVEY", "4"), True),
        ("    2.1  The Genesis of Transferability: AlexNet to ResNet", toc_map.get("2.1", "4"), False),
        ("    2.2  Deep Residual Learning & Feature Reuse (He et al., 2016)", toc_map.get("2.2", "4"), False),
        ("    2.3  Compound Scaling & Neural Architecture Search (Tan & Le, 2019)", toc_map.get("2.3", "4"), False),
        ("    2.4  Mobile Inverted Bottlenecks & Edge Vision (Sandler et al., 2018)", toc_map.get("2.4", "5"), False),
        ("    2.5  The ImageNet Pre-training Paradigm: Rethinking Defaults", toc_map.get("2.5", "5"), False),
        ("    2.6  Biomedical Visual Domain Shift & Transfusion Analysis", toc_map.get("2.6", "5"), False),
        ("    2.7  Standardized Medical Image Benchmarks: MedMNIST", toc_map.get("2.7", "5"), False),
        ("    2.8  Representational Similarity: CCA vs CKA (Kornblith et al., 2019)", toc_map.get("2.8", "6"), False),
        ("    2.9  Negative Transfer & Representational Distortion", toc_map.get("2.9", "6"), False),
        ("    2.10 Comprehensive Literature Review & Comparison Matrix", toc_map.get("2.10", "6"), False),
        ("3. PROBLEM IDENTIFICATION AND METHODOLOGY", toc_map.get("3. PROBLEM IDENTIFICATION AND METHODOLOGY", "8"), True),
        ("    3.1  Problem Statement & Industrial Gaps", toc_map.get("3.1", "8"), False),
        ("    3.2  Formal Mathematical Problem Formulation", toc_map.get("3.2", "8"), False),
        ("    3.3  Research Questions & Boundary Hypotheses", toc_map.get("3.3", "8"), False),
        ("    3.4  Mathematical Formulation of Linear CKA", toc_map.get("3.4", "9"), False),
        ("    3.5  Methodology Flowchart and Phased Architecture", toc_map.get("3.5", "9"), False),
        ("4. PROPOSED SYSTEM AND ARCHITECTURAL DESIGN", toc_map.get("4. PROPOSED SYSTEM AND ARCHITECTURAL DESIGN", "11"), True),
        ("    4.1  Global System Architecture Overview", toc_map.get("4.1", "11"), False),
        ("    4.2  Data Ingestion & Visual Domain Shift Analysis", toc_map.get("4.2", "11"), False),
        ("    4.3  Vision Backbone Architectures & Micro-Topologies", toc_map.get("4.3", "12"), False),
        ("    4.4  Four Transfer Adaptation Strategies & Freezing Logic", toc_map.get("4.4", "13"), False),
        ("    4.5  Standardized Head Design & Parameter Allocation", toc_map.get("4.5", "14"), False),
        ("    4.6  Feature Extraction Hooking & CKA Calibration Engine", toc_map.get("4.6", "15"), False),
        ("5. EXPERIMENTAL RESULTS AND DISCUSSION", toc_map.get("5. EXPERIMENTAL RESULTS AND DISCUSSION", "16"), True),
        ("    5.1  Benchmark Experimental Setup & Hardware Configuration", toc_map.get("5.1", "16"), False),
        ("    5.2  Complete 24-Configuration Matrix Empirical Results", toc_map.get("5.2", "16"), False),
        ("    5.3  Comparative Architectural Generalization", toc_map.get("5.3", "17"), False),
        ("    5.4  Computational Latency & Efficiency Profiles", toc_map.get("5.4", "18"), False),
        ("    5.5  Transfer Benefit Delta Margin Across Domain Boundaries", toc_map.get("5.5", "18"), False),
        ("    5.6  Representation Drift Diagnosis: Near-Domain (CIFAR-10)", toc_map.get("5.6", "19"), False),
        ("    5.7  Representation Drift Diagnosis: Far-Domain (PathMNIST)", toc_map.get("5.7", "20"), False),
        ("    5.8  Representation Drift Curves Across Depth & Insights", toc_map.get("5.8", "20"), False),
        ("6. PRACTITIONER GUIDELINES & DECISION FRAMEWORK", toc_map.get("6. PRACTITIONER GUIDELINES & DECISION FRAMEWORK", "22"), True),
        ("    6.1  Strategic Decision Matrix for Applied Vision Engineering", toc_map.get("6.1", "22"), False),
        ("    6.2  Adaptation Strategy Decision Tree Flowchart", toc_map.get("6.2", "22"), False),
        ("    6.3  Core Practical Rules of Thumb & Failure Modes", toc_map.get("6.3", "23"), False),
        ("7. CONCLUSION AND FUTURE SCOPE", toc_map.get("7. CONCLUSION AND FUTURE SCOPE", "24"), True),
        ("    7.1  Comprehensive Summary of Empirical Findings", toc_map.get("7.1", "24"), False),
        ("    7.2  Threats to Validity & Research Limitations", toc_map.get("7.2", "24"), False),
        ("    7.3  Future Research Directions & Next-Gen Paradigms", toc_map.get("7.3", "24"), False),
        ("APPENDIX: CORE SOURCE CODE LISTINGS", toc_map.get("APPENDIX", "25"), True),
        ("REFERENCES", toc_map.get("REFERENCES", "27"), True)
    ]

    for title, pg, is_major in toc_entries:
        p_row = doc.add_paragraph()
        p_row.paragraph_format.space_before = Pt(0.5 if is_major else 0)
        p_row.paragraph_format.space_after = Pt(0.5 if is_major else 0)
        p_row.paragraph_format.line_spacing = 1.0
        p_row.paragraph_format.tab_stops.add_tab_stop(Inches(5.7), docx.enum.text.WD_TAB_ALIGNMENT.RIGHT, docx.enum.text.WD_TAB_LEADER.DOTS)
        
        r_t = p_row.add_run(title)
        format_run(r_t, font_name="Times New Roman", size_pt=9.5 if is_major else 8.5, bold=is_major)
        
        r_p = p_row.add_run(f"\t{pg}")
        format_run(r_p, font_name="Times New Roman", size_pt=9.5 if is_major else 8.5, bold=is_major)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. LIST OF TABLES (PAGE 6) - 3-COLUMN TABLE AS IN TEMPLATE
    # -------------------------------------------------------------
    p_lot_title = doc.add_paragraph()
    p_lot_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot_title.paragraph_format.space_before = Pt(18)
    p_lot_title.paragraph_format.space_after = Pt(12)
    r_lot = p_lot_title.add_run("LIST OF TABLES")
    format_run(r_lot, font_name="Times New Roman", size_pt=14, bold=True)

    t_lot = doc.add_table(rows=len(rd.TABLES) + 1, cols=3)
    t_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = t_lot.rows[0].cells
    hdr_cells[0].text = "TABLE NO"
    hdr_cells[1].text = "TABLE TITLE"
    hdr_cells[2].text = "PAGE NO"
    for cell in hdr_cells:
        set_cell_shading(cell, "F1F5F9")
        set_cell_border(cell, color="94A3B8")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p.runs:
            format_run(p.runs[0], font_name="Times New Roman", size_pt=10.5, bold=True)

    for r_idx, (t_id, t_info) in enumerate(rd.TABLES.items()):
        row_cells = t_lot.rows[r_idx + 1].cells
        row_cells[0].text = t_id
        caption_clean = t_info["caption"].replace(f"Table {t_id}: ", "")
        row_cells[1].text = caption_clean
        pg = table_map.get(t_id, "1")
        row_cells[2].text = str(pg)
        
        bg_col = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx in range(3):
            set_cell_shading(row_cells[c_idx], bg_col)
            set_cell_border(row_cells[c_idx], color="CBD5E1")
            set_cell_margins(row_cells[c_idx], top=65, bottom=65, left=100, right=100)
            p = row_cells[c_idx].paragraphs[0]
            if c_idx in [0, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if p.runs:
                format_run(p.runs[0], font_name="Times New Roman", size_pt=10, bold=(c_idx==2))

    t_lot.rows[0].cells[0].width = Inches(1.3)
    t_lot.rows[0].cells[1].width = Inches(4.1)
    t_lot.rows[0].cells[2].width = Inches(0.9)
    for r in t_lot.rows[1:]:
        r.cells[0].width = Inches(1.3)
        r.cells[1].width = Inches(4.1)
        r.cells[2].width = Inches(0.9)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. LIST OF FIGURES (PAGE 7) - 3-COLUMN TABLE AS IN TEMPLATE
    # -------------------------------------------------------------
    p_lof_title = doc.add_paragraph()
    p_lof_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof_title.paragraph_format.space_before = Pt(18)
    p_lof_title.paragraph_format.space_after = Pt(12)
    r_lof = p_lof_title.add_run("LIST OF FIGURES")
    format_run(r_lof, font_name="Times New Roman", size_pt=14, bold=True)

    t_lof = doc.add_table(rows=len(rd.FIGURES) + 1, cols=3)
    t_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = t_lof.rows[0].cells
    hdr_cells[0].text = "FIGURE NO"
    hdr_cells[1].text = "FIGURE TITLE"
    hdr_cells[2].text = "PAGE NO"
    for cell in hdr_cells:
        set_cell_shading(cell, "F1F5F9")
        set_cell_border(cell, color="94A3B8")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p.runs:
            format_run(p.runs[0], font_name="Times New Roman", size_pt=10.5, bold=True)

    for r_idx, fig in enumerate(rd.FIGURES):
        row_cells = t_lof.rows[r_idx + 1].cells
        row_cells[0].text = fig["id"]
        row_cells[1].text = fig["title"]
        pg = fig_map.get(fig["id"], "1")
        row_cells[2].text = str(pg)
        
        bg_col = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx in range(3):
            set_cell_shading(row_cells[c_idx], bg_col)
            set_cell_border(row_cells[c_idx], color="CBD5E1")
            set_cell_margins(row_cells[c_idx], top=65, bottom=65, left=100, right=100)
            p = row_cells[c_idx].paragraphs[0]
            if c_idx in [0, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if p.runs:
                format_run(p.runs[0], font_name="Times New Roman", size_pt=10, bold=(c_idx==2))

    t_lof.rows[0].cells[0].width = Inches(1.3)
    t_lof.rows[0].cells[1].width = Inches(4.1)
    t_lof.rows[0].cells[2].width = Inches(0.9)
    for r in t_lof.rows[1:]:
        r.cells[0].width = Inches(1.3)
        r.cells[1].width = Inches(4.1)
        r.cells[2].width = Inches(0.9)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. LIST OF ABBREVIATIONS (PAGE 8)
    # -------------------------------------------------------------
    p_abb_title = doc.add_paragraph()
    p_abb_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abb_title.paragraph_format.space_before = Pt(18)
    p_abb_title.paragraph_format.space_after = Pt(12)
    r_abb = p_abb_title.add_run("LIST OF ABBREVIATIONS")
    format_run(r_abb, font_name="Times New Roman", size_pt=14, bold=True)

    t_abb = doc.add_table(rows=len(rd.ABBREVIATIONS) + 1, cols=2)
    t_abb.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = t_abb.rows[0].cells
    hdr_cells[0].text = "ABBREVIATION"
    hdr_cells[1].text = "EXPANSION / DEFINITION"
    for cell in hdr_cells:
        set_cell_shading(cell, "F1F5F9")
        set_cell_border(cell, color="94A3B8")
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        p = cell.paragraphs[0]
        if p.runs:
            format_run(p.runs[0], font_name="Times New Roman", size_pt=10.5, bold=True)

    for r_idx, (abbr, desc) in enumerate(rd.ABBREVIATIONS):
        row_cells = t_abb.rows[r_idx + 1].cells
        row_cells[0].text = abbr
        row_cells[1].text = desc
        bg_col = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx in range(2):
            set_cell_shading(row_cells[c_idx], bg_col)
            set_cell_border(row_cells[c_idx], color="CBD5E1")
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            if p.runs:
                format_run(p.runs[0], font_name="Times New Roman", size_pt=9.5, bold=(c_idx==0))

    t_abb.rows[0].cells[0].width = Inches(1.8)
    t_abb.rows[0].cells[1].width = Inches(4.2)
    for r in t_abb.rows[1:]:
        r.cells[0].width = Inches(1.8)
        r.cells[1].width = Inches(4.2)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 9. CHAPTERS 1 TO 7 (PAGE 9 ONWARDS)
    # -------------------------------------------------------------
    for ch_key in ["1", "2", "3", "4", "5", "6", "7"]:
        ch_data = rd.CHAPTERS[ch_key]
        
        p_ch = doc.add_paragraph()
        p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ch.paragraph_format.space_before = Pt(14 if ch_key == "7" else 18)
        p_ch.paragraph_format.space_after = Pt(3)
        p_ch.paragraph_format.keep_with_next = True
        r_ch_no = p_ch.add_run(f"CHAPTER {ch_key}\n")
        format_run(r_ch_no, font_name="Times New Roman", size_pt=14, bold=True)
        r_ch_ti = p_ch.add_run(ch_data["title"])
        format_run(r_ch_ti, font_name="Times New Roman", size_pt=15, bold=True)
        
        for sec in ch_data["sections"]:
            add_heading_2(doc, f"{sec['num']}  {sec['title']}")
            
            sp_after = 2.5 if ch_key == "7" else 5
            ln_sp = 1.12 if ch_key == "7" else 1.15
            for p_txt in sec["paras"]:
                add_paragraph_styled(doc, p_txt, space_after=sp_after, line_spacing=ln_sp)
            if "bullets" in sec:
                for b_txt in sec["bullets"]:
                    add_bullet_point(doc, b_txt, space_after=sp_after)
                    
            if sec["num"] == "2.10":
                add_table_data(doc, "2.1", rd.TABLES["2.1"])
            elif sec["num"] == "3.5":
                add_figure_image(doc, "cv_figures/fig3_1_methodology_flowchart.png", "3.1", "Research Methodology and Phased Experimental Flowchart", width_in=5.4)
            elif sec["num"] == "4.1":
                add_figure_image(doc, "cv_figures/fig4_1_global_architecture.png", "4.1", "Global System Architecture for Empirical Benchmark & Representation Diagnosis", width_in=5.6)
            elif sec["num"] == "4.2":
                add_figure_image(doc, "cv_figures/fig4_2_domain_divergence.png", "4.2", "Visual Domain Divergence: Near-Domain (CIFAR-10) vs Far-Domain (PathMNIST Histology)", width_in=5.6)
                add_table_data(doc, "4.1", rd.TABLES["4.1"])
            elif sec["num"] == "4.3":
                add_figure_image(doc, "cv_figures/fig4_3_micro_topologies.png", "4.3", "Comparative Micro-Architectural Block Topologies: ResNet-50 vs EfficientNet-B0 vs MobileNet-V2", width_in=5.6)
                add_table_data(doc, "4.2", rd.TABLES["4.2"])
            elif sec["num"] == "4.4":
                add_figure_image(doc, "cv_figures/fig4_4_adaptation_regimes.png", "4.4", "Architectural Topologies of the Four Adaptation Regimes & Freezing Logic", width_in=5.6)
                add_table_data(doc, "4.3", rd.TABLES["4.3"])
            elif sec["num"] == "4.5":
                add_table_data(doc, "4.4", rd.TABLES["4.4"])
            elif sec["num"] == "4.6":
                add_figure_image(doc, "cv_figures/fig4_5_cka_pipeline.png", "4.5", "Linear CKA (Centered Kernel Alignment) Mathematical Pipeline", width_in=5.6)
            elif sec["num"] == "5.1":
                add_table_data(doc, "5.1", rd.TABLES["5.1"])
            elif sec["num"] == "5.2":
                add_table_data(doc, "5.2", rd.TABLES["5.2"])
            elif sec["num"] == "5.3":
                add_figure_image(doc, "cv_figures/fig5_1_top1_accuracy.png", "5.1", "Top-1 Accuracy Across Architectures, Domains, and Adaptation Strategies", width_in=5.6)
            elif sec["num"] == "5.4":
                add_figure_image(doc, "cv_figures/fig5_2_training_duration.png", "5.2", "Computational Training Duration Across Architectures and Adaptation Regimes", width_in=5.6)
            elif sec["num"] == "5.5":
                add_figure_image(doc, "cv_figures/fig5_3_transfer_delta_margin.png", "5.3", "Transfer Benefit Delta Margin Across Near-Domain (CIFAR-10) and Far-Domain (PathMNIST)", width_in=5.4)
                add_table_data(doc, "5.3", rd.TABLES["5.3"])
            elif sec["num"] == "5.6":
                add_figure_image(doc, "cv_figures/fig5_4_cka_heatmaps_cifar10.png", "5.4", "Linear CKA Layer-wise Representation Heatmaps for Near-Domain (CIFAR-10)", width_in=5.6)
            elif sec["num"] == "5.7":
                add_figure_image(doc, "cv_figures/fig5_5_cka_heatmaps_pathmnist.png", "5.5", "Linear CKA Layer-wise Representation Heatmaps for Far-Domain (PathMNIST)", width_in=5.6)
            elif sec["num"] == "5.8":
                add_figure_image(doc, "cv_figures/fig5_6_drift_curves_depth.png", "5.6", "Representational Drift Across Network Depth: Near-Domain vs Far-Domain Alignment", width_in=5.4)
                add_table_data(doc, "5.4", rd.TABLES["5.4"])
            elif sec["num"] == "6.1":
                add_table_data(doc, "6.1", rd.TABLES["6.1"])
            elif sec["num"] == "6.2":
                add_figure_image(doc, "cv_figures/fig6_1_decision_flowchart.png", "6.1", "Transfer Learning Adaptation Strategy Decision Framework Flowchart", width_in=5.4)
                
        doc.add_page_break()

    # -------------------------------------------------------------
    # 10. APPENDIX: CORE SOURCE CODE LISTINGS
    # -------------------------------------------------------------
    p_app_title = doc.add_paragraph()
    p_app_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_app_title.paragraph_format.space_before = Pt(18)
    p_app_title.paragraph_format.space_after = Pt(10)
    r_app = p_app_title.add_run("APPENDIX: CORE SOURCE CODE LISTINGS")
    format_run(r_app, font_name="Times New Roman", size_pt=14, bold=True)

    for item in rd.APPENDIX_CODE:
        add_code_block(doc, item["title"], item["code"])

    doc.add_page_break()

    # -------------------------------------------------------------
    # 11. REFERENCES
    # -------------------------------------------------------------
    p_ref_title = doc.add_paragraph()
    p_ref_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ref_title.paragraph_format.space_before = Pt(16)
    p_ref_title.paragraph_format.space_after = Pt(8)
    r_ref = p_ref_title.add_run("REFERENCES")
    format_run(r_ref, font_name="Times New Roman", size_pt=14, bold=True)

    for ref in rd.REFERENCES:
        p_r = doc.add_paragraph()
        p_r.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_r.paragraph_format.left_indent = Inches(0.35)
        p_r.paragraph_format.first_line_indent = Inches(-0.35)
        p_r.paragraph_format.space_before = Pt(0.5)
        p_r.paragraph_format.space_after = Pt(2.0)
        p_r.paragraph_format.line_spacing = 1.10
        r_rf = p_r.add_run(ref)
        format_run(r_rf, font_name="Times New Roman", size_pt=9.5)

    doc.save(output_path)
    print(f"Saved document to {output_path}")

def run_alignment_pipeline():
    temp_docx = "temp_pass1.docx"
    temp_pdf = "temp_pass1.pdf"
    
    print("=== PASS 1: Building initial draft for page number extraction ===")
    build_docx(temp_docx, {}, {}, {})
    
    print("Converting draft to PDF with LibreOffice...")
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", temp_docx], check=True)
    
    print("Extracting exact page numbers from PDF via pdftotext...")
    out = subprocess.check_output(["pdftotext", temp_pdf, "-"]).decode("utf-8", errors="ignore")
    pages_raw = out.split("\x0c")
    pages = [re.sub(r"\s+", " ", p) for p in pages_raw]
    print(f"Total pages in converted PDF: {len(pages)}")

    first_body_pdf_page = None
    for p_idx, p_text in enumerate(pages, start=1):
        if "CHAPTER 1" in p_text and p_idx > 5:
            first_body_pdf_page = p_idx
            break
            
    print(f"First body page (CHAPTER 1) detected on PDF page: {first_body_pdf_page}")
    page_offset = first_body_pdf_page - 1
    
    prelim_headings = [
        ("ABSTRACT", "ABSTRACT"),
        ("LIST OF TABLES", "LIST OF TABLES"),
        ("LIST OF FIGURES", "LIST OF FIGURES"),
        ("LIST OF ABBREVIATIONS", "LIST OF ABBREVIATIONS")
    ]

    body_headings = [
        ("1. INTRODUCTION", "CHAPTER 1"),
        ("1.1", "1.1 Objective of the Research Investigation"),
        ("1.2", "1.2 Computer Vision & Feature Hierarchies"),
        ("1.3", "1.3 Theoretical Foundations of Visual Transfer Learning"),
        ("1.4", "1.4 Inductive Biases in Convolutional Architectures"),
        ("1.5", "1.5 Statistical Divergence Across Visual Domain Manifolds"),
        ("1.6", "1.6 Problem Scope, Delimitations, & Operational Assumptions"),
        ("1.7", "1.7 Organization of the Project Report"),
        ("2. LITERATURE SURVEY", "CHAPTER 2"),
        ("2.1", "2.1 The Genesis of Transferability"),
        ("2.2", "2.2 Deep Residual Learning & Feature Reuse"),
        ("2.3", "2.3 Compound Scaling & Neural Architecture Search"),
        ("2.4", "2.4 Mobile Inverted Bottlenecks & Edge Vision"),
        ("2.5", "2.5 The ImageNet Pre-training Paradigm"),
        ("2.6", "2.6 Biomedical Visual Domain Shift"),
        ("2.7", "2.7 Standardized Medical Image Benchmarks"),
        ("2.8", "2.8 Representational Similarity: CCA vs CKA"),
        ("2.9", "2.9 Negative Transfer & Representational Distortion"),
        ("2.10", "2.10 Comprehensive Literature Review"),
        ("3. PROBLEM IDENTIFICATION AND METHODOLOGY", "CHAPTER 3"),
        ("3.1", "3.1 Problem Statement & Industrial Gaps"),
        ("3.2", "3.2 Formal Mathematical Problem Formulation"),
        ("3.3", "3.3 Research Questions & Boundary Hypotheses"),
        ("3.4", "3.4 Mathematical Formulation of Linear CKA"),
        ("3.5", "3.5 Methodology Flowchart and Phased Architecture"),
        ("4. PROPOSED SYSTEM AND ARCHITECTURAL DESIGN", "CHAPTER 4"),
        ("4.1", "4.1 Global System Architecture Overview"),
        ("4.2", "4.2 Data Ingestion & Visual Domain Shift Analysis"),
        ("4.3", "4.3 Vision Backbone Architectures & Micro-Topologies"),
        ("4.4", "4.4 Four Transfer Adaptation Strategies & Freezing Logic"),
        ("4.5", "4.5 Standardized Head Design & Parameter Allocation"),
        ("4.6", "4.6 Feature Extraction Hooking & CKA Calibration Engine"),
        ("5. EXPERIMENTAL RESULTS AND DISCUSSION", "CHAPTER 5"),
        ("5.1", "5.1 Benchmark Experimental Setup & Hardware Configuration"),
        ("5.2", "5.2 Complete 24-Configuration Matrix Empirical Results"),
        ("5.3", "5.3 Comparative Architectural Generalization"),
        ("5.4", "5.4 Computational Latency & Efficiency Profiles"),
        ("5.5", "5.5 Transfer Benefit Delta Margin Across Domain Boundaries"),
        ("5.6", "5.6 Representation Drift Diagnosis: Near-Domain (CIFAR-10)"),
        ("5.7", "5.7 Representation Drift Diagnosis: Far-Domain (PathMNIST)"),
        ("5.8", "5.8 Representation Drift Curves Across Depth & Insights"),
        ("6. PRACTITIONER GUIDELINES & DECISION FRAMEWORK", "CHAPTER 6"),
        ("6.1", "6.1 Strategic Decision Matrix for Applied Vision Engineering"),
        ("6.2", "6.2 Adaptation Strategy Decision Tree Flowchart"),
        ("6.3", "6.3 Core Practical Rules of Thumb & Failure Modes"),
        ("7. CONCLUSION AND FUTURE SCOPE", "CHAPTER 7"),
        ("7.1", "7.1 Comprehensive Summary of Empirical Findings"),
        ("7.2", "7.2 Threats to Validity & Research Limitations"),
        ("7.3", "7.3 Future Research Directions & Next-Gen Paradigms"),
        ("APPENDIX", "APPENDIX: CORE SOURCE CODE LISTINGS"),
        ("REFERENCES", "REFERENCES")
    ]

    roman_map = {1: "i", 2: "ii", 3: "iii", 4: "iv", 5: "v", 6: "vi", 7: "vii", 8: "viii", 9: "ix", 10: "x"}
    final_toc_map = {}
    
    # 1. Preliminaries: search only before first_body_pdf_page and skip TOC page (page 5)
    for h_key, h_search in prelim_headings:
        for p_idx in range(3, first_body_pdf_page):
            if p_idx == 5: # Skip TOC page itself
                continue
            if h_search in pages[p_idx - 1]:
                final_toc_map[h_key] = roman_map.get(p_idx, str(p_idx))
                break

    # 2. Body headings: search starting from first_body_pdf_page
    for h_key, h_search in body_headings:
        for p_idx in range(first_body_pdf_page, len(pages) + 1):
            if h_search in pages[p_idx - 1]:
                final_toc_map[h_key] = str(p_idx - page_offset)
                break

    # 3. Tables map
    final_table_map = {}
    for t_id, t_info in rd.TABLES.items():
        search_str = f"Table {t_id}:"
        for p_idx in range(first_body_pdf_page, len(pages) + 1):
            if search_str in pages[p_idx - 1]:
                final_table_map[t_id] = str(p_idx - page_offset)
                break

    # 4. Figures map
    final_fig_map = {}
    for fig in rd.FIGURES:
        search_str = f"Figure {fig['id']}:"
        for p_idx in range(first_body_pdf_page, len(pages) + 1):
            if search_str in pages[p_idx - 1]:
                final_fig_map[fig["id"]] = str(p_idx - page_offset)
                break

    print("\n--- FINAL COMPUTED TOC PAGE MAP ---")
    for k, v in final_toc_map.items():
        print(f"  {k:50} -> {v}")

    print("\n--- FINAL COMPUTED TABLE PAGE MAP ---")
    for k, v in final_table_map.items():
        print(f"  Table {k:5} -> {v}")

    print("\n--- FINAL COMPUTED FIGURE PAGE MAP ---")
    for k, v in final_fig_map.items():
        print(f"  Figure {k:5} -> {v}")

    for f in [temp_docx, temp_pdf]:
        if os.path.exists(f): os.remove(f)

    # -------------------------------------------------------------
    # PASS 2: BUILD FINAL ALIGNED DOCUMENTS
    # -------------------------------------------------------------
    print("\n=== PASS 2: Building Final Aligned DOCX & PDF ===")
    final_docx = "CV_Project_Report.docx"
    build_docx(final_docx, final_toc_map, final_table_map, final_fig_map)

    print("Generating Final PDF via LibreOffice...")
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", final_docx], check=True)
    
    shutil.copyfile(final_docx, "CV_PROJECT_REPORT.docx")
    shutil.copyfile("CV_Project_Report.pdf", "CV_PROJECT_REPORT.pdf")
    
    print("\nSUCCESS! Generated both:")
    print("  - CV_Project_Report.docx (and CV_PROJECT_REPORT.docx)")
    print("  - CV_Project_Report.pdf (and CV_PROJECT_REPORT.pdf)")

if __name__ == "__main__":
    run_alignment_pipeline()
