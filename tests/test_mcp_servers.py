"""Unit tests for Phase 3: Multi-Server MCP Architecture.
Tests all 4 MCP servers and their specialized tools.
"""
from pathlib import Path
import numpy as np
import pytest

from mcp_servers.physics_diagnostic_server import (
    analyze_vibration_signal,
    calculate_envelope_orders
)
from mcp_servers.cmms_inventory_server import (
    check_spare_parts_stock,
    reserve_spare_parts,
    create_work_order
)
from mcp_servers.production_scada_server import (
    get_production_plan,
    calculate_derating_strategy,
    evaluate_downtime_financial_impact
)
from mcp_servers.safety_sop_server import (
    get_safety_loto_procedure,
    generate_thai_maintenance_pdf
)


def test_physics_diagnostic_server():
    """Test vibration analysis and envelope order calculations."""
    dummy_signal = list(np.random.normal(0, 0.2, 4096))
    
    # Tool 1: calculate_envelope_orders
    ord_res = calculate_envelope_orders(bearing="6205")
    assert "6205" in ord_res["bearing"]
    assert ord_res["fault_orders"]["inner_race"] > 0
    assert ord_res["fault_orders"]["outer_race"] > 0
    
    # Tool 2: analyze_vibration_signal
    diag = analyze_vibration_signal(signal=dummy_signal, rpm=1800.0, bearing="6205")
    assert "time_features" in diag
    assert "rms" in diag["time_features"]
    assert "kurtosis" in diag["time_features"]
    assert "physics_check" in diag


def test_cmms_inventory_server():
    """Test spare parts query, stock reservation, and work order creation."""
    # Ensure test stock is populated
    from db import get_db
    db = get_db()
    with db._get_conn() as conn:
        conn.cursor().execute("UPDATE spare_parts_inventory SET stock_quantity = 5 WHERE part_number = 'SKF 6205-2RS'")
        conn.commit()

    # Tool 1: check_spare_parts_stock
    stock = check_spare_parts_stock(bearing_model="SKF 6205-2RS")
    assert "part_number" in stock
    assert stock["is_available"] is True
    
    # Tool 2: reserve_spare_parts
    resv = reserve_spare_parts(bearing_model="SKF 6205-2RS", quantity=1)
    assert resv["status"] == "reserved"
    assert "reservation_id" in resv
    
    # Tool 3: create_work_order
    wo = create_work_order(
        machine_id="PUMP-01",
        fault_type="inner_race",
        recommended_action="Replace SKF 6205 bearing",
        planned_start="2026-10-25T14:00:00+07:00",
        safety_deadline="2026-10-25T18:00:00+07:00",
        parts_required=["SKF 6205-2RS"],
        urgency="URGENT",
        summary_th="แผนเปลี่ยนตลับลูกปืนปั๊มน้ำหล่อเย็น"
    )
    assert wo["status"] in ("created", "success")
    assert "work_order_id" in wo


def test_production_scada_server():
    """Test production schedule lookup, derating calculation, and downtime financial impact."""
    # Tool 1: get_production_plan
    plan = get_production_plan(machine_id="PUMP-01")
    assert "current_batch" in plan
    assert "next_planned_maintenance_window" in plan
    
    # Tool 2: calculate_derating_strategy
    derate = calculate_derating_strategy(
        current_rpm=1800.0,
        current_p05_rul_hours=18.0,
        target_hours_needed=28.0,
        max_rpm_reduction_pct=20.0
    )
    assert derate["rpm_reduction_pct"] > 0
    assert derate["derated_rpm"] < 1800.0
    # Fatigue life L10h extension
    assert derate["derated_rul_p05_hours"] > 18.0
    
    # Tool 3: evaluate_downtime_financial_impact
    impact = evaluate_downtime_financial_impact(
        machine_id="PUMP-01",
        unplanned_downtime_hours=8.0,
        planned_downtime_hours=2.5
    )
    assert impact["financial_metrics"]["net_savings_thb"] > 0


def test_safety_sop_server(tmp_path):
    """Test LOTO procedures retrieval and Thai PDF generation."""
    # Tool 1: get_safety_loto_procedure
    sop = get_safety_loto_procedure(machine_id="PUMP-01", fault_type="inner_race")
    assert len(sop["loto_procedure"]["electrical"]) >= 3
    assert len(sop["loto_procedure"]["mechanical"]) >= 2
    assert len(sop["loto_procedure"]["ppe"]) >= 3
    
    # Tool 2: generate_thai_maintenance_pdf
    sample_md = "# ใบสั่งซ่อมบำรุงเร่งด่วน\n- เครื่องจักร: PUMP-01\n- การดำเนินการ: สับเปลี่ยนตลับลูกปืน\n- มาตรการ: ปฏิบัติตาม LOTO"
    out_pdf = tmp_path / "test_thai_wo.pdf"
    res = generate_thai_maintenance_pdf(
        markdown_content=sample_md,
        output_filename=str(out_pdf),
        title="ใบสั่งงานซ่อมบำรุง"
    )
    assert res["status"] == "success"
    assert Path(res["pdf_path"]).exists()
    assert Path(res["pdf_path"]).stat().st_size > 1000
    
    with open(res["pdf_path"], "rb") as f:
        header = f.read(4)
        assert header == b"%PDF"
