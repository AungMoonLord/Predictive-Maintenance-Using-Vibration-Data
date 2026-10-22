import pytest
from pdf_generator import find_browser, markdown_to_html_doc, markdown_to_pdf_bytes


def test_find_browser():
    browser = find_browser()
    assert browser is not None
    assert "edge" in browser.lower() or "chrome" in browser.lower()


def test_markdown_to_html_doc():
    md = "# Test Report\n\n| Item | Value |\n|---|---|\n| Machine | PUMP-01 |\n\n- Step 1\n- Step 2"
    html = markdown_to_html_doc(md, title="Unit Test Doc")
    assert "<!DOCTYPE html>" in html
    assert "Test Report" in html
    assert "PUMP-01" in html
    assert "Sarabun" in html


def test_markdown_to_pdf_bytes():
    md = """# รายงานสุขภาพตลับลูกปืน
**Job:** TEST-01 | **เวลาวิเคราะห์:** 21/10/2026

## 1. สรุปผล
| หัวข้อ | ผลลัพธ์ |
|---|---|
| สถานะ | S1: เริ่มเสื่อม |
| ตำแหน่งที่เสียหาย | แหวนรอบใน |

## 2. คู่มือช่างเทคนิค
1. ตรวจสอบความแน่น (Interference fit)
2. อุ่นด้วย Induction Heater 100–110°C
"""
    pdf = markdown_to_pdf_bytes(md, title="Thai Test PDF")
    assert pdf is not None
    assert len(pdf) > 1000
    assert pdf.startswith(b"%PDF")
