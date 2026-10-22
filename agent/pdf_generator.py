"""Generate professional PDF maintenance reports from Markdown.
Uses headless browser (Edge/Chrome) for perfect Thai typography and vector quality,
with ReportLab as robust, zero-dependency pure-Python fallback.
"""
import io
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

# Register Thai fonts if available
FONT_DIR = Path(__file__).resolve().parent / "fonts"
REG_FONT = FONT_DIR / "Sarabun-Regular.ttf"
BOLD_FONT = FONT_DIR / "Sarabun-Bold.ttf"

if REG_FONT.exists():
    try:
        pdfmetrics.registerFont(TTFont("Sarabun", str(REG_FONT)))
    except Exception:
        pass
if BOLD_FONT.exists():
    try:
        pdfmetrics.registerFont(TTFont("Sarabun-Bold", str(BOLD_FONT)))
    except Exception:
        pass


def find_browser():
    for p in EDGE_PATHS + CHROME_PATHS:
        if os.path.exists(p):
            return p
    for cmd in ["google-chrome-stable", "google-chrome", "chromium", "chromium-browser", "msedge", "chrome"]:
        p = shutil.which(cmd)
        if p:
            return p
    return None


def markdown_to_html_doc(md_text, title="MechAgent Report"):
    html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "nl2br"])
    
    html_body = re.sub(r'<strong>(EMERGENCY)</strong>', r'<span class="badge badge-emergency">\1</span>', html_body)
    html_body = re.sub(r'<strong>(HIGH)</strong>', r'<span class="badge badge-high">\1</span>', html_body)
    html_body = re.sub(r'<strong>(MEDIUM)</strong>', r'<span class="badge badge-medium">\1</span>', html_body)
    html_body = re.sub(r'<strong>(LOW)</strong>', r'<span class="badge badge-low">\1</span>', html_body)
    
    html_doc = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap');
@page {{
    size: A4 portrait;
    margin: 16mm 14mm 16mm 14mm;
}}
*, *:before, *:after {{
    box-sizing: border-box;
}}
body {{
    font-family: 'Sarabun', 'Tahoma', 'Leelawadee', sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
}}
.brand-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 10px;
    margin-bottom: 16px;
}}
.brand-title {{
    font-size: 15pt;
    font-weight: 700;
    color: #0369a1;
    margin: 0;
}}
.brand-sub {{
    font-size: 8.5pt;
    color: #64748b;
    margin-top: 3px;
}}
.doc-stamp {{
    text-align: right;
    font-size: 8pt;
    color: #64748b;
}}
h1 {{
    font-size: 13pt;
    color: #0f172a;
    background: #f1f5f9;
    padding: 8px 12px;
    border-left: 5px solid #0284c7;
    border-radius: 0 4px 4px 0;
    margin-top: 0;
    margin-bottom: 12px;
}}
h2 {{
    font-size: 11pt;
    color: #0369a1;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 4px;
    margin-top: 16px;
    margin-bottom: 8px;
    page-break-after: avoid;
}}
h3 {{
    font-size: 10pt;
    color: #334155;
    margin-top: 10px;
    margin-bottom: 6px;
    page-break-after: avoid;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 14px 0;
    font-size: 9pt;
}}
th, td {{
    padding: 6px 8px;
    border: 1px solid #cbd5e1;
    text-align: left;
}}
th {{
    background-color: #f8fafc;
    color: #0f172a;
    font-weight: 600;
    border-bottom: 2px solid #94a3b8;
}}
tr:nth-child(even) td {{
    background-color: #f8fafc;
}}
ul, ol {{
    padding-left: 18px;
    margin-top: 4px;
    margin-bottom: 10px;
}}
li {{
    margin-bottom: 3px;
}}
.badge {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 8.5pt;
}}
.badge-emergency {{ background-color: #fee2e2; color: #b91c1c; border: 1px solid #f87171; }}
.badge-high {{ background-color: #ffedd5; color: #c2410c; border: 1px solid #fb923c; }}
.badge-medium {{ background-color: #fef3c7; color: #b45309; border: 1px solid #fbbf24; }}
.badge-low {{ background-color: #d1fae5; color: #047857; border: 1px solid #34d399; }}
.doc-footer {{
    margin-top: 20px;
    padding-top: 8px;
    border-top: 1px solid #e2e8f0;
    font-size: 8pt;
    color: #64748b;
    display: flex;
    justify-content: space-between;
}}
</style>
</head>
<body>
<div class="brand-header">
    <div>
        <div class="brand-title">⚙️ MechAgent Predictive Maintenance</div>
        <div class="brand-sub">Physics-Informed Agentic Reliability Engineering System</div>
    </div>
    <div class="doc-stamp">
        <div>เอกสารทางการ (Official Report)</div>
        <div>มาตรฐาน ISO 13373 Vibration Condition Monitoring</div>
    </div>
</div>
{html_body}
<div class="doc-footer">
    <div>MechAgent AI System • ศูนย์วิเคราะห์ความสั่นสะเทือนและสุขภาพเครื่องจักร</div>
    <div>พิมพ์ผ่านระบบอัตโนมัติ</div>
</div>
</body>
</html>"""
    return html_doc


def generate_pdf_from_html(html_content, out_pdf_path=None):
    browser = find_browser()
    if not browser:
        raise RuntimeError("No Chrome or Edge browser found on system for PDF export.")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_html = Path(tmp_dir) / "report.html"
        tmp_pdf = Path(tmp_dir) / "report.pdf"
        tmp_html.write_text(html_content, encoding="utf-8")
        
        file_url = tmp_html.as_uri()
        cmd = [
            browser,
            "--headless=new" if "chrome" in browser.lower() else "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--run-all-compositor-stages-before-draw",
            "--no-pdf-header-footer",
            f"--print-to-pdf={str(tmp_pdf)}",
            file_url,
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        
        if not tmp_pdf.exists() or tmp_pdf.stat().st_size == 0:
            raise RuntimeError(f"Browser failed to generate PDF. Return code: {res.returncode}. Stderr: {res.stderr.decode('utf-8', errors='ignore')}")
            
        pdf_bytes = tmp_pdf.read_bytes()
        if out_pdf_path:
            Path(out_pdf_path).write_bytes(pdf_bytes)
        return pdf_bytes


def generate_pdf_reportlab(md_text, title="MechAgent Report"):
    """Robust, pure-Python fallback using ReportLab with Thai Sarabun font support."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    has_sarabun = "Sarabun" in pdfmetrics.getRegisteredFontNames()
    base_font = "Sarabun" if has_sarabun else "Helvetica"
    bold_font = "Sarabun-Bold" if "Sarabun-Bold" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"

    styles = getSampleStyleSheet()
    
    style_title = ParagraphStyle(
        "ReportTitle",
        fontName=bold_font,
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0369a1")
    )
    style_subtitle = ParagraphStyle(
        "ReportSubtitle",
        fontName=base_font,
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#64748b")
    )
    style_h1 = ParagraphStyle(
        "ReportH1",
        fontName=bold_font,
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=5,
        spaceBefore=10,
        spaceAfter=6
    )
    style_h2 = ParagraphStyle(
        "ReportH2",
        fontName=bold_font,
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0284c7"),
        spaceBefore=8,
        spaceAfter=4
    )
    style_h3 = ParagraphStyle(
        "ReportH3",
        fontName=bold_font,
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceBefore=6,
        spaceAfter=3
    )
    style_body = ParagraphStyle(
        "ReportBody",
        fontName=base_font,
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#1e293b")
    )
    style_table_header = ParagraphStyle(
        "TableHeader",
        fontName=bold_font,
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )
    style_table_cell = ParagraphStyle(
        "TableCell",
        fontName=base_font,
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#334155")
    )

    story = []

    # Brand Header
    story.append(Paragraph("⚙️ MechAgent Predictive Maintenance", style_title))
    story.append(Paragraph("Physics-Informed Agentic Reliability Engineering System • ISO 13373 Standard", style_subtitle))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=10))

    lines = md_text.splitlines()
    in_table = False
    table_rows = []

    for line in lines:
        s = line.strip()
        if not s:
            if in_table and table_rows:
                t = Table(table_rows, colWidths=[160, 360])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                story.append(t)
                story.append(Spacer(1, 6))
                in_table = False
                table_rows = []
            continue

        if s.startswith("|") and s.endswith("|"):
            parts = [p.strip() for p in s[1:-1].split("|")]
            if parts and all(c in "- :" for c in parts[0]):
                continue
            if not in_table:
                in_table = True
                table_rows = [[Paragraph(f"<b>{p}</b>", style_table_header) for p in parts]]
            else:
                table_rows.append([Paragraph(p, style_table_cell) for p in parts])
            continue
        elif in_table and table_rows:
            t = Table(table_rows, colWidths=[160, 360])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
            in_table = False
            table_rows = []

        if s.startswith("# "):
            story.append(Paragraph(s[2:], style_h1))
        elif s.startswith("## "):
            story.append(Paragraph(s[3:], style_h2))
        elif s.startswith("### "):
            story.append(Paragraph(s[4:], style_h3))
        elif s.startswith("- ") or s.startswith("* "):
            story.append(Paragraph(f"• {s[2:]}", style_body))
        elif s.startswith("  - ") or s.startswith("  * "):
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;◦ {s[4:]}", style_body))
        elif re.match(r"^[0-9]+\.\s", s):
            story.append(Paragraph(s, style_body))
        else:
            formatted = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", s)
            story.append(Paragraph(formatted, style_body))

    if in_table and table_rows:
        t = Table(table_rows, colWidths=[160, 360])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t)

    # Footer
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=4))
    story.append(Paragraph("MechAgent AI System • ศูนย์วิเคราะห์ความสั่นสะเทือนและสุขภาพเครื่องจักร • พิมพ์ผ่านระบบอัตโนมัติ", style_subtitle))

    doc.build(story)
    return buf.getvalue()


def markdown_to_pdf_bytes(md_text, title="MechAgent Report"):
    # 1. Try headless browser first (Chrome/Edge) for high-fidelity HTML printing
    try:
        browser = find_browser()
        if browser:
            html_doc = markdown_to_html_doc(md_text, title=title)
            return generate_pdf_from_html(html_doc)
    except Exception as e:
        # Log and fall through to ReportLab
        pass
        
    # 2. Pure-Python ReportLab fallback (100% reliable on any cloud/container environment)
    return generate_pdf_reportlab(md_text, title=title)
