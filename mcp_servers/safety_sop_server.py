"""MCP Server 4: Safety & SOP Server.
Provides standardized Lockout/Tagout (LOTO) safety protocols,
bearing replacement instructions, and official Thai PDF report compilation.
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent"))
from pdf_generator import markdown_to_pdf_bytes

BKK = timezone(timedelta(hours=7))

TOOLS = [
    {
        "name": "get_safety_loto_procedure",
        "description": "Retrieves official Lockout/Tagout (LOTO) safety instructions, electrical isolation steps, and required PPE for machine maintenance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "machine_id": {"type": "string", "description": "Machine identifier (e.g. PUMP-01)"},
                "fault_type": {"type": "string", "default": "inner_race", "description": "Type of component fault"}
            },
            "required": ["machine_id"]
        }
    },
    {
        "name": "generate_thai_maintenance_pdf",
        "description": "Compiles the diagnostic analysis and work order into an official vector PDF maintenance report in Thai with Sarabun typography.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "markdown_content": {"type": "string", "description": "Markdown text of the report"},
                "output_filename": {"type": "string", "default": "work_order_report.pdf", "description": "Target PDF filename"},
                "title": {"type": "string", "default": "รายงานการซ่อมบำรุงตลับลูกปืน (Bearing Maintenance Report)"}
            },
            "required": ["markdown_content"]
        }
    }
]

SAFETY_LOTO_PROTOCOLS = {
    "electrical": [
        "ตัดสวิตช์เบรกเกอร์ไฟฟ้าหลัก (Main Circuit Breaker) ที่ตู้ MCC",
        "ใส่กุญแจล็อกนิรภัยส่วนบุคคล (Safety Padlock) พร้อมคล้องป้ายเตือนอันตราย (Danger Lockout Tag)",
        "ใช้เครื่องวัดแรงดันไฟฟ้า (Voltage Tester) ตรวจสอบให้มั่นใจว่าแรงดันไฟฟ้าเป็นศูนย์ (Zero Energy Verification)"
    ],
    "mechanical": [
        "ปิดวาล์วทางดูดและทางจ่าย (Suction & Discharge Valves) และคล้องกุญแจล็อกเพื่อตัดแรงดันของไหล",
        "คลายแรงดันตกค้างในระบบท่อและตัวปั๊ม/อุปกรณ์ผ่าน Drain Valve",
        "รอให้อุณหภูมิของตลับลูกปืนและ Housing เย็นลงต่ำกว่า 50°C ก่อนเริ่มสัมผัสชิ้นส่วน"
    ],
    "ppe": [
        "ถุงมือนิรภัยกันความร้อนและสารเคมี (Heat & Chemical Resistant Gloves)",
        "แว่นตานิรภัยมาตรฐาน ANSI Z87.1 (Safety Glasses)",
        "รองเท้านิรภัยหัวเหล็กกันกระแทกและพื้นกันลื่น (Safety Shoes)"
    ],
    "mounting_sop": [
        "1. ถอดคัปปลิ้ง และทำเครื่องหมายตำแหน่งแนวแกน (Alignment Reference Mark)",
        "2. ใช้ตัวดูดตลับลูกปืน (Bearing Puller) จับที่แหวนใน ห้ามใช้ค้อนตีโดยตรงเด็ดขาด",
        "3. ตรวจสอบสภาพเพลาและ Housing: ค่า Runout ต้องไม่เกิน 0.02 mm และไม่มีรอยสนิมขัดสี",
        "4. อุ่นตลับลูกปืนใหม่ด้วยเครื่องกำเนิดความร้อนเหนี่ยวนำ (Induction Heater) ที่อุณหภูมิ 100–110°C (ห้ามใช้ไฟแก๊สเป่า)",
        "5. สวมตลับลูกปืนเข้าเพลาจนชนบ่าทันที และกดค้างไว้จนกระทั่งเย็นตัวลง",
        "6. เติมจาระบีหล่อลื่นตามคู่มือในปริมาณ 30–50% ของช่องว่างภายในลูกปืน (ห้ามเติมจนแน่นเกินไป)",
        "7. ตั้งศูนย์เพลาด้วยเลเซอร์ (Laser Shaft Alignment) ให้ค่าเบี่ยงเบนแนวแกน ≤ 0.05 mm",
        "8. ปลดล็อก LOTO ดำเนินการทดสอบเดินเครื่อง 30 นาที และวัดค่าการสั่นสะเทือนเพื่อบันทึกเป็น Baseline ใหม่"
    ]
}


def handle_get_safety_loto_procedure(machine_id: str, fault_type: str = "inner_race") -> Dict[str, Any]:
    return {
        "status": "success",
        "machine_id": machine_id,
        "fault_type": fault_type,
        "loto_required": True,
        "loto_procedure": {
            "electrical": SAFETY_LOTO_PROTOCOLS["electrical"],
            "mechanical": SAFETY_LOTO_PROTOCOLS["mechanical"],
            "ppe": SAFETY_LOTO_PROTOCOLS["ppe"]
        },
        "electrical_isolation": SAFETY_LOTO_PROTOCOLS["electrical"],
        "mechanical_isolation": SAFETY_LOTO_PROTOCOLS["mechanical"],
        "required_ppe": SAFETY_LOTO_PROTOCOLS["ppe"],
        "standard_sop_steps": SAFETY_LOTO_PROTOCOLS["mounting_sop"],
        "safety_officer_signoff_required": True
    }


def handle_generate_thai_maintenance_pdf(markdown_content: str, output_filename: str = "work_order_report.pdf",
                                         title: str = "รายงานการซ่อมบำรุงตลับลูกปืน") -> Dict[str, Any]:
    try:
        pdf_bytes = markdown_to_pdf_bytes(markdown_content, title=title)
        out_dir = Path(__file__).resolve().parents[1] / "outputs"
        out_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = out_dir / output_filename
        pdf_path.write_bytes(pdf_bytes)
        return {
            "status": "success",
            "pdf_path": str(pdf_path),
            "file_size_bytes": len(pdf_bytes),
            "message": f"Successfully compiled Thai PDF report ({len(pdf_bytes):,} bytes) with Sarabun font."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"PDF compilation failed: {str(e)}"
        }


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if tool_name == "get_safety_loto_procedure":
        return handle_get_safety_loto_procedure(**arguments)
    elif tool_name == "generate_thai_maintenance_pdf":
        return handle_generate_thai_maintenance_pdf(**arguments)
    return {"error": f"Unknown tool: {tool_name}"}


# Aliases matching master prompt naming
get_safety_loto_procedure = handle_get_safety_loto_procedure
generate_thai_maintenance_pdf = handle_generate_thai_maintenance_pdf


if __name__ == "__main__":
    print("Testing get_safety_loto_procedure:")
    res = execute_tool("get_safety_loto_procedure", {"machine_id": "PUMP-01"})
    print(json.dumps(res, indent=2, ensure_ascii=False))
