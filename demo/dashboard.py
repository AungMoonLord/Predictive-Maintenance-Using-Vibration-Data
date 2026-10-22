"""MechAgent: Agentic AI Predictive Maintenance Dashboard
Runs locally with the trained model or connects to an AWS HTTP API.
Usage:
    streamlit run demo/dashboard.py
"""
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Configure UTF-8 for console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "src"))
sys.path.insert(0, str(BASE_DIR / "agent"))

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import streamlit as st

from bearing_physics import get_bearing, envelope_spectrum, time_features
from mech_config import FS, N_SAMPLES, CLASSES
from pdf_generator import markdown_to_pdf_bytes
from real_dataset import load_cwru_mat, load_xjtu_csv, prepare_signal_window
from report import build_report, FAULT_TH, severity_of
from simulate import simulate_signal
from tools import approval_token

BKK = timezone(timedelta(hours=7))

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="MechAgent | AI Predictive Maintenance",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    .main-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }
    
    .kpi-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.4);
    }
    
    .kpi-title {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 6px;
    }
    
    .kpi-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 4px;
    }
    
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-green { background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-yellow { background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-orange { background-color: rgba(249, 115, 22, 0.2); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.3); }
    .badge-red { background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-blue { background-color: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    
    .sop-step {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
    
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #38bdf8;
        margin-top: 18px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- MASTER DATA -----------------
MACHINES_DB = {
    "PUMP-01": {
        "name": "ปั๊มน้ำหล่อเย็นหลัก #1 (Cooling Water Pump #1)",
        "line": "Utility Plant A",
        "bearing_model": "SKF 6205-2RS",
        "bearing_key": "6205",
        "criticality": "A (Critical)",
        "standby_machine": "PUMP-02 (Standby)",
        "rated_rpm": 1800,
        "history": [10, 14, 19, 26, 34],
    },
    "MOTOR-07": {
        "name": "มอเตอร์ขับสายพานลำเลียง (Packaging Conveyor Motor)",
        "line": "Packaging Line 2",
        "bearing_model": "SKF 6205-2RS",
        "bearing_key": "6205",
        "criticality": "B (Medium)",
        "standby_machine": "None (No standby)",
        "rated_rpm": 1500,
        "history": [6, 8, 11, 15, 22],
    },
    "FAN-03": {
        "name": "พัดลมดูดอากาศห้องพ่นสี (Paint Shop Exhaust Fan)",
        "line": "Paint Shop Facility",
        "bearing_model": "SKF 6208",
        "bearing_key": "6208",
        "criticality": "B (Medium)",
        "standby_machine": "None (No standby)",
        "rated_rpm": 2950,
        "history": [8, 9, 12, 18, 30],
    },
}

SPARE_PARTS_DB = {
    "SKF 6205-2RS": {"stock": 4, "location": "Warehouse A-03-2", "lead_time_days": 2, "price_thb": 450, "substitutes": ["NSK 6205DDU", "FAG 6205-2RSR"]},
    "SKF 6208": {"stock": 1, "location": "Warehouse A-03-4", "lead_time_days": 5, "price_thb": 890, "substitutes": ["NSK 6208DDU"]},
    "SKF 6310": {"stock": 0, "location": "Warehouse B-01-1", "lead_time_days": 7, "price_thb": 1450, "substitutes": ["NTN 6310LLU"]},
}

# ----------------- CACHED LOCAL PREDICTOR -----------------
@st.cache_resource(show_spinner="กำลังโหลดโมเดล Multitask AI...")
def load_local_predictor():
    model_dir = BASE_DIR / "artifacts" / "model"
    if not (model_dir / "model.pt").exists() or not (model_dir / "mechagent_config.json").exists():
        return None
    from inference import MechAgentPredictor
    return MechAgentPredictor(str(model_dir))

predictor = load_local_predictor()

# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.title("⚙️ MechAgent Control")
    st.caption("ระบบตรวจจับความผิดปกติและประเมินอายุคงเหลือ (RUL)")
    
    st.markdown("---")
    
    # Engine Mode: Standalone Physics-Informed MTL Model
    engine_mode = "🚀 Local Model (Standalone AI)"
    api_url = os.environ.get("MECHAGENT_API", "https://jynfhl5nc9.execute-api.ap-southeast-1.amazonaws.com").rstrip("/")
    
    st.subheader("1. เลือกเครื่องจักร (Equipment)")
    machine_key = st.selectbox("เลือกเครื่องจักรเป้าหมาย:", list(MACHINES_DB.keys()), format_func=lambda k: f"{k} - {MACHINES_DB[k]['name'][:25]}...")
    machine_info = MACHINES_DB[machine_key]
    bearing_model = machine_info["bearing_model"]
    bearing_key = machine_info["bearing_key"]
    
    b_geom = get_bearing(bearing_key)
    orders = b_geom.fault_orders()
    
    with st.expander("ℹ️ ข้อมูลตลับลูกปืน & Order Frequencies", expanded=False):
        st.write(f"**Model:** `{b_geom.name}`")
        st.write(f"**จำนวนเม็ดลูกปืน:** {b_geom.n_balls} เม็ด")
        st.write(f"**BPFI (Inner):** `{orders['inner_race']:.2f}X`")
        st.write(f"**BPFO (Outer):** `{orders['outer_race']:.2f}X`")
        st.write(f"**BSF (Ball):** `{orders['ball']:.2f}X`")
        st.write(f"**FTF (Cage):** `{orders['cage']:.2f}X`")

    st.markdown("---")
    st.subheader("2. แหล่งข้อมูลการสั่นสะเทือน (Vibration Data Source)")
    
    data_source_mode = st.radio(
        "เลือกประเภทแหล่งสัญญาณ:",
        ["🎲 จำลองสัญญาณ (Simulation)", "📂 ข้อมูลจริงจาก LAB (CWRU / XJTU-SY)"],
        index=0,
        help="สลับระหว่างการสร้างสัญญาณจำลองตามฟิสิกส์ หรือโหลดข้อมูลจริงจากตลับลูกปืนในห้องทดลอง"
    )
    
    real_sig_ready = False
    real_signal = None
    real_rpm = machine_info["rated_rpm"]
    
    if data_source_mode == "📂 ข้อมูลจริงจาก LAB (CWRU / XJTU-SY)":
        st.info("💡 ข้อมูลจริงจากห้องทดลอง CWRU (Case Western Reserve) และ XJTU-SY (Xi'an Jiaotong University)")
        
        lab_choice = st.radio(
            "เลือกฐานข้อมูลแล็บ:",
            ["🔬 XJTU-SY Run-to-Failure (Nested Time-series)", "⚙️ CWRU Bearing Dataset (.mat)"],
            index=0
        )
        
        target_source = None
        source_name = ""
        
        if "XJTU-SY" in lab_choice:
            xjtu_base = BASE_DIR / "real_dataset_from_lab" / "XJTU-SY" / "XJTU-SY_Bearing_Datasets"
            cond_dirs = [d for d in xjtu_base.iterdir() if d.is_dir()] if xjtu_base.exists() else []
            cond_names = [d.name for d in cond_dirs] if cond_dirs else ["40Hz10kN", "35Hz12kN", "37.5Hz11kN"]
            
            sel_cond = st.selectbox("เลือกสภาวะการทดสอบ (Condition):", cond_names)
            
            cond_path = xjtu_base / sel_cond
            bearing_dirs = [d for d in cond_path.iterdir() if d.is_dir()] if cond_path.exists() else []
            bearing_names = [d.name for d in bearing_dirs] if bearing_dirs else ["Bearing3_4", "Bearing1_1"]
            
            sel_bearing = st.selectbox("เลือกลูกปืนทดสอบ (Bearing):", bearing_names)
            
            b_path = cond_path / sel_bearing
            csv_files = []
            if b_path.exists():
                # Critical requirement: sort numerically by integer stem!
                csv_files = sorted([f for f in b_path.glob("*.csv")],
                                   key=lambda p: int(p.stem) if p.stem.isdigit() else 999999)
            
            if csv_files:
                file_idx = st.slider(
                    f"ช่วงเวลาการทดสอบ (นาทีที่ 1 ถึง {len(csv_files)}):",
                    min_value=1,
                    max_value=len(csv_files),
                    value=min(120, len(csv_files)),
                    step=1,
                    help="เลือกไฟล์ตามลำดับเวลา เพื่อดูวิวัฒนาการความเสื่อมสภาพ (Run-to-Failure Evolution)"
                )
                chosen_file = csv_files[file_idx - 1]
                target_source = str(chosen_file)
                source_name = f"{sel_cond}/{sel_bearing}/{chosen_file.name}"
            else:
                st.warning("ไม่พบไฟล์ CSV ในโฟลเดอร์นี้")
        else:
            cwru_base = BASE_DIR / "real_dataset_from_lab" / "CWRU"
            mat_files = sorted([f for f in cwru_base.glob("*.mat")]) if cwru_base.exists() else []
            mat_names = [f.name for f in mat_files] if mat_files else ["Normal_0.mat", "IR007_0.mat", "OR0076_0.mat"]
            
            sel_mat = st.selectbox("เลือกไฟล์ทดสอบ CWRU (.mat):", mat_names)
            if mat_files:
                target_source = str(cwru_base / sel_mat)
                source_name = f"CWRU/{sel_mat}"
                
        if target_source is not None:
            try:
                if source_name.endswith(".mat"):
                    raw_s, det_rpm, det_fault, det_sev = load_cwru_mat(target_source)
                else:
                    raw_s, det_rpm = load_xjtu_csv(target_source)
                    det_fault, det_sev = "unknown", 0.5
                    
                real_signal = prepare_signal_window(raw_s)
                real_rpm = float(det_rpm)
                real_sig_ready = True
                
                st.success(f"✅ โหลดข้อมูลสำเร็จ: `{source_name}`")
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("ความยาวข้อมูลดิบ", f"{len(raw_s):,} pts")
                    st.metric("Resampled Signal", f"{len(real_signal):,} pts")
                with c2:
                    st.metric("ความเร็วรอบเพลา", f"{real_rpm:.0f} RPM")
                    rms_val = float(np.sqrt(np.mean(real_signal**2)))
                    st.metric("RMS Level", f"{rms_val:.3f} g")
                    
                real_rpm = st.number_input("ปรับแต่งความเร็วรอบเพลา (RPM):", min_value=300, max_value=6000, value=int(real_rpm), step=50)
            except Exception as ex:
                st.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์: {ex}")
            
        sim_fault = "normal"
        sim_sev = 0.5
        sim_rpm = real_rpm
    else:
        col_preset1, col_preset2 = st.columns(2)
        with col_preset1:
            if st.button("ปกติ (Healthy)", use_container_width=True):
                st.session_state["sim_fault"] = "normal"
                st.session_state["sim_sev"] = 0.0
                st.session_state["sim_rpm"] = machine_info["rated_rpm"]
        with col_preset2:
            if st.button("วิกฤต (Severe)", use_container_width=True):
                st.session_state["sim_fault"] = "inner_race"
                st.session_state["sim_sev"] = 0.75
                st.session_state["sim_rpm"] = machine_info["rated_rpm"]

        fault_options = ["normal", "inner_race", "outer_race", "ball", "cage"]
        fault_labels = {
            "normal": "🟢 ปกติ (Healthy)",
            "inner_race": "🔴 แหวนรอบใน (Inner Race Fault)",
            "outer_race": "🟠 แหวนรอบนอก (Outer Race Fault)",
            "ball": "🟡 เม็ดลูกปืน (Ball Spin Fault)",
            "cage": "🟣 รังลูกปืน (Cage Failure)",
        }
        
        sim_fault = st.selectbox(
            "รูปแบบความเสียหาย:",
            fault_options,
            index=fault_options.index(st.session_state.get("sim_fault", "inner_race")),
            format_func=lambda f: fault_labels[f]
        )
        
        # Engineering guardrail: Lock Severity to 0.0 when fault is Healthy (normal)
        if sim_fault == "normal":
            sim_sev = 0.0
            st.slider(
                "ระดับความรุนแรง (Severity):",
                0.0, 1.0, 0.0, step=0.05, disabled=True,
                help="🛡️ Guardrail: รูปแบบปกติ (Healthy) ถูกล็อกค่า Severity ให้เป็น 0.0 เสมอตามหลักวิศวกรรม"
            )
        else:
            sim_sev = st.slider(
                "ระดับความรุนแรง (Severity):",
                0.0, 1.0,
                float(st.session_state.get("sim_sev", 0.65)),
                step=0.05,
                help="0.0 = ของใหม่, 1.0 = เสียหายขั้นวิกฤต"
            )
        
        sim_rpm = st.slider(
            "ความเร็วรอบเพลา (RPM):",
            900, 3600,
            int(st.session_state.get("sim_rpm", machine_info["rated_rpm"])),
            step=50
        )
        
    mc_samples = st.slider("Monte Carlo Dropout Samples:", min_value=50, max_value=200, value=100, step=10, help="ประเมิน Epistemic Uncertainty ของ RUL ให้มีเสถียรภาพทางสถิติ (P05 <= P50 <= P95)")
    
    st.markdown("---")
    analyze_btn = st.button("🚀 วิเคราะห์ความสั่นสะเทือน (Analyze Vibration)", type="primary", use_container_width=True)

# ----------------- MAIN VIEW -----------------
# Header banner
st.markdown(f"""
<div class="main-header">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
        <div>
            <h1 style="margin:0; font-size:1.85rem; font-weight:800; background:linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                MechAgent: Physics-Informed Agentic Maintenance
            </h1>
            <p style="margin:6px 0 0 0; color:#94a3b8; font-size:0.95rem;">
                ระบบ AI วิเคราะห์แรงสั่นสะเทือนตลับลูกปืน • ประเมิน RUL • ค้นหาคู่มือซ่อม • ออกใบสั่งงานอัตโนมัติ
            </p>
        </div>
        <div style="text-align:right;">
            <span class="badge badge-blue">Engine: {'Local Model' if 'Local' in engine_mode else 'AWS Serverless'}</span>
            <div style="font-size:0.85rem; color:#64748b; margin-top:4px;">
                เวลาโรงงาน: {datetime.now(BKK):%d/%m/%Y %H:%M:%S}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Run Analysis Trigger
if analyze_btn:
    if data_source_mode == "📂 ข้อมูลจริงจาก LAB (CWRU / XJTU-SY)" and not real_sig_ready:
        st.error("กรุณาอัปโหลดไฟล์หรือเลือกตัวอย่างจากแล็บก่อนกดวิเคราะห์")
    else:
        with st.spinner("กำลังประมวลผลสัญญาณและวิเคราะห์ด้วย AI + Envelope Physics..."):
            rng = np.random.default_rng()
            if data_source_mode == "📂 ข้อมูลจริงจาก LAB (CWRU / XJTU-SY)":
                signal = real_signal
                active_rpm = float(real_rpm)
            else:
                signal = simulate_signal(sim_fault, sim_sev, float(sim_rpm), rng, bearing=bearing_key)
                active_rpm = float(sim_rpm)
                
            st.session_state["current_signal"] = signal
            st.session_state["current_rpm"] = active_rpm
            st.session_state["current_bearing"] = bearing_key
            st.session_state["current_machine"] = machine_key
            
            if "Local" in engine_mode:
                if predictor is None:
                    st.error("ไม่พบโมเดลที่บันทึกไว้ใน `artifacts/model/` กรุณารัน `python src/pipeline.py --quick` ก่อนใช้งาน")
                else:
                    pred = predictor.predict(signal, active_rpm, bearing=bearing_key, mc_samples=mc_samples)
                    job_id = f"LOCAL-{int(time.time()*1000)%1000000}"
                    rep = build_report(pred, machine_info, now=datetime.now(BKK), job_id=job_id)
                    
                    # Run Multi-Agent Collaborative Debate
                    from agent.agent_core import run_agent
                    ctx = {
                        "job_id": job_id,
                        "machine_id": machine_key,
                        "rpm": active_rpm,
                        "bearing_model": bearing_model,
                        "prediction": pred,
                        "report": rep,
                        "deadline_iso": rep["summary"]["replace_by_iso"],
                        "brief": {
                            "job_id": job_id,
                            "machine_id": machine_key,
                            "rpm": active_rpm,
                            "report_summary": rep["summary"]
                        }
                    }
                    agent_res = run_agent(ctx)
                    
                    # Log telemetry to real database
                    try:
                        from db import get_db
                        get_db().log_telemetry(
                            machine_id=machine_key,
                            rpm=active_rpm,
                            rms=float(pred.get("features", {}).get("rms", 0.5)),
                            kurtosis=float(pred.get("features", {}).get("kurtosis", 3.0)),
                            predicted_fault=pred["fault"],
                            confidence=float(pred["confidence"]),
                            degradation_pct=float(pred["degradation_pct"]),
                            rul_p05=float(pred["rul_hours"]["p05"]),
                            rul_p50=float(pred["rul_hours"]["p50"]),
                            rul_p95=float(pred["rul_hours"]["p95"]),
                            urgency=rep["summary"].get("urgency", "LOW")
                        )
                    except Exception as db_err:
                        print("DB logging note:", db_err)
                        
                    st.session_state["analysis_result"] = {
                        "prediction": pred,
                        "report": rep,
                        "agent": agent_res,
                        "plan": agent_res.get("work_order"),
                        "job_id": job_id,
                        "machine": machine_info,
                        "time": datetime.now(BKK),
                    }
            else:
                if not api_url:
                    st.error("กรุณาระบุ AWS API Gateway URL ในแถบด้านซ้าย")
                else:
                    try:
                        payload = {
                            "machine_id": machine_key,
                            "rpm": active_rpm,
                            "fs": FS,
                            "bearing": bearing_key,
                            "signal": np.round(signal, 4).tolist()
                        }
                        r = requests.post(f"{api_url}/analyze", json=payload, timeout=30)
                        r.raise_for_status()
                        job_id = r.json()["job_id"]
                    
                        with st.status(f"Job {job_id}: ประมวลผลบน AWS Cloud...", expanded=True) as status_box:
                            job_data = {}
                            for _ in range(60):
                                res = requests.get(f"{api_url}/reports/{job_id}", timeout=15).json()
                                job_data = res.get("job", {})
                                status_box.update(label=f"AWS Lambda Status: {job_data.get('status')}")
                                if job_data.get("done"):
                                    break
                                time.sleep(3)
                        
                        if job_data.get("done"):
                            st.session_state["analysis_result"] = {
                                "prediction": job_data.get("prediction", {}),
                                "report": job_data.get("report", {}),
                                "agent": job_data.get("agent"),
                                "plan": job_data.get("plan"),
                                "job_id": job_id,
                                "machine": machine_info,
                                "time": datetime.now(BKK),
                            }
                        else:
                            st.error(f"API Timeout or Error: {job_data.get('error', 'Unknown')}")
                    except Exception as e:
                        st.error(f"การเชื่อมต่อ AWS API ล้มเหลว: {e}")

# If we have analysis result in session state, display it
res = st.session_state.get("analysis_result")
signal_data = st.session_state.get("current_signal")

if res:
    pred = res["prediction"]
    rep = res["report"]
    s = rep.get("summary", {})
    sev = s.get("severity", {})
    rul = pred.get("rul_hours", {})
    phys = pred.get("physics", {})
    
    # ----------------- TOP KPI ROW -----------------
    urgency = s.get("urgency", "LOW")
    urg_badge = {
        "LOW": "badge-green",
        "MEDIUM": "badge-yellow",
        "HIGH": "badge-orange",
        "EMERGENCY": "badge-red"
    }.get(urgency, "badge-blue")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">ตำแหน่งความเสียหาย</div>
            <div class="kpi-value">{s.get('fault_th', '-')}</div>
            <span class="badge {urg_badge}">Conf: {pred.get('confidence', 0)*100:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        deg = s.get('degradation_pct', 0)
        deg_color = "badge-green" if deg < 30 else ("badge-yellow" if deg < 60 else "badge-red")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">ระดับการเสื่อมสภาพ</div>
            <div class="kpi-value">{deg:.1f}%</div>
            <span class="badge {deg_color}">{sev.get('code', 'S0')}: {sev.get('label', '')[:10]}</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">ต้องเปลี่ยนภายใน</div>
            <div class="kpi-value" style="font-size:1.35rem;">{s.get('replace_within', {}).get('text', '-')}</div>
            <span class="badge badge-blue">Worst Case P05: {rul.get('p05', 0):.1f} ชม.</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">ระดับความเร่งด่วน</div>
            <div class="kpi-value">{urgency}</div>
            <span class="badge {urg_badge}">เส้นตาย: {s.get('replace_by_iso', '')[11:16]} น.</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col5:
        agree = pred.get('ai_physics_agree', False)
        agree_badge = "badge-green" if agree else "badge-yellow"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Physics Verification</div>
            <div class="kpi-value" style="font-size:1.3rem;">{'สอดคล้อง (Agree)' if agree else 'ตรวจซ้ำ (Review)'}</div>
            <span class="badge {agree_badge}">Peak: {phys.get('physics_fault', '-')}</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # ----------------- TABS CONTENT -----------------
    tab_overview, tab_physics, tab_guide, tab_agent, tab_report = st.tabs([
        "📊 ภาพรวม & RUL (Overview)",
        "📈 ฟิสิกส์ & สเปกตรัม (Envelope Spectrum)",
        "🛠️ คู่มือช่างเทคนิค & SOP (Technician Guide)",
        "🤖 การตัดสินใจของ Agent (Approval & Audit)",
        "📄 รายงานฉบับเต็ม (Full Report)",
    ])
    
    # ----------------- TAB 1: OVERVIEW & GAUGES -----------------
    with tab_overview:
        c_left, c_right = st.columns([1, 1])
        
        with c_left:
            # Degradation Gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=deg,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "ระดับการเสื่อมสภาพของตลับลูกปืน (Degradation %)", 'font': {'size': 18, 'color': '#f8fafc'}},
                delta={'reference': 20, 'increasing': {'color': "#f43f5e"}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
                    'bar': {'color': "#38bdf8", 'thickness': 0.28},
                    'bgcolor': "#1e293b",
                    'borderwidth': 1,
                    'bordercolor': "#334155",
                    'steps': [
                        {'range': [0, 10], 'color': '#10b981'},
                        {'range': [10, 30], 'color': '#3b82f6'},
                        {'range': [30, 60], 'color': '#f59e0b'},
                        {'range': [60, 85], 'color': '#f97316'},
                        {'range': [85, 100], 'color': '#ef4444'},
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 3},
                        'thickness': 0.75,
                        'value': deg
                    }
                }
            ))
            fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "#f8fafc", 'family': "Inter"}, height=320, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            st.info(f"💡 **ข้อเสนอแนะทันที:** {s.get('recommended_action', '-')}")

        with c_right:
            # RUL Fan Distribution Plot
            p05 = rul.get("p05", 0)
            p50 = rul.get("p50", 0)
            p95 = rul.get("p95", 0)
            
            fig_rul = go.Figure()
            fig_rul.add_trace(go.Bar(
                x=["P05 (Worst Case)", "P50 (Expected Life)", "P95 (Optimistic)"],
                y=[p05, p50, p95],
                marker_color=["#ef4444", "#38bdf8", "#10b981"],
                text=[f"{p05:.1f} ชม.", f"{p50:.1f} ชม.", f"{p95:.1f} ชม."],
                textposition='auto',
            ))
            fig_rul.update_layout(
                title="ช่วงอายุการใช้งานคงเหลือ (RUL Uncertainty Band)",
                yaxis_title="ชั่วโมง (Hours)",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(30, 41, 59, 0.4)",
                font={'color': "#f8fafc", 'family': "Inter"},
                height=320,
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(fig_rul, use_container_width=True)
            
            st.caption(f"🛡️ **Safety Guardrail:** ระบบจะใช้ค่า P05 ({p05:.1f} ชั่วโมง) เป็นเส้นตายในการวางแผนงาน เพื่อป้องกัน Unplanned Downtime 100%")

        # Class Probability Chart
        class_probs = pred.get("class_probs", {})
        if class_probs:
            st.subheader("ความน่าจะเป็นของตำแหน่งความเสียหาย (Fault Classification Probabilities)")
            df_probs = pd.DataFrame({
                "Fault Class": [FAULT_TH.get(k, k) for k in class_probs.keys()],
                "Probability": list(class_probs.values())
            }).sort_values(by="Probability", ascending=True)
            
            fig_prob = px.bar(
                df_probs,
                x="Probability",
                y="Fault Class",
                orientation='h',
                color="Probability",
                color_continuous_scale="Viridis",
                text="Probability"
            )
            fig_prob.update_traces(texttemplate='%{text:.1%}', textposition='outside')
            fig_prob.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(30, 41, 59, 0.4)",
                font={'color': "#f8fafc"},
                xaxis=dict(range=[0, 1.1], tickformat=".0%"),
                height=240,
                margin=dict(l=20, r=20, t=20, b=20),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_prob, use_container_width=True)

        # Historical Degradation Curve from Real Database (Phase 4)
        try:
            from db import get_db
            telemetry_rows = get_db().get_telemetry_history(machine_key, limit=35)
            if telemetry_rows and len(telemetry_rows) > 1:
                st.subheader("📈 แนวโน้มความเสื่อมสภาพย้อนหลัง (Historical Degradation & Telemetry Curve)")
                st.caption(f"ข้อมูลจริงที่จัดเก็บบน Database สำหรับเครื่อง `{machine_key}` ({len(telemetry_rows)} ช่วงเวลาทดสอบ)")
                df_telem = pd.DataFrame(telemetry_rows)
                
                fig_hist = go.Figure()
                fig_hist.add_trace(go.Scatter(
                    x=df_telem["timestamp"],
                    y=df_telem["degradation_pct"],
                    mode="lines+markers",
                    name="Degradation (%)",
                    line=dict(color="#f43f5e", width=2.5),
                    marker=dict(size=6)
                ))
                fig_hist.add_trace(go.Scatter(
                    x=df_telem["timestamp"],
                    y=df_telem["rms"] * 40,
                    mode="lines",
                    name="Vibration RMS (scaled x40)",
                    line=dict(color="#38bdf8", width=1.5, dash="dot")
                ))
                fig_hist.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(30, 41, 59, 0.4)",
                    font={'color': "#f8fafc", 'family': "Inter"},
                    yaxis_title="Degradation Index (%)",
                    height=280,
                    margin=dict(l=20, r=20, t=30, b=20),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_hist, use_container_width=True)
        except Exception:
            pass

    # ----------------- TAB 2: SIGNAL & PHYSICS SPECTRUM -----------------
    with tab_physics:
        col_sig1, col_sig2 = st.columns([2, 1])
        
        with col_sig1:
            st.subheader("สัญญาณแรงสั่นสะเทือนในโดเมนเวลา (Vibration Time Domain)")
            if signal_data is not None:
                samples_to_show = 1600 # 0.1 s
                t_axis = np.arange(samples_to_show) / FS * 1000 # ms
                fig_time = go.Figure()
                fig_time.add_trace(go.Scatter(
                    x=t_axis,
                    y=signal_data[:samples_to_show],
                    mode='lines',
                    line=dict(color="#38bdf8", width=1.5),
                    name="Acceleration (g)"
                ))
                fig_time.update_layout(
                    xaxis_title="เวลา (มิลลิวินาที / ms)",
                    yaxis_title="ความเร่ง (Acceleration, g)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(30, 41, 59, 0.4)",
                    font={'color': "#f8fafc"},
                    height=280,
                    margin=dict(l=20, r=20, t=20, b=20),
                )
                st.plotly_chart(fig_time, use_container_width=True)
                
        with col_sig2:
            st.subheader("คุณลักษณะทางสถิติ (Time Features)")
            tf = phys.get("time_features", time_features(signal_data if signal_data is not None else np.zeros(100)))
            st.write(f"• **RMS:** `{tf.get('rms', 0):.4f} g`")
            st.write(f"• **Peak:** `{tf.get('peak', 0):.4f} g`")
            st.write(f"• **Crest Factor:** `{tf.get('crest', 0):.2f}`")
            st.write(f"• **Kurtosis:** `{tf.get('kurtosis', 0):.2f}` (ค่าปกติ ~3.0)")
            st.write(f"• **Skewness:** `{tf.get('skewness', 0):.2f}`")

        st.markdown("---")
        st.subheader("Order Spectrum & Envelope Analysis (Order Domain)")
        st.caption("การแปลงสัญญาณด้วย Hilbert Transform ผ่าน Band-pass 1-5 kHz และ Order Normalization ไม่ขึ้นกับความเร็วรอบ")
        
        env_spec = phys.get("envelope_order_spectrum", {})
        if env_spec and "order" in env_spec:
            order_x = env_spec["order"]
            amp_y = env_spec["amp"]
            
            fig_env = go.Figure()
            fig_env.add_trace(go.Scatter(
                x=order_x,
                y=amp_y,
                mode='lines',
                line=dict(color="#818cf8", width=1.5),
                name="Envelope Amp"
            ))
            
            # Add vertical markers for bearing fault orders
            fr_colors = {"inner_race": "#ef4444", "outer_race": "#f97316", "ball": "#eab308", "cage": "#a855f7"}
            for fk, fo in orders.items():
                fig_env.add_vline(
                    x=fo,
                    line_width=1.5,
                    line_dash="dash",
                    line_color=fr_colors.get(fk, "white"),
                    annotation_text=f"{fk[:5].upper()}: {fo:.2f}X",
                    annotation_position="top right",
                )
                
            fig_env.update_layout(
                xaxis_title="Order (พหุคูณความเร็วรอบเพลา / Multiples of Running Speed)",
                yaxis_title="Envelope Amplitude",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(30, 41, 59, 0.4)",
                font={'color': "#f8fafc"},
                height=360,
                margin=dict(l=20, r=20, t=30, b=20),
            )
            st.plotly_chart(fig_env, use_container_width=True)

        # Physics Scores Table
        scores = phys.get("scores", {})
        if scores:
            st.markdown("##### ตารางตรวจจับฮาร์มอนิกความถี่เฉพาะ (Harmonic Verification Table)")
            table_rows = []
            for k, val in scores.items():
                table_rows.append({
                    "ตำแหน่งชำรุด": FAULT_TH.get(k, k),
                    "Order (X)": val.get("order"),
                    "ความถี่ (Hz)": val.get("freq_hz"),
                    "Harmonic SNR (1X, 2X, 3X)": str(val.get("harmonic_snr")),
                    "ตรวจพบพีค (Detected)": "✅ พบพีคชัดเจน" if val.get("detected") else "❌ ไม่พบ",
                })
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

    # ----------------- TAB 3: TECHNICIAN GUIDE & SOP -----------------
    with tab_guide:
        tech_guide = s.get("technician_guide", {})
        specific_insp = tech_guide.get("specific_inspection", [])
        precautions = tech_guide.get("precautions", [])
        standard_sop = tech_guide.get("standard_sop", [])
        
        st.markdown(f"""
        <div style="background:rgba(56, 189, 248, 0.1); border-left:4px solid #38bdf8; padding:16px; border-radius:4px; margin-bottom:20px;">
            <h3 style="margin:0; color:#38bdf8;">🛠️ คู่มือปฏิบัติงานและแนวทางแก้ปัญหาสำหรับช่างเทคนิค</h3>
            <p style="margin:6px 0 0 0; color:#e2e8f0;">
                เครื่องจักร: <b>{machine_info['name']}</b> | ตลับลูกปืน: <b>{bearing_model}</b> | ตำแหน่งตรวจพบ: <b>{s.get('fault_th')}</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        c_diag1, c_diag2 = st.columns([1, 1])
        with c_diag1:
            st.markdown(f"<div class='section-title'>🔍 จุดตรวจสอบเฉพาะกรณี {s.get('fault_th')}</div>", unsafe_allow_html=True)
            for item in specific_insp:
                st.markdown(f"<div class='sop-step'>• {item}</div>", unsafe_allow_html=True)
                
            if precautions:
                st.markdown("<div class='section-title' style='color:#f87171;'>⚠️ ข้อควรระวังสำคัญ (Critical Precautions)</div>", unsafe_allow_html=True)
                for item in precautions:
                    st.markdown(f"<div class='sop-step' style='border-color:rgba(239, 68, 68, 0.4); background:rgba(239, 68, 68, 0.08);'>⚠️ {item}</div>", unsafe_allow_html=True)
                    
        with c_diag2:
            st.markdown("<div class='section-title'>📦 ข้อมูลอะไหล่ในคลัง (Spare Parts Status)</div>", unsafe_allow_html=True)
            part_info = SPARE_PARTS_DB.get(bearing_model, {"stock": 0, "location": "ไม่พบ", "lead_time_days": "-", "price_thb": "-", "substitutes": []})
            
            stock_color = "badge-green" if part_info["stock"] > 0 else "badge-red"
            st.markdown(f"""
            <div style="background:rgba(30, 41, 59, 0.6); border:1px solid rgba(148,163,184,0.2); border-radius:8px; padding:16px;">
                <p><b>ตลับลูกปืนมาตรฐาน:</b> <code>{bearing_model}</code></p>
                <p><b>จำนวนคงเหลือในคลัง:</b> <span class="badge {stock_color}">{part_info['stock']} ชิ้น</span></p>
                <p><b>ตำแหน่งจัดเก็บ:</b> {part_info['location']}</p>
                <p><b>ระยะเวลาจัดซื้อ (Lead Time):</b> {part_info['lead_time_days']} วัน</p>
                <p><b>รุ่นทดแทนที่ใช้ได้ (Substitutes):</b> {', '.join(part_info['substitutes'])}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='section-title'>📋 เช็คลิสต์ขั้นตอนการเปลี่ยนตลับลูกปืน (Standard SOP Checklist)</div>", unsafe_allow_html=True)
        st.caption("ช่างเทคนิคสามารถกดเช็คถูกเมื่อปฏิบัติการแต่ละขั้นตอนเสร็จสิ้นหน้างาน:")
        
        checked_count = 0
        for i, step in enumerate(standard_sop):
            step_chk = st.checkbox(step, key=f"sop_chk_{i}")
            if step_chk:
                checked_count += 1
                
        progress_val = checked_count / max(1, len(standard_sop))
        st.progress(progress_val, text=f"ความคืบหน้าการทำงาน: {checked_count}/{len(standard_sop)} ขั้นตอน ({progress_val*100:.0f}%)")

    # ----------------- TAB 4: MULTI-AGENT COLLABORATIVE DEBATE & WORK ORDER -----------------
    with tab_agent:
        st.markdown("<div class='section-title'>🧠 สถาปัตยกรรม Multi-Agent Collaborative Debate & การสั่งการอัตโนมัติ</div>", unsafe_allow_html=True)
        st.caption("การโต้แย้งและร่วมตัดสินใจระหว่าง 3 AI Sub-Agents: Safety vs Operations & Economics สรุปโดย Arbiter Agent")
        
        agent_data = res.get("agent") or {}
        debate_turns = agent_data.get("debate", [])
        
        # Display 3-Agent Collaborative Debate Cards
        if debate_turns:
            for turn in debate_turns:
                agent_name = turn.get("agent", "")
                agent_role = turn.get("role", "")
                msg = turn.get("message", "")
                
                if "Safety" in agent_name:
                    b_color = "#ef4444"
                    bg_color = "rgba(239, 68, 68, 0.08)"
                    icon = "🛡️"
                    badge_cls = "badge-red"
                elif "Operations" in agent_name:
                    b_color = "#f59e0b"
                    bg_color = "rgba(245, 158, 11, 0.08)"
                    icon = "🏭"
                    badge_cls = "badge-yellow"
                else:
                    b_color = "#38bdf8"
                    bg_color = "rgba(56, 189, 248, 0.08)"
                    icon = "⚖️"
                    badge_cls = "badge-blue"
                    
                st.markdown(f"""
                <div style="background:{bg_color}; border-left:4px solid {b_color}; border-radius:6px; padding:14px; margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span style="font-weight:700; color:{b_color};">{icon} {agent_name}</span>
                        <span class="badge {badge_cls}">{agent_role}</span>
                    </div>
                    <div style="font-size:0.92rem; line-height:1.6; color:#f1f5f9;">{msg}</div>
                </div>
                """, unsafe_allow_html=True)
                
        # Work Order & HITL Approval
        st.markdown("---")
        col_plan1, col_plan2 = st.columns([3, 2])
        with col_plan1:
            st.markdown("##### 📝 ใบสั่งซ่อมบำรุงและมาตรการควบคุม (Work Order Execution)")
            planned_start = datetime.now(BKK) + timedelta(hours=min(rul.get('p05', 24) * 0.5, 48))
            
            st.write(f"• **งานที่ต้องปฏิบัติ:** {s.get('recommended_action')}")
            st.write(f"• **กำหนดเริ่มงาน:** `{planned_start:%d/%m/%Y %H:%M}` น. (ก่อนเส้นตาย P05)")
            st.write(f"• **อะไหล่เป้าหมาย:** `{bearing_model}`")
            st.write(f"• **เครื่องสำรอง:** {machine_info.get('standby_machine') or 'ไม่มีเครื่องสำรอง'}")
            
            derate_info = agent_data.get("derating")
            if derate_info and derate_info.get("derated_rpm"):
                st.info(f"⚙️ **Derating Plan Active:** ปรับความเร็วรอบเหลือ `{derate_info['derated_rpm']:.0f} RPM` (ลดลง {derate_info.get('rpm_reduction_pct')}%) เพื่อยืดอายุไปถึงรอบหยุดซ่อมตามแผน")
            
            st.markdown("---")
            st.markdown("##### การอนุมัติของหัวหน้างาน (Human-in-the-Loop Approval)")
            
            btn_app1, btn_app2, btn_app3 = st.columns(3)
            with btn_app1:
                if st.button("✅ อนุมัติใบสั่งซ่อม (Approve)", type="primary", use_container_width=True):
                    st.session_state["approval_status"] = "APPROVED"
                    st.session_state["approval_token"] = approval_token(res["job_id"], "approve")
                    try:
                        from db import get_db
                        db_obj = get_db()
                        # Reserve spare part and update DB
                        wo_id = agent_data.get("work_order", {}).get("work_order_id") or f"WO-{res['job_id']}"
                        db_obj.update_work_order_status(wo_id, "APPROVED", approver="Chief Reliability Engineer")
                        db_obj.reserve_spare_part(bearing_model, 1)
                        st.session_state["db_approved"] = True
                    except Exception as ex_db:
                        print("DB approval exception:", ex_db)
                        
            with btn_app2:
                if st.button("⏳ เลื่อน 24 ชม. (Postpone)", use_container_width=True):
                    st.session_state["approval_status"] = "POSTPONED_24H"
                    st.session_state["approval_token"] = approval_token(res["job_id"], "postpone")
            with btn_app3:
                if st.button("❌ ปฏิเสธแผน (Reject)", use_container_width=True):
                    st.session_state["approval_status"] = "REJECTED"
                    st.session_state["approval_token"] = approval_token(res["job_id"], "reject")
                    
            status_current = st.session_state.get("approval_status", "PENDING_APPROVAL")
            status_badge = "badge-yellow" if status_current == "PENDING_APPROVAL" else ("badge-green" if status_current == "APPROVED" else "badge-red")
            st.markdown(f"**สถานะใบสั่งงาน:** <span class='badge {status_badge}'>{status_current}</span>", unsafe_allow_html=True)
            
            if status_current == "APPROVED":
                st.success(f"✅ อนุมัติใบสั่งงานเรียบร้อยแล้ว! ตัดสต็อกอะไหล่ `{bearing_model}` ในระบบคลังสินค้าสำเร็จ (Token: `{st.session_state.get('approval_token', '')}`)")
                
        with col_plan2:
            st.markdown("##### กฎความปลอดภัยและการควบคุมต้นทุน")
            st.markdown(f"""
            <div style="background:rgba(30, 41, 59, 0.4); border:1px solid rgba(148,163,184,0.15); border-radius:8px; padding:14px; font-size:0.9rem;">
                <p>1. <b>Strict Safety Deadline:</b> ต้องเริ่มซ่อมก่อนเส้นตาย P05 (<b>{s.get('replace_by_iso', '')[:16]}</b>) เด็ดขาด</p>
                <p>2. <b>Zero-Energy LOTO:</b> ช่างทุกคนต้องคล้องกุญแจ Padlock ตรวจวัดแรงดันไฟฟ้าศูนย์ก่อนถอดชิ้นส่วน</p>
                <p>3. <b>Fatigue Life Derating:</b> ยืดอายุ RUL ด้วยการปรับลด RPM ผ่าน VFD ช่วยประหยัดค่าเสียโอกาสการผลิตได้หลายหมื่นบาท</p>
            </div>
            """, unsafe_allow_html=True)

    # ----------------- TAB 5: FULL REPORT & DOWNLOAD -----------------
    with tab_report:
        st.subheader("📄 รายงานการบำรุงรักษาทางการ (Official Maintenance Report)")
        md_text = rep.get("markdown", "")
        
        try:
            pdf_bytes = markdown_to_pdf_bytes(md_text, title=f"MechAgent Report - {machine_key}")
            st.download_button(
                label="📕 ดาวน์โหลดรายงานฉบับสมบูรณ์ (.PDF)",
                data=pdf_bytes,
                file_name=f"Report_{res.get('job_id')}_{machine_key}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"⚠️ เกิดข้อผิดพลาดในการสร้างไฟล์ PDF: {e}")
            
        st.markdown("---")
        st.markdown(md_text)

else:
    # Initial landing screen when no analysis has been run
    st.info("👈 กรุณากดปุ่ม **'🚀 วิเคราะห์ความสั่นสะเทือน (Analyze Vibration)'** ในแถบด้านซ้าย เพื่อเริ่มการวิเคราะห์จำลอง")
    
    col_intro1, col_intro2 = st.columns(2)
    with col_intro1:
        st.markdown("""
        ### 🎯 จุดเด่นของระบบ MechAgent
        - **Physics-Informed MTL AI:** ผสานพลัง DistilHuBERT (Audio Backbone) ร่วมกับ Order Spectrum Physics
        - **Zero Hallucination:** ตัวเลข RUL และผลการวิเคราะห์ตำแหน่งชำรุดคำนวณจากสูตรและโมเดลโดยตรง ไม่ผ่าน LLM
        - **Worst-case P05 Deadline:** ประเมินความเสี่ยงเพื่อความปลอดภัยสูงสุด ป้องกันเครื่องจักรล็อกเฉียบพลัน
        - **SOP & Troubleshooting Checklist:** มีขั้นตอนปฏิบัติมาตรฐานให้ช่างเทคนิคทำตามได้ทันที
        """)
    with col_intro2:
        st.markdown("""
        ### 🏭 รองรับเครื่องจักรในโรงงาน
        - **PUMP-01:** ปั๊มน้ำหล่อเย็นหลัก (Criticality A, Standby PUMP-02)
        - **MOTOR-07:** มอเตอร์สายพานลำเลียง (Criticality B)
        - **FAN-03:** พัดลมดูดอากาศ (SKF 6208 Zero-shot Bearing)
        """)
