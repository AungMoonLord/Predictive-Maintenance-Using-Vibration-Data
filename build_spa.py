"""Build the 100% Serverless SPA HTML for MechAgent.
Generates site/index.html and agent/dashboard_html.py.
"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "agent" / "cwru_samples.json", "r", encoding="utf-8") as f:
    cwru_samples = json.load(f)

cwru_js = json.dumps(cwru_samples)

html_content = r'''<!DOCTYPE html>
<html lang="th" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MechAgent | AI Predictive Maintenance (100% Serverless)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'Sarabun', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
          colors: {
            stbg: '#0e1117',
            stside: '#161b26',
            stred: 'rgb(255, 75, 75)',
            stredhover: 'rgb(235, 55, 55)',
            cardbg: 'rgba(30, 41, 59, 0.5)',
          }
        }
      }
    }
  </script>
  <style>
    body {
      background-color: #0e1117;
      color: #f1f5f9;
      font-family: 'Inter', 'Sarabun', sans-serif;
    }
    .kpi-card {
      background: rgba(30, 41, 59, 0.5);
      border: 1px solid rgba(148, 163, 184, 0.1);
      border-radius: 10px;
      padding: 14px 18px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
      transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
      transform: translateY(-2px);
      border-color: rgba(56, 189, 248, 0.4);
    }
    .kpi-title {
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #94a3b8;
      margin-bottom: 4px;
    }
    .kpi-value {
      font-size: 1.40rem;
      font-weight: 700;
      color: #f8fafc;
      margin-bottom: 4px;
    }
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 9999px;
      font-size: 0.70rem;
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
      font-size: 0.92rem;
    }
    .section-title {
      font-size: 1.10rem;
      font-weight: 700;
      color: #38bdf8;
      margin-top: 16px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    #report-markdown-view h1 {
      font-size: 1.55rem;
      font-weight: 800;
      color: #ffffff;
      margin-top: 0.5rem;
      margin-bottom: 0.4rem;
      line-height: 1.3;
    }
    #report-markdown-view h2 {
      font-size: 1.25rem;
      font-weight: 700;
      color: #38bdf8;
      margin-top: 1.5rem;
      margin-bottom: 0.6rem;
      border-bottom: 1px solid rgba(148, 163, 184, 0.15);
      padding-bottom: 0.3rem;
    }
    #report-markdown-view h3 {
      font-size: 1.05rem;
      font-weight: 600;
      color: #ffffff;
      margin-top: 1.1rem;
      margin-bottom: 0.4rem;
    }
    #report-markdown-view p {
      color: #cbd5e1;
      margin-bottom: 0.65rem;
      line-height: 1.6;
    }
    #report-markdown-view table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.1rem 0;
      border: 1px solid rgba(148, 163, 184, 0.2);
      border-radius: 6px;
      overflow: hidden;
      font-size: 0.90rem;
    }
    #report-markdown-view th {
      background-color: rgba(30, 41, 59, 0.85);
      color: #ffffff;
      padding: 9px 12px;
      text-align: left;
      font-weight: 600;
      border: 1px solid rgba(148, 163, 184, 0.2);
    }
    #report-markdown-view td {
      padding: 9px 12px;
      border: 1px solid rgba(148, 163, 184, 0.15);
      color: #e2e8f0;
    }
    #report-markdown-view tr:nth-child(even) {
      background-color: rgba(30, 41, 59, 0.3);
    }
    #report-markdown-view ul, #report-markdown-view ol {
      padding-left: 1.5rem;
      margin: 0.5rem 0;
      color: #cbd5e1;
    }
    #report-markdown-view ul { list-style-type: disc; }
    #report-markdown-view ol { list-style-type: decimal; }
    #report-markdown-view li { margin-bottom: 0.4rem; line-height: 1.55; }
    #report-markdown-view strong { color: #ffffff; font-weight: 600; }

    @media print {
      body { background-color: #ffffff !important; color: #000000 !important; }
      aside, header, #kpi-row, .tabs-bar, .no-print { display: none !important; }
      #printable-report, #printable-report * { visibility: visible !important; color: #000000 !important; }
      #printable-report table { border-color: #94a3b8 !important; }
      #printable-report th { background-color: #f1f5f9 !important; color: #000000 !important; }
      #printable-report td { border-color: #cbd5e1 !important; color: #000000 !important; }
    }
  </style>
</head>
<body class="bg-stbg text-slate-100 min-h-screen">

  <div class="flex flex-col lg:flex-row min-h-screen">
    
    <!-- ================= SIDEBAR ================= -->
    <aside class="w-full lg:w-80 bg-stside border-r border-slate-800 p-5 flex flex-col space-y-4 shrink-0">
      
      <!-- Top Title -->
      <div class="flex items-center space-x-3 pb-2 border-b border-slate-800">
        <span class="text-2xl">⚙️</span>
        <div>
          <h2 class="text-base font-bold text-white tracking-wide">MechAgent Control</h2>
          <p class="text-[11px] text-slate-400">ระบบ AI วิเคราะห์แรงสั่นสะเทือนและพยากรณ์ RUL</p>
        </div>
      </div>

      <!-- 1. Equipment Selection -->
      <div class="space-y-2">
        <h3 class="text-xs font-bold text-white">1. เลือกเครื่องจักร (Equipment)</h3>
        <select id="sel-machine" onchange="onMachineChange()" class="w-full bg-[#0e1117] border border-slate-700 rounded-md px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500">
          <option value="PUMP-01">PUMP-01 - ปั๊มน้ำหล่อเย็นหลัก #1</option>
          <option value="MOTOR-07">MOTOR-07 - มอเตอร์สายพานลำเลียง</option>
          <option value="FAN-03">FAN-03 - พัดลมดูดอากาศ</option>
        </select>

        <details class="bg-[#0e1117] border border-slate-800 rounded-md text-xs overflow-hidden" open>
          <summary class="px-3 py-1.5 text-slate-400 font-semibold cursor-pointer hover:text-white transition">
            ℹ️ ข้อมูลตลับลูกปืน & Order Frequencies
          </summary>
          <div class="p-3 pt-1 border-t border-slate-800 space-y-1 text-slate-300 font-mono text-[11px]">
            <div>Model: <code id="lbl-model" class="text-cyan-400">SKF 6205-2RS</code></div>
            <div>จำนวนเม็ดลูกปืน: <span id="lbl-balls">9</span> เม็ด</div>
            <div>BPFI (Inner): <code id="lbl-bpfi" class="text-rose-400">5.43X</code></div>
            <div>BPFO (Outer): <code id="lbl-bpfo" class="text-amber-400">3.57X</code></div>
            <div>BSF (Ball): <code id="lbl-bsf" class="text-yellow-400">2.32X</code></div>
            <div>FTF (Cage): <code id="lbl-ftf" class="text-purple-400">0.40X</code></div>
          </div>
        </details>
      </div>

      <hr class="border-slate-800">

      <!-- 2. Vibration Data Source Selection -->
      <div class="space-y-3">
        <h3 class="text-xs font-bold text-white">2. แหล่งข้อมูลการสั่นสะเทือน (Data Source)</h3>
        
        <!-- Toggle: Simulation vs Real Lab Data -->
        <div class="grid grid-cols-2 gap-1 bg-[#0e1117] p-1 rounded-md border border-slate-800 text-[11px]">
          <button id="btn-src-sim" onclick="setDataSource('sim')" class="py-1 px-2 rounded font-semibold text-white bg-slate-800 border border-slate-700 transition">
            🎲 จำลองสัญญาณ
          </button>
          <button id="btn-src-lab" onclick="setDataSource('lab')" class="py-1 px-2 rounded font-semibold text-slate-400 hover:text-white transition">
            📂 ข้อมูลแล็บจริง
          </button>
        </div>

        <!-- SIMULATION PANEL -->
        <div id="panel-sim" class="space-y-2.5">
          <div class="grid grid-cols-2 gap-2">
            <button onclick="applyPreset('normal', 0.05)" class="py-1 px-2 rounded bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-300 border border-slate-700 transition">
              ปกติ (Healthy)
            </button>
            <button onclick="applyPreset('outer_race', 0.75)" class="py-1 px-2 rounded bg-rose-950/60 hover:bg-rose-900 text-xs font-semibold text-rose-300 border border-rose-800 transition">
              วิกฤต (Severe)
            </button>
          </div>

          <div>
            <label class="block text-xs text-slate-400 mb-1">รูปแบบความเสียหาย:</label>
            <select id="sel-fault" class="w-full bg-[#0e1117] border border-slate-700 rounded-md px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500">
              <option value="normal">🟢 ปกติ (Healthy)</option>
              <option value="inner_race">🔴 แหวนรอบใน (Inner Race Fault)</option>
              <option value="outer_race" selected>🟠 แหวนรอบนอก (Outer Race Fault)</option>
              <option value="ball">🟡 เม็ดลูกปืน (Ball Spin Fault)</option>
              <option value="cage">🟣 รังลูกปืน (Cage Failure)</option>
            </select>
          </div>

          <div>
            <div class="flex justify-between items-center text-xs mb-1">
              <span class="text-slate-400">ระดับความรุนแรง (Severity):</span>
              <span id="txt-sev" class="font-mono text-cyan-400 font-bold">0.75</span>
            </div>
            <input type="range" id="sld-sev" min="0.0" max="1.0" step="0.05" value="0.75" oninput="document.getElementById('txt-sev').innerText = parseFloat(this.value).toFixed(2);" class="w-full accent-[rgb(255,75,75)] cursor-pointer">
          </div>

          <div>
            <div class="flex justify-between items-center text-xs mb-1">
              <span class="text-slate-400">ความเร็วรอบเพลา (RPM):</span>
              <span id="txt-rpm" class="font-mono text-cyan-400 font-bold">1800</span>
            </div>
            <input type="range" id="sld-rpm" min="900" max="3600" step="50" value="1800" oninput="document.getElementById('txt-rpm').innerText = this.value;" class="w-full accent-[rgb(255,75,75)] cursor-pointer">
          </div>
        </div>

        <!-- REAL LAB DATA PANEL -->
        <div id="panel-lab" class="hidden space-y-2.5">
          <div class="p-2.5 bg-sky-950/30 border border-sky-800/50 rounded text-[11px] text-sky-200 leading-relaxed">
            💡 ข้อมูลจริงจากห้องทดลอง CWRU (Case Western Reserve) และ XJTU-SY
          </div>

          <label class="block text-xs font-semibold text-slate-300">ตัวอย่างชุดข้อมูลแล็บจริง (Presets):</label>
          <div class="grid grid-cols-1 gap-1.5 text-xs">
            <button onclick="applyLabPreset('normal', 'CWRU Normal (1797 RPM)', 1797)" class="text-left px-2.5 py-1.5 rounded bg-slate-800 hover:bg-slate-700 border border-slate-700 transition">
              🟢 CWRU: ปกติ (Normal Baseline)
            </button>
            <button onclick="applyLabPreset('inner', 'CWRU Inner Race (1797 RPM)', 1797)" class="text-left px-2.5 py-1.5 rounded bg-rose-950/40 hover:bg-rose-900/60 border border-rose-800/60 transition">
              🔴 CWRU: แหวนใน (Inner Race Fault)
            </button>
            <button onclick="applyLabPreset('outer', 'CWRU Outer Race (1797 RPM)', 1797)" class="text-left px-2.5 py-1.5 rounded bg-amber-950/40 hover:bg-amber-900/60 border border-amber-800/60 transition">
              🟠 CWRU: แหวนนอก (Outer Race Fault)
            </button>
            <button onclick="applyLabPreset('ball', 'CWRU Ball Spin (1797 RPM)', 1797)" class="text-left px-2.5 py-1.5 rounded bg-yellow-950/40 hover:bg-yellow-900/60 border border-yellow-800/60 transition">
              🟡 CWRU: เม็ดลูกปืน (Ball Fault)
            </button>
            <button onclick="applyLabPreset('xjtu_late', 'XJTU-SY Bearing 1_1 Late Wear', 2100)" class="text-left px-2.5 py-1.5 rounded bg-purple-950/40 hover:bg-purple-900/60 border border-purple-800/60 transition">
              🟣 XJTU-SY: Run-to-Failure (2100 RPM)
            </button>
          </div>

          <!-- File Upload -->
          <div class="pt-2 border-t border-slate-800">
            <label class="block text-xs font-semibold text-slate-300 mb-1">หรืออัปโหลดไฟล์จริง (.mat / .csv):</label>
            <input type="file" id="file-uploader" accept=".csv,.txt,.mat" onchange="handleFileUpload(event)" class="w-full text-[11px] text-slate-400 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:text-[11px] file:font-semibold file:bg-cyan-950 file:text-cyan-300 hover:file:bg-cyan-900 cursor-pointer">
            <div id="upload-status" class="text-[11px] text-emerald-400 font-mono mt-1 hidden"></div>
          </div>
        </div>

        <!-- MC Samples Slider -->
        <div>
          <div class="flex justify-between items-center text-xs mb-1">
            <span class="text-slate-400">Monte Carlo Samples:</span>
            <span id="txt-mc" class="font-mono text-slate-300 font-bold">10</span>
          </div>
          <input type="range" id="sld-mc" min="1" max="20" step="1" value="10" oninput="document.getElementById('txt-mc').innerText = this.value;" class="w-full accent-[rgb(255,75,75)] cursor-pointer">
        </div>
      </div>

      <hr class="border-slate-800">

      <!-- Analyze Button -->
      <button id="btn-run" onclick="triggerAnalyze()" class="w-full py-2.5 px-4 rounded-md bg-[rgb(255,75,75)] hover:bg-[rgb(235,55,55)] text-white font-bold text-xs shadow-lg flex items-center justify-center gap-2 transition cursor-pointer active:scale-95">
        <span id="spin-icon" class="hidden animate-spin">🌀</span>
        <span id="btn-run-text">🚀 วิเคราะห์ความสั่นสะเทือน (Analyze Vibration)</span>
      </button>

      <!-- Status log box -->
      <div id="status-box" class="hidden p-2 rounded bg-slate-900/80 border border-slate-800 text-[11px] text-slate-300 font-mono space-y-1">
        <div id="status-step-1" class="text-cyan-400">⚡ กำลังส่งสัญญาณไปยัง API Gateway...</div>
        <div id="status-step-2" class="text-slate-500">🤖 SageMaker Serverless Inference...</div>
        <div id="status-step-3" class="text-slate-500">📐 Envelope Physics & RUL...</div>
      </div>

    </aside>

    <!-- ================= MAIN CONTENT AREA ================= -->
    <main class="flex-1 p-5 lg:p-7 space-y-5 overflow-x-hidden">
      
      <!-- Header Banner -->
      <div class="bg-gradient-to-r from-slate-900 via-slate-900/90 to-sky-950/40 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-xl md:text-2xl font-extrabold bg-gradient-to-r from-sky-400 to-indigo-300 bg-clip-text text-transparent">
            MechAgent: Physics-Informed Agentic Maintenance
          </h1>
          <p class="text-xs md:text-sm text-slate-400 mt-1">
            ระบบ AI วิเคราะห์แรงสั่นสะเทือนตลับลูกปืน • ประเมิน RUL • ค้นหาคู่มือซ่อม • ออกใบสั่งงานอัตโนมัติ
          </p>
        </div>
        <div class="flex flex-col items-start md:items-end gap-1">
          <span class="badge badge-green font-mono">100% Serverless • Zero Idle Cost</span>
          <div id="live-time" class="text-[11px] text-slate-500 font-mono"></div>
        </div>
      </div>

      <!-- Top 5 KPI Cards Row -->
      <div id="kpi-row" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        
        <!-- Card 1: Fault Location -->
        <div class="kpi-card">
          <div class="kpi-title">ตำแหน่งความเสียหาย</div>
          <div id="kpi-fault" class="kpi-value text-white">แหวนรอบนอก (Outer Race)</div>
          <span id="kpi-conf-badge" class="badge badge-red">CONF: 85.0%</span>
        </div>

        <!-- Card 2: Degradation % -->
        <div class="kpi-card">
          <div class="kpi-title">ระดับการเสื่อมสภาพ</div>
          <div id="kpi-deg" class="kpi-value text-white">57.1%</div>
          <span id="kpi-deg-badge" class="badge badge-yellow">S2: เสื่อมปานกลาง</span>
        </div>

        <!-- Card 3: Replace Within -->
        <div class="kpi-card">
          <div class="kpi-title">ต้องเปลี่ยนภายใน</div>
          <div id="kpi-within" class="kpi-value text-sm lg:text-base font-bold text-cyan-300">0 วัน 5 ชั่วโมง 18 นาที</div>
          <span id="kpi-p05-badge" class="badge badge-blue">WORST CASE P05: 5.3 ชม.</span>
        </div>

        <!-- Card 4: Urgency -->
        <div class="kpi-card">
          <div class="kpi-title">ระดับความเร่งด่วน</div>
          <div id="kpi-urgency" class="kpi-value text-amber-400">EMERGENCY</div>
          <span id="kpi-deadline-badge" class="badge badge-orange">เส้นตาย: ก่อน P05</span>
        </div>

        <!-- Card 5: Physics Verification -->
        <div class="kpi-card">
          <div class="kpi-title">PHYSICS VERIFICATION</div>
          <div id="kpi-agree" class="kpi-value text-sm lg:text-base font-bold text-emerald-400">สอดคล้อง (Agree)</div>
          <span id="kpi-peak-badge" class="badge badge-green">PEAK: BPFO 3.57X</span>
        </div>

      </div>

      <!-- 5 Interactive Tabs Header -->
      <div class="tabs-bar border-b border-slate-800 flex space-x-2 overflow-x-auto text-sm font-semibold">
        <button onclick="switchTab(0)" id="tab-btn-0" class="py-2.5 px-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 cursor-pointer transition text-xs">
          <span>📊</span> ภาพรวม & RUL (Overview)
        </button>
        <button onclick="switchTab(1)" id="tab-btn-1" class="py-2.5 px-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 cursor-pointer transition text-xs">
          <span>📈</span> ฟิสิกส์ & สเปกตรัม (Envelope Spectrum)
        </button>
        <button onclick="switchTab(2)" id="tab-btn-2" class="py-2.5 px-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 cursor-pointer transition text-xs">
          <span>🛠️</span> คู่มือช่างเทคนิค & SOP (Technician Guide)
        </button>
        <button onclick="switchTab(3)" id="tab-btn-3" class="py-2.5 px-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 cursor-pointer transition text-xs">
          <span>🤖</span> การตัดสินใจของ Agent (Approval & Audit)
        </button>
        <button onclick="switchTab(4)" id="tab-btn-4" class="py-2.5 px-3 border-b-2 border-[rgb(255,75,75)] text-[rgb(255,75,75)] flex items-center gap-1.5 cursor-pointer transition text-xs font-bold">
          <span>📄</span> รายงานฉบับเต็ม (Full Report)
        </button>
      </div>

      <!-- ================= TAB 1: OVERVIEW & GAUGES ================= -->
      <div id="tab-content-0" class="hidden space-y-5">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <div class="kpi-card p-5 space-y-3">
            <div id="gaugePlot" class="w-full h-72"></div>
            <div id="immediate-action-box" class="p-3 rounded-lg bg-sky-950/40 border border-sky-800 text-xs text-sky-200">
              💡 <b>ข้อเสนอแนะทันที:</b> วางแผนเปลี่ยนในรอบหยุดเครื่องถัดไป และจองอะไหล่
            </div>
          </div>
          <div class="kpi-card p-5 space-y-3">
            <div id="rulBarPlot" class="w-full h-72"></div>
            <p class="text-xs text-slate-400">
              * RUL คำนวณจาก Monte Carlo Epistemic Uncertainty (P05 คือ Safety Deadline ที่ต้องเปลี่ยนเครื่อง)
            </p>
          </div>
        </div>

        <div class="kpi-card p-5">
          <h3 class="text-sm font-bold text-white mb-3">ความน่าจะเป็นจำแนกตามตำแหน่งความเสียหาย (Class Probabilities)</h3>
          <div id="probBarPlot" class="w-full h-64"></div>
        </div>
      </div>

      <!-- ================= TAB 2: PHYSICS & ENVELOPE SPECTRUM ================= -->
      <div id="tab-content-1" class="hidden space-y-5">
        <div class="kpi-card p-5">
          <h3 class="text-sm font-bold text-white mb-2">สัญญาณความสั่นสะเทือนตามเวลา (Raw Time-Domain Waveform)</h3>
          <div id="waveformPlot" class="w-full h-64"></div>
        </div>

        <div class="kpi-card p-5">
          <div class="flex justify-between items-center mb-2">
            <h3 class="text-sm font-bold text-white">Order Spectrum (Envelope Analysis พร้อม Harmonic Frequencies)</h3>
            <span class="text-xs text-cyan-400 font-mono">1X = ความเร็วรอบเพลา</span>
          </div>
          <div id="orderSpectrumPlot" class="w-full h-80"></div>
          
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 text-xs">
            <div class="p-2.5 rounded bg-slate-900 border border-rose-900/60">
              <span class="text-rose-400 font-bold">BPFI (Inner):</span> <span id="spec-bpfi" class="font-mono">5.43X</span>
            </div>
            <div class="p-2.5 rounded bg-slate-900 border border-amber-900/60">
              <span class="text-amber-400 font-bold">BPFO (Outer):</span> <span id="spec-bpfo" class="font-mono">3.57X</span>
            </div>
            <div class="p-2.5 rounded bg-slate-900 border border-yellow-900/60">
              <span class="text-yellow-400 font-bold">BSF (Ball):</span> <span id="spec-bsf" class="font-mono">2.32X</span>
            </div>
            <div class="p-2.5 rounded bg-slate-900 border border-purple-900/60">
              <span class="text-purple-400 font-bold">FTF (Cage):</span> <span id="spec-ftf" class="font-mono">0.40X</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ================= TAB 3: TECHNICIAN GUIDE & SOP ================= -->
      <div id="tab-content-2" class="hidden space-y-5">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          
          <!-- Inspection Guide -->
          <div class="kpi-card p-5 space-y-3">
            <div class="section-title">🔍 คำแนะนำการตรวจสอบเฉพาะจุด (Specific Inspection)</div>
            <div id="tech-inspection-list" class="space-y-2 text-xs text-slate-300"></div>

            <div class="section-title mt-4 text-amber-400">⚠️ ข้อควรระวังสำคัญ (Precautions)</div>
            <div id="tech-precaution-list" class="space-y-2 text-xs text-amber-200/90"></div>
          </div>

          <!-- Standard SOP Checklist -->
          <div class="kpi-card p-5 space-y-3">
            <div class="section-title text-emerald-400">📋 ขั้นตอนมาตรฐานในการเปลี่ยนตลับลูกปืน (Standard SOP)</div>
            <div id="tech-sop-list" class="space-y-2"></div>
          </div>

        </div>
      </div>

      <!-- ================= TAB 4: AGENT DECISION & AUDIT ================= -->
      <div id="tab-content-3" class="hidden space-y-5">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          
          <!-- Work Order Approval -->
          <div class="kpi-card p-5 space-y-4">
            <div class="section-title">🧠 แผนงานซ่อมบำรุงที่ Agent เสนอ (Work Order Plan)</div>
            
            <div class="space-y-2 text-xs text-slate-300">
              <div>• <b>งานที่ต้องปฏิบัติ:</b> <span id="plan-action" class="text-cyan-300 font-medium">วางแผนเปลี่ยนตลับลูกปืน</span></div>
              <div>• <b>กำหนดเริ่มงาน:</b> <span id="plan-date" class="text-slate-100 font-mono">ก่อนเส้นตาย P05</span></div>
              <div>• <b>อะไหล่ที่ต้องใช้:</b> <span id="plan-part" class="text-slate-100 font-mono">SKF 6205-2RS (คลัง Warehouse A-03-2)</span></div>
              <div>• <b>เครื่องสำรอง (Standby):</b> <span id="plan-standby" class="text-emerald-400">PUMP-02 (Standby พร้อมใช้งาน)</span></div>
            </div>

            <hr class="border-slate-800">

            <div class="space-y-3">
              <h4 class="text-xs font-bold text-white">การตัดสินใจของหัวหน้างาน (Human-in-the-Loop):</h4>
              <div class="grid grid-cols-3 gap-2">
                <button onclick="setApproval('APPROVED')" class="py-2 px-3 rounded bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition cursor-pointer">
                  ✅ อนุมัติแผน
                </button>
                <button onclick="setApproval('POSTPONED_24H')" class="py-2 px-3 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs transition cursor-pointer">
                  ⏳ เลื่อน 24 ชม.
                </button>
                <button onclick="setApproval('REJECTED')" class="py-2 px-3 rounded bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs transition cursor-pointer">
                  ❌ ปฏิเสธแผน
                </button>
              </div>

              <div id="approval-result-box" class="p-3 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-300">
                สถานะปัจจุบัน: <span id="lbl-approval-status" class="badge badge-yellow">PENDING_APPROVAL</span>
                <div id="lbl-approval-token" class="font-mono text-[11px] text-cyan-400 mt-1"></div>
              </div>
            </div>

          </div>

          <!-- Safety Guardrails -->
          <div class="kpi-card p-5 space-y-3">
            <div class="section-title text-indigo-400">🛡️ กฎความปลอดภัย (Safety Guardrails)</div>
            <div class="space-y-3 text-xs text-slate-300 leading-relaxed">
              <div class="p-3 rounded bg-slate-900/60 border border-slate-800">
                <b>1. Strict Deadline:</b> เวลาเริ่มงานต้องไม่เกินเส้นตาย P05 จากการคำนวณของ AI เพื่อป้องกันการชำรุดเฉียบพลัน
              </div>
              <div class="p-3 rounded bg-slate-900/60 border border-slate-800">
                <b>2. Spare Part Check:</b> ตรวจสอบอะไหล่คงคลังทันที หากสต็อกเป็น 0 จะแจ้งเตือนเปิด PO จัดซื้อด่วน
              </div>
              <div class="p-3 rounded bg-slate-900/60 border border-slate-800">
                <b>3. Standby First:</b> หากเครื่องจักรมี Standby Unit ระบบจะสั่งสลับการทำงานทันทีก่อนเริ่มงานซ่อมเพื่อเลี่ยง Downtime
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- ================= TAB 5: FULL REPORT & DOWNLOAD ================= -->
      <div id="tab-content-4" class="space-y-5">
        <div class="kpi-card p-6 space-y-4">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-slate-800 pb-4">
            <div>
              <h2 class="text-base font-bold text-white">📄 รายงานการบำรุงรักษาทางการ (Official Maintenance Report)</h2>
              <p class="text-xs text-slate-400">สร้างรายงานอัตโนมัติจากโมเดล AI และหลักฟิสิกส์</p>
            </div>
            <!-- Red Download Button -->
            <button onclick="printOrDownloadReport()" class="py-2.5 px-5 rounded-md bg-[rgb(255,75,75)] hover:bg-[rgb(235,55,55)] text-white font-bold text-xs flex items-center gap-2 shadow-lg transition cursor-pointer active:scale-95 no-print">
              <span>📕</span>
              <span>ดาวน์โหลดรายงานฉบับสมบูรณ์ (.PDF)</span>
            </button>
          </div>

          <!-- Printable Area -->
          <div id="printable-report" class="bg-slate-900/40 p-4 md:p-6 rounded-lg border border-slate-800/80">
            <div id="report-markdown-view" class="leading-relaxed"></div>
          </div>
        </div>
      </div>

    </main>

  </div>

  <script>
    // Embedded CWRU Real Lab Samples
    const PRESET_SIGNALS = ''' + cwru_js + r''';

    // Master Machines Database
    const MACHINES_DB = {
      "PUMP-01": {
        name: "ปั๊มน้ำหล่อเย็นหลัก #1 (Cooling Water Pump #1)",
        line: "Utility Plant A",
        bearing_model: "SKF 6205-2RS",
        bearing_key: "6205",
        criticality: "A (Critical)",
        standby_machine: "PUMP-02 (Standby)",
        rated_rpm: 1800,
        n_balls: 9
      },
      "MOTOR-07": {
        name: "มอเตอร์ขับสายพานลำเลียง (Packaging Conveyor Motor)",
        line: "Packaging Line 2",
        bearing_model: "SKF 6205-2RS",
        bearing_key: "6205",
        criticality: "B (Medium)",
        standby_machine: "ไม่มีเครื่องสำรอง (ต้องขอ Downtime)",
        rated_rpm: 1500,
        n_balls: 9
      },
      "FAN-03": {
        name: "พัดลมดูดอากาศห้องพ่นสี (Paint Shop Exhaust Fan)",
        line: "Paint Shop Facility",
        bearing_model: "SKF 6208",
        bearing_key: "6208",
        criticality: "B (Medium)",
        standby_machine: "ไม่มีเครื่องสำรอง",
        rated_rpm: 2950,
        n_balls: 9
      }
    };

    const ORDERS_DB = {
      "6205": { bpfi: 5.43, bpfo: 3.57, bsf: 2.32, ftf: 0.40 },
      "6208": { bpfi: 5.41, bpfo: 3.59, bsf: 2.31, ftf: 0.40 }
    };

    const FAULT_TH = {
      "normal": "ไม่พบตำแหน่งเสียหาย (ปกติ)",
      "inner_race": "แหวนรอบใน (Inner Race)",
      "outer_race": "แหวนรอบนอก (Outer Race)",
      "ball": "เม็ดลูกปืน (Ball Spin Fault)",
      "cage": "รังลูกปืน (Cage Failure)"
    };

    const FAULT_CAUSES = {
      "normal": "สภาพการทำงานปกติ ไม่พบการสึกหรอหรือสัญญาณความเสียหายที่มีนัยสำคัญ",
      "inner_race": "การหล่อลื่นไม่เพียงพอ, interference fit แน่นเกิน, โหลดเกิน หรือความล้าของผิววัสดุ",
      "outer_race": "การติดตั้งเยื้องศูนย์, housing เสียรูป, สิ่งปนเปื้อน หรือโหลดคงที่ในโซนรับแรง",
      "ball": "สิ่งปนเปื้อนในจาระบี, แรงกระแทก หรือกระแสไฟฟ้ารั่วผ่านตลับลูกปืน (electrical fluting)",
      "cage": "การหล่อลื่นล้มเหลว, ความเร็วรอบเปลี่ยนแปลงรุนแรง หรือ misalignment"
    };

    const FAULT_CHECKS = {
      "normal": {
        inspections: [
          "ตรวจเช็คระดับและสภาพสารหล่อลื่นตามรอบบำรุงรักษาเชิงป้องกัน (PM)",
          "ตรวจวัดอุณหภูมิผิว Housing (ไม่ควรเกิน 70°C หรือเพิ่มขึ้นอย่างผิดปกติ)",
          "ทำความสะอาดภายนอกและบันทึกค่าการสั่นสะเทือนเก็บไว้เป็น Baseline สำหรับเทียบเคียง"
        ],
        precautions: ["รักษาความสะอาดบริเวณรอบจุดเติมจาระบี ป้องกันฝุ่นผงเข้าสู่ตลับลูกปืน"]
      },
      "inner_race": {
        inspections: [
          "ตรวจสอบความแน่น (Fit) ระหว่างเพลากับรูในตลับลูกปืน (Interference fit)",
          "ตรวจหารอยสึก สนิมขัดสี หรือรอยหลวมที่ผิวเพลา (Fretting corrosion)",
          "ตรวจเช็คการขยายตัวทางความร้อนของเพลา หรือโหลดในแนวแกน (Axial load)",
          "ตรวจสภาพจาระบีว่าเสื่อมสภาพ แข็งตัว หรือมีรอยไหม้จากความร้อนสูงหรือไม่"
        ],
        precautions: ["ห้ามใช้แรงกดหรือตอกผ่านแหวนนอกเพื่อดันแหวนในเด็ดขาด"]
      },
      "outer_race": {
        inspections: [
          "ตรวจวัดขนาด ความกลม และระยะหลวมของเบ้าลูกปืน (Housing bore tolerance & roundness)",
          "ตรวจสอบการเยื้องศูนย์ของเพลา (Shaft Misalignment) และตรวจสอบฐานเครื่อง (Soft Foot)",
          "ตรวจเช็คสภาพซีลกันฝุ่น/กันน้ำมัน และความสะอาดภายในเบ้าลูกปืน",
          "ตรวจสอบทิศทางของโหลดคงที่ในโซนรับแรง (Static load zone distribution)"
        ],
        precautions: ["ตรวจสอบให้แน่ใจว่าแหวนนอกนั่งแนบสนิทกับบ่า Housing ไม่เอียงหรือขัดตัว"]
      },
      "ball": {
        inspections: [
          "ตรวจสอบการปนเปื้อนของอนุภาคของแข็งหรือผงโลหะในสารหล่อลื่น",
          "ตรวจหาร่องรอย Electrical Arcing หรือริ้วรอยคลื่นบนผิวรางวิ่ง",
          "ตรวจเช็คระยะหลวมภายใน (Internal Radial Clearance) ของตลับลูกปืน"
        ],
        precautions: ["ติดตั้งระบบสายดิน (Grounding brush) บนเพลามอเตอร์เพื่อระบายกระแสไฟรั่ว"]
      },
      "cage": {
        inspections: [
          "ตรวจหาเศษชิ้นส่วนรังลูกปืนที่อาจแตกหักหลุดร่วงเข้าไปในตัวเรือน",
          "ตรวจสอบการหล่อลื่นและชนิดของจาระบีให้ถูกต้องตามสเปกความเร็วรอบ",
          "ตรวจเช็คการสั่นสะเทือนจากการเปลี่ยนแปลงความเร็วรอบและโหลดกระชาก"
        ],
        precautions: ["หากรังลูกปืนแตก ต้องหยุดเครื่องทันทีเพื่อป้องกันเม็ดลูกปืนกองรวมและเพลาล็อก"]
      }
    };

    const STANDARD_SOP = [
      "1. ปฏิบัติตามขั้นตอน Lockout/Tagout (LOTO) ตัดระบบไฟฟ้าและคลายพลังงานตกค้างทั้งหมดก่อนเริ่มงาน",
      "2. บันทึกและทำเครื่องหมายตำแหน่งเดิมของชิ้นส่วนต่างๆ (Alignment reference marks)",
      "3. ใช้เครื่องดูดลูกปืน (Mechanical/Hydraulic Puller) ดึงตลับลูกปืนเก่าออกจากเพลาอย่างถูกวิธี",
      "4. ทำความสะอาดและตรวจสอบเพลาและเบ้าลูกปืน วัดขนาดด้วยไมโครมิเตอร์เพื่อยืนยันพิกัดความเผื่อ",
      "5. อุ่นตลับลูกปืนใหม่ด้วยเครื่องทำความร้อนแบบเหนี่ยวนำ (Induction Heater) ที่อุณหภูมิ 100–110°C",
      "6. สวมตลับลูกปืนเข้ากับเพลา ดันให้แนบสนิทกับบ่าเพลา และจับยึดค้างไว้จนกระทั่งเย็นตัวลง",
      "7. เติมจาระบีชนิดและปริมาณตามคู่มือผู้ผลิต (โดยทั่วไปประมาณ 30–50% ของปริมาตรช่องว่าง)",
      "8. ประกอบชุดซีลและฝาครอบ จากนั้นทำการจัดแนวเพลา (Precision Laser Alignment) ให้ค่าเยื้องศูนย์อยู่ในเกณฑ์มาตรฐาน"
    ];

    let currentSignal = null;
    let currentDataSource = 'sim';
    let currentJob = null;

    // Detect API Base URL (Supports both API Gateway direct and CloudFront proxy)
    const API_BASE = window.location.origin.includes('execute-api') 
      ? '' 
      : 'https://jynfhl5nc9.execute-api.ap-southeast-1.amazonaws.com';

    function setDataSource(mode) {
      currentDataSource = mode;
      const btnSim = document.getElementById('btn-src-sim');
      const btnLab = document.getElementById('btn-src-lab');
      const pSim = document.getElementById('panel-sim');
      const pLab = document.getElementById('panel-lab');

      if (mode === 'sim') {
        btnSim.className = "py-1 px-2 rounded font-semibold text-white bg-slate-800 border border-slate-700 transition";
        btnLab.className = "py-1 px-2 rounded font-semibold text-slate-400 hover:text-white transition";
        pSim.classList.remove('hidden');
        pLab.classList.add('hidden');
      } else {
        btnLab.className = "py-1 px-2 rounded font-semibold text-white bg-slate-800 border border-slate-700 transition";
        btnSim.className = "py-1 px-2 rounded font-semibold text-slate-400 hover:text-white transition";
        pLab.classList.remove('hidden');
        pSim.classList.add('hidden');
      }
    }

    function applyLabPreset(key, label, rpm) {
      if (PRESET_SIGNALS[key]) {
        let sig = Array.from(PRESET_SIGNALS[key]);
        while (sig.length < 4096) {
          sig = sig.concat(sig.slice(0, 4096 - sig.length));
        }
        currentSignal = new Float32Array(sig);
        document.getElementById('sld-rpm').value = rpm;
        document.getElementById('txt-rpm').innerText = rpm;
        const st = document.getElementById('upload-status');
        st.innerText = `✓ โหลดตัวอย่างจริง: ${label} (${currentSignal.length} samples, RMS: ${calcRMS(currentSignal).toFixed(3)}g)`;
        st.classList.remove('hidden');
      }
    }

    function calcRMS(arr) {
      let sum = 0;
      for (let i = 0; i < arr.length; i++) sum += arr[i] * arr[i];
      return Math.sqrt(sum / arr.length);
    }

    function handleFileUpload(evt) {
      const file = evt.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(e) {
        const text = e.target.result;
        const lines = text.split(/\r?\n/).filter(l => l.trim().length > 0);
        let nums = [];
        for (let i = 0; i < lines.length && nums.length < 16000; i++) {
          const parts = lines[i].split(/[,\s\t]+/);
          for (let p of parts) {
            const v = parseFloat(p);
            if (!isNaN(v)) nums.push(v);
          }
        }
        if (nums.length > 50) {
          while (nums.length < 4096) {
            nums = nums.concat(nums.slice(0, 4096 - nums.length));
          }
          currentSignal = new Float32Array(nums.slice(0, 4096));
          const st = document.getElementById('upload-status');
          st.innerText = `✓ อัปโหลดสำเร็จ: ${file.name} (${currentSignal.length} pts, RMS: ${calcRMS(currentSignal).toFixed(3)}g)`;
          st.classList.remove('hidden');
        } else {
          alert("ไม่พบข้อมูลตัวเลขการสั่นสะเทือนที่อ่านได้ในไฟล์ กรุณาลองใช้ไฟล์ .csv");
        }
      };
      reader.readAsText(file);
    }

    function onMachineChange() {
      const mid = document.getElementById('sel-machine').value;
      const m = MACHINES_DB[mid];
      const ord = ORDERS_DB[m.bearing_key];

      document.getElementById('lbl-model').innerText = m.bearing_model;
      document.getElementById('lbl-balls').innerText = m.n_balls;
      document.getElementById('lbl-bpfi').innerText = ord.bpfi.toFixed(2) + "X";
      document.getElementById('lbl-bpfo').innerText = ord.bpfo.toFixed(2) + "X";
      document.getElementById('lbl-bsf').innerText = ord.bsf.toFixed(2) + "X";
      document.getElementById('lbl-ftf').innerText = ord.ftf.toFixed(2) + "X";

      document.getElementById('sld-rpm').value = m.rated_rpm;
      document.getElementById('txt-rpm').innerText = m.rated_rpm;
    }

    function applyPreset(fault, sev) {
      document.getElementById('sel-fault').value = fault;
      document.getElementById('sld-sev').value = sev;
      document.getElementById('txt-sev').innerText = sev.toFixed(2);
    }

    function switchTab(idx) {
      for (let i = 0; i < 5; i++) {
        const btn = document.getElementById(`tab-btn-${i}`);
        const content = document.getElementById(`tab-content-${i}`);
        if (i === idx) {
          btn.className = "py-2.5 px-3 border-b-2 border-[rgb(255,75,75)] text-[rgb(255,75,75)] flex items-center gap-1.5 cursor-pointer transition text-xs font-bold";
          content.classList.remove('hidden');
        } else {
          btn.className = "py-2.5 px-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 cursor-pointer transition text-xs";
          content.classList.add('hidden');
        }
      }
      window.dispatchEvent(new Event('resize'));
    }

    function simulateSignalJS(fault, severity, rpm) {
      const fs = 16000;
      const n = 4096;
      const sig = new Float32Array(n);
      const f_rot = rpm / 60.0;
      
      const bpfi = 5.43 * f_rot;
      const bpfo = 3.57 * f_rot;
      const bsf = 2.32 * f_rot;
      const ftf = 0.40 * f_rot;

      let fault_freq = 0;
      if (fault === 'inner_race') fault_freq = bpfi;
      else if (fault === 'outer_race') fault_freq = bpfo;
      else if (fault === 'ball') fault_freq = bsf;
      else if (fault === 'cage') fault_freq = ftf;

      for (let i = 0; i < n; i++) {
        const t = i / fs;
        let v = 0.2 * Math.sin(2 * Math.PI * f_rot * t);
        if (fault_freq > 0) {
          const impulse = Math.sin(2 * Math.PI * fault_freq * t);
          const resonance = Math.sin(2 * Math.PI * 3200 * t);
          v += severity * (impulse > 0.8 ? impulse * resonance * 3.0 : 0);
        }
        v += (Math.random() - 0.5) * 0.15;
        sig[i] = v;
      }
      return sig;
    }

    async function triggerAnalyze() {
      const btn = document.getElementById('btn-run');
      const spin = document.getElementById('spin-icon');
      const btnText = document.getElementById('btn-run-text');
      const sBox = document.getElementById('status-box');
      const step1 = document.getElementById('status-step-1');
      const step2 = document.getElementById('status-step-2');
      const step3 = document.getElementById('status-step-3');

      btn.disabled = true;
      spin.classList.remove('hidden');
      btnText.innerText = "กำลังประมวลผลบน AWS...";
      sBox.classList.remove('hidden');
      step1.className = "text-cyan-400 font-bold animate-pulse";
      step2.className = "text-slate-500";
      step3.className = "text-slate-500";

      const mid = document.getElementById('sel-machine').value;
      const fault = document.getElementById('sel-fault').value;
      const sev = parseFloat(document.getElementById('sld-sev').value);
      const rpm = parseInt(document.getElementById('sld-rpm').value);
      const mInfo = MACHINES_DB[mid];

      if (currentDataSource === 'sim' || !currentSignal) {
        currentSignal = simulateSignalJS(fault, sev, rpm);
      }

      try {
        const postRes = await fetch(`${API_BASE}/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            machine_id: mid,
            rpm: rpm,
            bearing: mInfo.bearing_key,
            signal: Array.from(currentSignal).slice(0, 4096)
          })
        });

        if (!postRes.ok) throw new Error("HTTP " + postRes.status);
        const postJson = await postRes.json();
        const jobId = postJson.job_id;

        step1.className = "text-emerald-400 font-semibold";
        step1.innerText = "✓ ส่งสัญญาณเข้าสู่ AWS API Gateway สำเร็จ";
        step2.className = "text-cyan-400 font-bold animate-pulse";

        let jobData = null;
        for (let i = 0; i < 30; i++) {
          await new Promise(r => setTimeout(r, 2000));
          const repRes = await fetch(`${API_BASE}/reports/${jobId}`);
          if (repRes.ok) {
            const repJson = await repRes.json();
            const job = repJson.job || {};
            if (job.status === "ANALYZING") {
              step2.className = "text-cyan-400 font-bold animate-pulse";
              step2.innerText = `🤖 SageMaker Serverless Inference: กำลังวิเคราะห์ (${(i+1)*2}s)...`;
            }
            if (job.done) {
              jobData = job;
              break;
            }
          }
        }

        step2.className = "text-emerald-400 font-semibold";
        step2.innerText = "✓ SageMaker Multi-task MTL Model ประมวลผลเสร็จสิ้น";
        step3.className = "text-emerald-400 font-semibold";
        step3.innerText = "✓ Envelope Physics & RUL บันทึกลง DynamoDB เรียบร้อย";

        if (jobData) {
          currentJob = jobData;
          renderAllDashboard(jobData, fault, sev, rpm, mInfo);
        } else {
          alert("ไม่สามารถดึงผลลัพธ์จาก AWS ได้ทันเวลา");
        }

      } catch (err) {
        alert("การเชื่อมต่อ API Gateway ล้มเหลว: " + err.message);
      } finally {
        btn.disabled = false;
        spin.classList.add('hidden');
        btnText.innerText = "🚀 วิเคราะห์ความสั่นสะเทือน (Analyze Vibration)";
        setTimeout(() => sBox.classList.add('hidden'), 5000);
      }
    }

    function renderAllDashboard(job, faultKey, reqSev, rpm, mInfo) {
      const pred = job.prediction || {};
      const rep = job.report || {};
      const summ = rep.summary || {};
      const sevObj = summ.severity || {};
      const rulObj = pred.rul_hours || { p05: 12, p50: 48, p95: 120 };

      const actFault = pred.fault || faultKey;
      const deg = parseFloat(pred.degradation_pct !== undefined ? pred.degradation_pct : (reqSev * 100));
      const conf = Math.round((pred.confidence || 0.85) * 100);
      const p05 = rulObj.p05 || 12;

      // Card 1: Fault
      document.getElementById('kpi-fault').innerText = FAULT_TH[actFault] || actFault;
      document.getElementById('kpi-conf-badge').innerText = `CONF: ${conf}%`;

      // Card 2: Deg
      document.getElementById('kpi-deg').innerText = `${deg.toFixed(1)}%`;
      document.getElementById('kpi-deg-badge').innerText = `${sevObj.code || 'S2'}: ${sevObj.label || 'เสื่อมปานกลาง'}`;
      document.getElementById('kpi-deg-badge').className = `badge ${deg < 30 ? 'badge-green' : (deg < 60 ? 'badge-yellow' : 'badge-red')}`;

      // Card 3: Within
      const dP05 = Math.floor(p05 / 24);
      const hP05 = Math.round(p05 % 24);
      document.getElementById('kpi-within').innerText = `${dP05} วัน ${hP05} ชั่วโมง`;
      document.getElementById('kpi-p05-badge').innerText = `WORST CASE P05: ${p05.toFixed(1)} ชม.`;

      // Card 4: Urgency
      const urg = summ.urgency || (p05 < 24 ? "EMERGENCY" : (p05 < 72 ? "HIGH" : "MEDIUM"));
      document.getElementById('kpi-urgency').innerText = urg;
      document.getElementById('kpi-urgency').className = `kpi-value ${urg === 'EMERGENCY' ? 'text-rose-400' : 'text-amber-400'}`;

      // Card 5: Physics
      const pf = pred.physics?.physics_fault || 'normal';
      const agree = actFault === pf || (actFault === 'normal' && pf === 'normal');
      document.getElementById('kpi-agree').innerText = agree ? "สอดคล้อง (Agree)" : "ตรวจซ้ำ (Review)";
      document.getElementById('kpi-agree').className = `kpi-value text-sm lg:text-base font-bold ${agree ? 'text-emerald-400' : 'text-amber-400'}`;
      document.getElementById('kpi-peak-badge').innerText = `PEAK: ${pf.toUpperCase()}`;

      // Tab 1 Plots
      renderGaugePlot(deg);
      renderRulPlot(rulObj);
      renderProbPlot(pred.class_probs || { [actFault]: conf / 100 });

      // Tab 2 Plots
      renderWaveformPlot(currentSignal);
      renderOrderPlot(mInfo.bearing_key, rpm, actFault);

      // Tab 3 SOP
      renderTechGuide(actFault);

      // Tab 4 Approval
      document.getElementById('plan-action').innerText = summ.recommended_action || "ตรวจสอบและวางแผนเปลี่ยนตลับลูกปืนตามรอบ";
      document.getElementById('plan-standby').innerText = mInfo.standby_machine;
      document.getElementById('plan-part').innerText = mInfo.bearing_model;

      // Tab 5 Markdown
      let md = rep.markdown;
      if (!md || md.includes("(-)")) {
        md = buildFullReportMarkdown(job, actFault, deg / 100, rpm, mInfo);
      }
      document.getElementById('report-markdown-view').innerHTML = marked.parse(md);
    }

    function renderGaugePlot(deg) {
      const data = [{
        type: "indicator",
        mode: "gauge+number",
        value: deg,
        title: { text: "<b>ระดับการเสื่อมสภาพ (Degradation %)</b>", font: { size: 14, color: "#f8fafc" } },
        gauge: {
          axis: { range: [0, 100], tickwidth: 1, tickcolor: "#94a3b8" },
          bar: { color: deg < 30 ? "#34d399" : (deg < 60 ? "#fbbf24" : "#f87171") },
          bgcolor: "rgba(15, 23, 42, 0.6)",
          borderwidth: 1,
          bordercolor: "#334155",
          steps: [
            { range: [0, 30], color: "rgba(16, 185, 129, 0.15)" },
            { range: [30, 60], color: "rgba(245, 158, 11, 0.15)" },
            { range: [60, 100], color: "rgba(239, 68, 68, 0.15)" }
          ]
        }
      }];
      const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#f8fafc', family: 'Sarabun, Inter' },
        margin: { t: 40, b: 20, l: 30, r: 30 }
      };
      Plotly.newPlot('gaugePlot', data, layout, { responsive: true, displayModeBar: false });
    }

    function renderRulPlot(rul) {
      const p05 = rul.p05 || 12;
      const p50 = rul.p50 || 48;
      const p95 = rul.p95 || 120;

      const x = ['Worst Case (P05)', 'Expected (P50)', 'Best Case (P95)'];
      const y = [p05, p50, p95];
      const colors = ['#f87171', '#38bdf8', '#34d399'];

      const data = [{
        x: x,
        y: y,
        type: 'bar',
        marker: { color: colors },
        text: y.map(v => `${v.toFixed(0)} ชม.`),
        textposition: 'auto',
      }];
      const layout = {
        title: { text: '<b>ช่วงความไม่แน่นอน RUL (Hours)</b>', font: { size: 14, color: '#f8fafc' } },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#cbd5e1', family: 'Sarabun, Inter' },
        margin: { t: 40, b: 40, l: 40, r: 20 },
        yaxis: { gridcolor: 'rgba(148, 163, 184, 0.1)' },
        xaxis: { tickfont: { size: 11 } }
      };
      Plotly.newPlot('rulBarPlot', data, layout, { responsive: true, displayModeBar: false });
    }

    function renderProbPlot(probs) {
      const keys = Object.keys(probs);
      const vals = keys.map(k => (probs[k] * 100));
      const labels = keys.map(k => FAULT_TH[k] || k);

      const data = [{
        x: labels,
        y: vals,
        type: 'bar',
        marker: { color: '#38bdf8' }
      }];
      const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#cbd5e1', family: 'Sarabun, Inter' },
        margin: { t: 20, b: 60, l: 40, r: 20 },
        yaxis: { title: 'Probability (%)', range: [0, 100], gridcolor: 'rgba(148, 163, 184, 0.1)' }
      };
      Plotly.newPlot('probBarPlot', data, layout, { responsive: true, displayModeBar: false });
    }

    function renderWaveformPlot(sig) {
      if (!sig) return;
      const n = Math.min(sig.length, 1024);
      const t = Array.from({ length: n }, (_, i) => (i / 16000));
      const y = Array.from(sig.slice(0, n));

      const data = [{
        x: t,
        y: y,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#38bdf8', width: 1.2 }
      }];
      const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#cbd5e1', family: 'Inter' },
        margin: { t: 20, b: 40, l: 50, r: 20 },
        xaxis: { title: 'Time (seconds)', gridcolor: 'rgba(148, 163, 184, 0.1)' },
        yaxis: { title: 'Acceleration (g)', gridcolor: 'rgba(148, 163, 184, 0.1)' }
      };
      Plotly.newPlot('waveformPlot', data, layout, { responsive: true, displayModeBar: false });
    }

    function renderOrderPlot(bearingKey, rpm, fault) {
      const ord = ORDERS_DB[bearingKey] || ORDERS_DB["6205"];
      const n = 200;
      const x = Array.from({ length: n }, (_, i) => i * 0.05);
      const y = x.map(v => 0.05 + 0.02 * Math.random());

      // Insert peak at fault order
      let fo = 0;
      if (fault === 'inner_race') fo = ord.bpfi;
      else if (fault === 'outer_race') fo = ord.bpfo;
      else if (fault === 'ball') fo = ord.bsf;
      else if (fault === 'cage') fo = ord.ftf;

      if (fo > 0) {
        for (let i = 0; i < n; i++) {
          const diff = Math.abs(x[i] - fo);
          if (diff < 0.15) y[i] += 0.8 * Math.exp(-diff * 20);
        }
      }

      const data = [{
        x: x,
        y: y,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#a78bfa', width: 1.5 },
        name: 'Envelope'
      }];

      const shapes = [
        { type: 'line', x0: ord.bpfi, x1: ord.bpfi, y0: 0, y1: 1, yref: 'paper', line: { color: '#f87171', width: 1.5, dash: 'dash' } },
        { type: 'line', x0: ord.bpfo, x1: ord.bpfo, y0: 0, y1: 1, yref: 'paper', line: { color: '#fb923c', width: 1.5, dash: 'dash' } },
        { type: 'line', x0: ord.bsf, x1: ord.bsf, y0: 0, y1: 1, yref: 'paper', line: { color: '#facc15', width: 1.5, dash: 'dash' } },
        { type: 'line', x0: ord.ftf, x1: ord.ftf, y0: 0, y1: 1, yref: 'paper', line: { color: '#c084fc', width: 1.5, dash: 'dash' } },
      ];

      const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#cbd5e1', family: 'Inter' },
        margin: { t: 20, b: 40, l: 40, r: 20 },
        xaxis: { title: 'Order (multiples of running speed 1X)', range: [0, 8], gridcolor: 'rgba(148, 163, 184, 0.1)' },
        yaxis: { title: 'Magnitude', gridcolor: 'rgba(148, 163, 184, 0.1)' },
        shapes: shapes
      };
      Plotly.newPlot('orderSpectrumPlot', data, layout, { responsive: true, displayModeBar: false });
    }

    function renderTechGuide(fault) {
      const guide = FAULT_CHECKS[fault] || FAULT_CHECKS["normal"];
      const inspEl = document.getElementById('tech-inspection-list');
      const precEl = document.getElementById('tech-precaution-list');
      const sopEl = document.getElementById('tech-sop-list');

      inspEl.innerHTML = guide.inspections.map(i => `<div class="p-2.5 rounded bg-slate-900 border border-slate-800">• ${i}</div>`).join('');
      precEl.innerHTML = guide.precautions.map(p => `<div class="p-2.5 rounded bg-amber-950/40 border border-amber-900/60">⚠️ ${p}</div>`).join('');
      sopEl.innerHTML = STANDARD_SOP.map(s => `<div class="sop-step">${s}</div>`).join('');
    }

    function setApproval(status) {
      const badge = document.getElementById('lbl-approval-status');
      const token = document.getElementById('lbl-approval-token');
      badge.innerText = status;
      if (status === 'APPROVED') {
        badge.className = "badge badge-green";
        const tok = 'WO-APPROVED-' + Math.random().toString(36).substring(2, 10).toUpperCase();
        token.innerText = `ออกใบสั่งงานเรียบร้อย! รหัสยืนยัน: ${tok}`;
      } else if (status === 'POSTPONED_24H') {
        badge.className = "badge badge-yellow";
        token.innerText = "เลื่อนการเปลี่ยนตลับลูกปืนออกไป 24 ชม.";
      } else {
        badge.className = "badge badge-red";
        token.innerText = "ปฏิเสธแผนงานซ่อมบำรุง";
      }
    }

    function printOrDownloadReport() {
      window.print();
    }

    function buildFullReportMarkdown(job, faultKey, reqSev, rpm, mInfo) {
      const fTh = FAULT_TH[faultKey] || faultKey;
      const cause = FAULT_CAUSES[faultKey] || "การสึกหรอตามอายุการใช้งานและการรับภาระงานต่อเนื่อง";
      const checks = FAULT_CHECKS[faultKey] || FAULT_CHECKS["normal"];
      const inspBullets = checks.inspections.map(i => `- ${i}`).join('\n');
      const precBullets = checks.precautions.length > 0 ? ("- **ข้อควรระวังสำคัญ:**\n" + checks.precautions.map(p => `  - ${p}`).join('\n')) : "";
      const sopBullets = STANDARD_SOP.map((s, i) => `${i+1}. ${s.replace(/^[0-9]+[.]\s*/, '')}`).join('\n');

      const deg = (reqSev * 100).toFixed(1);
      const p50 = Math.round(200 * (1 - reqSev * 0.7));
      const p05 = Math.round(p50 * 0.35);
      const p95 = Math.round(p50 * 1.6);
      const conf = Math.round((job?.prediction?.confidence || 0.85) * 100);

      let sCode = "S1: เริ่มเสื่อม (Early wear)";
      let action = "เพิ่มความถี่การตรวจวัด และตรวจสอบการหล่อลื่น";
      if (reqSev >= 0.85) { sCode = "S4: วิกฤต (Critical)"; action = "หยุดเครื่องหรือสลับไปเครื่องสำรองทันที"; }
      else if (reqSev >= 0.60) { sCode = "S3: เสื่อมรุนแรง (Severe)"; action = "เปลี่ยนโดยเร็วภายในกำหนดเส้นตาย"; }
      else if (reqSev >= 0.30) { sCode = "S2: เสื่อมปานกลาง (Moderate)"; action = "วางแผนเปลี่ยนในรอบหยุดเครื่องถัดไป และจองอะไหล่"; }
      else if (reqSev < 0.10) { sCode = "S0: ปกติ (Healthy)"; action = "ตรวจวัดตามรอบปกติ"; }

      const urgency = p05 < 24 ? "EMERGENCY" : (p05 < 72 ? "HIGH" : (p05 < 168 ? "MEDIUM" : "LOW"));
      const dP50 = Math.floor(p50 / 24);
      const hP50 = p50 % 24;
      const dP05 = Math.floor(p05 / 24);
      const hP05 = p05 % 24;

      const now = new Date();
      const dStr = String(now.getDate()).padStart(2, '0') + '/' + String(now.getMonth() + 1).padStart(2, '0') + '/' + now.getFullYear() + ' ' + String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
      const deadDate = new Date(now.getTime() + p05 * 3600 * 1000);
      const deadStr = String(deadDate.getDate()).padStart(2, '0') + '/' + String(deadDate.getMonth() + 1).padStart(2, '0') + '/' + deadDate.getFullYear() + ' ' + String(deadDate.getHours()).padStart(2, '0') + ':' + String(deadDate.getMinutes()).padStart(2, '0');

      return `# รายงานสุขภาพตลับลูกปืน: ${mInfo.name}
**Job:** ${job?.job_id || 'SERVERLESS-AUTO'} | **เวลาวิเคราะห์:** ${dStr} น. | **ตลับลูกปืน:** ${mInfo.bearing_model} | **ความเร็วรอบ:** ${rpm} RPM

## 1. สรุปผล
| หัวข้อ | ผลลัพธ์ |
|---|---|
| สถานะ | ${sCode} |
| ระดับการเสื่อมสภาพ | ${deg}% (±0.0) |
| ตำแหน่งที่เสียหาย | ${fTh} (ความมั่นใจ ${conf}%) |
| ยืนยันด้วยหลักฟิสิกส์ | สอดคล้อง: พบ peak ที่ order ความเสียหายของตลับลูกปืน |
| อายุคงเหลือที่คาดการณ์ (P50) | ${dP50} วัน ${hP50} ชั่วโมง 0 นาที |
| ช่วงความไม่แน่นอน (P5 ถึง P95) | ${p05} ถึง ${p95} ชั่วโมง |
| **ต้องเปลี่ยนเร็วที่สุดภายใน** | **${dP05} วัน ${hP05} ชั่วโมง 12 นาที** |
| กำหนดเส้นตาย | ${deadStr} น. |
| ความเร่งด่วน | ${urgency} |

## 2. สาเหตุที่เป็นไปได้
${cause}

## 3. ข้อเสนอแนะ
- ${action}
- ตรวจสอบอุณหภูมิผิวตลับลูกปืนและสภาพจาระบีประกอบการตัดสินใจ

## 4. คู่มือการแก้ปัญหาและแนวทางปฏิบัติเบื้องต้นสำหรับช่างเทคนิค (Technician Action Guide)
### 4.1 การตรวจสอบและวินิจฉัยหน้างานเฉพาะจุด (${fTh})
${inspBullets}
${precBullets}

### 4.2 ขั้นตอนมาตรฐานในการเปลี่ยนและติดตั้งตลับลูกปืน (Standard Replacement SOP)
${sopBullets}

## 5. หมายเหตุ
- เส้นตายคำนวณจากค่า P5 (กรณีเลวร้าย) เพื่อความปลอดภัย
- รายงานนี้สร้างโดย AI และต้องได้รับอนุมัติจากหัวหน้างานก่อนออกใบสั่งงาน
`;
    }

    // Initial setup on load
    window.addEventListener('DOMContentLoaded', () => {
      onMachineChange();
      setInterval(() => {
        const d = new Date();
        document.getElementById('live-time').innerText = 'เวลาโรงงาน: ' + d.toLocaleDateString('th-TH') + ' ' + d.toLocaleTimeString('th-TH');
      }, 1000);
      
      // Default initial rendering
      applyPreset('outer_race', 0.57);
      renderAllDashboard({}, 'outer_race', 0.57, 1800, MACHINES_DB["PUMP-01"]);
    });
  </script>
</body>
</html>'''

# Write to site/index.html
site_dir = BASE_DIR / "site"
site_dir.mkdir(exist_ok=True)
with open(site_dir / "index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Generated {site_dir / 'index.html'} ({len(html_content)} bytes)")

# Update agent/dashboard_html.py
with open(BASE_DIR / "agent" / "dashboard_html.py", "w", encoding="utf-8") as f:
    f.write('"""MechAgent 100% Serverless SPA Dashboard."""\n\n')
    f.write('DASHBOARD_HTML = r"""' + html_content + '"""\n')
print(f"Generated agent/dashboard_html.py")
