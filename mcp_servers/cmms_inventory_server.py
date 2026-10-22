"""MCP Server 2: CMMS & Inventory Server.
Provides tools to inspect spare parts stock, reserve parts, issue purchase
requisitions (PR) if inventory is depleted, and create maintenance work orders.
"""
import json
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from db import get_db

BKK = timezone(timedelta(hours=7))

TOOLS = [
    {
        "name": "check_spare_parts_stock",
        "description": "Checks warehouse inventory for a specific bearing model, availability, safety stock, and known substitutes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "bearing_model": {"type": "string", "description": "Bearing part number or model (e.g. SKF 6205-2RS, SKF 6208)"}
            },
            "required": ["bearing_model"]
        }
    },
    {
        "name": "reserve_spare_parts",
        "description": "Reserves a quantity of spare bearings from the warehouse and decrements available inventory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "bearing_model": {"type": "string", "description": "Bearing part number to reserve"},
                "quantity": {"type": "integer", "default": 1, "description": "Quantity to allocate"}
            },
            "required": ["bearing_model"]
        }
    },
    {
        "name": "create_purchase_requisition",
        "description": "Generates an expedited Purchase Requisition (PR) when stock is zero or below safety stock.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "bearing_model": {"type": "string", "description": "Bearing model to purchase"},
                "quantity": {"type": "integer", "default": 2, "description": "Quantity to order"},
                "urgency": {"type": "string", "enum": ["ROUTINE", "EXPEDITED", "EMERGENCY"], "default": "EXPEDITED"},
                "justification": {"type": "string", "description": "Reason for PR"}
            },
            "required": ["bearing_model"]
        }
    },
    {
        "name": "create_work_order",
        "description": "Generates an official maintenance Work Order (WO) with planned start, safety deadline, and reserved parts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "machine_id": {"type": "string", "description": "Machine identifier (e.g. PUMP-01)"},
                "fault": {"type": "string", "description": "Diagnosed bearing fault location"},
                "degradation_pct": {"type": "number", "description": "Predicted degradation percentage"},
                "planned_start": {"type": "string", "description": "ISO timestamp for proposed maintenance window"},
                "deadline_iso": {"type": "string", "description": "P05 worst-case safety deadline"},
                "parts_allocated": {"type": "array", "items": {"type": "string"}, "description": "List of reserved bearing models"},
                "urgency": {"type": "string", "description": "Urgency rating (NORMAL, PLAN_MAINTENANCE, URGENT, EMERGENCY)"},
                "notes": {"type": "string", "description": "Technician instructions or remarks"}
            },
            "required": ["machine_id", "fault", "planned_start", "deadline_iso"]
        }
    }
]


def handle_check_spare_parts_stock(bearing_model: str) -> Dict[str, Any]:
    db = get_db()
    part = db.get_spare_part(bearing_model)
    if not part:
        # Search partial match
        all_parts = db.list_spare_parts()
        for p in all_parts:
            if bearing_model.lower() in p["part_number"].lower() or bearing_model.lower() in p["bearing_model"].lower():
                part = p
                break
    if not part:
        return {
            "status": "not_found",
            "bearing_model": bearing_model,
            "message": f"Part {bearing_model} is not tracked in warehouse inventory",
            "action": "create_purchase_requisition"
        }
    return {
        "status": "in_stock" if part["stock_quantity"] > 0 else "out_of_stock",
        "is_available": part["stock_quantity"] > 0,
        "part_number": part["part_number"],
        "stock_quantity": part["stock_quantity"],
        "safety_stock": part["safety_stock"],
        "unit_price_thb": part["unit_price_thb"],
        "lead_time_days": part["lead_time_days"],
        "bin_location": part["bin_location"],
        "substitutes": part.get("substitutes", []),
        "below_safety_stock": part["stock_quantity"] <= part["safety_stock"]
    }


def handle_reserve_spare_parts(bearing_model: str, quantity: int = 1) -> Dict[str, Any]:
    db = get_db()
    res = db.reserve_spare_part(bearing_model, qty=quantity)
    res["reservation_id"] = f"RESV-{uuid.uuid4().hex[:8].upper()}"
    return res


def handle_create_purchase_requisition(bearing_model: str, quantity: int = 2,
                                       urgency: str = "EXPEDITED", justification: str = "") -> Dict[str, Any]:
    pr_id = f"PR-{uuid.uuid4().hex[:8].upper()}"
    now = datetime.now(BKK)
    return {
        "pr_id": pr_id,
        "created_at": now.isoformat(),
        "bearing_model": bearing_model,
        "order_quantity": quantity,
        "urgency": urgency,
        "vendor": "Authorized Industrial Bearing Distributor",
        "estimated_arrival": (now + timedelta(days=2 if urgency == "EMERGENCY" else 5)).isoformat(),
        "justification": justification or "Automated Predictive Maintenance Replenishment",
        "status": "SUBMITTED_TO_PURCHASING"
    }


def handle_create_work_order(**kwargs) -> Dict[str, Any]:
    db = get_db()
    wo_id = db.create_work_order(kwargs)
    wo = db.get_work_order(wo_id)
    return {
        "status": "success",
        "work_order_id": wo_id,
        "details": wo
    }


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if tool_name == "check_spare_parts_stock":
        return handle_check_spare_parts_stock(**arguments)
    elif tool_name == "reserve_spare_parts":
        return handle_reserve_spare_parts(**arguments)
    elif tool_name == "create_purchase_requisition":
        return handle_create_purchase_requisition(**arguments)
    elif tool_name == "create_work_order":
        return handle_create_work_order(**arguments)
    return {"error": f"Unknown tool: {tool_name}"}


# Aliases matching master prompt naming
check_spare_parts_stock = handle_check_spare_parts_stock
reserve_spare_parts = handle_reserve_spare_parts
create_purchase_requisition = handle_create_purchase_requisition
create_work_order = handle_create_work_order


if __name__ == "__main__":
    print("Testing check_spare_parts_stock for SKF 6205-2RS:")
    res = execute_tool("check_spare_parts_stock", {"bearing_model": "SKF 6205-2RS"})
    print(json.dumps(res, indent=2, ensure_ascii=False))
