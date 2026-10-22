"""Quick CLI tool to inspect the MechAgent Database (SQLite).
Usage:
    python inspect_db.py
    python inspect_db.py --table vibration_telemetry
    python inspect_db.py --table spare_parts_inventory
    python inspect_db.py --table work_orders
"""
import argparse
import sqlite3
import sys
from pathlib import Path

# Configure UTF-8 for console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DB_PATH = Path("data/mechagent.db")

def inspect(table_name=None, limit=10):
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH.resolve()}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    tables = [
        "equipments",
        "spare_parts_inventory",
        "vibration_telemetry",
        "work_orders"
    ]

    if table_name:
        target_tables = [table_name]
    else:
        target_tables = tables

    print("=" * 80)
    print(f"📁 MechAgent Database Inspector: {DB_PATH.resolve()}")
    print("=" * 80)

    for tbl in target_tables:
        try:
            count = cursor.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            print(f"\n📊 ตาราง: [{tbl}] (จำนวนทั้งหมด {count:,} แถว)")
            print("-" * 80)
            
            rows = cursor.execute(f"SELECT * FROM {tbl} ORDER BY rowid DESC LIMIT ?", (limit,)).fetchall()
            if not rows:
                print("   (ตารางยังว่างเปล่า)")
                continue

            cols = rows[0].keys()
            header = " | ".join(f"{c[:18]:<18}" for c in cols[:6])
            print("   " + header)
            print("   " + "-" * len(header))

            for r in rows:
                line = " | ".join(f"{str(r[c])[:18]:<18}" for c in cols[:6])
                print("   " + line)

            if count > limit:
                print(f"   ... และอีก {count - limit} รายการ (แสดง {limit} รายการล่าสุด)")
        except Exception as e:
            print(f"❌ ไม่สามารถอ่านตาราง {tbl}: {e}")

    conn.close()
    print("\n" + "=" * 80)
    print("💡 คำแนะนำ: คุณสามารถใช้โปรแกรม 'DB Browser for SQLite' หรือ VS Code Extension 'SQLite Viewer'")
    print("   เปิดไฟล์ data/mechagent.db เพื่อดูและแก้ไขข้อมูลแบบ GUI ได้โดยตรง")
    print("=" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", type=str, help="Specific table to inspect")
    parser.add_argument("--limit", type=int, default=10, help="Row limit")
    args = parser.parse_args()
    inspect(args.table, args.limit)
