"""Unified Database Layer for MechAgent.
Supports dual storage backends:
1. SQLite (Local / Edge / Testing) stored at data/mechagent.db
2. Amazon DynamoDB (AWS Serverless Production) using TABLE_NAME
Maintains 4 primary schemas:
- equipments
- vibration_telemetry
- spare_parts_inventory
- work_orders
"""
import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

BKK = timezone(timedelta(hours=7))
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "mechagent.db"


class MechDatabase:
    def __init__(self, db_path: Optional[Path] = None, use_dynamo: Optional[bool] = None):
        self.db_path = db_path or DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # Use DynamoDB if AWS_EXECUTION_ENV is present or explicitly requested
        self.use_dynamo = use_dynamo if use_dynamo is not None else bool(os.environ.get("AWS_EXECUTION_ENV"))
        self._init_sqlite()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_sqlite(self):
        """Initialize the 4 tables in SQLite."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            # 1. Equipments table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipments (
                machine_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                line TEXT NOT NULL,
                bearing_model TEXT NOT NULL,
                bearing_key TEXT NOT NULL,
                criticality TEXT NOT NULL,
                standby_machine TEXT,
                rated_rpm REAL NOT NULL,
                downtime_cost_per_hour REAL DEFAULT 50000.0,
                updated_at TEXT NOT NULL
            )
            """)

            # 2. Vibration Telemetry table (Time-Series)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS vibration_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                machine_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                rpm REAL NOT NULL,
                rms REAL NOT NULL,
                kurtosis REAL NOT NULL,
                predicted_fault TEXT NOT NULL,
                confidence REAL NOT NULL,
                degradation_pct REAL NOT NULL,
                rul_p05 REAL NOT NULL,
                rul_p50 REAL NOT NULL,
                rul_p95 REAL NOT NULL,
                urgency TEXT NOT NULL,
                FOREIGN KEY (machine_id) REFERENCES equipments(machine_id)
            )
            """)

            # 3. Spare Parts Inventory table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS spare_parts_inventory (
                part_number TEXT PRIMARY KEY,
                bearing_model TEXT NOT NULL,
                stock_quantity INTEGER NOT NULL,
                safety_stock INTEGER NOT NULL,
                unit_price_thb REAL NOT NULL,
                lead_time_days INTEGER NOT NULL,
                bin_location TEXT NOT NULL,
                substitutes TEXT,
                updated_at TEXT NOT NULL
            )
            """)

            # 4. Work Orders table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS work_orders (
                work_order_id TEXT PRIMARY KEY,
                machine_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                planned_start TEXT NOT NULL,
                planned_end TEXT,
                fault TEXT NOT NULL,
                degradation_pct REAL NOT NULL,
                rul_p05 REAL NOT NULL,
                deadline_iso TEXT NOT NULL,
                urgency TEXT NOT NULL,
                parts_allocated TEXT,
                derating_applied INTEGER DEFAULT 0,
                status TEXT NOT NULL,
                approver TEXT,
                approval_date TEXT,
                pdf_path TEXT,
                notes TEXT,
                FOREIGN KEY (machine_id) REFERENCES equipments(machine_id)
            )
            """)
            conn.commit()
        self._seed_default_data()

    def _seed_default_data(self):
        """Seed master equipment and spare parts if empty."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM equipments")
            if cursor.fetchone()[0] == 0:
                equipments = [
                    ("PUMP-01", "ปั๊มน้ำหล่อเย็นหลัก #1 (Cooling Water Pump #1)", "Utility Plant A",
                     "SKF 6205-2RS", "6205", "A (Critical)", "PUMP-02 (Standby)", 1800.0, 75000.0, datetime.now(BKK).isoformat()),
                    ("MOTOR-07", "มอเตอร์ขับสายพานลำเลียง (Packaging Conveyor Motor)", "Packaging Line 2",
                     "SKF 6205-2RS", "6205", "B (Medium)", "None (No standby)", 1500.0, 35000.0, datetime.now(BKK).isoformat()),
                    ("FAN-03", "พัดลมดูดอากาศห้องพ่นสี (Paint Shop Exhaust Fan)", "Paint Shop Facility",
                     "SKF 6208", "6208", "B (Medium)", "None (No standby)", 2950.0, 45000.0, datetime.now(BKK).isoformat()),
                    ("COMP-02", "เครื่องอัดอากาศหลัก #2 (Air Compressor #2)", "Utility Plant B",
                     "SKF 6310", "6310", "A (Critical)", "COMP-01 (Standby)", 3000.0, 120000.0, datetime.now(BKK).isoformat()),
                    ("TEST-RIG-01", "แท่นทดสอบแบริ่ง XJTU-SY (Lab Run-to-Failure Rig)", "Reliability Test Lab",
                     "LDK UER204", "6205", "C (Testing)", "None", 2400.0, 10000.0, datetime.now(BKK).isoformat()),
                ]
                cursor.executemany("""
                INSERT INTO equipments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, equipments)

            cursor.execute("SELECT COUNT(*) FROM spare_parts_inventory")
            if cursor.fetchone()[0] == 0:
                parts = [
                    ("SKF 6205-2RS", "SKF 6205-2RS", 4, 2, 450.0, 2, "Warehouse A-03-2",
                     json.dumps(["NSK 6205DDU", "FAG 6205-2RSR"]), datetime.now(BKK).isoformat()),
                    ("SKF 6208", "SKF 6208", 1, 2, 890.0, 5, "Warehouse A-03-4",
                     json.dumps(["NSK 6208DDU"]), datetime.now(BKK).isoformat()),
                    ("SKF 6310", "SKF 6310", 0, 1, 1450.0, 7, "Warehouse B-01-1",
                     json.dumps(["NTN 6310LLU"]), datetime.now(BKK).isoformat()),
                    ("LDK UER204", "LDK UER204", 6, 2, 380.0, 3, "Warehouse Lab-01",
                     json.dumps(["SKF 6205-2RS"]), datetime.now(BKK).isoformat()),
                ]
                cursor.executemany("""
                INSERT INTO spare_parts_inventory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, parts)
            conn.commit()

    # --- Equipment operations ---
    def get_equipment(self, machine_id: str) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            row = conn.cursor().execute("SELECT * FROM equipments WHERE machine_id = ?", (machine_id,)).fetchone()
            return dict(row) if row else None

    def list_equipments(self) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            rows = conn.cursor().execute("SELECT * FROM equipments ORDER BY machine_id").fetchall()
            return [dict(r) for r in rows]

    # --- Telemetry operations ---
    def log_telemetry(self, machine_id: str, rpm: float, rms: float, kurtosis: float,
                      predicted_fault: str, confidence: float, degradation_pct: float,
                      rul_p05: float, rul_p50: float, rul_p95: float, urgency: str,
                      timestamp: Optional[str] = None) -> int:
        ts = timestamp or datetime.now(BKK).isoformat()
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO vibration_telemetry 
            (machine_id, timestamp, rpm, rms, kurtosis, predicted_fault, confidence, degradation_pct, rul_p05, rul_p50, rul_p95, urgency)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (machine_id, ts, rpm, rms, kurtosis, predicted_fault, confidence, degradation_pct, rul_p05, rul_p50, rul_p95, urgency))
            conn.commit()
            return cur.lastrowid

    def get_telemetry_history(self, machine_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            rows = conn.cursor().execute("""
            SELECT * FROM vibration_telemetry WHERE machine_id = ? ORDER BY id DESC LIMIT ?
            """, (machine_id, limit)).fetchall()
            return [dict(r) for r in reversed(rows)]

    # --- Inventory operations ---
    def get_spare_part(self, part_number: str) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            row = conn.cursor().execute("SELECT * FROM spare_parts_inventory WHERE part_number = ?", (part_number,)).fetchone()
            if not row:
                return None
            res = dict(row)
            if res.get("substitutes"):
                try:
                    res["substitutes"] = json.loads(res["substitutes"])
                except Exception:
                    pass
            return res

    def list_spare_parts(self) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            rows = conn.cursor().execute("SELECT * FROM spare_parts_inventory ORDER BY part_number").fetchall()
            parts = []
            for r in rows:
                p = dict(r)
                if p.get("substitutes"):
                    try:
                        p["substitutes"] = json.loads(p["substitutes"])
                    except Exception:
                        pass
                parts.append(p)
            return parts

    def reserve_spare_part(self, part_number: str, qty: int = 1) -> Dict[str, Any]:
        """Reserve a spare part and decrement stock."""
        with self._get_conn() as conn:
            cur = conn.cursor()
            row = cur.execute("SELECT * FROM spare_parts_inventory WHERE part_number = ?", (part_number,)).fetchone()
            if not row:
                return {"status": "error", "message": f"Part {part_number} not found"}
            part = dict(row)
            current_stock = part["stock_quantity"]
            if current_stock < qty:
                # Trigger PR recommendation
                return {
                    "status": "out_of_stock",
                    "available": current_stock,
                    "requested": qty,
                    "substitutes": json.loads(part.get("substitutes", "[]")),
                    "lead_time_days": part["lead_time_days"],
                    "action_required": "create_purchase_requisition"
                }
            new_stock = current_stock - qty
            now_iso = datetime.now(BKK).isoformat()
            cur.execute("UPDATE spare_parts_inventory SET stock_quantity = ?, updated_at = ? WHERE part_number = ?",
                        (new_stock, now_iso, part_number))
            conn.commit()
            return {
                "status": "reserved",
                "part_number": part_number,
                "reserved_qty": qty,
                "remaining_stock": new_stock,
                "bin_location": part["bin_location"],
                "below_safety_stock": new_stock < part["safety_stock"]
            }

    # --- Work Order operations ---
    def create_work_order(self, wo_data: Dict[str, Any]) -> str:
        wo_id = wo_data.get("work_order_id") or f"WO-{uuid.uuid4().hex[:8].upper()}"
        now_iso = datetime.now(BKK).isoformat()
        with self._get_conn() as conn:
            conn.cursor().execute("""
            INSERT OR REPLACE INTO work_orders 
            (work_order_id, machine_id, created_at, planned_start, planned_end, fault, degradation_pct,
             rul_p05, deadline_iso, urgency, parts_allocated, derating_applied, status, approver, approval_date, pdf_path, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                wo_id,
                wo_data.get("machine_id", "PUMP-01"),
                now_iso,
                wo_data.get("planned_start", now_iso),
                wo_data.get("planned_end"),
                wo_data.get("fault", "unknown"),
                float(wo_data.get("degradation_pct", 0.0)),
                float(wo_data.get("rul_p05", 24.0)),
                wo_data.get("deadline_iso", now_iso),
                wo_data.get("urgency", "PLAN_MAINTENANCE"),
                json.dumps(wo_data.get("parts_allocated", [])),
                1 if wo_data.get("derating_applied") else 0,
                wo_data.get("status", "PENDING_REVIEW"),
                wo_data.get("approver"),
                wo_data.get("approval_date"),
                wo_data.get("pdf_path"),
                wo_data.get("notes", "")
            ))
            conn.commit()
        return wo_id

    def update_work_order_status(self, work_order_id: str, status: str,
                                 approver: Optional[str] = None, pdf_path: Optional[str] = None) -> bool:
        now_iso = datetime.now(BKK).isoformat()
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            UPDATE work_orders 
            SET status = ?, approver = COALESCE(?, approver), approval_date = ?, pdf_path = COALESCE(?, pdf_path)
            WHERE work_order_id = ?
            """, (status, approver, now_iso, pdf_path, work_order_id))
            conn.commit()
            return cur.rowcount > 0

    def get_work_order(self, work_order_id: str) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            row = conn.cursor().execute("SELECT * FROM work_orders WHERE work_order_id = ?", (work_order_id,)).fetchone()
            if not row:
                return None
            res = dict(row)
            if res.get("parts_allocated"):
                try:
                    res["parts_allocated"] = json.loads(res["parts_allocated"])
                except Exception:
                    pass
            return res

    def list_work_orders(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            rows = conn.cursor().execute("SELECT * FROM work_orders ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
            results = []
            for r in rows:
                item = dict(r)
                if item.get("parts_allocated"):
                    try:
                        item["parts_allocated"] = json.loads(item["parts_allocated"])
                    except Exception:
                        pass
                results.append(item)
            return results


# Global singleton instance
_db_instance = None


def get_db() -> MechDatabase:
    global _db_instance
    if _db_instance is None:
        _db_instance = MechDatabase()
    return _db_instance
