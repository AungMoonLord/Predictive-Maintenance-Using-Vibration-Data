"""Step 4 – deterministic maintenance report. Numbers come ONLY from the model (no LLM hallucination)."""
from datetime import datetime, timedelta, timezone

BKK = timezone(timedelta(hours=7))

FAULT_TH = {
    "normal": "ไม่พบตำแหน่งเสียหาย (ปกติ)",
    "inner_race": "แหวนรอบใน (Inner Race)",
    "outer_race": "แหวนรอบนอก (Outer Race)",
    "ball": "เม็ดลูกปืน (Rolling Element / Ball)",
    "cage": "รังลูกปืน (Cage)",
}
FAULT_CAUSES = {
    "normal": "สภาพการทำงานปกติ ไม่พบการสึกหรอหรือสัญญาณความเสียหายที่มีนัยสำคัญ",
    "inner_race": "การหล่อลื่นไม่เพียงพอ, interference fit แน่นเกิน, โหลดเกิน หรือความล้าของผิววัสดุ",
    "outer_race": "การติดตั้งเยื้องศูนย์, housing เสียรูป, สิ่งปนเปื้อน หรือโหลดคงที่ในโซนรับแรง",
    "ball": "สิ่งปนเปื้อนในจาระบี, แรงกระแทก หรือกระแสไฟฟ้ารั่วผ่านตลับลูกปืน (electrical fluting)",
    "cage": "การหล่อลื่นล้มเหลว, ความเร็วรอบเปลี่ยนแปลงรุนแรง หรือ misalignment",
}
SEVERITY_LEVELS = [
    (10, "S0", "ปกติ (Healthy)", "ตรวจวัดตามรอบปกติ"),
    (30, "S1", "เริ่มเสื่อม (Early wear)", "เพิ่มความถี่การตรวจวัด และตรวจสอบการหล่อลื่น"),
    (60, "S2", "เสื่อมปานกลาง (Moderate)", "วางแผนเปลี่ยนในรอบหยุดเครื่องถัดไป และจองอะไหล่"),
    (85, "S3", "เสื่อมรุนแรง (Severe)", "เปลี่ยนโดยเร็วภายในกำหนดเส้นตาย"),
    (1e9, "S4", "วิกฤต (Critical)", "หยุดเครื่องหรือสลับไปเครื่องสำรองทันที"),
]

TECHNICIAN_GUIDES = {
    "normal": {
        "inspection": [
            "ตรวจเช็คระดับและสภาพสารหล่อลื่นตามรอบบำรุงรักษาเชิงป้องกัน (PM)",
            "ตรวจวัดอุณหภูมิผิว Housing (ไม่ควรเกิน 70°C หรือเพิ่มขึ้นอย่างผิดปกติ)",
            "ทำความสะอาดภายนอกและบันทึกค่าการสั่นสะเทือนเก็บไว้เป็น Baseline สำหรับเทียบเคียง",
        ],
        "precautions": [
            "รักษาความสะอาดบริเวณรอบจุดเติมจาระบี ป้องกันฝุ่นผงและสิ่งแปลกปลอมเข้าสู่ตลับลูกปืน",
        ],
    },
    "inner_race": {
        "inspection": [
            "ตรวจสอบความแน่น (Fit) ระหว่างเพลากับรูในตลับลูกปืน (Interference fit)",
            "ตรวจหารอยสึก สนิมขัดสี หรือรอยหลวมที่ผิวเพลา (Fretting corrosion) หากพบต้องซ่อมเพลาก่อนติดตั้งใหม่",
            "ตรวจเช็คการขยายตัวทางความร้อนของเพลา หรือโหลดในแนวแกน (Axial load) ที่อาจสูงเกินพิกัด",
            "ตรวจสภาพจาระบีว่าเสื่อมสภาพ แข็งตัว หรือมีรอยไหม้จากความร้อนสูงหรือไม่",
        ],
        "precautions": [
            "ห้ามใช้แรงกดหรือตอกผ่านแหวนนอกเพื่อดันแหวนในเด็ดขาด เพราะจะทำให้ผิวรางวิ่งเป็นรอยบุบ (True Brinelling)",
        ],
    },
    "outer_race": {
        "inspection": [
            "ตรวจวัดขนาด ความกลม และระยะหลวมของเบ้าลูกปืน (Housing bore tolerance & roundness)",
            "ตรวจสอบการเยื้องศูนย์ของเพลา (Shaft Misalignment) และตรวจสอบฐานเครื่อง (Soft Foot)",
            "ตรวจเช็คสภาพซีลกันฝุ่น/กันน้ำมัน (Seal condition) และความสะอาดภายในเบ้าลูกปืน",
            "ตรวจสอบทิศทางของโหลดคงที่ในโซนรับแรง (Static load zone distribution)",
        ],
        "precautions": [
            "ตรวจสอบให้แน่ใจว่าแหวนนอกนั่งแนบสนิทกับบ่า Housing ไม่เกิดการเอียงหรือขัดตัว",
        ],
    },
    "ball": {
        "inspection": [
            "ตรวจวิเคราะห์หาสิ่งปนเปื้อนในจาระบี (เศษผงโลหะ, ทราย, ความชื้น หรือน้ำ)",
            "หากขับเคลื่อนด้วยมอเตอร์ปรับรอบ (Inverter / VFD) ให้ตรวจหารอยไหม้ขนานกัน (Electrical Fluting) จากกระแสไฟฟ้ารั่ว",
            "หากพบปัญหากระแสไฟฟ้ารั่ว ให้ติดตั้ง Shaft Grounding Ring หรือเปลี่ยนใช้ตลับลูกปืนฉนวนไฟฟ้า (Ceramic / Insulated bearing)",
            "ตรวจเช็คประวัติว่าเครื่องจักรเคยได้รับแรงกระแทกเฉียบพลันขณะหยุดนิ่งหรือขนย้ายหรือไม่ (False Brinelling)",
        ],
        "precautions": [
            "หลีกเลี่ยงการเคาะ กระแทก หรือตอกลงบนชุดตลับลูกปืนในทุกขั้นตอน",
        ],
    },
    "cage": {
        "inspection": [
            "⚠️ ข้อควรระวังเร่งด่วน: ความเสียหายที่ Cage เสี่ยงต่อการแตกกระจายและทำให้เพลาติดขัดเฉียบพลัน (Catastrophic seizure) ควรเตรียมหยุดเครื่องโดยเร็ว",
            "ตรวจระบบหล่อลื่นทันที – การขาดสารหล่อลื่นหรือจาระบีไหม้เป็นสาเหตุอันดับ 1 ที่ทำให้ cage ขาดหรือแตก",
            "ตรวจสอบการเปลี่ยนแปลงความเร็วรอบอย่างรุนแรง (Speed fluctuation / Shock load)",
            "ตรวจเช็คการเยื้องศูนย์ (Misalignment) และการแกว่งตัวของเพลา",
        ],
        "precautions": [
            "หากได้ยินเสียงเสียดสีแหลมดังผิดปกติ ให้สลับไปใช้เครื่องจักรสำรอง (Standby unit) ทันที",
        ],
    },
}

STANDARD_SOP = [
    "ความปลอดภัย (Safety & LOTO): ดำเนินการ Lockout/Tagout ตัดระบบไฟฟ้าและคลายพลังงานตกค้าง แขวนป้ายเตือน และรอให้อุณหภูมิชิ้นส่วนเย็นต่ำกว่า 50°C",
    "การถอด (Disassembly): มาร์กตำแหน่ง Alignment เดิม จากนั้นใช้ Bearing Puller หรือ Hydraulic Puller จับที่แหวนใน ห้ามใช้ค้อนตีโดยตรง",
    "การตรวจสอบเพลาและเบ้า (Inspection): ตรวจวัด Runout ของเพลา (ต้องไม่เกิน 0.02 mm) ตรวจสอบความสะอาดและรอยขรุขระของบ่าเพลา/เบ้าลูกปืน",
    "การอุ่นติดตั้ง (Heating & Mounting): อุ่นตลับลูกปืนใหม่ด้วย Induction Heater ที่อุณหภูมิ 100–110°C (ห้ามเกิน 120°C และห้ามใช้ไฟแก๊สเป่า) สวมเข้าเพลาจนชนบ่าทันทีและกดค้างจนเย็นตัว",
    "การหล่อลื่น (Lubrication): เติมจาระบีตามสเปก (แนะนำ Lithium Complex NLGI 2) ในปริมาณ 30–50% ของช่องว่างภายในตลับลูกปืน (ห้ามเติมจนแน่นเกินไปเพื่อป้องกันความร้อนสะสม)",
    "การตั้งศูนย์และทดสอบ (Alignment & Commissioning): ตั้งศูนย์เพลาด้วย Laser Alignment ให้ได้ค่าเบี่ยงเบน ≤ 0.05 mm จากนั้นเดินเครื่องทดสอบ (Test Run) 30 นาที และวัด Vibration Baseline บันทึกเป็นประวัติใหม่",
]


def severity_of(pct):
    for limit, code, label, action in SEVERITY_LEVELS:
        if pct < limit:
            return {"code": code, "label": label, "action": action}


def split_duration(hours):
    total = max(0, int(hours * 60))          # floor → conservative
    d, rem = divmod(total, 1440)
    h, m = divmod(rem, 60)
    return {"days": d, "hours": h, "minutes": m, "text": f"{d} วัน {h} ชั่วโมง {m} นาที"}


def build_report(pred, machine=None, now=None, job_id=None):
    machine, now = machine or {}, now or datetime.now(BKK)
    fault, deg = pred["fault"], float(pred["degradation_pct"])
    rul = pred["rul_hours"]
    cap = float(rul.get("cap", 1000.0))
    sev = severity_of(deg)
    deadline_h = float(rul["p05"])           # P5 = worst case → safety deadline
    beyond = rul["p50"] >= 0.95 * cap
    replace_by = now + timedelta(hours=deadline_h)
    dur, exp = split_duration(deadline_h), split_duration(rul["p50"])
    urgency = ("EMERGENCY" if deadline_h < 24 else "HIGH" if deadline_h < 72
               else "MEDIUM" if deadline_h < 168 else "LOW")
    phys = pred.get("physics", {})
    pf = phys.get("physics_fault", "normal")
    if fault == "normal":
        phys_txt = "ไม่พบ peak ผิดปกติ" if pf == "normal" else f"พบ peak ที่ {FAULT_TH[pf]} → แนะนำตรวจซ้ำ"
    elif pf == fault:
        s = phys["scores"][fault]
        phys_txt = f"สอดคล้อง: พบ peak ที่ order {s['order']} ({s['freq_hz']} Hz), SNR {s['harmonic_snr']}"
    else:
        phys_txt = "ยังไม่พบ peak ชัดเจน (อาจเป็นระยะเริ่มต้น) → ใช้ผล AI ร่วมกับการตรวจซ้ำ"
    action = sev["action"] if fault != "normal" or deg >= 10 else "ตรวจวัดตามรอบปกติ"
    rul_txt = f"มากกว่า {cap / 24:.0f} วัน (เกินช่วงพยากรณ์)" if beyond else exp["text"]
    deadline_txt = "ยังไม่ต้องเปลี่ยน" if (beyond and fault == "normal") else dur["text"]

    guide = TECHNICIAN_GUIDES.get(fault, TECHNICIAN_GUIDES["normal"])
    insp_bullets = "\n".join(f"  - {step}" for step in guide["inspection"])
    prec_bullets = "\n".join(f"  - {step}" for step in guide.get("precautions", []))
    sop_bullets = "\n".join(f"{i+1}. {step}" for i, step in enumerate(STANDARD_SOP))

    summary = {
        "job_id": job_id, "machine_id": machine.get("machine_id"), "analyzed_at": now.isoformat(),
        "fault": fault, "fault_th": FAULT_TH[fault], "confidence": pred["confidence"],
        "degradation_pct": deg, "severity": sev, "rul_p50_h": rul["p50"], "rul_p05_h": rul["p05"],
        "rul_p95_h": rul["p95"], "replace_within": dur, "replace_by_iso": replace_by.isoformat(),
        "urgency": urgency, "physics_fault": pf, "ai_physics_agree": pred.get("ai_physics_agree"),
        "recommended_action": action,
        "technician_guide": {
            "specific_inspection": guide["inspection"],
            "precautions": guide.get("precautions", []),
            "standard_sop": STANDARD_SOP,
        },
    }

    m_name = machine.get('name', 'เครื่องจักร')
    mid = machine.get('machine_id')
    title_suffix = f" ({mid})" if mid and mid != '-' and mid not in m_name else ""

    md = f"""# รายงานสุขภาพตลับลูกปืน: {m_name}{title_suffix}
**Job:** {job_id} | **เวลาวิเคราะห์:** {now:%d/%m/%Y %H:%M} น. | **ตลับลูกปืน:** {machine.get('bearing_model', pred.get('bearing'))} | **ความเร็วรอบ:** {pred.get('rpm', 0):.0f} RPM

## 1. สรุปผล
| หัวข้อ | ผลลัพธ์ |
|---|---|
| สถานะ | {sev['code']}: {sev['label']} |
| ระดับการเสื่อมสภาพ | {deg:.1f}% (±{pred.get('degradation_std_pct', 0):.1f}) |
| ตำแหน่งที่เสียหาย | {FAULT_TH[fault]} (ความมั่นใจ {pred['confidence'] * 100:.0f}%) |
| ยืนยันด้วยหลักฟิสิกส์ | {phys_txt} |
| อายุคงเหลือที่คาดการณ์ (P50) | {rul_txt} |
| ช่วงความไม่แน่นอน (P5 ถึง P95) | {rul['p05']:.0f} ถึง {rul['p95']:.0f} ชั่วโมง |
| **ต้องเปลี่ยนเร็วที่สุดภายใน** | **{deadline_txt}** |
| กำหนดเส้นตาย | {replace_by:%d/%m/%Y %H:%M} น. |
| ความเร่งด่วน | {urgency} |

## 2. สาเหตุที่เป็นไปได้
{FAULT_CAUSES[fault]}

## 3. ข้อเสนอแนะ
- {action}
- ตรวจสอบอุณหภูมิตลับลูกปืนและสภาพจาระบีประกอบการตัดสินใจ

## 4. คู่มือการแก้ปัญหาและแนวทางปฏิบัติเบื้องต้นสำหรับช่างเทคนิค (Technician Action Guide)
### 4.1 การตรวจสอบและวินิจฉัยหน้างานเฉพาะจุด ({FAULT_TH[fault]})
{insp_bullets}
- **ข้อควรระวังสำคัญ:**
{prec_bullets}

### 4.2 ขั้นตอนมาตรฐานในการเปลี่ยนและติดตั้งตลับลูกปืน (Standard Replacement SOP)
{sop_bullets}

## 5. หมายเหตุ
- เส้นตายคำนวณจากค่า P5 (กรณีเลวร้าย) เพื่อความปลอดภัย
- รายงานนี้สร้างโดย AI และต้องได้รับอนุมัติจากหัวหน้างานก่อนออกใบสั่งงาน
"""
    tg = (f"[{urgency}] {machine.get('machine_id', '-')} {machine.get('name', '')}\n"
          f"สถานะ: {sev['code']} {sev['label']} | เสื่อม {deg:.1f}%\n"
          f"ตำแหน่ง: {FAULT_TH[fault]} ({pred['confidence'] * 100:.0f}%)\n"
          f"ต้องเปลี่ยนภายใน: {deadline_txt}\nเส้นตาย: {replace_by:%d/%m/%Y %H:%M}")
    return {"summary": summary, "markdown": md, "telegram": tg}
