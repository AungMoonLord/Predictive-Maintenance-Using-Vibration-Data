import pytest
from datetime import datetime, timezone, timedelta

from report import build_report, severity_of, split_duration

BKK = timezone(timedelta(hours=7))


def test_split_duration():
    res = split_duration(25.5)
    assert res["days"] == 1
    assert res["hours"] == 1
    assert res["minutes"] == 30
    assert "1 วัน 1 ชั่วโมง 30 นาที" in res["text"]

    zero = split_duration(0)
    assert zero["days"] == 0
    assert zero["hours"] == 0
    assert zero["minutes"] == 0


def test_severity_levels():
    assert severity_of(5)["code"] == "S0"
    assert severity_of(20)["code"] == "S1"
    assert severity_of(50)["code"] == "S2"
    assert severity_of(75)["code"] == "S3"
    assert severity_of(95)["code"] == "S4"


def test_build_report():
    pred = {
        "fault": "inner_race",
        "confidence": 0.85,
        "degradation_pct": 45.0,
        "degradation_std_pct": 3.2,
        "rul_hours": {"p05": 48.0, "p50": 120.0, "p95": 250.0, "cap": 1000.0},
        "physics": {"physics_fault": "inner_race", "scores": {"inner_race": {"order": 5.415, "freq_hz": 162.45, "harmonic_snr": [10.0, 8.0, 5.0]}}},
        "ai_physics_agree": True,
        "rpm": 1800,
        "bearing": "6205"
    }
    now = datetime(2026, 10, 21, 12, 0, tzinfo=BKK)
    rep = build_report(pred, {"machine_id": "PUMP-01", "name": "ปั๊มน้ำหล่อเย็น #1"}, now=now, job_id="job-123")

    assert "summary" in rep
    assert "markdown" in rep
    assert "telegram" in rep

    s = rep["summary"]
    assert s["job_id"] == "job-123"
    assert s["fault"] == "inner_race"
    assert s["confidence"] == 0.85
    assert s["urgency"] in ("PLAN_MAINTENANCE", "HIGH")
    assert "แหวนรอบใน" in rep["markdown"]
    assert "คู่มือการแก้ปัญหาและแนวทางปฏิบัติเบื้องต้นสำหรับช่างเทคนิค" in rep["markdown"]
    assert "LOTO" in rep["markdown"]
    assert "technician_guide" in s
    assert len(s["technician_guide"]["specific_inspection"]) > 0
    assert len(s["technician_guide"]["standard_sop"]) > 0
