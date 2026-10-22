from datetime import datetime, timedelta, timezone
import pytest

from handler import gatekeeper
from tools import BKK, TOOL_SPECS, approval_token, exp_trend_rul


def test_tool_specs():
    assert len(TOOL_SPECS) == 7
    names = [t["toolSpec"]["name"] for t in TOOL_SPECS]
    assert "get_machine_profile" in names
    assert "get_health_history" in names
    assert "submit_for_approval" in names


def test_approval_token():
    t1 = approval_token("job-001", "approve")
    t2 = approval_token("job-001", "approve")
    t3 = approval_token("job-001", "reject")
    assert t1 == t2
    assert t1 != t3
    assert len(t1) == 32


def test_exp_trend_rul():
    now = datetime.now(BKK)
    # Exponential growth in degradation: 10, 20, 40
    readings = [
        {"sk": f"READING#{(now - timedelta(hours=20)).isoformat()}", "deg_pct": 10.0},
        {"sk": f"READING#{(now - timedelta(hours=10)).isoformat()}", "deg_pct": 20.0},
        {"sk": f"READING#{now.isoformat()}", "deg_pct": 40.0},
    ]
    res = exp_trend_rul(readings, failure_pct=100.0)
    assert res["status"] == "ok"
    assert "rul_hours_trend" in res
    assert res["rul_hours_trend"] > 0


def test_gatekeeper_decision():
    now = datetime.now(BKK)
    profile = {"machine_id": "PUMP-01"}

    # Healthy -> no LLM call
    healthy_pred = {
        "fault": "normal",
        "confidence": 0.95,
        "degradation_pct": 5.0,
        "rul_hours": {"p05": 500.0, "p50": 800.0},
        "physics": {"physics_fault": "normal"},
    }
    trigger, reasons = gatekeeper(healthy_pred, profile, now)
    assert not trigger

    # Fault detected with high confidence -> trigger LLM
    fault_pred = {
        "fault": "inner_race",
        "confidence": 0.85,
        "degradation_pct": 35.0,
        "rul_hours": {"p05": 48.0, "p50": 100.0},
        "physics": {"physics_fault": "inner_race"},
    }
    trigger, reasons = gatekeeper(fault_pred, profile, now)
    assert trigger
    assert any("inner_race" in r for r in reasons)
