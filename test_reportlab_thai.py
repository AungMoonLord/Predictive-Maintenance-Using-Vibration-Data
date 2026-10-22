import io
import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_dir = Path(__file__).resolve().parent / "fonts"
reg_font_path = font_dir / "Sarabun-Regular.ttf"
bold_font_path = font_dir / "Sarabun-Bold.ttf"

if reg_font_path.exists():
    pdfmetrics.registerFont(TTFont("Sarabun", str(reg_font_path)))
if bold_font_path.exists():
    pdfmetrics.registerFont(TTFont("Sarabun-Bold", str(bold_font_path)))

def generate_pdf_reportlab(md_text, title="MechAgent Report"):
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
                # Flush table
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
            # Markdown table line
            parts = [p.strip() for p in s[1:-1].split("|")]
            if parts and all(c in "- :" for c in parts[0]):
                # Table separator row
                continue
            if not in_table:
                in_table = True
                table_rows = [[Paragraph(f"<b>{p}</b>", style_table_header) for p in parts]]
            else:
                table_rows.append([Paragraph(p, style_table_cell) for p in parts])
            continue
        elif in_table and table_rows:
            # Table ended
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

        # Headings and body
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
            # Format bold text
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

if __name__ == "__main__":
    test_md = """# รายงานสุขภาพตลับลูกปืน: ปั๊มน้ำหล่อเย็นหลัก #1
**Job:** LOCAL-112577 | **เวลาวิเคราะห์:** 22/10/2026 | **ตลับลูกปืน:** SKF 6205-2RS

## 1. สรุปผล
| หัวข้อ | ผลลัพธ์ |
|---|---|
| สถานะ | S1: เริ่มเสื่อม |
| ตำแหน่งที่เสียหาย | แหวนรอบใน (ความมั่นใจ 75.0%) |
| ต้องเปลี่ยนเร็วที่สุดภายใน | 0 วัน 13 ชั่วโมง 12 นาที |

## 2. คู่มือการแก้ปัญหาสำหรับช่างเทคนิค
### 4.1 การตรวจสอบและวินิจฉัยหน้างาน
- ตรวจสอบการเยื้องศูนย์ของเพลา
- ข้อควรระวังสำคัญ:
  - ตรวจสอบให้แน่ใจว่าแหวนนอกนั่งแนบสนิทกับบ่า Housing

### 4.2 ขั้นตอนมาตรฐานในการเปลี่ยนและติดตั้งตลับลูกปืน
1. ความปลอดภัย (Safety & LOTO): ดำเนินการตัดระบบไฟฟ้า
2. การถอด: ใช้ Bearing Puller ห้ามใช้ค้อนตี
3. การอุ่นติดตั้ง: อุ่นตลับลูกปืนด้วย Induction Heater ที่อุณหภูมิ 100-110°C
"""
    pdf = generate_pdf_reportlab(test_md)
    print("ReportLab PDF generated successfully! Bytes:", len(pdf))
    assert pdf.startswith(b"%PDF")
    with open("test_out.pdf", "wb") as f:
        f.write(pdf)
    print("Saved to test_out.pdf")
