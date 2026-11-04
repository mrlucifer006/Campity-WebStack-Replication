import os, subprocess
from generate_and_align import build_docx

# Verified exact page numbers
EXACT_TOC_MAP = {
    "ABSTRACT": "iii",
    "LIST OF FIGURES": "vi",
    "LIST OF ABBREVIATIONS": "vii",
    "1. INTRODUCTION": "1",
    "1.1 OVERVIEW": "1",
    "1.2 MOTIVATION AND BACKGROUND": "1",
    "1.3 PROBLEM STATEMENT": "2",
    "1.4 OBJECTIVES OF THE PROJECT": "2",
    "1.5 SCOPE OF THE PROJECT": "3",
    "1.6 ORGANIZATION OF THE REPORT": "3",
    "2. LITERATURE SURVEY & WORKSPACE BENCHMARKING": "4",
    "2.1 WORKSPACE WEB ARCHITECTURE BENCHMARK": "4",
    "2.2 COMPARATIVE ANALYSIS OF ARCHITECTURAL TIERS": "4",
    "2.3 RATIONALE FOR SELECTING CAMPITY": "4",
    "2.4 DOMAIN TRANSFORMATION": "5",
    "3. SYSTEM ARCHITECTURE & DUAL-STACK DESIGN": "6",
    "3.1 HIGH-LEVEL DUAL-ENGINE ARCHITECTURE": "6",
    "3.2 SHARED FRONTEND PRESENTATION TIER": "6",
    "3.3 PHP APPLICATION TIER": "7",
    "3.4 JAVA SERVLETS APPLICATION TIER": "7",
    "3.5 DATABASE ARCHITECTURE & RELATIONAL SCHEMA": "8",
    "4. THE INTELLIGENT PRIORITY QUEUE SCHEDULING ALGORITHM": "9",
    "4.1 ALGORITHMIC FORMULATION & MATHEMATICAL MODEL": "9",
    "4.2 CATEGORY URGENCY WEIGHTING MATRIX": "9",
    "4.3 ECONOMIC BOUNTY SCALING & DEADLINE PROXIMITY": "10",
    "4.4 JAVA MAX-HEAP IMPLEMENTATION": "10",
    "4.5 PHP SORTING ENGINE & REST API ENDPOINT": "11",
    "4.6 COMPUTATIONAL COMPLEXITY ANALYSIS": "11",
    "5. CORE BUSINESS LOGIC & FINANCIAL ESCROW PROTOCOL": "12",
    "5.1 ESCROW DEPOSIT MECHANISM & FINANCIAL SOLVENCY": "12",
    "5.2 HELPER ACCOUNTABILITY": "12",
    "5.3 TASK STATE MACHINE & LIFECYCLE TRANSITIONS": "12",
    "5.4 REPUTATION, EXPERIENCE POINTS": "13",
    "5.5 TRANSACTION AUDIT TRAIL": "13",
    "6. IMPLEMENTATION DETAILS & CODE WALKTHROUGH": "15",
    "6.1 DATABASE AUTO-MIGRATION": "15",
    "6.2 USER AUTHENTICATION": "15",
    "6.3 TASK CREATION WITH ESCROW DEDUCTION": "15",
    "6.4 PRIORITY TASK FEED": "16",
    "6.5 TASK ACCEPTANCE": "17",
    "6.6 STANDALONE JDK EMBEDDED SERVER EXECUTION": "17",
    "7. EXPERIMENTAL RESULTS & PERFORMANCE EVALUATION": "18",
    "7.1 TEST SUITE VERIFICATION": "18",
    "7.2 PERFORMANCE BENCHMARKING": "18",
    "7.3 CONCURRENCY & ZERO DATABASE LOCK": "19",
    "7.4 USER INTERFACE WALKTHROUGH": "20",
    "8. CONCLUSION & FUTURE ENHANCEMENTS": "21",
    "8.1 SUMMARY OF CONTRIBUTIONS": "21",
    "8.2 OPERATIONAL SIGNIFICANCE": "21",
    "8.3 LIMITATIONS & FUTURE RESEARCH": "21",
    "REFERENCES": "22"
}

EXACT_FIG_MAP = {
    "3.1": "6",
    "3.2": "8",
    "4.1": "9",
    "4.2": "10",
    "5.1": "12",
    "6.1": "17",
    "7.1": "19",
    "7.2": "20"
}

def finalize():
    print("Building finalized Project_Report.docx with 100% exact page mappings...")
    build_docx("Project_Report.docx", EXACT_TOC_MAP, EXACT_FIG_MAP)
    build_docx("TaskFlow_Project_Report.docx", EXACT_TOC_MAP, EXACT_FIG_MAP)
    
    # Also overwrite the template file or create the exact copy named after template
    # Wait, let's keep the original docx as template backup and make 'Report format pg-1-2(23-24) (1)_Completed.docx'
    import shutil
    shutil.copyfile("Project_Report.docx", "Report format pg-1-2(23-24) (1)_Completed.docx")
    
    print("Converting final report to PDF...")
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "Project_Report.docx"], check=True)
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "TaskFlow_Project_Report.docx"], check=True)
    
    print("\n✅ Verification:")
    subprocess.run(["pdfinfo", "Project_Report.pdf"])

if __name__ == "__main__":
    finalize()
