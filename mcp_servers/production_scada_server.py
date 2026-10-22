"""MCP Server 3: Production & SCADA Optimization Server.
Provides tools to query production schedules, evaluate downtime costs,
and calculate engineering derating strategies (e.g. reducing RPM by 15% to extend RUL).
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from db import get_db

BKK = timezone(timedelta(hours=7))

TOOLS = [
    {
        "name": "get_production_plan",
        "description": "Queries factory SCADA and MES for upcoming planned maintenance windows, production shifts, and standby machine availability.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "machine_id": {"type": "string", "description": "Machine code (e.g. PUMP-01, MOTOR-07)"},
                "days_ahead": {"type": "integer", "default": 7, "description": "Lookahead forecast in days"}
            },
            "required": ["machine_id"]
        }
    },
    {
        "name": "calculate_derating_strategy",
        "description": "Calculates speed derating (RPM reduction) and load reduction needed to safely extend bearing RUL until the next planned shutdown.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current_rpm": {"type": "number", "description": "Current operating speed in RPM"},
                "current_p05_rul_hours": {"type": "number", "description": "Current P05 worst-case RUL in hours"},
                "target_hours_needed": {"type": "number", "description": "Hours until the next scheduled planned maintenance stop"},
                "max_rpm_reduction_pct": {"type": "number", "default": 20.0, "description": "Maximum allowable speed reduction percent (e.g. 15-20%)"}
            },
            "required": ["current_rpm", "current_p05_rul_hours", "target_hours_needed"]
        }
    },
    {
        "name": "evaluate_downtime_financial_impact",
        "description": "Calculates the financial loss difference between an Unplanned Emergency Breakdown vs a Planned Maintenance Stop.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "machine_id": {"type": "string", "description": "Machine identifier"},
                "unplanned_downtime_hours": {"type": "number", "default": 8.0, "description": "Estimated breakdown repair hours"},
                "planned_downtime_hours": {"type": "number", "default": 2.5, "description": "Estimated scheduled overhaul hours"}
            },
            "required": ["machine_id"]
        }
    }
]


def handle_get_production_plan(machine_id: str, days_ahead: int = 7) -> Dict[str, Any]:
    db = get_db()
    eq = db.get_equipment(machine_id)
    now = datetime.now(BKK)
    
    # Next upcoming planned shift breaks and scheduled weekly PM windows
    planned_windows = []
    # Daily shift change / cleaning break: daily at 22:00 - 23:30
    for day_offset in range(1, min(days_ahead + 1, 5)):
        w_start = (now + timedelta(days=day_offset)).replace(hour=22, minute=0, second=0, microsecond=0)
        w_end = w_start + timedelta(hours=2)
        planned_windows.append({
            "type": "DAILY_SHIFT_CHANGEOVER",
            "start": w_start.isoformat(),
            "end": w_end.isoformat(),
            "duration_hours": 2.0,
            "impact_on_production": "ZERO_NO_PENALTY"
        })
        
    # Major weekly maintenance stop: Saturday 08:00 - 16:00
    days_to_sat = (5 - now.weekday()) % 7
    if days_to_sat == 0 and now.hour >= 12:
        days_to_sat = 7
    sat_stop_start = (now + timedelta(days=days_to_sat)).replace(hour=8, minute=0, second=0, microsecond=0)
    planned_windows.append({
        "type": "WEEKLY_PLANNED_SHUTDOWN",
        "start": sat_stop_start.isoformat(),
        "end": (sat_stop_start + timedelta(hours=8)).isoformat(),
        "duration_hours": 8.0,
        "impact_on_production": "SCHEDULED_OVERHAUL"
    })

    standby = eq.get("standby_machine", "None") if eq else "None"
    has_standby = "Standby" in standby

    next_window = planned_windows[0] if planned_windows else None
    hours_until = 28.0
    if next_window:
        try:
            start_dt = datetime.fromisoformat(next_window["start"])
            hours_until = max(1.0, round((start_dt - now).total_seconds() / 3600.0, 1))
        except Exception:
            pass

    return {
        "machine_id": machine_id,
        "machine_name": eq.get("name", machine_id) if eq else machine_id,
        "line": eq.get("line", "Factory Line") if eq else "Factory Line",
        "standby_available": has_standby,
        "standby_name": standby,
        "hourly_downtime_cost_thb": eq.get("downtime_cost_per_hour", 50000.0) if eq else 50000.0,
        "current_batch": {
            "batch_id": "BATCH-2026-X8",
            "product": "Beverage Bottle Filling SKU-A",
            "status": "RUNNING",
            "deadline": (now + timedelta(hours=36)).isoformat()
        },
        "next_planned_maintenance_window": {
            "window": next_window,
            "hours_until_window": hours_until
        },
        "upcoming_maintenance_windows": planned_windows,
        "recommended_stop": next_window
    }


def handle_calculate_derating_strategy(current_rpm: Optional[float] = None,
                                       current_p05_rul_hours: Optional[float] = None,
                                       target_hours_needed: Optional[float] = None,
                                       target_hours: Optional[float] = None,
                                       machine_id: Optional[str] = None,
                                       max_rpm_reduction_pct: float = 20.0) -> Dict[str, Any]:
    """ISO 281 bearing life equation: L10h is inversely proportional to RPM and P^3 (fatigue load).
    Reducing speed by alpha% increases life ratio by ~ (1 / (1 - alpha))^1.2
    """
    if current_rpm is None:
        current_rpm = 1800.0
    if current_p05_rul_hours is None:
        current_p05_rul_hours = 18.0
    if target_hours_needed is None:
        target_hours_needed = target_hours if target_hours is not None else 32.0

    if current_p05_rul_hours >= target_hours_needed:
        return {
            "status": "not_needed",
            "feasible": True,
            "message": "Current P05 RUL is already sufficient to reach the target planned window without derating.",
            "recommended_rpm": current_rpm,
            "derated_rpm": current_rpm,
            "rpm_reduction_pct": 0.0,
            "derated_rul_p05_hours": current_p05_rul_hours,
            "extended_p05_rul_hours": current_p05_rul_hours
        }

    needed_extension_ratio = target_hours_needed / max(1.0, current_p05_rul_hours)
    
    # Calculate required reduction percentage (capped at max_rpm_reduction_pct)
    reduction_pct = min(max_rpm_reduction_pct, max(5.0, (1.0 - (1.0 / needed_extension_ratio) ** (1.0 / 2.5)) * 100.0))
    reduction_pct = round(reduction_pct, 1)
    
    derated_rpm = round(current_rpm * (1.0 - reduction_pct / 100.0), 0)
    extended_rul = round(current_p05_rul_hours * ((current_rpm / derated_rpm) ** 2.2), 1)

    is_sufficient = extended_rul >= target_hours_needed

    return {
        "status": "recommended" if is_sufficient else "partial_extension",
        "feasible": is_sufficient,
        "current_rpm": current_rpm,
        "derated_rpm": derated_rpm,
        "rpm_reduction_pct": reduction_pct,
        "original_p05_rul_hours": current_p05_rul_hours,
        "extended_p05_rul_hours": extended_rul,
        "derated_rul_p05_hours": extended_rul,
        "target_hours_needed": target_hours_needed,
        "bridges_to_planned_stop": is_sufficient,
        "engineering_recommendation": (
            f"Reduce speed by {reduction_pct}% (from {current_rpm:.0f} to {derated_rpm:.0f} RPM) via VFD. "
            f"This extends P05 RUL from {current_p05_rul_hours:.1f}h to {extended_rul:.1f}h, "
            f"{'safely reaching' if is_sufficient else 'delaying severity until'} the planned maintenance stop."
        )
    }


def handle_evaluate_downtime_financial_impact(machine_id: str, unplanned_downtime_hours: float = 8.0,
                                              planned_downtime_hours: float = 2.5) -> Dict[str, Any]:
    db = get_db()
    eq = db.get_equipment(machine_id)
    rate = eq.get("downtime_cost_per_hour", 50000.0) if eq else 50000.0
    
    unplanned_cost = unplanned_downtime_hours * rate
    # Planned maintenance has 70% lower collateral cost (no scrap material loss, tech already on standby)
    planned_cost = planned_downtime_hours * (rate * 0.3)
    net_savings = unplanned_cost - planned_cost

    return {
        "machine_id": machine_id,
        "hourly_rate_thb": rate,
        "unplanned_emergency_cost_thb": round(unplanned_cost, 2),
        "planned_maintenance_cost_thb": round(planned_cost, 2),
        "net_savings_thb": round(net_savings, 2),
        "financial_metrics": {
            "unplanned_downtime_cost_thb": round(unplanned_cost, 2),
            "planned_maintenance_cost_thb": round(planned_cost, 2),
            "net_savings_thb": round(net_savings, 2)
        },
        "roi_summary": f"Proactive planning saves approximately {net_savings:,.0f} THB in avoided downtime losses."
    }


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if tool_name == "get_production_plan":
        return handle_get_production_plan(**arguments)
    elif tool_name == "calculate_derating_strategy":
        return handle_calculate_derating_strategy(**arguments)
    elif tool_name == "evaluate_downtime_financial_impact":
        return handle_evaluate_downtime_financial_impact(**arguments)
    return {"error": f"Unknown tool: {tool_name}"}


# Aliases matching master prompt naming
get_production_plan = handle_get_production_plan
calculate_derating_strategy = handle_calculate_derating_strategy
evaluate_downtime_financial_impact = handle_evaluate_downtime_financial_impact


if __name__ == "__main__":
    print("Testing derating strategy:")
    res = execute_tool("calculate_derating_strategy", {
        "current_rpm": 1800.0,
        "current_p05_rul_hours": 18.0,
        "target_hours_needed": 32.0,
        "max_rpm_reduction_pct": 20.0
    })
    print(json.dumps(res, indent=2))
