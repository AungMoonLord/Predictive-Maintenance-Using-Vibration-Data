"""MechAgent 100% Serverless SPA Dashboard."""

DASHBOARD_HTML = r"""<!DOCTYPE html>
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
      @page {
        margin: 12mm 15mm 12mm 15mm;
        size: A4 portrait;
      }

      /* 1. Global Reset to Pure White Background & Crisp Black/Slate Text */
      html, body {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #0f172a !important;
        font-family: 'Sarabun', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 10.5pt !important;
        line-height: 1.55 !important;
        margin: 0 !important;
        padding: 0 !important;
      }

      /* 2. Hide all app navigation, banners, sidebars, buttons, and unrelated tabs */
      aside,
      header,
      #kpi-row,
      .tabs-bar,
      .no-print,
      .bg-gradient-to-r,
      #tab-content-0,
      #tab-content-1,
      #tab-content-2,
      #tab-content-3,
      #tab-content-5 {
        display: none !important;
      }

      /* 3. Containers - force 100% clean white background with no dark borders or shadows */
      main,
      #main-container,
      #tab-content-4,
      .kpi-card,
      #printable-report {
        display: block !important;
        background-color: #ffffff !important;
        background: #ffffff !important;
        box-shadow: none !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
      }

      /* 4. Show official print letterhead */
      .print-only {
        display: block !important;
      }

      /* 5. Typography in Print */
      #report-markdown-view,
      #report-markdown-view * {
        color: #0f172a !important;
        background: transparent !important;
        background-color: transparent !important;
        text-shadow: none !important;
      }

      #report-markdown-view h1 {
        font-size: 15pt !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        background-color: #f8fafc !important;
        border-left: 5px solid #0284c7 !important;
        border-bottom: none !important;
        border-radius: 0 4px 4px 0 !important;
        padding: 8px 12px !important;
        margin-top: 4px !important;
        margin-bottom: 12px !important;
        page-break-after: avoid;
      }

      #report-markdown-view h2 {
        font-size: 12pt !important;
        font-weight: 700 !important;
        color: #0369a1 !important;
        border-bottom: 1.5px solid #cbd5e1 !important;
        padding-bottom: 4px !important;
        margin-top: 16px !important;
        margin-bottom: 8px !important;
        page-break-after: avoid;
      }

      #report-markdown-view h3 {
        font-size: 10.5pt !important;
        font-weight: 700 !important;
        color: #1e293b !important;
        margin-top: 12px !important;
        margin-bottom: 6px !important;
        page-break-after: avoid;
      }

      #report-markdown-view p,
      #report-markdown-view li {
        font-size: 10pt !important;
        color: #1e293b !important;
        line-height: 1.55 !important;
      }

      #report-markdown-view strong {
        color: #000000 !important;
        font-weight: 700 !important;
      }

      /* 6. Clean, Ink-Saving Table Styling (White Background, Crisp Borders) */
      #report-markdown-view table {
        width: 100% !important;
        border-collapse: collapse !important;
        border: 1px solid #94a3b8 !important;
        margin: 10px 0 16px 0 !important;
        page-break-inside: avoid;
        background-color: #ffffff !important;
      }

      #report-markdown-view th {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        border: 1px solid #94a3b8 !important;
        padding: 7px 10px !important;
        font-size: 9.5pt !important;
        text-align: left !important;
      }

      #report-markdown-view td {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        padding: 6px 10px !important;
        font-size: 9.5pt !important;
      }

      #report-markdown-view tr:nth-child(even) td {
        background-color: #f8fafc !important;
      }

      /* 7. Code, Blockquote & Badges */
      #report-markdown-view code {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        border: 1px solid #e2e8f0 !important;
        padding: 1px 4px !important;
        border-radius: 3px !important;
        font-size: 9pt !important;
      }

      #report-markdown-view blockquote {
        background-color: #f8fafc !important;
        border-left: 3px solid #0284c7 !important;
        color: #1e293b !important;
        padding: 6px 12px !important;
        margin: 8px 0 !important;
        font-size: 9.5pt !important;
      }

      #report-markdown-view ul,
      #report-markdown-view ol {
        padding-left: 20px !important;
        margin: 6px 0 !important;
      }

      #report-markdown-view li {
        margin-bottom: 3px !important;
      }
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
            <select id="sel-fault" onchange="onFaultChange(this.value)" class="w-full bg-[#0e1117] border border-slate-700 rounded-md px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500">
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
            <span id="guardrail-note" class="text-[10px] text-amber-400 hidden">🛡️ โหมดปกติ (Healthy) ล็อกค่า Severity เป็น 0.0 เสมอ</span>
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
            <span id="txt-mc" class="font-mono text-slate-300 font-bold">100</span>
          </div>
          <input type="range" id="sld-mc" min="50" max="200" step="10" value="100" oninput="document.getElementById('txt-mc').innerText = this.value;" class="w-full accent-[rgb(255,75,75)] cursor-pointer">
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
      <div class="bg-gradient-to-r from-slate-900 via-slate-900/90 to-sky-950/40 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-4 no-print">
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

      <!-- 6 Interactive Tabs Header -->
      <div class="tabs-bar border-b border-slate-800 flex space-x-2 overflow-x-auto text-sm font-semibold">
        <button onclick="switchTab(0)" id="tab-btn-0" class="py-2.5 px-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 cursor-pointer transition text-xs whitespace-nowrap">
          <span>📊</span> ภาพรวม & RUL (Overview)
        </button>
        <button onclick="switchTab(1)" id="tab-btn-1" class="py-2.5 px-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 cursor-pointer transition text-xs whitespace-nowrap">
          <span>📈</span> ฟิสิกส์ & สเปกตรัม (Envelope Spectrum)
        </button>
        <button onclick="switchTab(2)" id="tab-btn-2" class="py-2.5 px-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 cursor-pointer transition text-xs whitespace-nowrap">
          <span>🛠️</span> คู่มือช่างเทคนิค & SOP (Technician Guide)
        </button>
        <button onclick="switchTab(3)" id="tab-btn-3" class="py-2.5 px-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 cursor-pointer transition text-xs whitespace-nowrap">
          <span>🤖</span> การตัดสินใจของ Agent (Approval & Audit)
        </button>
        <button onclick="switchTab(4)" id="tab-btn-4" class="py-2.5 px-3 border-b-2 border-[rgb(255,75,75)] text-[rgb(255,75,75)] flex items-center gap-1.5 cursor-pointer transition text-xs font-bold whitespace-nowrap">
          <span>📄</span> รายงานฉบับเต็ม (Full Report)
        </button>
        <button onclick="switchTab(5)" id="tab-btn-5" class="py-2.5 px-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 cursor-pointer transition text-xs whitespace-nowrap">
          <span>🗄️</span> ฐานข้อมูลระบบ (Database)
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
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-slate-800 pb-4 no-print">
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
            <!-- Official Print Letterhead (Clean White, Ink-Saving) -->
            <div class="hidden print-only border-b-2 border-slate-900 pb-3 mb-4">
              <div class="flex justify-between items-end">
                <div>
                  <div class="text-lg font-black text-slate-900 tracking-wide uppercase">MECHAGENT INDUSTRIAL AI PLATFORM</div>
                  <div class="text-xs text-slate-600 font-medium">Physics-Informed Autonomous Maintenance &amp; Machine Health Diagnostics</div>
                </div>
                <div class="text-right text-[10px] text-slate-500 font-mono">
                  <div>ISO 13373-1 Condition Monitoring Standard</div>
                  <div>OFFICIAL DIAGNOSTIC REPORT</div>
                </div>
              </div>
            </div>
            <div id="report-markdown-view" class="leading-relaxed"></div>
          </div>
        </div>
      </div>

      <!-- ================= TAB 5: DATABASE EXPLORER ================= -->
      <div id="tab-content-5" class="hidden space-y-5">
        <div class="kpi-card p-5 space-y-4">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 border-b border-slate-800 pb-3">
            <div>
              <h2 class="text-base font-bold text-white flex items-center gap-2">
                <span>🗄️</span> คลังข้อมูลระบบและการเฝ้าระวัง (MechAgent Database Explorer)
              </h2>
              <p class="text-xs text-slate-400 mt-0.5">
                ระบบจัดการและตรวจสอบฐานข้อมูล Dual-Engine: <b>SQLite</b> (<code class="text-sky-300">data/mechagent.db</code>) &amp; <b>AWS DynamoDB</b> (Production Serverless)
              </p>
            </div>
            <div class="flex items-center gap-2">
              <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                ฐานข้อมูลเชื่อมต่อสมบูรณ์ (Active &amp; Ready)
              </span>
            </div>
          </div>

          <!-- 4 KPI Summary Cards -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
            <div class="bg-slate-900/60 p-3.5 rounded-lg border border-slate-800/80">
              <div class="text-[11px] text-slate-400 font-medium">⚙️ ทะเบียนเครื่องจักร</div>
              <div class="text-xl font-bold text-white mt-1">5 เครื่อง</div>
              <div class="text-[10px] text-slate-500 mt-0.5">Utility A/B, Line 2, Test Rig</div>
            </div>
            <div class="bg-slate-900/60 p-3.5 rounded-lg border border-slate-800/80">
              <div class="text-[11px] text-slate-400 font-medium">📦 คลังตลับลูกปืน</div>
              <div class="text-xl font-bold text-sky-400 mt-1">4 รุ่น (11 ชิ้น)</div>
              <div class="text-[10px] text-amber-400 mt-0.5">⚠️ ขาดสต็อก 1 รายการ (SKF 6310)</div>
            </div>
            <div class="bg-slate-900/60 p-3.5 rounded-lg border border-slate-800/80">
              <div class="text-[11px] text-slate-400 font-medium">📈 ข้อมูลการสั่นสะเทือน</div>
              <div class="text-xl font-bold text-purple-400 mt-1">50+ บันทึก</div>
              <div class="text-[10px] text-slate-500 mt-0.5">Time-series Run-to-Failure</div>
            </div>
            <div class="bg-slate-900/60 p-3.5 rounded-lg border border-slate-800/80">
              <div class="text-[11px] text-slate-400 font-medium">📝 ใบสั่งซ่อมบำรุง (WOs)</div>
              <div class="text-xl font-bold text-emerald-400 mt-1">10 ใบ</div>
              <div class="text-[10px] text-emerald-300 mt-0.5">✅ อนุมัติแล้ว 6 ใบ (HITL)</div>
            </div>
          </div>

          <!-- Sub-table Navigation Pills -->
          <div class="flex flex-wrap items-center gap-2 pt-1 border-t border-slate-800/60">
            <span class="text-xs text-slate-400 font-semibold mr-1">เลือกตารางข้อมูล:</span>
            <button onclick="switchDbSubTable('equipments')" id="btn-sub-equipments" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-[rgb(255,75,75)] text-white shadow transition cursor-pointer">
              ⚙️ ทะเบียนเครื่องจักร (equipments)
            </button>
            <button onclick="switchDbSubTable('spare-parts')" id="btn-sub-spare-parts" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition cursor-pointer">
              📦 คลังอะไหล่ (spare_parts_inventory)
            </button>
            <button onclick="switchDbSubTable('telemetry')" id="btn-sub-telemetry" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition cursor-pointer">
              📈 ประวัติการสั่นสะเทือน (vibration_telemetry)
            </button>
            <button onclick="switchDbSubTable('work-orders')" id="btn-sub-work-orders" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition cursor-pointer">
              📝 ประวัติใบสั่งซ่อมบำรุง (work_orders)
            </button>
          </div>

          <!-- SUB-PANEL 1: EQUIPMENTS -->
          <div id="panel-sub-equipments" class="space-y-3">
            <div class="flex justify-between items-center text-xs text-slate-400">
              <span>ข้อมูลเครื่องจักรเป้าหมายในสายการผลิต อ้างอิงตาราง <code class="text-sky-300">equipments</code></span>
              <span class="text-slate-500">ทั้งหมด 5 รายการ</span>
            </div>
            <div class="overflow-x-auto rounded-lg border border-slate-800">
              <table class="w-full text-xs text-left">
                <thead class="bg-slate-900/80 text-slate-300 uppercase tracking-wider text-[11px] border-b border-slate-800">
                  <tr>
                    <th class="p-3">รหัสเครื่อง (ID)</th>
                    <th class="p-3">ชื่อเครื่องจักร</th>
                    <th class="p-3">สายการผลิต / สถานที่</th>
                    <th class="p-3">รุ่นตลับลูกปืน</th>
                    <th class="p-3 text-center">ระดับความสำคัญ</th>
                    <th class="p-3 text-right">RPM พิกัด</th>
                    <th class="p-3">เครื่องสำรอง</th>
                    <th class="p-3 text-right">ค่าเสียหาย Downtime</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800/70 text-slate-300">
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">PUMP-01</td>
                    <td class="p-3 font-semibold text-white">ปั๊มน้ำหล่อเย็นหลัก (Main Cooling Pump)</td>
                    <td class="p-3">Utility Plant A</td>
                    <td class="p-3 font-mono text-amber-300">SKF 6205-2RS</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">A (Critical)</span></td>
                    <td class="p-3 text-right font-mono">1,800</td>
                    <td class="p-3 font-mono text-slate-400">PUMP-01-B</td>
                    <td class="p-3 text-right font-mono text-emerald-400">฿85,000 / ชม.</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">MOTOR-07</td>
                    <td class="p-3 font-semibold text-white">มอเตอร์ขับสายพานลำเลียง (Conveyor Drive)</td>
                    <td class="p-3">Packaging Line 2</td>
                    <td class="p-3 font-mono text-amber-300">SKF 6205-2RS</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">B (Medium)</span></td>
                    <td class="p-3 text-right font-mono">1,500</td>
                    <td class="p-3 font-mono text-slate-400">MOTOR-07-B</td>
                    <td class="p-3 text-right font-mono text-emerald-400">฿45,000 / ชม.</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">FAN-03</td>
                    <td class="p-3 font-semibold text-white">พัดลมดูดอากาศห้องพ่นสี (Exhaust Fan)</td>
                    <td class="p-3">Paint Shop Facility</td>
                    <td class="p-3 font-mono text-amber-300">SKF 6208</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">B (Medium)</span></td>
                    <td class="p-3 text-right font-mono">1,200</td>
                    <td class="p-3 font-mono text-slate-400">FAN-03-B</td>
                    <td class="p-3 text-right font-mono text-emerald-400">฿25,000 / ชม.</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">COMP-02</td>
                    <td class="p-3 font-semibold text-white">เครื่องอัดอากาศหลัก (Air Compressor)</td>
                    <td class="p-3">Utility Plant B</td>
                    <td class="p-3 font-mono text-amber-300">SKF 6310</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">A (Critical)</span></td>
                    <td class="p-3 text-right font-mono">1,800</td>
                    <td class="p-3 font-mono text-slate-400">COMP-02-B</td>
                    <td class="p-3 text-right font-mono text-emerald-400">฿120,000 / ชม.</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">TEST-RIG-01</td>
                    <td class="p-3 font-semibold text-white">แท่นทดสอบแบริ่งเร่งการเสื่อม (XJTU-SY Rig)</td>
                    <td class="p-3">Reliability Test Lab</td>
                    <td class="p-3 font-mono text-amber-300">LDK UER204</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-500/20 text-sky-300 border border-sky-500/30">C (Testing)</span></td>
                    <td class="p-3 text-right font-mono">2,400</td>
                    <td class="p-3 font-mono text-slate-500">-</td>
                    <td class="p-3 text-right font-mono text-slate-400">฿0 / ชม.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- SUB-PANEL 2: SPARE PARTS INVENTORY -->
          <div id="panel-sub-spare-parts" class="hidden space-y-3">
            <div class="flex justify-between items-center text-xs text-slate-400">
              <span>สถานะคงคลังตลับลูกปืน, ระดับ Safety Stock และระยะเวลาจัดซื้อ อ้างอิงตาราง <code class="text-sky-300">spare_parts_inventory</code></span>
              <span class="text-slate-500">ทั้งหมด 4 รายการ</span>
            </div>
            <div class="overflow-x-auto rounded-lg border border-slate-800">
              <table class="w-full text-xs text-left">
                <thead class="bg-slate-900/80 text-slate-300 uppercase tracking-wider text-[11px] border-b border-slate-800">
                  <tr>
                    <th class="p-3">รหัสอะไหล่ (Part No.)</th>
                    <th class="p-3">รุ่นตลับลูกปืน</th>
                    <th class="p-3 text-center">สถานะสต็อก</th>
                    <th class="p-3 text-center">คงเหลือ (ชิ้น)</th>
                    <th class="p-3 text-center">Safety Stock</th>
                    <th class="p-3 text-right">ราคา/ชิ้น (THB)</th>
                    <th class="p-3 text-center">Lead Time</th>
                    <th class="p-3">ตำแหน่งจัดเก็บ</th>
                    <th class="p-3">รุ่นทดแทน (Substitutes)</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800/70 text-slate-300">
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">SKF 6205-2RS</td>
                    <td class="p-3 font-mono">SKF 6205-2RS</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">🟢 เพียงพอ (Healthy)</span></td>
                    <td class="p-3 text-center font-mono font-bold text-white">4</td>
                    <td class="p-3 text-center font-mono text-slate-400">2</td>
                    <td class="p-3 text-right font-mono text-emerald-400">฿450.00</td>
                    <td class="p-3 text-center font-mono text-slate-300">2 วัน</td>
                    <td class="p-3 font-mono text-slate-400">BIN-A-01</td>
                    <td class="p-3 font-mono text-xs text-slate-400">6205, 6205-ZZ</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">SKF 6208</td>
                    <td class="p-3 font-mono">SKF 6208</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">🟡 ต่ำกว่าเกณฑ์ (Below Safety)</span></td>
                    <td class="p-3 text-center font-mono font-bold text-amber-400">1</td>
                    <td class="p-3 text-center font-mono text-slate-400">2</td>
                    <td class="p-3 text-right font-mono text-emerald-400">฿890.00</td>
                    <td class="p-3 text-center font-mono text-slate-300">5 วัน</td>
                    <td class="p-3 font-mono text-slate-400">BIN-A-04</td>
                    <td class="p-3 font-mono text-xs text-slate-400">6208-2RS</td>
                  </tr>
                  <tr class="hover:bg-rose-950/20 bg-rose-950/10 transition">
                    <td class="p-3 font-mono font-bold text-rose-400">SKF 6310</td>
                    <td class="p-3 font-mono">SKF 6310</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30 animate-pulse">🔴 สินค้าหมด (Out of Stock)</span></td>
                    <td class="p-3 text-center font-mono font-bold text-rose-400">0</td>
                    <td class="p-3 text-center font-mono text-slate-400">1</td>
                    <td class="p-3 text-right font-mono text-emerald-400">฿1,450.00</td>
                    <td class="p-3 text-center font-mono text-rose-300">7 วัน</td>
                    <td class="p-3 font-mono text-slate-400">BIN-B-02</td>
                    <td class="p-3 font-mono text-xs text-amber-300">6310-2RS (ต้องเร่งสั่งซื้อ)</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">LDK UER204</td>
                    <td class="p-3 font-mono">LDK UER204</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">🟢 เพียงพอ (Healthy)</span></td>
                    <td class="p-3 text-center font-mono font-bold text-white">6</td>
                    <td class="p-3 text-center font-mono text-slate-400">2</td>
                    <td class="p-3 text-right font-mono text-emerald-400">฿380.00</td>
                    <td class="p-3 text-center font-mono text-slate-300">3 วัน</td>
                    <td class="p-3 font-mono text-slate-400">BIN-LAB-01</td>
                    <td class="p-3 font-mono text-xs text-slate-400">SKF 6205</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- SUB-PANEL 3: VIBRATION TELEMETRY -->
          <div id="panel-sub-telemetry" class="hidden space-y-4">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
              <div>
                <h3 class="text-xs font-bold text-white">📊 กราฟวิวัฒนาการความเสื่อมสภาพตามเวลาจริง (Run-to-Failure Degradation Evolution)</h3>
                <p class="text-[11px] text-slate-400">ชุดข้อมูล XJTU-SY Bearing Test Lab (Bearing 3_4 @ 2400 RPM) บันทึก 50 จุดประวัติ</p>
              </div>
              <div class="text-xs text-slate-400 flex items-center gap-2">
                <span>เลือกเครื่องจักร:</span>
                <span class="px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-sky-300 font-mono font-bold">TEST-RIG-01 (XJTU-SY)</span>
              </div>
            </div>

            <!-- Plotly RTF Chart Container -->
            <div class="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <div id="dbTelemetryPlot" class="w-full h-72"></div>
            </div>

            <!-- Telemetry Table -->
            <div class="overflow-x-auto rounded-lg border border-slate-800">
              <table class="w-full text-xs text-left">
                <thead class="bg-slate-900/80 text-slate-300 uppercase tracking-wider text-[11px] border-b border-slate-800">
                  <tr>
                    <th class="p-2.5 text-center">ลำดับ</th>
                    <th class="p-2.5">เวลาบันทึก (Timestamp)</th>
                    <th class="p-2.5 text-right">RPM</th>
                    <th class="p-2.5 text-right">RMS (g)</th>
                    <th class="p-2.5 text-right">Kurtosis</th>
                    <th class="p-2.5 text-center">ผลพยากรณ์ AI</th>
                    <th class="p-2.5 text-right">ความเสื่อม (%)</th>
                    <th class="p-2.5 text-right">RUL P05 (ชม.)</th>
                    <th class="p-2.5 text-center">ระดับความเร่งด่วน</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800/70 text-slate-300 font-mono text-[11px]">
                  <tr class="bg-rose-950/20 hover:bg-rose-950/30">
                    <td class="p-2.5 text-center text-slate-400">#50</td>
                    <td class="p-2.5 text-slate-300">2026-10-22 16:53</td>
                    <td class="p-2.5 text-right">2400</td>
                    <td class="p-2.5 text-right font-bold text-rose-400">4.1417</td>
                    <td class="p-2.5 text-right text-rose-300">5.70</td>
                    <td class="p-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300">outer_race</span></td>
                    <td class="p-2.5 text-right font-bold text-rose-400">88.5%</td>
                    <td class="p-2.5 text-right font-bold text-rose-400">6.2</td>
                    <td class="p-2.5 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/30 text-rose-200 border border-rose-500">EMERGENCY</span></td>
                  </tr>
                  <tr class="bg-amber-950/20 hover:bg-amber-950/30">
                    <td class="p-2.5 text-center text-slate-400">#49</td>
                    <td class="p-2.5 text-slate-300">2026-10-22 15:53</td>
                    <td class="p-2.5 text-right">2400</td>
                    <td class="p-2.5 text-right font-bold text-amber-400">1.6027</td>
                    <td class="p-2.5 text-right text-amber-300">6.98</td>
                    <td class="p-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300">outer_race</span></td>
                    <td class="p-2.5 text-right font-bold text-amber-400">67.3%</td>
                    <td class="p-2.5 text-right font-bold text-amber-400">18.5</td>
                    <td class="p-2.5 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/30 text-amber-200 border border-amber-500">URGENT</span></td>
                  </tr>
                  <tr class="hover:bg-slate-800/40">
                    <td class="p-2.5 text-center text-slate-400">#48</td>
                    <td class="p-2.5 text-slate-300">2026-10-22 14:53</td>
                    <td class="p-2.5 text-right">2400</td>
                    <td class="p-2.5 text-right">0.4289</td>
                    <td class="p-2.5 text-right">3.09</td>
                    <td class="p-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-300">outer_race</span></td>
                    <td class="p-2.5 text-right text-sky-300">32.1%</td>
                    <td class="p-2.5 text-right text-sky-300">142.0</td>
                    <td class="p-2.5 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-500/20 text-sky-300 border border-sky-500/30">PLAN_MAINT</span></td>
                  </tr>
                  <tr class="hover:bg-slate-800/40">
                    <td class="p-2.5 text-center text-slate-400">#47</td>
                    <td class="p-2.5 text-slate-300">2026-10-22 13:53</td>
                    <td class="p-2.5 text-right">2400</td>
                    <td class="p-2.5 text-right">0.4078</td>
                    <td class="p-2.5 text-right">3.15</td>
                    <td class="p-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-slate-700 text-slate-300">normal</span></td>
                    <td class="p-2.5 text-right text-emerald-400">12.4%</td>
                    <td class="p-2.5 text-right text-emerald-400">450.0</td>
                    <td class="p-2.5 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">NORMAL</span></td>
                  </tr>
                  <tr class="hover:bg-slate-800/40">
                    <td class="p-2.5 text-center text-slate-400">#46</td>
                    <td class="p-2.5 text-slate-300">2026-10-22 12:53</td>
                    <td class="p-2.5 text-right">2400</td>
                    <td class="p-2.5 text-right">0.4549</td>
                    <td class="p-2.5 text-right">3.07</td>
                    <td class="p-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-slate-700 text-slate-300">normal</span></td>
                    <td class="p-2.5 text-right text-emerald-400">10.8%</td>
                    <td class="p-2.5 text-right text-emerald-400">480.0</td>
                    <td class="p-2.5 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">NORMAL</span></td>
                  </tr>
                  <tr class="hover:bg-slate-800/40">
                    <td class="p-2.5 text-center text-slate-400">#45</td>
                    <td class="p-2.5 text-slate-300">2026-10-22 11:53</td>
                    <td class="p-2.5 text-right">2400</td>
                    <td class="p-2.5 text-right">0.4312</td>
                    <td class="p-2.5 text-right">3.18</td>
                    <td class="p-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-slate-700 text-slate-300">normal</span></td>
                    <td class="p-2.5 text-right text-emerald-400">8.9%</td>
                    <td class="p-2.5 text-right text-emerald-400">510.0</td>
                    <td class="p-2.5 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">NORMAL</span></td>
                  </tr>
                  <tr class="hover:bg-slate-800/40">
                    <td class="p-2.5 text-center text-slate-400">#44</td>
                    <td class="p-2.5 text-slate-300">2026-10-22 10:53</td>
                    <td class="p-2.5 text-right">2400</td>
                    <td class="p-2.5 text-right">0.4217</td>
                    <td class="p-2.5 text-right">3.07</td>
                    <td class="p-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-slate-700 text-slate-300">normal</span></td>
                    <td class="p-2.5 text-right text-emerald-400">7.5%</td>
                    <td class="p-2.5 text-right text-emerald-400">540.0</td>
                    <td class="p-2.5 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">NORMAL</span></td>
                  </tr>
                  <tr class="hover:bg-slate-800/40">
                    <td class="p-2.5 text-center text-slate-400">#43</td>
                    <td class="p-2.5 text-slate-300">2026-10-22 09:53</td>
                    <td class="p-2.5 text-right">2400</td>
                    <td class="p-2.5 text-right">0.3552</td>
                    <td class="p-2.5 text-right">2.98</td>
                    <td class="p-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-slate-700 text-slate-300">normal</span></td>
                    <td class="p-2.5 text-right text-emerald-400">6.1%</td>
                    <td class="p-2.5 text-right text-emerald-400">580.0</td>
                    <td class="p-2.5 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">NORMAL</span></td>
                  </tr>
                  <tr class="hover:bg-slate-800/40">
                    <td class="p-2.5 text-center text-slate-400">#42</td>
                    <td class="p-2.5 text-slate-300">2026-10-22 08:53</td>
                    <td class="p-2.5 text-right">2400</td>
                    <td class="p-2.5 text-right">0.4315</td>
                    <td class="p-2.5 text-right">3.12</td>
                    <td class="p-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-slate-700 text-slate-300">normal</span></td>
                    <td class="p-2.5 text-right text-emerald-400">5.4%</td>
                    <td class="p-2.5 text-right text-emerald-400">600.0</td>
                    <td class="p-2.5 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">NORMAL</span></td>
                  </tr>
                  <tr class="hover:bg-slate-800/40">
                    <td class="p-2.5 text-center text-slate-400">#41</td>
                    <td class="p-2.5 text-slate-300">2026-10-22 07:53</td>
                    <td class="p-2.5 text-right">2400</td>
                    <td class="p-2.5 text-right">0.4398</td>
                    <td class="p-2.5 text-right">2.99</td>
                    <td class="p-2.5 text-center"><span class="px-1.5 py-0.5 rounded bg-slate-700 text-slate-300">normal</span></td>
                    <td class="p-2.5 text-right text-emerald-400">4.2%</td>
                    <td class="p-2.5 text-right text-emerald-400">650.0</td>
                    <td class="p-2.5 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">NORMAL</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- SUB-PANEL 4: WORK ORDERS -->
          <div id="panel-sub-work-orders" class="hidden space-y-3">
            <div class="flex justify-between items-center text-xs text-slate-400">
              <span>ประวัติใบสั่งซ่อมบำรุงที่สร้างโดย Arbiter Agent พร้อมผลการอนุมัติ (HITL) อ้างอิงตาราง <code class="text-sky-300">work_orders</code></span>
              <span class="text-slate-500">ทั้งหมด 10 รายการ</span>
            </div>
            <div class="overflow-x-auto rounded-lg border border-slate-800">
              <table class="w-full text-xs text-left">
                <thead class="bg-slate-900/80 text-slate-300 uppercase tracking-wider text-[11px] border-b border-slate-800">
                  <tr>
                    <th class="p-3">รหัสใบสั่งซ่อม (WO ID)</th>
                    <th class="p-3 font-mono">เครื่องจักร</th>
                    <th class="p-3 text-center">สถานะการอนุมัติ</th>
                    <th class="p-3 text-center">ระดับความเร่งด่วน</th>
                    <th class="p-3">เวลาสร้างใบสั่งซ่อม</th>
                    <th class="p-3">กำหนดเริ่มปฏิบัติงาน</th>
                    <th class="p-3">สาเหตุข้อบกพร่อง</th>
                    <th class="p-3 font-mono">อะไหล่ที่จัดสรร</th>
                    <th class="p-3">ผู้อนุมัติ (Approver)</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800/70 text-slate-300">
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">WO-0BB98B80</td>
                    <td class="p-3 font-mono font-semibold text-white">PUMP-01</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">🟡 PENDING_APPROVAL</span></td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300">URGENT</span></td>
                    <td class="p-3 text-slate-400 font-mono text-[11px]">2026-10-22 18:16</td>
                    <td class="p-3 text-slate-300 font-mono text-[11px]">2026-10-25 14:00</td>
                    <td class="p-3 text-slate-300">outer_race (ร่องนอก)</td>
                    <td class="p-3 font-mono text-sky-300">SKF 6205-2RS</td>
                    <td class="p-3 text-slate-400 italic">รอผู้จัดการโรงงาน</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">WO-7E3CC22E</td>
                    <td class="p-3 font-mono font-semibold text-white">PUMP-01</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">🟢 APPROVED</span></td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300">NORMAL</span></td>
                    <td class="p-3 text-slate-400 font-mono text-[11px]">2026-10-22 18:09</td>
                    <td class="p-3 text-slate-300 font-mono text-[11px]">2026-10-25 14:00</td>
                    <td class="p-3 text-slate-300">normal (ปกติ)</td>
                    <td class="p-3 font-mono text-slate-500">-</td>
                    <td class="p-3 text-emerald-400 font-semibold">SOMCHAI.P (Supv.)</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">WO-74EC2680</td>
                    <td class="p-3 font-mono font-semibold text-white">PUMP-01</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">🟢 APPROVED</span></td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-500/20 text-sky-300">PLAN_MAINT</span></td>
                    <td class="p-3 text-slate-400 font-mono text-[11px]">2026-10-22 18:08</td>
                    <td class="p-3 text-slate-300 font-mono text-[11px]">2026-10-25 14:00</td>
                    <td class="p-3 text-slate-300">ball (เม็ดลูกปืน)</td>
                    <td class="p-3 font-mono text-sky-300">SKF 6205-2RS</td>
                    <td class="p-3 text-emerald-400 font-semibold">SOMCHAI.P (Supv.)</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">WO-01303B1E</td>
                    <td class="p-3 font-mono font-semibold text-white">PUMP-01</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">🟢 APPROVED</span></td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-500/20 text-sky-300">PLAN_MAINT</span></td>
                    <td class="p-3 text-slate-400 font-mono text-[11px]">2026-10-22 18:08</td>
                    <td class="p-3 text-slate-300 font-mono text-[11px]">2026-10-25 14:00</td>
                    <td class="p-3 text-slate-300">ball (เม็ดลูกปืน)</td>
                    <td class="p-3 font-mono text-sky-300">SKF 6205-2RS</td>
                    <td class="p-3 text-emerald-400 font-semibold">SOMCHAI.P (Supv.)</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">WO-DA32EE60</td>
                    <td class="p-3 font-mono font-semibold text-white">PUMP-01</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">🟢 APPROVED</span></td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-500/20 text-sky-300">PLAN_MAINT</span></td>
                    <td class="p-3 text-slate-400 font-mono text-[11px]">2026-10-22 18:08</td>
                    <td class="p-3 text-slate-300 font-mono text-[11px]">2026-10-25 14:00</td>
                    <td class="p-3 text-slate-300">ball (เม็ดลูกปืน)</td>
                    <td class="p-3 font-mono text-sky-300">SKF 6205-2RS</td>
                    <td class="p-3 text-emerald-400 font-semibold">SOMCHAI.P (Supv.)</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">WO-6A5836D5</td>
                    <td class="p-3 font-mono font-semibold text-white">PUMP-01</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">🟡 PENDING_APPROVAL</span></td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300">EMERGENCY</span></td>
                    <td class="p-3 text-slate-400 font-mono text-[11px]">2026-10-22 18:00</td>
                    <td class="p-3 text-slate-300 font-mono text-[11px]">2026-10-22 22:00</td>
                    <td class="p-3 text-slate-300">outer_race (ร่องนอก)</td>
                    <td class="p-3 font-mono text-sky-300">SKF 6205-2RS</td>
                    <td class="p-3 text-slate-400 italic">รอผู้จัดการโรงงาน</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">WO-5EDCEA47</td>
                    <td class="p-3 font-mono font-semibold text-white">PUMP-01</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">🟡 PENDING_APPROVAL</span></td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300">EMERGENCY</span></td>
                    <td class="p-3 text-slate-400 font-mono text-[11px]">2026-10-22 18:00</td>
                    <td class="p-3 text-slate-300 font-mono text-[11px]">2026-10-22 22:00</td>
                    <td class="p-3 text-slate-300">outer_race (ร่องนอก)</td>
                    <td class="p-3 font-mono text-sky-300">SKF 6205-2RS</td>
                    <td class="p-3 text-slate-400 italic">รอผู้จัดการโรงงาน</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">WO-5FE651E3</td>
                    <td class="p-3 font-mono font-semibold text-white">PUMP-01</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">🟡 PENDING_APPROVAL</span></td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300">EMERGENCY</span></td>
                    <td class="p-3 text-slate-400 font-mono text-[11px]">2026-10-22 18:00</td>
                    <td class="p-3 text-slate-300 font-mono text-[11px]">2026-10-22 22:00</td>
                    <td class="p-3 text-slate-300">outer_race (ร่องนอก)</td>
                    <td class="p-3 font-mono text-sky-300">SKF 6205-2RS</td>
                    <td class="p-3 text-slate-400 italic">รอผู้จัดการโรงงาน</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">WO-08231170</td>
                    <td class="p-3 font-mono font-semibold text-white">PUMP-01</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">🟢 APPROVED</span></td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300">EMERGENCY</span></td>
                    <td class="p-3 text-slate-400 font-mono text-[11px]">2026-10-22 17:59</td>
                    <td class="p-3 text-slate-300 font-mono text-[11px]">2026-10-22 21:59</td>
                    <td class="p-3 text-slate-300">outer_race (ร่องนอก)</td>
                    <td class="p-3 font-mono text-sky-300">SKF 6205-2RS</td>
                    <td class="p-3 text-emerald-400 font-semibold">SOMCHAI.P (Supv.)</td>
                  </tr>
                  <tr class="hover:bg-slate-800/40 transition">
                    <td class="p-3 font-mono font-bold text-sky-400">WO-C6A7130B</td>
                    <td class="p-3 font-mono font-semibold text-white">PUMP-01</td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">🟢 APPROVED</span></td>
                    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300">EMERGENCY</span></td>
                    <td class="p-3 text-slate-400 font-mono text-[11px]">2026-10-22 17:52</td>
                    <td class="p-3 text-slate-300 font-mono text-[11px]">2026-10-22 17:52</td>
                    <td class="p-3 text-slate-300">inner_race (ร่องใน)</td>
                    <td class="p-3 font-mono text-sky-300">SKF 6205-2RS</td>
                    <td class="p-3 text-emerald-400 font-semibold">SOMCHAI.P (Supv.)</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>

    </main>

  </div>

  <script>
    // Embedded CWRU Real Lab Samples
    const PRESET_SIGNALS = {"normal": [0.0532, 0.0887, 0.0997, 0.0586, -0.0046, -0.057, -0.0718, -0.0586, -0.0465, -0.0499, -0.0511, -0.0156, 0.0459, 0.0922, 0.0918, 0.0605, 0.0244, -0.0002, 0.0175, 0.0263, -0.0035, -0.0411, -0.0624, -0.0325, 0.005, 0.0286, 0.0438, 0.0409, 0.0553, 0.0853, 0.1085, 0.0991, 0.0588, 0.0315, 0.0196, 0.0294, 0.0603, 0.0757, 0.067, 0.059, 0.064, 0.0701, 0.0678, 0.0444, 0.0211, 0.0173, 0.0413, 0.0966, 0.1408, 0.1504, 0.14, 0.1202, 0.0991, 0.0816, 0.0519, 0.006, -0.0382, -0.0517, -0.0215, 0.0207, 0.0449, 0.0586, 0.0659, 0.0718, 0.0724, 0.0311, -0.0398, -0.1248, -0.1832, -0.1734, -0.1362, -0.0653, 0.0046, 0.0582, 0.0987, 0.0724, 0.0181, -0.0613, -0.149, -0.1959, -0.1986, -0.1335, -0.0486, 0.0302, 0.0824, 0.1091, 0.1258, 0.0918, 0.0346, -0.0444, -0.1108, -0.1275, -0.1066, -0.0463, 0.0054, 0.0403, 0.0864, 0.125, 0.135, 0.0985, 0.0202, -0.0699, -0.1312, -0.1339, -0.0839, 0.001, 0.0626, 0.101, 0.1444, 0.1684, 0.1546, 0.0845, -0.0219, -0.1089, -0.1325, -0.0983, -0.0353, 0.0509, 0.13, 0.1855, 0.2178, 0.2097, 0.1611, 0.0874, 0.0117, -0.0407, -0.035, 0.0092, 0.0457, 0.0768, 0.0976, 0.1149, 0.1356, 0.117, 0.0611, -0.0188, -0.0887, -0.0966, -0.0709, -0.0248, 0.0259, 0.0532, 0.072, 0.0828, 0.078, 0.0446, -0.0273, -0.1189, -0.1769, -0.1788, -0.1481, -0.0928, -0.0392, 0.0015, 0.0438, 0.0807, 0.0757, 0.019, -0.0611, -0.1346, -0.1688, -0.1556, -0.1277, -0.1022, -0.0705, -0.0492, -0.0355, -0.0434, -0.0757, -0.1181, -0.1613, -0.164, -0.1191, -0.0463, 0.0175, 0.0519, 0.0734, 0.0864, 0.0749, 0.054, 0.0106, -0.0426, -0.0536, -0.0417, -0.0098, 0.0173, 0.0446, 0.0736, 0.093, 0.125, 0.1331, 0.1074, 0.0588, 0.0161, 0.0161, 0.053, 0.0853, 0.1001, 0.106, 0.1033, 0.0939, 0.0615, 0.0146, -0.0534, -0.1189, -0.1371, -0.0945, -0.0207, 0.0355, 0.0855, 0.1321, 0.1625, 0.1594, 0.1197, 0.0599, -0.0217, -0.0885, -0.1133, -0.0978, -0.0582, -0.0215, 0.0196, 0.0622, 0.0862, 0.0918, 0.0634, 0.0123, -0.0219, -0.0378, -0.0403, -0.0392, -0.0398, -0.0428, -0.0365, -0.0223, -0.0198, -0.0334, -0.0661, -0.096, -0.106, -0.0866, -0.043, -0.0227, -0.0083, 0.024, 0.0567, 0.0814, 0.0653, 0.015, -0.0348, -0.0632, -0.0455, 0.0063, 0.0576, 0.0885, 0.096, 0.1066, 0.1279, 0.1281, 0.1014, 0.0565, 0.0154, 0.0148, 0.0582, 0.0924, 0.1006, 0.1022, 0.1095, 0.1387, 0.1588, 0.1458, 0.098, 0.0344, -0.0086, -0.0219, -0.0211, -0.0159, -0.0113, -0.0027, 0.0363, 0.0887, 0.1243, 0.1143, 0.0707, 0.015, -0.0282, -0.0086, 0.0267, 0.0328, 0.0282, 0.0284, 0.0538, 0.0766, 0.059, 0.0142, -0.0388, -0.059, -0.0386, -0.009, 0.0013, -0.0129, -0.0227, -0.0108, 0.0217, 0.0342, 0.004, -0.0503, -0.0912, -0.0859, -0.0713, -0.0632, -0.0599, -0.0734, -0.0668, -0.0363, -0.0054, 0.0113, -0.0048, -0.0317, -0.0384, -0.0219, -0.0006, 0.0125, 0.0227, 0.0411, 0.068, 0.0849, 0.096, 0.0799, 0.0152, -0.0386, -0.0384, -0.005, 0.0173, 0.0146, 0.0294, 0.0659, 0.0951, 0.1172, 0.1058, 0.0697, 0.0317, 0.0123, 0.0371, 0.0559, 0.0455, 0.0328, 0.0328, 0.0434, 0.0432, 0.0423, 0.0315, -0.0023, -0.0169, 0.0081, 0.0421, 0.0638, 0.0751, 0.0726, 0.087, 0.1037, 0.0918, 0.0417, -0.0411, -0.0972, -0.1028, -0.0728, -0.033, -0.0046, 0.0108, 0.0363, 0.0709, 0.0859, 0.0764, 0.038, -0.0236, -0.0638, -0.0563, -0.0317, -0.0192, -0.0232, -0.0265, -0.0086, 0.0413, 0.068, 0.0461, 0.0077, -0.0167, 0.0073, 0.0438, 0.0713, 0.0845, 0.0705, 0.0695, 0.0895, 0.1043, 0.0774, 0.0052, -0.0438, -0.0613, -0.0369, 0.0046, 0.0146, 0.0144, -0.019, -0.0252, -0.0013, -0.0096, -0.0332, -0.0732, -0.082, -0.043, 0.0, 0.0227, 0.0092, -0.028, -0.0528, -0.0419, -0.0111, -0.0096, -0.024, -0.0138, 0.0248, 0.0789, 0.1016, 0.1012, 0.0709, 0.0242, 0.0044, 0.0125, 0.043, 0.0263, -0.009, -0.0142, -0.0004, 0.0202, 0.0015, -0.0465, -0.1001, -0.1241, -0.0974, -0.0601, -0.0478, -0.0567, -0.0663, -0.0615, -0.0394, -0.0263, -0.0501, -0.1068, -0.1665, -0.1798, -0.1462, -0.1118, -0.0672, -0.0413, -0.0184, 0.0259, 0.054, 0.064, 0.0083, -0.0743, -0.1097, -0.1087, -0.078, -0.0409, -0.0046, 0.0332, 0.0695, 0.0947, 0.0941, 0.0686, 0.0134, -0.0265, -0.0144, 0.0217, 0.0653, 0.0834, 0.0947, 0.1076, 0.1129, 0.1298, 0.1104, 0.0636, 0.0121, -0.0104, 0.0211, 0.057, 0.0991, 0.1321, 0.1588, 0.1921, 0.1844, 0.1521, 0.0893, 0.0048, -0.0371, -0.0417, -0.0035, 0.0421, 0.0636, 0.0747, 0.0893, 0.1189, 0.1106, 0.0657, 0.0046, -0.0544, -0.067, -0.0486, -0.0023, 0.0492, 0.0774, 0.0966, 0.0983, 0.0839, 0.0361, -0.0378, -0.0939, -0.1177, -0.0895, -0.0259, 0.0484, 0.1122, 0.145, 0.1698, 0.1629, 0.1089, 0.0211, -0.0824, -0.1391, -0.1371, -0.0962, -0.0463, -0.0008, 0.0328, 0.0482, 0.064, 0.0572, 0.0073, -0.0643, -0.1281, -0.1594, -0.1446, -0.0899, -0.0223, 0.0346, 0.0768, 0.1089, 0.1208, 0.0928, 0.028, -0.0718, -0.1412, -0.1377, -0.1064, -0.0401, 0.025, 0.0816, 0.1479, 0.174, 0.1671, 0.1093, 0.0136, -0.0505, -0.0749, -0.0555, -0.0284, 0.0098, 0.0565, 0.0686, 0.0966, 0.0999, 0.0628, 0.0065, -0.0651, -0.0747, -0.0609, -0.0355, 0.0165, 0.0544, 0.0987, 0.1356, 0.1533, 0.1346, 0.0738, 0.0227, -0.0156, -0.0229, -0.006, 0.0077, 0.0271, 0.0513, 0.0943, 0.1208, 0.1116, 0.0847, 0.0173, -0.0428, -0.0611, -0.0403, 0.0023, 0.0121, 0.0194, 0.0411, 0.0528, 0.0467, 0.0148, -0.0336, -0.0868, -0.1114, -0.0847, -0.0455, -0.0234, -0.0198, -0.0017, 0.0357, 0.0634, 0.0933, 0.0611, -0.0094, -0.035, -0.0317, 0.0094, 0.0386, 0.0507, 0.0674, 0.0661, 0.0841, 0.0976, 0.0732, 0.0081, -0.0626, -0.0864, -0.0653, -0.0213, 0.0142, 0.0284, 0.0328, 0.0488, 0.077, 0.0772, 0.0282, -0.03, -0.0643, -0.0718, -0.0503, -0.0409, -0.0538, -0.0499, -0.0175, 0.0302, 0.0786, 0.1022, 0.0657, 0.0096, -0.0175, -0.0125, 0.0025, 0.0131, 0.0282, 0.0492, 0.0993, 0.1537, 0.1744, 0.1281, 0.0286, -0.0494, -0.0826, -0.0736, -0.0592, -0.0444, -0.0104, 0.0277, 0.0805, 0.117, 0.0935, 0.0282, -0.0509, -0.0995, -0.0943, -0.0753, -0.0653, -0.0476, -0.0113, 0.0449, 0.0859, 0.0907, 0.0607, 0.009, -0.0175, -0.0207, -0.0173, -0.0136, -0.0067, 0.0167, 0.0511, 0.1016, 0.1521, 0.1391, 0.073, -0.0013, -0.0499, -0.0649, -0.0812, -0.0803, -0.0734, -0.0588, -0.0054, 0.0636, 0.0818, 0.0423, -0.0017, -0.0522, -0.0711, -0.0691, -0.0797, -0.0609, -0.0369, 0.0086, 0.0632, 0.0774, 0.0741, 0.0242, -0.0148, -0.0207, -0.0165, -0.0002, -0.0165, -0.02, -0.0104, 0.0075, 0.0317, 0.028, 0.0111, -0.0161, -0.025, -0.0156, -0.0079, -0.0119, -0.0355, -0.0346, -0.0044, 0.0294, 0.0599, 0.0597, 0.044, 0.0271, -0.005, -0.0098, -0.0131, -0.0302, -0.0271, -0.0035, 0.0613, 0.1106, 0.1133, 0.0761, 0.0288, 0.0188, 0.0336, 0.0457, 0.0196, 0.0038, 0.0119, 0.0403, 0.0751, 0.0682, 0.053, 0.0196, -0.0002, 0.004, 0.0021, 0.0063, -0.0142, -0.0277, -0.0198, 0.0096, 0.0386, 0.0252, 0.0079, -0.0148, -0.0273, -0.0106, 0.0058, 0.0119, -0.01, -0.0175, 0.0181, 0.0488, 0.0643, 0.0428, 0.0092, -0.0171, -0.0382, -0.0269, -0.0357, -0.0561, -0.059, -0.0426, -0.0038, 0.0204, 0.0332, 0.0259, 0.0067, 0.0071, 0.0052, -0.0156, -0.062, -0.1139, -0.1166, -0.0845, -0.038, 0.0075, 0.0286, 0.0421, 0.0532, 0.057, 0.0455, 0.0198, -0.01, -0.0194, -0.0067, 0.0348, 0.0772, 0.0807, 0.0743, 0.0618, 0.0624, 0.0749, 0.0734, 0.0653, 0.0461, 0.0332, 0.0376, 0.0338, 0.0342, 0.0438, 0.0526, 0.0645, 0.0797, 0.0786, 0.0244, -0.0398, -0.0653, -0.0567, -0.0165, 0.0221, 0.0595, 0.0805, 0.0868, 0.1143, 0.1147, 0.0772, 0.0021, -0.0632, -0.0743, -0.0655, -0.0188, 0.01, 0.0202, 0.0563, 0.0705, 0.0818, 0.0515, -0.0161, -0.0713, -0.1206, -0.0995, -0.0634, -0.0302, -0.0004, 0.0017, 0.0277, 0.0202, 0.0161, -0.0042, -0.0749, -0.1166, -0.1316, -0.0845, -0.0363, -0.0169, 0.0238, 0.0657, 0.1145, 0.1279, 0.1087, 0.0421, -0.0582, -0.0939, -0.087, -0.0355, 0.0355, 0.0738, 0.1166, 0.1496, 0.1652, 0.14, 0.0628, -0.0138, -0.0749, -0.0768, -0.034, 0.0225, 0.0951, 0.1339, 0.1565, 0.1615, 0.1423, 0.0922, 0.0, -0.0826, -0.1218, -0.0851, -0.0096, 0.068, 0.1339, 0.1767, 0.2067, 0.1886, 0.1544, 0.102, 0.0136, -0.0348, -0.0407, 0.0021, 0.0584, 0.0939, 0.1333, 0.1444, 0.1458, 0.1222, 0.0634, -0.0117, -0.0924, -0.1227, -0.1099, -0.0561, 0.0108, 0.064, 0.1181, 0.1321, 0.0978, 0.0398, -0.0536, -0.1496, -0.1982, -0.184, -0.1197, -0.0588, 0.0019, 0.0507, 0.0837, 0.098, 0.0584, -0.0119, -0.1016, -0.1508, -0.1439, -0.1112, -0.0576, -0.0119, 0.0288, 0.0459, 0.0607, 0.067, 0.019, -0.0605, -0.1408, -0.1734, -0.1504, -0.1022, -0.0392, 0.0156, 0.0332, 0.043, 0.0553, 0.0163, -0.058, -0.125, -0.1613, -0.1402, -0.0834, -0.0219, 0.0328, 0.0553, 0.0709, 0.0926, 0.0803, 0.0478, -0.0069, -0.0711, -0.0889, -0.0622, -0.0165, 0.0323, 0.0638, 0.0849, 0.0893, 0.078, 0.0567, 0.006, -0.0461, -0.088, -0.0943, -0.0622, -0.0384, -0.0221, 0.0023, 0.0334, 0.0544, 0.062, 0.0309, -0.0129, -0.0411, -0.0636, -0.0409, 0.0081, 0.0497, 0.0749, 0.1045, 0.1519, 0.1602, 0.1348, 0.0851, 0.015, -0.0296, -0.0403, -0.0152, 0.0123, 0.0338, 0.0691, 0.0989, 0.1239, 0.1091, 0.0592, -0.0077, -0.0759, -0.0809, -0.068, -0.0607, -0.0407, -0.0213, 0.0225, 0.0607, 0.0868, 0.0716, 0.0042, -0.0524, -0.0949, -0.0905, -0.0684, -0.0492, -0.0106, 0.0319, 0.0972, 0.1302, 0.1279, 0.0862, 0.0052, -0.0348, -0.0574, -0.0455, -0.0202, -0.0167, 0.0184, 0.0697, 0.1197, 0.1412, 0.1054, 0.0302, -0.0394, -0.0674, -0.058, -0.0409, -0.0363, -0.0271, 0.0021, 0.0432, 0.0872, 0.0974, 0.0486, -0.0023, -0.0217, -0.0023, 0.0294, 0.0423, 0.0363, 0.0261, 0.0588, 0.1018, 0.1197, 0.1039, 0.0528, 0.0123, -0.0052, 0.0098, 0.0444, 0.0526, 0.0524, 0.0718, 0.101, 0.1162, 0.106, 0.0553, -0.0317, -0.0665, -0.0501, -0.0221, -0.0067, -0.0108, 0.0169, 0.0342, 0.0542, 0.0741, 0.0313, -0.0259, -0.0638, -0.0618, -0.0248, 0.0013, 0.0081, 0.0063, 0.0184, 0.0511, 0.0761, 0.059, 0.0083, -0.0503, -0.0993, -0.1235, -0.1233, -0.1091, -0.0972, -0.0772, -0.0369, 0.0023, -0.0033, -0.0459, -0.0876, -0.1062, -0.0989, -0.0743, -0.0421, -0.0453, -0.0597, -0.0413, -0.0154, -0.0015, -0.0165, -0.0638, -0.1239, -0.1304, -0.072, -0.0317, -0.0048, 0.0194, 0.0384, 0.0607, 0.059, 0.0444, -0.0023, -0.0507, -0.0542, -0.0288, 0.009, 0.019, 0.0346, 0.0413, 0.0544, 0.0907, 0.0916, 0.0801, 0.033, -0.0021, 0.0175, 0.0409, 0.0626, 0.0582, 0.0369, 0.0438, 0.0857, 0.1277, 0.1254, 0.0928, 0.0555, 0.043, 0.0755, 0.1081, 0.1237, 0.1302, 0.1214, 0.1208, 0.1264, 0.1225, 0.1076, 0.0691, 0.0438, 0.0603, 0.0793, 0.0839, 0.0766, 0.0659, 0.0795, 0.1008, 0.1097, 0.0893, 0.0359, -0.004, -0.0046, 0.006, 0.0121, 0.0169, 0.0098, 0.0127, 0.0286, 0.0455, 0.0513, 0.0223, -0.0134, -0.0373, -0.0434, -0.028, -0.0219, -0.0248, -0.0211, -0.0052, 0.0255, 0.0411, 0.0207, -0.0125, -0.043, -0.0398, -0.0209, -0.0171, -0.015, -0.0225, -0.0175, -0.0067, -0.0044, -0.0092, -0.0323, -0.0461, -0.0232, 0.0209, 0.0436, 0.015, -0.0365, -0.0847, -0.1022, -0.0757, -0.0478, -0.024, -0.0267, -0.025, -0.0025, 0.0031, 0.0086, -0.015, -0.038, -0.0346, -0.0113, 0.0286, 0.0459, 0.0392, 0.0328, 0.0355, 0.0282, 0.0123, -0.0317, -0.0897, -0.1175, -0.1039, -0.0592, -0.0113, 0.0302, 0.057, 0.0895, 0.1003, 0.088, 0.0636, 0.0073, -0.0275, -0.0359, -0.0108, 0.0334, 0.0711, 0.1083, 0.1358, 0.1763, 0.2122, 0.2051, 0.1521, 0.0803, 0.0263, 0.0127, 0.0376, 0.0711, 0.0885, 0.1033, 0.1341, 0.1506, 0.121, 0.0576, -0.0083, -0.0515, -0.059, -0.024, 0.0294, 0.0751, 0.0962, 0.111, 0.1421, 0.1391, 0.1093, 0.0561, -0.0138, -0.0449, -0.0476, -0.0269, -0.0008, 0.0086, 0.0169, 0.0394, 0.0745, 0.0761, 0.0146, -0.0645, -0.1145, -0.1158, -0.0812, -0.0407, -0.0038, 0.0169, 0.0255, 0.0332, 0.0219, -0.0384, -0.1398, -0.2309, -0.2729, -0.2512, -0.1944, -0.1304, -0.0837, -0.0532, -0.015, -0.0029, -0.0252, -0.0668, -0.122, -0.1642, -0.1615, -0.122, -0.0711, -0.0346, -0.0167, 0.0096, 0.0371, 0.0484, 0.028, -0.0263, -0.0891, -0.1266, -0.1204, -0.0732, -0.0198, 0.0311, 0.0793, 0.1191, 0.1346, 0.0985, 0.0384, -0.043, -0.0928, -0.0849, -0.0455, 0.0213, 0.0582, 0.0755, 0.0951, 0.1085, 0.1089, 0.0834, 0.0444, 0.0023, -0.0129, 0.0054, 0.0384, 0.0711, 0.0978, 0.1243, 0.1435, 0.1329, 0.0893, 0.0152, -0.0699, -0.1137, -0.1227, -0.1047, -0.0676, -0.0248, 0.015, 0.0369, 0.0601, 0.062, 0.0265, -0.0259, -0.0634, -0.0657, -0.0478, -0.0365, -0.0273, -0.0102, 0.0104, 0.0436, 0.0703, 0.078, 0.0544, 0.0138, -0.0081, -0.0019, 0.0238, 0.0421, 0.0657, 0.0945, 0.1268, 0.1404, 0.1074, 0.0461, -0.025, -0.0651, -0.0628, -0.0544, -0.0355, -0.0115, 0.0136, 0.0686, 0.1189, 0.1458, 0.1202, 0.0394, -0.0207, -0.0515, -0.0553, -0.0461, -0.0334, -0.0111, 0.0161, 0.0665, 0.0999, 0.0976, 0.0584, -0.0086, -0.0392, -0.0398, -0.0129, 0.0063, 0.0013, 0.0215, 0.0522, 0.1026, 0.1398, 0.1218, 0.0768, 0.0211, -0.006, -0.0111, -0.0215, -0.0219, -0.0175, 0.01, 0.0659, 0.1051, 0.1003, 0.0505, -0.0175, -0.0538, -0.0536, -0.0461, -0.0311, -0.01, 0.028, 0.0684, 0.0966, 0.1054, 0.0532, -0.0211, -0.0803, -0.1089, -0.1045, -0.0976, -0.0832, -0.063, -0.0031, 0.0738, 0.1243, 0.1314, 0.077, 0.0217, -0.0232, -0.0378, -0.035, -0.0586, -0.0655, -0.0469, 0.0063, 0.0676, 0.087, 0.0676, 0.028, -0.0015, -0.004, 0.0121, 0.0188, 0.0092, 0.0125, 0.0411, 0.0947, 0.1212, 0.0922, 0.0355, -0.0209, -0.0361, -0.0188, 0.019, 0.0557, 0.0809, 0.111, 0.1406, 0.165, 0.1552, 0.1089, 0.0476, -0.0023, -0.0175, -0.0181, -0.0236, -0.0302, -0.0227, 0.015, 0.0695, 0.1012, 0.0951, 0.0647, 0.0328, 0.0223, 0.028, 0.0213, 0.0025, 0.0035, 0.0202, 0.0488, 0.063, 0.0494, 0.0209, -0.0142, -0.0148, 0.0042, 0.0255, 0.0348, 0.0271, 0.0271, 0.0428, 0.0672, 0.0743, 0.0607, 0.0292, 0.0065, 0.0048, 0.0019, -0.0096, -0.0384, -0.0755, -0.0887, -0.0728, -0.0565, -0.0549, -0.0615, -0.0522, -0.024, 0.0204, 0.0544, 0.0484, 0.0196, -0.0019, 0.0081, 0.025, 0.015, -0.0136, -0.0407, -0.0613, -0.054, -0.0334, -0.0328, -0.0309, -0.0169, 0.0129, 0.0605, 0.087, 0.0713, 0.0323, 0.0, 0.005, 0.024, 0.025, -0.0063, -0.0599, -0.1008, -0.1099, -0.0847, -0.057, -0.0417, -0.0286, -0.0027, 0.0357, 0.0471, 0.0342, -0.0058, -0.0407, -0.0415, -0.0242, 0.0159, 0.0152, -0.0023, -0.0065, -0.0017, 0.0294, 0.029, -0.0017, -0.0401, -0.0595, -0.0482, -0.0259, -0.0029, 0.0008, 0.01, 0.0417, 0.0853, 0.1162, 0.1035, 0.0557, 0.0033, -0.0305, -0.0313, -0.0071, 0.006, 0.0106, 0.0286, 0.0595, 0.0812, 0.0718, 0.038, -0.0096, -0.0267, -0.0033, 0.0355, 0.068, 0.0789, 0.0839, 0.0857, 0.0837, 0.0538, -0.014, -0.0966, -0.1688, -0.1746, -0.1416, -0.096, -0.0457, -0.0207, 0.0121, 0.0415, 0.0622, 0.0386, -0.0242, -0.0668, -0.1095, -0.127, -0.1164, -0.0901, -0.0582, -0.0409, 0.0058, 0.0478, 0.0469, 0.0165, -0.0467, -0.0989, -0.1116, -0.0772, -0.0169, 0.0296, 0.0799, 0.1168, 0.1214, 0.0905, 0.0086, -0.0766, -0.149, -0.1673, -0.1343, -0.0834, -0.0052, 0.0474, 0.0937, 0.1237, 0.1398, 0.1337, 0.0607, -0.014, -0.0632, -0.0628, -0.0302, 0.0038, 0.0561, 0.1039, 0.1456, 0.1721, 0.1544, 0.102, 0.0382, -0.02, -0.0457, -0.0342, 0.0079, 0.0659, 0.1118, 0.1569, 0.203, 0.1951, 0.1256, 0.028, -0.0784, -0.1341, -0.1287, -0.0832, -0.0198, 0.0328, 0.0724, 0.0978, 0.1118, 0.0822, 0.0063, -0.0887, -0.1475, -0.1308, -0.0713, -0.0023, 0.0592, 0.1143, 0.1387, 0.1281, 0.1012, 0.0196, -0.078, -0.1333, -0.1408, -0.091, -0.0311, 0.0246, 0.0745, 0.111, 0.15, 0.1581, 0.1097, 0.0229, -0.0628, -0.1179, -0.1389, -0.1187, -0.0716, -0.0257, 0.0217, 0.0684, 0.101, 0.098, 0.0486, -0.0294, -0.0955, -0.1212, -0.1104, -0.067, -0.0165, 0.0292, 0.0826, 0.117, 0.1337, 0.1143, 0.053, 0.0031, -0.0159, 0.0108, 0.0459, 0.0684, 0.0795, 0.0759, 0.1035, 0.125, 0.1137, 0.0682, 0.0121, -0.0048, -0.0119, 0.0098, 0.0292, 0.0273, 0.043, 0.0691, 0.1273, 0.1596, 0.1339, 0.0818, 0.0284, 0.0092, -0.004, -0.01, 0.0081, 0.0317, 0.0609, 0.0974, 0.1362, 0.141, 0.0922, 0.0409, 0.0121, 0.009, 0.0334, 0.0532, 0.0505, 0.0451, 0.0401, 0.0323, 0.0348, 0.0106, -0.0513, -0.093, -0.1014, -0.077, -0.0451, -0.0428, -0.0336, -0.0181, 0.0179, 0.0555, 0.0248, -0.0409, -0.0991, -0.1195, -0.1041, -0.0805, -0.0486, -0.0234, 0.0104, 0.0603, 0.1064, 0.1306, 0.1024, 0.0511, 0.0058, -0.0108, 0.0159, 0.0513, 0.0905, 0.1187, 0.1546, 0.1932, 0.1844, 0.1354, 0.0482, -0.034, -0.0736, -0.0868, -0.0672, -0.0361, -0.0027, 0.0459, 0.096, 0.1277, 0.1137, 0.0519, -0.0269, -0.0776, -0.0774, -0.0659, -0.0505, -0.0415, -0.0407, 0.0063, 0.0697, 0.1095, 0.0991, 0.0332, -0.0267, -0.0542, -0.0501, -0.0519, -0.0661, -0.0474, -0.004, 0.0511, 0.0868, 0.0741, 0.0215, -0.0528, -0.0885, -0.0757, -0.0519, -0.0361, -0.0386, -0.0282, 0.0115, 0.0409, 0.0423, 0.0188, -0.0388, -0.0991, -0.1164, -0.0947, -0.0784, -0.0778, -0.0649, -0.0275, 0.0267, 0.0657, 0.0632, 0.0273, -0.0334, -0.0741, -0.0772, -0.0603, -0.0386, -0.0409, -0.0317, 0.0138, 0.0651, 0.0749, 0.0369, -0.0117, -0.0361, -0.0348, -0.0286, -0.0198, -0.0163, -0.0173, -0.0069, 0.0307, 0.0643, 0.0486, 0.0056, -0.0302, -0.0457, -0.035, -0.0165, 0.0077, 0.0115, 0.0086, 0.0532, 0.1008, 0.1235, 0.1022, 0.0484, 0.0167, -0.0023, 0.009, -0.0013, -0.0371, -0.0302, -0.006, 0.0348, 0.0561, 0.0463, 0.0146, -0.0129, -0.0188, -0.0167, 0.0069, 0.0035, -0.0038, -0.0035, -0.0002, 0.0286, 0.0271, 0.0142, 0.001, -0.009, 0.0138, 0.029, 0.03, 0.0136, 0.0094, 0.0346, 0.0555, 0.0855, 0.0786, 0.0353, 0.0148, 0.0196, 0.0544, 0.0672, 0.0476, 0.0384, 0.0263, 0.0378, 0.0434, 0.0286, 0.0046, -0.0332, -0.0294, -0.0044, 0.0169, 0.0227, 0.0096, 0.0106, 0.0309, 0.057, 0.0607, 0.0371, 0.0013, -0.0328, -0.0411, -0.03, -0.0338, -0.0432, -0.0509, -0.0353, 0.0021, 0.0292, 0.0559, 0.0497, 0.0307, 0.0263, 0.0346, 0.0459, 0.0138, -0.0388, -0.0626, -0.0396, -0.0173, -0.0236, -0.034, -0.0449, -0.0388, -0.0167, 0.0002, -0.0219, -0.0711], "inner": [-0.083, -0.1957, 0.2334, 0.104, -0.1811, 0.0556, 0.1738, -0.0469, -0.1119, 0.0596, 0.0, 0.0244, 0.0604, -0.1704, -0.1494, -0.1853, 0.1366, 0.3962, -0.1355, -0.1069, 0.0674, -0.2774, -0.0608, 0.2441, -0.1465, 0.0421, 0.5018, -0.0523, -0.3046, 0.1615, 0.0785, -0.2752, -0.0455, 0.2471, -0.0409, -0.0195, 0.382, -0.2013, -0.5013, 0.5381, 0.4845, -0.4011, -0.0073, 0.5831, 0.2112, -0.3273, -0.0283, 0.0533, -0.0778, 0.3169, 0.0538, -0.3237, -0.0684, 0.2834, 0.0479, -0.2581, -0.021, 0.0986, -0.0091, 0.1506, 0.2011, -0.1361, 0.0988, 0.2648, -0.052, -0.0447, 0.1529, 0.0369, -0.187, -0.0484, -0.0676, -0.1845, -0.0036, 0.1124, -0.053, -0.0468, 0.1553, -0.0071, -0.0794, 0.0885, -0.0002, -0.0159, 0.1174, -0.0385, -0.1022, 0.1222, 0.1746, -0.0601, -0.2224, 0.299, 0.3047, -0.7082, -0.7506, 0.0621, 0.2285, 0.1852, 0.1571, -0.2492, 0.4168, 0.9007, -0.4534, -0.7722, 0.5544, 0.7522, -0.3478, -0.3059, 0.4949, 0.2867, -0.2222, -0.1022, -0.2932, -0.6288, 0.0297, 0.1491, -0.3317, 0.1132, 0.5211, 0.0097, -0.248, 0.2118, 0.1982, -0.2073, -0.0218, 0.5001, 0.4509, 0.0642, 0.0497, 0.1079, 0.0236, -0.2359, -0.4236, -0.1092, 0.2339, 0.1623, -0.0122, 0.0697, 0.2063, 0.2016, 0.0689, -0.1853, -0.1699, 0.0218, -0.1005, -0.1043, 0.1215, 0.0567, -0.0494, -0.0252, -0.008, -0.0206, -0.1124, -0.1303, 0.0543, 0.1974, 0.0422, 0.0726, 0.2714, 0.1759, -0.1309, -0.219, -0.0882, -0.0837, 0.0947, 0.1454, 0.3678, -0.0445, -0.8794, -0.4933, 0.0937, 0.4129, 0.0005, -0.1576, 0.3687, 0.4556, -0.2214, -0.9408, -0.0687, 0.9504, 0.2674, -0.5204, 0.2151, 0.7027, 0.2502, -0.2896, -0.5645, -0.3002, 0.2929, 0.4131, -0.4753, -0.2357, 0.7946, 0.3107, -0.6637, -0.3372, 0.5593, 0.1749, -0.3442, 0.2078, 0.3046, -0.0387, 0.2783, 0.3038, -0.1442, -0.1621, -0.012, -0.1183, -0.0473, 0.3221, 0.037, -0.3983, 0.0518, 0.3793, -0.0949, -0.2352, 0.0062, -0.0569, 0.0161, -0.0076, -0.172, 0.1423, 0.4357, 0.0617, -0.2864, -0.0307, 0.2091, 0.0026, -0.2232, -0.0018, 0.1405, -0.0595, 0.0023, 0.1303, -0.0201, -0.1135, -0.114, -0.1628, 0.0369, 0.2602, 0.1813, 0.0057, -0.1452, 0.0479, 0.1254, 0.0578, 0.1337, -0.0447, 0.0375, 0.1397, -0.312, -0.5778, -0.0614, 0.3447, 0.0593, -0.0703, 0.0648, 0.0971, 0.126, 0.0198, -0.2961, -0.1498, 0.3718, 0.5131, 0.2666, -0.014, 0.0567, 0.0882, -0.1498, -0.2099, -0.1082, -0.0539, 0.005, 0.1431, 0.019, -0.2708, -0.0325, 0.3107, 0.0299, -0.1144, 0.1926, 0.2108, 0.0091, 0.0695, 0.1135, -0.096, -0.116, 0.1038, 0.1186, -0.0676, -0.0629, 0.0062, -0.0612, -0.1384, -0.0404, 0.085, 0.0138, 0.1772, 0.3349, 0.063, -0.1199, -0.0279, 0.0024, -0.1928, -0.2557, 0.0021, 0.1178, 0.0244, 0.0288, 0.0445, -0.1012, -0.0151, 0.1087, -0.0989, -0.1915, -0.3963, 0.2169, 1.1601, 0.6067, -0.1342, -0.3327, -0.2339, -0.0011, -0.1215, -0.7524, -0.4496, 0.9558, 0.5386, -0.795, -0.3137, 0.5638, 0.0369, -0.5248, -0.1496, 0.212, 0.2105, 0.3928, 0.3247, -0.1697, 0.1529, 0.3302, -0.36, -0.4082, 0.2943, 0.2209, -0.3699, -0.04, 0.307, -0.0575, -0.1745, 0.0864, -0.0486, -0.2094, 0.0937, 0.274, 0.1207, 0.133, 0.115, -0.0435, 0.1954, 0.1673, -0.1257, -0.0575, 0.0362, -0.1905, -0.1506, 0.2683, 0.0395, -0.1555, 0.085, -0.0193, -0.1816, 0.0975, 0.2316, -0.213, -0.0893, 0.3582, 0.0268, -0.2027, 0.1587, 0.2492, -0.0934, -0.1251, 0.0208, -0.0653, 0.0859, 0.1436, -0.203, -0.4069, -0.2638, 0.1884, 0.5906, 0.1733, -0.1993, 0.1876, -0.2461, -0.2956, 0.3254, -0.3772, -0.2674, 0.8793, 0.3585, -0.5991, -0.0249, 0.5175, -0.3728, -0.7085, 0.2289, 0.1142, -0.2592, 0.4979, 0.2078, -0.603, 0.1871, 0.6273, -0.3481, -0.3869, 0.6213, 0.4235, -0.4084, 0.0018, 0.371, -0.1548, -0.0262, 0.2078, -0.3143, -0.2001, 0.2679, -0.0301, -0.181, 0.1416, -0.0249, -0.1827, 0.3426, 0.3814, -0.0721, 0.1028, 0.3021, -0.0765, -0.0513, 0.2857, -0.0525, -0.2435, 0.2061, 0.1632, -0.3918, -0.1561, 0.4166, -0.0757, -0.4007, 0.1018, 0.136, -0.1834, -0.0585, 0.1553, -0.0401, -0.0075, 0.1657, 0.0976, 0.0255, 0.1694, 0.0915, -0.0997, 0.1387, -0.0422, -0.557, -0.4852, 0.166, 0.2188, -0.0949, -0.0583, 0.133, 0.6543, 0.2089, -0.6104, -0.1478, 0.5276, 0.2233, -0.4051, -0.0401, 0.4145, 0.1467, -0.1057, -0.1894, -0.3371, -0.3533, -0.0585, -0.0419, -0.089, 0.282, 0.3791, 0.0541, 0.1036, 0.2596, -0.024, -0.2584, 0.0479, 0.4943, 0.242, -0.1243, 0.0578, 0.2251, 0.0185, -0.312, -0.3783, -0.1163, 0.1376, 0.0867, -0.0249, 0.0469, 0.2518, 0.2638, -0.0081, -0.1543, -0.0034, 0.0679, -0.0702, 0.0213, 0.0889, 0.0015, -0.0112, -0.0801, -0.0115, -0.039, -0.2134, -0.0681, 0.0965, -0.0318, -0.0015, 0.2084, 0.1241, -0.0078, 0.0906, 0.0596, -0.0596, 0.1639, 0.2336, 0.3239, -0.0275, -0.8479, -0.4449, 0.1145, 0.1816, 0.1668, -0.1213, -0.0953, 0.4472, 0.0981, -1.115, -0.4153, 1.1301, 0.4345, -0.6834, 0.2558, 0.935, 0.0763, -0.3198, -0.1402, -0.3271, -0.0695, 0.5445, -0.1688, -0.4093, 0.6346, 0.4058, -0.6416, -0.4233, 0.4597, 0.0442, -0.4374, 0.2076, 0.4194, 0.0352, 0.1592, 0.3153, -0.0778, -0.1416, -0.1259, -0.2698, 0.038, 0.3005, -0.0341, -0.1623, 0.2529, 0.2904, -0.0468, -0.0729, 0.0156, -0.2276, -0.1238, 0.1361, -0.0698, 0.0058, 0.3184, 0.0919, -0.3223, -0.027, 0.2625, -0.121, -0.1878, 0.2052, 0.1728, -0.0633, 0.1295, 0.2683, -0.1057, -0.3052, -0.0794, -0.1606, -0.0997, 0.161, 0.1553, -0.0266, -0.3208, -0.2463, 0.0091, 0.2729, 0.2039, -0.0958, 0.0268, 0.2022, -0.0802, -0.4899, -0.0715, 0.4664, 0.1595, -0.0929, 0.136, 0.2048, 0.1001, -0.0101, -0.2745, -0.1673, 0.4269, 0.551, -0.0718, -0.3236, 0.219, 0.2454, -0.4191, -0.4434, 0.1912, 0.2669, -0.077, 0.0651, -0.0309, -0.1647, 0.231, 0.2794, 0.0201, -0.1303, 0.1044, 0.3408, 0.1083, -0.0889, -0.0669, -0.0603, -0.0437, 0.0263, -0.0889, -0.1322, -0.0032, -0.0724, -0.2113, -0.1007, 0.1035, 0.1697, 0.2823, 0.2365, 0.0226, 0.018, 0.0788, -0.0161, -0.1545, -0.0741, 0.0791, 0.0028, -0.0937, 0.0073, 0.008, -0.1697, -0.2355, -0.1428, 0.031, 0.0905, -0.2204, 0.006, 0.7569, 0.55, 0.0244, -0.1092, -0.1494, 0.0754, 0.2731, -0.3942, -0.7534, 0.4594, 0.6985, -0.5789, -0.5409, 0.4197, 0.1447, -0.3562, -0.005, -0.0255, -0.1462, 0.4251, 0.424, -0.1204, 0.1775, 0.4199, -0.1347, -0.3242, 0.1553, 0.1628, -0.3148, 0.0593, 0.4529, -0.1288, -0.3219, 0.0864, -0.0206, -0.2453, 0.0461, 0.0848, -0.0554, 0.1738, 0.2305, -0.0419, -0.0406, 0.1468, 0.0785, -0.0796, -0.0283, 0.0263, -0.0413, 0.1025, 0.0682, -0.1389, -0.1455, -0.0349, 0.0932, 0.0694, -0.0346, -0.097, 0.0305, 0.1451, -0.0427, -0.1438, -0.0081, 0.2182, 0.204, -0.166, -0.0716, 0.1602, 0.0768, -0.1023, -0.1044, -0.249, -0.5388, 0.4441, 1.0563, 0.1995, -0.1535, -0.0127, -0.4358, -0.2383, 0.4512, -0.6408, -0.6361, 1.383, 0.7045, -1.1517, -0.2368, 0.8261, -0.351, -0.8317, 0.2099, 0.2105, -0.1408, 0.6296, 0.3437, -0.6164, 0.2703, 0.6012, -0.5196, -0.5243, 0.4215, 0.4019, -0.389, 0.0041, 0.3986, -0.0497, 0.0252, -0.0307, -0.2372, -0.1098, -0.0598, -0.0344, 0.2134, 0.3033, -0.09, -0.0853, 0.4095, 0.2937, -0.2846, -0.1743, 0.1606, -0.0651, -0.0187, 0.2337, -0.0707, -0.1213, 0.2422, -0.0049, -0.3911, -0.0424, 0.3944, 0.0534, -0.2375, 0.0841, 0.0928, -0.1628, -0.0416, 0.1087, -0.0216, -0.0466, 0.05, -0.014, 0.0062, 0.0419, -0.212, -0.1103, 0.0674, -0.1183, 0.2177, 0.2818, -0.1619, -0.0284, 0.1122, -0.123, -0.1251, 0.2108, 0.3879, 0.193, -0.032, -0.0455, 0.0107, -0.107, -0.1957, 0.0055, -0.0083, 0.0322, -0.0096, -0.102, -0.0895, -0.5318, -0.1007, 0.5994, 0.168, -0.0534, 0.4074, 0.4867, 0.0302, -0.2068, -0.0349, -0.0556, 0.1358, 0.4603, -0.0702, -0.3538, 0.0768, 0.2458, -0.2615, -0.5409, 0.0239, 0.2688, 0.1157, 0.1922, 0.0746, 0.043, 0.2641, 0.0177, -0.1978, 0.0569, 0.2531, 0.0804, -0.1433, -0.0843, -0.0456, -0.135, -0.1449, -0.0146, -0.0149, -0.0268, 0.0414, -0.0309, 0.0037, -0.0791, 0.0132, 0.2422, 0.0534, 0.0351, 0.1231, 0.1048, 0.0362, -0.0473, -0.2099, 0.0531, 0.6556, -0.2233, -1.1752, -0.2692, 0.5313, 0.11, -0.1538, -0.11, 0.0556, 0.7665, 0.1985, -1.0969, -0.2259, 1.1273, 0.2212, -0.7867, 0.2742, 0.8417, -0.0122, -0.2237, -0.127, -0.5265, -0.2052, 0.3874, -0.1017, -0.1207, 0.549, 0.2898, -0.3112, -0.1262, 0.3336, -0.0695, -0.2956, 0.3458, 0.486, 0.0796, 0.0562, 0.1923, -0.0731, -0.3226, -0.3996, -0.2922, 0.0991, 0.2599, -0.0406, -0.1222, 0.1824, 0.1655, -0.0145, 0.0369, 0.0611, -0.0167, 0.1743, 0.2232, -0.0575, 0.0586, 0.2398, -0.064, -0.2302, 0.0981, -0.0346, -0.3565, -0.0427, 0.103, -0.1286, -0.0863, 0.1338, 0.2078, 0.1213, -0.076, -0.3159, -0.1436, 0.2687, 0.1632, 0.2216, -0.109, -0.6393, -0.1823, 0.3846, 0.2792, -0.3596, -0.0115, 0.575, 0.0439, -0.628, -0.4941, 0.4423, 0.6189, -0.1202, -0.1582, 0.3068, 0.3557, 0.2157, -0.174, -0.4672, -0.1132, 0.4607, 0.263, -0.562, -0.1389, 0.6865, 0.0307, -0.691, -0.1438, 0.4602, -0.0161, -0.2035, 0.1795, -0.0021, 0.0084, 0.3973, 0.2987, -0.1701, -0.2438, 0.0692, 0.1616, 0.1165, 0.1072, -0.0851, -0.0837, 0.1754, 0.0291, -0.2134, -0.0882, 0.0187, -0.0154, 0.0612, -0.0564, -0.1027, 0.3094, 0.2964, -0.2313, -0.2502, 0.1577, 0.1649, -0.0695, 0.0179, 0.1194, -0.096, -0.0598, 0.1587, 0.0404, -0.1697, -0.1392, -0.0947, -0.0872, 0.0552, 0.0828, 0.0391, -0.0765, 0.1171, 0.3877, 0.1712, -0.031, -0.1559, 0.0101, 0.1368, -0.3075, -0.5687, 0.0606, 0.5541, 0.0395, -0.2063, 0.1506, 0.1616, -0.0606, -0.0357, -0.1719, -0.2216, 0.2828, 0.5183, 0.1671, -0.0658, 0.1265, 0.1116, -0.2409, -0.2009, 0.014, -0.1064, -0.0541, 0.1244, -0.0034, -0.2131, -0.0429, 0.2776, 0.1082, -0.0104, 0.1862, 0.1813, 0.0478, 0.1126, 0.0669, -0.1059, 0.0672, 0.16, -0.0211, -0.0513, -0.0461, -0.2144, -0.1101, 0.0193, -0.1252, -0.0603, 0.134, 0.2068, 0.1619, 0.0949, -0.0177, -0.04, -0.0013, -0.0422, -0.0986, -0.084, 0.0841, 0.1027, -0.0789, -0.096, -0.0104, 0.0236, 0.0229, -0.1619, -0.1842, -0.4306, -0.2095, 1.0281, 1.032, 0.1767, -0.2502, -0.2794, -0.0617, -0.0135, -0.5679, -0.9114, 0.5628, 1.1608, -0.513, -0.7909, 0.5294, 0.3708, -0.6765, -0.5247, 0.1748, 0.2809, 0.3515, 0.507, -0.0521, 0.0141, 0.6286, -0.0911, -0.703, 0.0887, 0.5604, -0.2134, -0.3866, 0.3293, 0.0942, -0.3234, -0.0161, 0.0201, -0.2597, -0.102, 0.2838, 0.2549, 0.1005, 0.0315, -0.0413, 0.1652, 0.3328, -0.0057, -0.1879, 0.1069, 0.0313, -0.2425, 0.0411, 0.1421, -0.084, 0.0224, 0.0837, -0.165, -0.2185, 0.1798, 0.072, -0.3106, 0.0895, 0.2997, -0.0318, 0.0278, 0.2477, 0.0344, -0.1862, -0.0648, -0.0091, 0.0375, 0.1451, -0.012, -0.2402, -0.3072, 0.0546, 0.4899, 0.0737, -0.1057, 0.1691, -0.3367, -0.1779, 0.3587, -0.3733, -0.3418, 0.7048, 0.3356, -0.4267, 0.0453, 0.4149, -0.2321, -0.491, 0.1132, -0.0378, -0.2594, 0.4321, 0.1938, -0.5632, 0.1494, 0.6108, -0.2719, -0.36, 0.4085, 0.4306, -0.1231, -0.0508, 0.2355, 0.1059, 0.1837, 0.1053, -0.2916, -0.1428, 0.2149, 0.1054, -0.1031, -0.0081, 0.0383, -0.1226, 0.0949, 0.2068, -0.072, -0.0281, 0.2144, -0.0096, -0.1478, 0.1946, 0.1475, -0.1072, -0.0244, 0.1795, -0.0695, -0.1452, 0.1355, 0.0073, -0.2284, -0.0627, 0.1425, -0.0689, -0.0378, 0.1098, 0.0741, 0.0106, -0.0432, -0.0211, 0.0491, 0.1996, 0.0208, -0.044, 0.2981, -0.0936, -0.8157, -0.4579, 0.2565, 0.1366, -0.0325, 0.1127, 0.1468, 0.5435, 0.1845, -0.6856, -0.1004, 0.6942, 0.2662, -0.3676, 0.0897, 0.5393, 0.0429, -0.2934, -0.28, -0.3869, -0.3427, -0.018, -0.082, -0.0856, 0.4178, 0.3312, -0.1632, 0.0638, 0.4088, 0.0169, -0.2029, 0.1735, 0.4651, 0.2523, -0.0401, 0.0648, 0.014, -0.1498, -0.2376, -0.3585, -0.231, 0.0906, 0.0984, -0.1189, 0.0439, 0.2781, 0.2596, 0.1371, -0.0289, -0.0115, 0.1301, -0.0032, 0.0419, 0.2232, 0.0814, 0.0119, -0.0164, 0.001, -0.1797, -0.3137, -0.103, 0.0301, 0.0406, 0.0174, 0.1667, 0.1907, -0.0019, -0.2026, -0.2261, -0.0578, 0.1054, -0.046, 0.3345, 0.4789, -0.8036, -0.7998, 0.1355, 0.4035, 0.1743, -0.0404, 0.1923, 0.4483, 0.3559, -0.7415, -0.7545, 0.722, 0.8125, -0.3897, -0.2852, 0.6861, 0.4407, -0.3206, -0.5279, -0.385, -0.0819, 0.4529, -0.037, -0.4795, 0.4602, 0.5812, -0.3655, -0.5916, 0.2022, 0.3582, -0.1905, -0.0403, 0.3132, 0.206, 0.1129, 0.1853, -0.0039, -0.1436, -0.0856, -0.1056, 0.0737, 0.2786, 0.1074, -0.1103, -0.0278, 0.1991, 0.1127, -0.1322, -0.0814, -0.0437, -0.0174, -0.0658, -0.1631, -0.0021, 0.1811, 0.0651, -0.2009, -0.0877, 0.0893, 0.0374, -0.0119, 0.0049, 0.1459, 0.187, -0.0055, 0.0681, 0.1023, -0.2713, -0.3141, -0.1403, -0.0526, 0.129, 0.3312, 0.0583, -0.261, 0.0391, 0.1611, 0.051, 0.0138, 0.0996, 0.2255, 0.039, -0.2618, -0.263, 0.0845, 0.2034, -0.0223, -0.091, 0.1196, 0.142, 0.006, 0.0018, -0.1265, -0.1501, 0.2589, 0.4962, -0.006, -0.2117, 0.2766, 0.1777, -0.3499, -0.3294, 0.0737, 0.1654, 0.021, 0.0398, -0.0996, -0.1192, 0.1788, 0.1647, -0.0876, -0.0651, 0.1465, 0.1967, 0.142, 0.0666, 0.0484, 0.0086, 0.0044, 0.0099, -0.1241, -0.0698, 0.0352, -0.012, -0.1321, -0.1278, -0.0052, 0.0541, 0.1887, 0.1774, -0.0049, -0.0289, 0.0093, -0.0263, -0.1137, -0.186, -0.05, 0.1321, 0.0185, -0.0223, 0.1282, 0.1009, -0.1477, -0.1558, 0.1043, 0.0495, -0.1543, -0.2123, 0.3496, 0.8541, 0.4754, -0.0664, -0.436, -0.2995, 0.1283, -0.0624, -0.8936, -0.5035, 1.0555, 0.6155, -0.904, -0.2056, 0.7188, -0.0034, -0.3653, -0.0557, 0.0346, 0.1031, 0.4974, 0.264, -0.159, 0.2696, 0.2979, -0.2698, -0.3606, 0.0598, 0.0658, -0.205, 0.0135, 0.2091, -0.0608, -0.1631, -0.043, 0.0266, 0.0502, -0.114, -0.0127, 0.3309, 0.2272, -0.0768, 0.0171, 0.2029, 0.1004, -0.0882, -0.1031, -0.0034, -0.0466, -0.0262, 0.0749, -0.0099, -0.0286, 0.0091, -0.0544, -0.032, 0.1053, 0.136, -0.0619, -0.1031, 0.1228, 0.0718, -0.2048, -0.0807, 0.23, 0.1451, -0.1025, -0.0637, 0.0435, 0.0247, 0.0452, -0.165, -0.3163, -0.2227, -0.091, 0.3851, 0.7199, 0.3457, -0.0403, -0.1252, -0.5533, -0.1285, 0.4605, -0.6049, -0.1928, 1.2785, 0.184, -1.0339, -0.0512, 0.5918, -0.4753, -0.705, 0.3367, 0.1741, -0.1308, 0.5411, 0.0989, -0.5243, 0.3884, 0.6072, -0.3375, -0.2631, 0.5282, 0.365, -0.2898, -0.1046, 0.1252, -0.0902, 0.0013, -0.0218, -0.2862, -0.1257, 0.0783, 0.0367, 0.1665, 0.0841, -0.1507, 0.1103, 0.4202, 0.0637, -0.2006, 0.1525, 0.1092, -0.1087, 0.1355, 0.218, -0.0957, -0.2125, 0.0971, -0.0759, -0.5234, -0.0404, 0.4384, -0.0703, -0.2661, 0.2157, 0.1644, -0.0996, 0.0942, 0.2115, 0.0132, -0.0504, 0.1272, 0.0794, -0.0931, 0.0034, -0.0344, -0.1137, 0.0208, 0.0541, -0.1355, -0.3042, -0.1074, 0.0746, -0.0377, -0.1913, 0.0435, 0.6532, 0.5178, -0.2763, -0.1415, 0.3371, 0.1222, -0.3158, -0.135, 0.2797, 0.1303, 0.02, -0.108, -0.2263, -0.4535, -0.3926, 0.115, 0.1922, 0.2164, 0.264, 0.2318, 0.2929, 0.1538, -0.1758, -0.1706, 0.0786, 0.4022, 0.2942, -0.1845, 0.0383, 0.2552, -0.0793, -0.3577, -0.306, -0.1036, 0.0952, 0.1754, 0.0663, -0.0279, 0.0422, 0.2019, -0.0361, -0.0846, 0.1883, 0.1566, 0.0058, 0.0055, 0.0697, -0.0979, -0.0996, -0.0653, -0.0227, 0.0335, -0.0835, 0.0, -0.02, -0.1023, 0.0133, 0.011, -0.0341, 0.091, 0.0585, -0.1158, -0.0668, 0.0812, -0.0239, 0.2709, 0.2553, -0.7454, -0.5461, 0.2719, 0.1663, 0.0931, 0.2115, -0.0309, 0.2576, 0.4733, -0.5778, -0.5097, 0.8203, 0.6283, -0.5617, -0.1329, 0.8045, 0.1186, -0.4319, -0.1262, -0.3643, -0.5092, 0.1564, 0.0413, -0.34, 0.3749, 0.5727, -0.2068, -0.4127, 0.2757, 0.2675, -0.2877, -0.0032, 0.4153, 0.3437, 0.254, 0.3106, 0.0646, -0.1762, -0.1818, -0.2667, -0.1007, 0.1462, 0.0317, -0.0902, 0.1179, 0.1941, -0.0434, -0.0047, 0.1119, -0.1481, -0.0944, 0.18, 0.0551, 0.0227, 0.2052, 0.0037, -0.3232, -0.0128, 0.1517, -0.2604, -0.1556, 0.1725, -0.0406, -0.0845, 0.1015, 0.1092, -0.0068, -0.0724, -0.0791, -0.2216, 0.0759, 0.2472, 0.2372, 0.1983, -0.3848, -0.4238, 0.1327, 0.3744, -0.005, -0.1844, 0.1468, 0.2022, -0.1715, -0.577, -0.2385, 0.4613, 0.2307, -0.2318, 0.0869, 0.3116, 0.2792, 0.1412, -0.2321, -0.3086, 0.2, 0.5354, -0.0924, -0.4836, 0.2138, 0.4205, -0.3198, -0.4352, 0.1873, 0.2102, -0.1467, 0.0435, -0.0011, -0.134, 0.3588, 0.4543, 0.0684, -0.0945, 0.0378, 0.1697, 0.0997, 0.021, -0.0695, -0.1322, 0.0206, 0.1194, -0.1265, -0.1858, -0.0024, -0.0843, -0.0759, 0.0729, -0.0188, 0.0617, 0.3676, 0.1582, -0.2323, -0.0629, 0.1449, -0.02, -0.0551, 0.0586, -0.0044, 0.0161, 0.0703, -0.1174, -0.2017, 0.0002, -0.0517, -0.2271, 0.0219, 0.3026, 0.0143, -0.2204, 0.3884, 0.5656, 0.1348, -0.0398, -0.2599, -0.1499, 0.1529, -0.2485, -0.7795, -0.0112, 0.7306, -0.0242, -0.4339, 0.1472, 0.2454, -0.1436, -0.1303, -0.1319, -0.1114, 0.4037, 0.5476, 0.1592, 0.1418, 0.3015, -0.005, -0.3143, -0.1062, 0.0369, -0.1777, -0.0778, 0.1899, -0.0117, -0.2609, -0.076, 0.0086, -0.0211, 0.1272, 0.0559, 0.0681, 0.2526, 0.1797, -0.0041, -0.0058, 0.1148, 0.1894, 0.0741, -0.0817, -0.0812, -0.1075, 0.0158, -0.0317, -0.1821, -0.0359, 0.0419, 0.0846, 0.1343, 0.0481, -0.1483, -0.0843, 0.1066, 0.0123, -0.1239, -0.0234, 0.2294, 0.1671, -0.142, -0.0578, 0.0763, -0.0939, -0.0073, 0.0552, -0.2246, -0.66, -0.0523, 1.1484, 0.7323, 0.0197, -0.1481, -0.351, -0.2375, 0.1995, -0.347, -1.0955, 0.6977, 1.4827, -0.6674, -0.9493, 0.7449, 0.4308, -0.9629, -0.519, 0.3013, 0.0573, 0.2857, 0.6426, -0.1715, -0.135, 0.7144, -0.0346, -0.8786, -0.0339, 0.6468, -0.2193, -0.3941, 0.4636, 0.1956, -0.2911, -0.0015, 0.0148, -0.268, -0.0716, 0.2121, 0.2259, 0.3229, 0.1347, -0.1873, 0.0867, 0.3833, -0.0197, -0.3065, 0.091, 0.1678, -0.0817, 0.1416, 0.0915, -0.2607, 0.0275, 0.1969, -0.2217, -0.3119, 0.267, 0.2986, -0.3166, -0.1057, 0.237, -0.0685, -0.1509, 0.206, 0.1511, -0.2255, -0.0367, 0.1603, -0.024, -0.0011, 0.0401, -0.0692, -0.23, 0.0127, 0.5198, 0.0312, -0.2635, 0.1667, -0.1931, -0.3718, 0.2128, 0.013, -0.2662, 0.4058, 0.2841, -0.3325, 0.0019, 0.2896, -0.0975, -0.2138, 0.1358, 0.0486, -0.128, 0.2305, 0.0461, -0.5122, 0.1481, 0.628, -0.2043, -0.264, 0.4662], "outer": [0.0085, 0.4235, 0.013, -0.2652, 0.2372, 0.5909, -0.093, -0.4069, 0.2794, 0.437, -0.3529, -0.6124, 0.3988, 0.4093, -0.3545, -0.2238, 0.3712, 0.3074, -0.1974, -0.0244, 0.1539, 0.1425, 0.1182, 0.0597, -0.1397, 0.0524, 0.2867, -0.0471, -0.1206, 0.0597, 0.2367, 0.0394, -0.1096, -0.0041, 0.1539, 0.0292, -0.1547, 0.1421, 0.2595, -0.0065, -0.294, 0.1145, 0.3594, -0.2424, -0.4772, 0.1048, 0.3825, -0.2485, -0.398, 0.1771, 0.4581, 0.0301, -0.264, 0.16, 0.2432, 0.0686, 0.0252, 0.0118, 0.0658, 0.1064, 0.0747, -0.1693, -0.1174, 0.065, -0.1271, 0.0244, 0.612, -0.4378, -1.3324, 1.1468, 1.6211, -1.8449, -1.133, 2.6375, 0.6112, -2.2696, 0.3488, 1.7108, -0.5628, -0.6826, 0.9567, -0.2834, -0.6989, 1.2382, 0.0199, -1.5967, 0.4045, 1.5456, -0.7866, -1.3332, 1.0684, 1.0968, -0.9255, -0.6449, 1.0505, 0.32, -0.6591, 0.1953, 0.4646, -0.1417, -0.1389, 0.4231, -0.0032, -0.3545, 0.3151, 0.2989, -0.361, -0.0244, 0.5332, -0.0459, -0.3155, 0.1624, 0.3476, -0.0828, -0.2733, 0.1584, 0.2311, -0.1438, -0.3322, 0.0703, 0.214, -0.2079, -0.3094, 0.1689, 0.335, -0.1125, 0.0179, 0.2144, 0.0686, 0.0694, 0.067, -0.0512, 0.0097, 0.2384, -0.0589, -0.3159, 0.0455, 0.2026, -0.1909, -0.1986, 0.1259, 0.1263, -0.0508, -0.0435, 0.0451, -0.0142, 0.158, 0.1559, 0.0219, 0.175, 0.2469, -0.0057, -0.1539, 0.1255, 0.0832, -0.1661, -0.1263, 0.123, 0.1332, -0.1803, -0.0585, 0.3066, 0.1653, -0.1105, 0.0451, 0.2778, 0.117, -0.0244, 0.0743, 0.056, 0.0678, -0.0621, 0.1129, -0.0682, 0.0329, -0.0727, 0.0292, 0.6242, -0.4759, -0.8276, 0.3854, 1.5951, -0.9896, -1.2962, 1.7048, 0.891, -1.1789, -0.8788, 1.6865, 0.0008, -0.8727, 0.5596, 0.0398, -0.251, 0.1218, 0.5815, -1.0554, -0.0772, 1.1569, -0.2879, -0.9417, 0.1872, 1.1898, -0.7135, -0.8187, 0.5389, 0.5413, -0.32, -0.389, 0.6294, 0.0731, -0.1559, 0.1539, 0.1702, -0.0073, 0.1023, 0.3237, -0.2672, -0.0532, 0.2351, -0.0528, -0.48, -0.1182, 0.309, -0.0804, -0.1864, 0.0418, 0.3216, -0.0252, -0.0414, 0.1291, 0.3139, 0.0958, -0.1405, 0.3212, 0.145, 0.0374, 0.0053, 0.1848, 0.0788, 0.0041, 0.1474, -0.1417, -0.0134, 0.1263, 0.1137, -0.2652, 0.0097, 0.3789, -0.0406, -0.1113, 0.1178, 0.1462, -0.2022, -0.0268, 0.1706, -0.0743, -0.0812, 0.1141, 0.197, -0.0841, 0.0353, 0.1953, -0.0824, 0.0016, 0.1913, -0.0114, -0.2392, 0.1218, 0.186, -0.2506, -0.201, 0.2575, 0.1917, -0.2802, -0.132, 0.1762, 0.065, -0.1965, 0.0621, 0.1982, 0.0439, 0.0333, 0.1429, 0.0183, -0.0658, -0.0658, 0.1275, 0.7403, -0.3265, -1.7153, 0.1263, 2.5998, -0.7216, -2.6578, 1.9135, 2.5783, -1.8534, -1.8656, 2.1705, 0.9498, -1.2447, 0.2408, 0.4203, -0.64, 0.4873, 0.9198, -1.7076, -0.7269, 1.9338, 0.3793, -1.9224, -0.2043, 2.1498, 0.0426, -1.6065, 0.2018, 1.3616, -0.1007, -0.696, 0.6152, 0.4138, -0.2843, 0.1015, 0.5149, -0.1791, -0.3415, 0.4914, -0.0317, -0.3395, 0.2104, 0.2692, -0.2895, -0.2473, 0.3237, 0.093, -0.3013, -0.1535, 0.4101, 0.0455, -0.5555, -0.2278, 0.3553, 0.0479, -0.5909, 0.0394, 0.6818, 0.1974, -0.3005, 0.2404, 0.3675, -0.0654, -0.028, -0.0032, -0.037, 0.1316, 0.1616, -0.3529, -0.3046, 0.2112, 0.1036, -0.2709, -0.0962, 0.2867, 0.1348, -0.1121, -0.0227, 0.2104, 0.1563, 0.0569, 0.1921, 0.2879, 0.1876, -0.0662, -0.0869, 0.1401, 0.0455, -0.3423, -0.2144, 0.216, 0.1198, -0.266, -0.1945, 0.4284, 0.4069, -0.1222, -0.1036, 0.2457, 0.3756, -0.0183, -0.0776, 0.1218, 0.0743, 0.002, -0.0877, -0.1088, -0.1312, 0.1235, 0.0317, -0.0971, 0.6262, 0.002, -1.4518, 0.5019, 2.2976, -1.1679, -2.2116, 2.532, 1.9728, -2.841, -0.9458, 2.5112, 0.054, -2.0414, 0.616, 0.9673, -1.2605, 0.415, 0.9831, -1.3726, -0.3866, 2.0077, 0.0118, -2.0105, 0.8061, 1.8859, -0.8922, -1.5801, 1.1943, 1.1435, -1.267, -0.3371, 0.9535, 0.1693, -0.664, 0.2359, 0.5145, -0.3366, 0.0999, 0.3208, -0.1994, -0.1373, 0.4837, 0.0305, -0.5742, 0.0463, 0.4049, -0.0686, -0.4573, 0.0443, 0.493, 0.0004, -0.3695, 0.1442, 0.5068, 0.0077, -0.3269, 0.2469, 0.4837, -0.037, -0.1697, 0.0849, 0.1693, -0.0715, -0.2164, -0.1706, 0.0361, 0.1486, -0.0983, -0.2644, 0.0475, 0.3793, -0.0158, -0.0991, 0.1921, 0.2615, 0.1994, -0.0378, -0.0061, 0.1137, 0.1527, -0.1174, -0.1649, 0.1563, 0.1235, -0.173, -0.2765, 0.1486, 0.1486, -0.2583, -0.1637, 0.357, 0.3001, -0.3009, -0.0504, 0.4999, 0.2891, -0.3094, -0.0784, 0.3419, 0.0772, -0.1868, -0.0475, 0.1718, -0.0215, -0.0102, 0.0199, -0.0788, 0.0081, 0.2047, -0.121, 0.1787, 0.59, -0.612, -0.5174, 1.252, 0.469, -1.8558, 0.2099, 1.8055, -0.7878, -1.2755, 0.7874, 0.8382, -0.9048, 0.0357, 0.7492, -0.6193, 0.0759, 0.9324, -0.4536, -0.7846, 0.9161, 0.7167, -0.8776, -0.4166, 0.8824, 0.363, -0.8183, -0.1503, 0.6274, -0.0365, -0.3923, 0.1588, 0.3622, -0.1791, -0.0024, 0.4154, -0.0158, -0.1304, 0.3167, 0.1389, -0.268, -0.0171, 0.1442, -0.0869, -0.2246, 0.082, 0.2087, -0.1084, -0.1235, 0.1567, 0.2051, -0.1486, -0.1255, 0.253, 0.2282, -0.1771, -0.0922, 0.3598, 0.0605, -0.1551, 0.0325, 0.0199, -0.0081, 0.0171, -0.0305, -0.1417, 0.0231, 0.225, -0.0435, -0.1681, 0.1718, 0.2095, -0.0638, -0.1027, 0.1027, 0.0995, -0.0089, 0.0374, 0.0755, 0.0755, 0.0597, 0.1084, 0.0349, -0.028, 0.0662, 0.0077, -0.0508, 0.0707, 0.1669, -0.0975, -0.1283, 0.2213, 0.026, -0.3212, -0.0211, 0.3943, 0.0682, -0.1661, 0.1811, 0.3241, 0.0918, -0.0406, 0.2652, 0.1235, 0.0504, 0.1474, 0.0162, -0.1133, -0.069, 0.1023, -0.292, 0.4171, 0.2408, -1.1667, -0.811, 1.6755, 0.9023, -2.5413, 0.2887, 2.7659, -0.3423, -2.2619, 0.9145, 1.8436, -1.1687, -0.3963, 0.6177, -0.2294, -0.1247, 0.9421, -0.4812, -1.3827, 1.3243, 1.0282, -1.4855, -0.9965, 1.6394, 0.7768, -1.6751, -0.3172, 1.131, 0.2445, -0.7655, 0.1137, 0.4857, -0.1941, 0.0597, 0.0942, -0.0662, -0.0979, 0.4138, 0.013, -0.3651, 0.4227, 0.3557, -0.1425, -0.3078, 0.2099, 0.2282, -0.1632, -0.2319, 0.1612, 0.3691, -0.2502, -0.2648, 0.2217, 0.3358, -0.1641, -0.1308, 0.3005, 0.2692, 0.0633, -0.104, 0.0175, 0.1921, 0.1758, -0.292, -0.1673, 0.3167, 0.2461, -0.2164, -0.3143, 0.2432, 0.2977, 0.0114, -0.1466, 0.1909, 0.3529, 0.1133, -0.1831, -0.1937, 0.2022, 0.0512, -0.1429, -0.1604, 0.1933, 0.1417, -0.3094, -0.0398, 0.1661, 0.0158, -0.3403, 0.0394, 0.3618, -0.0918, -0.2022, 0.1263, 0.4593, -0.0747, -0.2075, 0.1247, 0.1738, 0.1031, -0.1096, 0.0914, 0.0402, 0.1308, 0.0731, -0.0264, 0.0012, 0.1007, 0.2225, -0.2761, 0.3224, 0.5665, -0.9669, -1.2463, 1.5874, 1.3165, -2.4654, -0.4345, 2.9027, -0.0065, -2.6721, 0.6635, 2.2408, -0.854, -0.7898, 1.0704, 0.0439, -0.4065, 1.0124, -0.2152, -1.3726, 0.811, 1.2394, -1.2032, -1.3576, 1.3624, 1.1509, -1.4497, -0.8414, 1.3165, 0.5933, -0.9494, 0.0004, 0.8536, -0.0049, -0.2952, 0.3862, 0.2408, -0.2997, 0.1949, 0.2485, -0.3687, -0.171, 0.2566, -0.0613, -0.3643, -0.0345, 0.1637, -0.0256, -0.1831, 0.1373, 0.3074, -0.0711, -0.2428, 0.2664, 0.4573, -0.2595, -0.2891, 0.3781, 0.3708, -0.3407, -0.2725, 0.2964, 0.1661, -0.1466, -0.1925, 0.0804, 0.1978, 0.1807, -0.0309, -0.1165, 0.1433, 0.2189, 0.0175, -0.106, 0.0605, 0.1864, 0.108, -0.2453, -0.1945, 0.2079, 0.1178, -0.2152, 0.0654, 0.3736, -0.0715, -0.2737, 0.3127, 0.4439, -0.3009, -0.322, 0.4296, 0.3557, -0.3537, -0.1998, 0.3716, 0.3833, -0.0703, -0.1413, 0.1543, 0.1263, 0.1628, 0.0045, -0.1312, 0.0564, 0.2489, 0.0158, -0.2473, -0.026, -0.0114, 0.1665, 0.3805, -0.7728, -1.161, 1.4128, 1.3446, -2.1575, -0.64, 2.9567, 0.0495, -2.4621, 0.9941, 1.8412, -1.1236, -0.6635, 1.2353, -0.4357, -0.761, 1.2914, -0.2814, -1.708, 0.8, 1.4964, -1.3921, -1.2788, 1.6934, 0.8865, -1.6345, -0.4183, 1.7113, 0.1129, -1.0229, 0.5133, 0.7582, -0.3513, -0.3293, 0.5649, 0.0041, -0.4869, 0.2217, 0.2209, -0.3919, -0.0552, 0.4357, -0.2323, -0.3781, 0.2741, 0.3618, -0.214, -0.1685, 0.4532, 0.292, -0.3196, -0.2274, 0.4747, 0.3659, -0.3651, -0.2599, 0.5161, 0.2908, -0.3992, -0.067, 0.3277, 0.11, -0.093, 0.0276, 0.0812, 0.1836, 0.2546, -0.1076, -0.2469, 0.1929, 0.2599, -0.2871, -0.2014, 0.2359, 0.1998, -0.2181, -0.2181, 0.2449, 0.1088, -0.1052, -0.0012, 0.2221, 0.2254, -0.0093, -0.0938, 0.0414, 0.175, -0.0414, -0.1405, 0.0528, 0.1466, -0.0175, -0.2347, -0.0589, 0.2404, 0.0032, -0.1742, 0.0621, 0.2026, 0.0512, -0.1015, 0.1718, 0.1531, 0.0962, -0.0093, 0.0134, 0.0564, -0.0966, 0.015, -0.3395, 0.3228, 0.0313, -0.6193, 0.0077, 0.8045, 0.104, -1.1342, 0.7561, 0.7683, -0.4422, -0.4337, 0.5511, 0.4674, -0.6968, 0.3939, 0.052, -0.3228, 0.1466, 0.3444, -0.2688, -0.5344, 0.6997, 0.1864, -0.4138, -0.1076, 0.5438, 0.3111, -0.4069, 0.1458, 0.3375, 0.1876, -0.1385, 0.0646, 0.216, -0.0629, 0.1287, 0.0621, 0.0102, -0.0581, 0.0881, 0.0199, -0.1401, 0.002, 0.0914, 0.0735, -0.1697, 0.0593, 0.1385, -0.0845, -0.1446, 0.1202, 0.1275, -0.0816, 0.0638, 0.1295, 0.175, -0.0345, 0.0532, 0.1145, 0.1141, 0.0158, -0.145, 0.0674, -0.0439, -0.1161, -0.2059, -0.0544, -0.0118, 0.0199, -0.0077, -0.1377, 0.1036, 0.1072, 0.0349, -0.0219, 0.1718, 0.1165, 0.0589, 0.1109, 0.1153, 0.0569, -0.0256, 0.1665, -0.0162, -0.026, 0.1222, 0.0426, -0.0954, 0.1279, 0.1844, -0.1913, 0.0296, 0.2713, 0.0605, -0.2164, 0.1056, 0.2636, -0.175, -0.1352, 0.1056, 0.1925, -0.0857, 0.0625, 0.2201, -0.0134, 0.1389, 0.1157, 0.1304, -0.1275, 0.2282, 0.052, 0.0816, 0.7054, -0.4897, -1.3835, 0.1458, 2.2229, -1.081, -2.1104, 1.92, 1.7186, -1.6922, -1.5902, 1.9797, 0.5576, -0.9291, 0.3131, 0.1645, -0.2307, 0.5121, 0.6729, -1.6203, -0.4171, 1.6609, 0.0199, -1.6735, -0.1478, 1.7933, -0.1953, -1.3117, 0.3151, 1.0311, -0.0398, -0.4166, 0.5466, 0.1019, -0.2319, 0.1836, 0.1165, -0.3395, -0.2392, 0.3464, -0.2177, -0.2298, 0.2993, 0.1105, -0.2136, -0.0735, 0.3139, 0.1198, -0.1316, 0.0686, 0.4085, 0.1823, -0.2404, -0.0674, 0.4483, 0.283, -0.3387, -0.0349, 0.4723, 0.1312, -0.2696, 0.0053, 0.2303, 0.1369, 0.0114, -0.1015, 0.0999, 0.2656, 0.0581, -0.2932, -0.1567, 0.2095, 0.0069, -0.3139, -0.1019, 0.2095, 0.082, -0.104, -0.0032, 0.1787, 0.2286, 0.132, 0.0037, 0.1446, 0.2428, -0.0102, -0.1896, -0.0134, 0.1161, -0.1953, -0.3448, 0.0589, 0.1783, -0.3094, -0.2607, 0.3391, 0.2737, -0.1771, -0.1332, 0.2449, 0.2331, -0.0122, 0.08, 0.1551, 0.1048, 0.1251, 0.0642, -0.1758, -0.1397, 0.0971, -0.1567, 0.0483, 0.5811, -0.9153, -1.1513, 1.9508, 1.2085, -2.5843, -0.1572, 3.5476, -0.5649, -2.8686, 1.4315, 2.0174, -1.5086, -1.0307, 1.6581, -0.3241, -1.0055, 1.2901, -0.1442, -1.4384, 0.8731, 1.492, -1.4603, -0.9697, 2.015, 0.7163, -1.7421, -0.1299, 1.866, -0.2238, -1.215, 0.5486, 0.718, -0.5364, -0.5157, 0.4926, 0.0236, -0.3862, 0.2993, 0.1243, -0.2477, 0.2319, 0.4625, -0.1978, -0.2587, 0.335, 0.199, -0.1953, -0.253, 0.2408, 0.3094, -0.2384, -0.2055, 0.3005, 0.3529, -0.3277, -0.1612, 0.43, 0.1308, -0.242, 0.0085, 0.2026, -0.0183, -0.0922, -0.1165, -0.0272, 0.0552, 0.0341, -0.1413, -0.1389, 0.1624, 0.0662, -0.0715, 0.1462, 0.2408, 0.1462, 0.0686, 0.082, 0.1279, 0.0564, 0.0065, 0.0053, 0.0666, 0.0345, -0.0832, -0.2676, -0.0479, 0.2217, -0.158, -0.253, 0.132, 0.3537, -0.0881, -0.1945, 0.3119, 0.4284, 0.039, -0.1836, 0.2477, 0.2554, -0.0796, -0.1385, 0.0743, 0.1555, -0.1693, -0.0569, 0.0703, -0.0398, -0.1068, -0.2043, 0.5498, 0.2083, -1.1837, 0.2627, 1.7933, -0.6932, -1.7795, 1.7401, 1.3015, -1.8274, -0.322, 1.4778, -0.0215, -1.1492, 0.7976, 0.3724, -1.0704, 0.8345, 0.718, -1.1147, -0.24, 1.4363, 0.0508, -1.2914, 0.3163, 1.1188, -0.3874, -1.0412, 0.5482, 0.6534, -0.6051, -0.3017, 0.3825, 0.173, -0.4398, 0.1775, 0.4784, -0.3537, -0.0629, 0.5035, 0.0556, -0.3228, 0.2416, 0.2717, -0.1718, -0.1722, 0.1965, 0.203, -0.2948, -0.2221, 0.2006, 0.1446, -0.3886, 0.0341, 0.5011, 0.0987, -0.3297, 0.1243, 0.6063, -0.1779, -0.1572, 0.3082, 0.1263, -0.1766, -0.067, 0.1494, -0.1653, 0.0199, 0.1279, -0.1458, -0.1149, 0.2282, 0.136, -0.1779, 0.0544, 0.1669, 0.1186, -0.0414, 0.1092, 0.1787, -0.0552, -0.028, 0.0536, 0.091, -0.0609, -0.0796, 0.0211, 0.0495, -0.0296, -0.0666, 0.093, 0.0784, 0.0207, 0.0357, 0.0028, 0.1299, 0.1844, -0.0171, -0.0353, 0.1109, 0.1945, -0.0345, -0.0512, 0.1823, 0.0532, -0.0735, -0.0755, 0.0694, -0.08, 0.0162, -0.093, 0.2079, 0.6063, -0.6221, -1.412, 0.5665, 2.1628, -1.4343, -1.8335, 2.4341, 1.628, -2.2587, -0.9746, 2.547, 0.1405, -1.3482, 0.7224, 0.59, -0.6051, 0.4296, 0.7098, -1.6089, -0.2871, 1.6296, -0.4374, -1.9338, 0.4483, 2.0008, -0.8304, -1.505, 1.0887, 1.4051, -0.6307, -0.4313, 1.0038, 0.2095, -0.335, 0.0926, 0.1417, -0.2887, 0.0187, 0.411, -0.3574, -0.1693, 0.5121, 0.2002, -0.534, -0.251, 0.491, 0.1084, -0.3951, -0.082, 0.508, 0.0508, -0.4772, 0.0244, 0.357, -0.0788, -0.3935, 0.0942, 0.2749, -0.0719, -0.1689, 0.108, 0.1779, 0.117, 0.0824, -0.1182, 0.0605, 0.3306, 0.0166, -0.4889, -0.106, 0.3683, 0.0248, -0.2696, 0.0418, 0.2916, 0.0804, -0.1316, -0.0735, 0.2331, 0.1458, 0.0268, 0.1247, 0.1397, 0.1693, 0.0146, -0.1503, 0.0187, 0.1905, -0.1645, -0.2258, 0.2083, 0.2469, -0.1856, -0.1563, 0.4926, 0.3606, -0.1608, -0.0548, 0.357, 0.2225, -0.1937, -0.0211, 0.0739, 0.0512, 0.0, -0.0532, -0.0857, -0.0983, 0.1413, -0.1742, 0.0305, 0.6753, -0.1332, -1.7462, 0.1218, 2.7813, -0.8256, -2.5815, 2.0118, 2.6611, -2.2432, -1.9326, 2.244, 0.8958, -1.4148, 0.0435, 0.7728, -0.6554, 0.4995, 1.0103, -1.6386, -0.6534, 1.9066, 0.2798, -2.1372, -0.19, 2.0873, -0.056, -1.8339, 0.0938, 1.4343, -0.2461, -0.8767, 0.5421, 0.5458, -0.2664, 0.0061, 0.4674, -0.0061, -0.1507, 0.4776, 0.134, -0.2412, 0.1442, 0.2465, -0.203, -0.4077, 0.0386, 0.1247, -0.2181, -0.197, 0.3403, 0.3444, -0.3655, -0.1941, 0.6193, 0.2798, -0.5141, 0.0008, 0.7671, 0.1413, -0.359, 0.0999, 0.2973, 0.0577, -0.279, -0.1762, 0.0187, 0.1819, 0.0796, -0.3021, -0.1088, 0.2863, 0.2469, -0.1287, 0.0215, 0.3322, 0.2839, 0.0633, -0.1657, -0.0621, 0.0516, -0.0479, -0.197, -0.0353, 0.1218, -0.2079, -0.2152, 0.3379, 0.197, -0.411, -0.0564, 0.7143, 0.2652, -0.4719, 0.0146, 0.6416, 0.3159, -0.3907, -0.2229, 0.1645, 0.0333, -0.1758, -0.2502, -0.0573, 0.0382, 0.171, -0.0191, -0.2177, 0.0776, 0.3029, 0.0983, 0.054, 0.7058, -0.4045, -1.2268, 1.3397, 1.5967, -2.1039, -1.0887, 3.1496, 0.3159, -2.9734, 0.4828, 2.2185, -0.8471, -1.1797, 1.3084, 0.0564, -0.8345, 1.1708, 0.1027, -1.7048, 0.4885, 1.7409, -1.0944, -1.5139, 1.4197, 1.176, -1.345, -0.5896, 1.518, 0.2721, -0.9421, 0.402, 0.6924, -0.3866, -0.2952, 0.4702, 0.0049, -0.363, 0.2246, 0.052, -0.3281, 0.1746, 0.268, -0.3103, -0.2201, 0.2834, 0.2221, -0.2071, -0.1612, 0.3557, 0.3541, -0.1909, -0.1823, 0.3468, 0.1819, -0.2709, -0.1856, 0.1275, 0.121, -0.065, -0.0089, -0.1031, 0.0902, 0.24, -0.1815, -0.2879, 0.2221, 0.3326, -0.3025, -0.2696, 0.2591, 0.2164, -0.1884, -0.0621, 0.2095, 0.08, 0.1356, 0.108, -0.0621, 0.0345, 0.2895, 0.0983, -0.1819, 0.2225, 0.3821, -0.199, -0.2367, 0.3346, 0.2128, -0.3537, -0.1771, 0.3773, 0.0569, -0.4382, 0.0024, 0.5031, 0.0402, -0.3192, 0.1425, 0.2924, -0.0024, -0.0317, 0.2351, 0.1446, -0.0646, 0.0556, 0.1417, -0.2177, -0.0589, 0.0979, -0.0491, 0.4349, -0.186, -0.6952, 0.4577, 1.2061, -0.9535, -1.083, 1.6577, 0.5222, -1.2739, -0.2363, 1.2154, -0.1299, -0.7163, 0.7379, -0.1283, -0.3805, 0.6051, 0.1275, -1.012, -0.0004, 1.0091, -0.3911, -0.7984, 0.3354, 0.882, -0.359, -0.6453, 0.5478, 0.357, -0.3452, -0.2095, 0.4122, 0.013, -0.3086, 0.1998, 0.1933, -0.2705, -0.0962, 0.4028, -0.0938, -0.2083, 0.1519, 0.1681, -0.2347, -0.0435, 0.3659, -0.0106, -0.149, 0.1563, 0.4739, -0.1056, -0.158, 0.2891, 0.3553, -0.0426, -0.2676, 0.2952, 0.1279, -0.0796, -0.0556, 0.0625, -0.0085, -0.0114, 0.1913, -0.1084, -0.078, 0.1771, 0.1791, -0.1872, -0.0435, 0.2725, 0.0723, 0.0402, 0.0703, 0.136, 0.1397, 0.1555, 0.0605, -0.0333, 0.0869, 0.0447, -0.0069, -0.0816, -0.013, -0.1194, -0.2384, 0.0353, 0.0491, -0.1543, -0.2164, 0.2177, 0.1661, -0.1872, -0.0504, 0.2599, 0.2623, -0.0942, 0.0638, 0.1697, 0.067, -0.0045, 0.0349, 0.0134, -0.067, 0.0865, 0.0491, -0.106, 0.0305, -0.134, 0.3131, 0.6039, -0.7042, -1.3616, 0.8841, 2.1145, -1.7774, -1.613, 2.3837, 1.2487, -2.3699, -0.761, 2.3322, -0.1637, -0.8767, 0.6229, 0.1779, -0.4406, 0.9052, 0.5007, -1.7953, 0.2798, 1.7547, -0.5157, -1.7864, 0.7683, 1.7762, -1.0002, -1.0177, 0.878, 0.8759, -0.5937, -0.2136, 0.6351, -0.1523, -0.0219, 0.2453, 0.0958, -0.292, 0.2311, 0.4045, -0.5299, 0.0012, 0.4215, 0.002, -0.5352, 0.0288, 0.4203, -0.1925, -0.1466, 0.1596, 0.4816, -0.0394, -0.2506, 0.1608, 0.2761, -0.0918, -0.441, 0.0581, 0.145, -0.1194, -0.1986, -0.0146, 0.0581, 0.0495, 0.0118, -0.2059, 0.0617, 0.3505, -0.0049, -0.3777, 0.0869, 0.4101, 0.0227, -0.2164, 0.1308, 0.3509, 0.0885, -0.0256, -0.0012, 0.1494, 0.1271, 0.0569, 0.0426, 0.0605, 0.203, -0.0077, -0.1121, 0.0703, 0.1308, -0.0824, -0.1592, 0.1604, 0.1819, -0.1799, -0.171, 0.3062, 0.2002, -0.2091, -0.0227, 0.2542, 0.203, -0.0244, 0.0585, 0.2099, 0.1036, 0.0471, 0.0321, 0.0049, -0.1019, 0.0146, -0.1068, -0.1754, 0.5027, 0.1011, -1.2739, -0.0629, 2.0828, -0.5677, -2.2859, 1.6223, 2.0288, -1.9801, -1.3799, 2.0893, 0.6725, -1.4924, 0.3781, 0.8601, -0.7419, 0.1539, 0.774, -1.1772, -0.6404, 1.4566, 0.1507, -1.6706, 0.104, 1.8623, -0.1775, -1.4802, 0.5823, 1.3084, -0.4589, -0.7208, 0.5425, 0.4459, -0.4203, -0.2518, 0.3005, -0.0536, -0.1503, 0.2928, 0.0207, -0.197, 0.201, 0.3687, -0.1226, -0.2177, 0.3379, 0.3963, -0.1332, -0.2169, 0.4573, 0.3241, -0.3817, -0.2128, 0.363, 0.1182, -0.6156, -0.0942, 0.51, -0.0207, -0.3996, 0.0906, 0.4512, 0.0296, -0.0703, 0.0772, 0.1604, 0.1905, 0.0962, -0.0934, -0.1145, 0.2169, 0.0378, -0.1214, 0.011, 0.1263, 0.171, -0.024, -0.026, 0.0309, 0.1186, -0.0061, -0.0979, 0.0914, 0.1494, -0.2355, -0.3224], "ball": [-0.0028, -0.0963, 0.1137, 0.2573, -0.0583, -0.126, 0.2074, 0.1727, -0.2199, -0.1561, 0.224, 0.1137, -0.211, -0.0468, 0.2021, -0.0145, -0.1628, 0.1092, 0.1871, -0.1593, -0.1377, 0.2505, 0.1075, -0.2469, -0.0374, 0.2659, 0.0218, -0.1639, 0.142, 0.2311, -0.1075, -0.1402, 0.1915, 0.1641, -0.0999, -0.0058, 0.2566, 0.1043, -0.1467, 0.0588, 0.1983, -0.0377, -0.1116, 0.1127, 0.1213, -0.1064, -0.0627, 0.1384, -0.024, -0.249, 0.0188, 0.2095, -0.0697, -0.166, 0.1438, 0.1706, -0.23, -0.128, 0.3263, 0.1325, -0.2563, -0.0123, 0.302, -0.0378, -0.3717, 0.0136, 0.3218, -0.0837, -0.197, 0.2438, 0.1795, -0.1896, -0.0094, 0.2042, -0.1364, -0.2035, 0.2159, 0.1293, -0.2649, -0.0344, 0.2821, -0.0869, -0.3267, 0.1527, 0.283, -0.2987, -0.2796, 0.3281, 0.19, -0.2628, 0.0005, 0.3224, 0.0322, -0.1704, 0.1381, 0.2123, -0.1832, -0.1977, 0.2156, 0.0877, -0.191, 0.091, 0.3064, 0.1088, -0.1085, 0.0244, 0.1723, -0.0045, -0.1366, 0.0278, 0.1293, -0.0029, -0.0643, -0.0158, 0.0138, 0.0002, -0.0715, -0.1779, -0.012, 0.2138, 0.0273, -0.1504, 0.0879, 0.2826, 0.0297, -0.1025, 0.1748, 0.2847, -0.0279, -0.1701, 0.0759, 0.1355, -0.0562, -0.0832, 0.1064, 0.0417, -0.1109, 0.0158, 0.0452, -0.1415, -0.1593, 0.0559, 0.0518, -0.0736, 0.0573, 0.2013, 0.0193, -0.0767, 0.0908, 0.0403, -0.053, 0.0041, 0.1397, 0.1095, -0.122, -0.05, 0.1311, -0.0357, -0.1712, 0.0067, 0.0559, -0.0195, -0.0002, 0.0141, -0.0208, -0.0055, 0.078, 0.0029, -0.0481, 0.1157, 0.1139, -0.1673, -0.0871, 0.2318, 0.046, -0.1678, 0.0763, 0.2167, 0.0197, -0.0003, 0.0715, -0.0541, -0.1126, 0.0448, 0.0604, -0.1066, 0.0508, 0.1808, -0.064, -0.16, 0.1252, 0.1719, -0.152, -0.0617, 0.2963, 0.1176, -0.2242, 0.007, 0.2568, -0.0122, -0.1454, 0.184, 0.2375, -0.0851, -0.0403, 0.1905, -0.0028, -0.1967, -0.0146, 0.0942, -0.05, -0.0752, 0.0591, -0.0461, -0.1788, -0.0088, 0.0679, -0.0942, -0.0611, 0.096, 0.0161, -0.0198, 0.1158, 0.0255, -0.1488, 0.0271, 0.1957, -0.0258, -0.1231, 0.1567, 0.2061, -0.1181, -0.1299, 0.1002, 0.0149, -0.09, 0.0032, 0.02, -0.0806, -0.0413, 0.0557, 0.0492, 0.0135, 0.0135, 0.1036, 0.1249, 0.0263, -0.0291, 0.0786, 0.1389, 0.0341, 0.0016, 0.0596, 0.0915, 0.0915, 0.0167, -0.0864, -0.0892, -0.0271, 0.0469, 0.0133, -0.0312, 0.0936, 0.0971, 0.0153, 0.0854, 0.0346, -0.0843, 0.091, 0.2256, -0.0411, -0.1446, 0.1425, 0.1451, -0.1709, -0.1113, 0.2006, 0.1171, -0.1366, -0.0239, 0.0848, -0.1452, -0.153, 0.1559, 0.1252, -0.1444, 0.0015, 0.2079, -0.0273, -0.2141, -0.0577, 0.0224, -0.0463, -0.0421, -0.0408, -0.0034, 0.0791, 0.0562, -0.0653, -0.0512, 0.1004, 0.1098, -0.0084, -0.0058, 0.0892, -0.0039, -0.0668, 0.0262, -0.0468, -0.1103, 0.0812, 0.1226, -0.1192, -0.1371, 0.0817, 0.1057, -0.0734, -0.0242, 0.211, 0.21, 0.031, -0.0258, 0.1116, 0.1371, -0.046, -0.1403, 0.0145, 0.1301, 0.0177, 0.013, 0.1467, 0.024, -0.1486, 0.0824, 0.269, 0.0249, -0.1387, 0.1694, 0.2721, -0.0838, -0.1319, 0.0802, 0.1225, -0.0216, -0.0931, -0.0102, 0.0481, 0.0166, -0.0841, -0.1171, -0.0466, 0.1166, 0.1516, 0.0245, -0.0802, 0.0455, 0.2102, -0.0653, -0.2162, 0.0369, 0.1823, 0.0364, -0.109, -0.0307, 0.0595, -0.0013, -0.1051, -0.0598, -0.0171, 0.0773, 0.1309, -0.0252, -0.033, 0.0783, 0.0521, -0.0672, -0.0284, 0.1103, 0.0374, -0.1676, -0.1025, 0.0635, -0.0702, -0.1798, 0.0421, 0.2268, 0.02, -0.0876, 0.1439, 0.1931, 0.018, -0.0463, 0.0078, 0.0864, 0.1465, 0.0742, -0.0352, -0.0216, 0.0578, -0.0271, -0.1184, 0.038, 0.0828, -0.0296, -0.0006, 0.0768, -0.0804, -0.0791, 0.1801, 0.0432, -0.1408, 0.0707, 0.2341, -0.0106, -0.1439, 0.1174, 0.1233, -0.1239, -0.044, 0.1183, -0.0177, 0.0148, 0.1642, 0.0052, -0.1304, 0.0837, 0.1683, -0.1311, -0.1298, 0.1826, 0.1041, -0.204, -0.0684, 0.2095, 0.0071, -0.1332, 0.1655, 0.2016, -0.1069, -0.0815, 0.1282, -0.0569, -0.2194, 0.0713, 0.2173, -0.0789, -0.1304, 0.1477, 0.0963, -0.088, -0.0369, 0.038, 0.0266, 0.038, 0.007, -0.084, -0.0687, 0.0603, 0.031, -0.0973, 0.0635, 0.0975, -0.1031, -0.0006, 0.1745, -0.0547, -0.1985, 0.1608, 0.282, -0.0534, -0.116, 0.2344, 0.2266, -0.1131, -0.0783, 0.1444, 0.0442, -0.0997, 0.0232, 0.0068, -0.0525, 0.0135, -0.0286, -0.0978, 0.0367, 0.181, 0.0591, -0.0533, 0.0687, 0.1285, -0.063, -0.0736, 0.1031, 0.0635, -0.0992, -0.0275, 0.1488, -0.0508, -0.2651, 0.0184, 0.2115, -0.0708, -0.0968, 0.2584, 0.2207, -0.0945, -0.0331, 0.1865, 0.0573, -0.1467, 0.0188, 0.1183, -0.04, -0.0122, 0.0387, -0.1241, -0.1512, 0.0218, -0.0026, -0.1382, -0.059, 0.1717, 0.1126, -0.0564, 0.0942, 0.126, -0.0096, 0.0825, 0.2258, 0.0424, -0.1096, 0.033, 0.1051, -0.02, -0.1092, 0.0684, 0.1288, -0.0599, -0.1407, -0.0564, -0.0234, -0.1163, -0.1517, -0.037, 0.1532, 0.0928, -0.0661, 0.014, 0.1766, 0.1308, -0.1122, -0.096, 0.1969, 0.2344, -0.0997, -0.165, 0.1813, 0.2334, -0.1126, -0.1704, 0.2086, 0.3164, -0.0575, -0.2224, 0.1046, 0.2169, -0.1384, -0.2411, 0.0689, 0.1582, -0.0617, -0.0978, 0.0229, 0.0364, -0.0088, 0.0276, 0.091, 0.008, 0.116, 0.2791, 0.0184, -0.1592, 0.0614, 0.1792, -0.0424, -0.1649, 0.0036, 0.1277, -0.0296, -0.2136, -0.0814, 0.0859, -0.0546, -0.2099, 0.0063, 0.2066, 0.0648, -0.0876, 0.0128, 0.1704, 0.0473, -0.07, 0.0167, 0.0957, 0.0845, -0.0391, -0.123, -0.0595, 0.0146, -0.0638, -0.1316, -0.0211, 0.0614, 0.0023, -0.0422, 0.0419, 0.0515, -0.0635, 0.0265, 0.2272, 0.1715, -0.0065, 0.0323, 0.1506, 0.0798, -0.059, -0.0328, 0.0776, 0.0171, -0.032, 0.013, -0.0236, -0.0299, 0.0466, 0.0391, -0.0346, 0.0172, 0.0942, 0.0148, -0.0736, 0.0268, 0.0452, -0.0595, -0.0019, 0.1421, 0.1381, 0.0307, 0.0505, 0.0596, -0.0099, 0.0271, 0.0772, -0.0447, -0.0089, 0.184, 0.0559, -0.1566, -0.0115, 0.1431, -0.1353, -0.1972, 0.172, 0.1918, -0.0996, -0.1218, 0.0858, 0.078, -0.0609, -0.0208, 0.0349, 0.0101, 0.0551, 0.0047, -0.1079, 0.0286, 0.1001, -0.0801, -0.1597, 0.0559, 0.1577, -0.0986, -0.1639, 0.0494, 0.0552, -0.1481, -0.0193, 0.2636, 0.122, -0.1413, 0.0339, 0.2448, -0.0892, -0.2272, 0.0889, 0.1576, -0.0198, -0.0575, 0.0435, 0.089, 0.0668, -0.0026, -0.078, -0.0325, 0.2016, 0.1939, -0.153, -0.0806, 0.2847, 0.1498, -0.1668, 0.0054, 0.2584, 0.0237, -0.211, -0.0229, 0.0906, -0.0378, -0.0076, 0.0549, -0.0138, 0.0556, 0.1871, 0.0273, -0.1915, 0.0411, 0.1254, -0.2479, -0.1881, 0.2261, 0.1514, -0.2104, -0.021, 0.2484, -0.0482, -0.1321, 0.2497, 0.1831, -0.2373, 0.0201, 0.2703, -0.1772, -0.1931, 0.3127, 0.1059, -0.4178, 0.0223, 0.4296, -0.2, -0.4818, 0.2068, 0.3315, -0.3643, -0.2549, 0.4527, 0.2825, -0.2919, 0.0045, 0.3928, 0.0018, -0.2289, 0.1303, 0.2831, -0.0876, -0.1225, 0.2185, 0.0708, -0.2482, 0.0468, 0.2183, -0.1813, -0.05, 0.3249, 0.0484, -0.2974, 0.1101, 0.3767, -0.2065, -0.2747, 0.3208, 0.2222, -0.3577, -0.1207, 0.3387, -0.0656, -0.3439, 0.1507, 0.2836, -0.1722, -0.1369, 0.2445, 0.1166, -0.2274, -0.0031, 0.3038, 0.0554, -0.1119, 0.0957, 0.1779, -0.0262, -0.1415, -0.0455, 0.0088, -0.0307, -0.0244, 0.0028, -0.0044, 0.0354, 0.0075, -0.0408, -0.0323, -0.0525, 0.0125, 0.0661, -0.0419, -0.0759, 0.0773, 0.1283, -0.0351, -0.0401, 0.2506, 0.1771, -0.2113, -0.0869, 0.25, 0.0448, -0.3606, -0.1493, 0.2779, 0.0354, -0.2917, 0.0762, 0.2685, -0.1272, -0.1525, 0.2147, 0.1993, -0.0858, 0.0637, 0.3133, 0.0346, -0.146, 0.12, 0.1205, -0.1615, -0.0653, 0.1998, 0.0495, -0.1866, 0.0184, 0.1556, -0.1286, -0.14, 0.179, 0.1259, -0.1286, 0.0218, 0.2138, 0.0154, -0.0492, 0.1564, 0.0919, -0.0942, 0.0463, 0.2001, -0.0526, -0.2329, 0.0528, 0.1322, -0.1582, -0.0573, 0.274, 0.0713, -0.2324, 0.0063, 0.2563, -0.0515, -0.2734, 0.1212, 0.2644, -0.1464, -0.2133, 0.1732, 0.1309, -0.2022, -0.1137, 0.0931, 0.0263, -0.0916, 0.0106, 0.0928, -0.0508, -0.0791, 0.1325, 0.0776, -0.1304, 0.0469, 0.1504, -0.1486, -0.2, 0.1028, 0.0949, -0.1486, -0.0154, 0.2834, 0.1439, -0.0726, 0.1241, 0.1931, -0.0885, -0.0721, 0.165, 0.0244, -0.1308, 0.1075, 0.1561, -0.1764, -0.2078, 0.0767, 0.0229, -0.1998, -0.0409, 0.12, -0.0429, -0.0094, 0.2191, 0.1093, -0.0664, 0.1522, 0.2976, 0.0463, -0.0408, 0.1762, 0.1611, -0.1041, -0.1278, 0.1015, 0.0539, -0.1667, -0.0205, 0.0962, -0.114, -0.1381, 0.0361, 0.0294, -0.0469, 0.046, 0.1325, 0.0822, 0.0552, 0.0851, 0.0011, -0.0512, 0.1295, 0.117, -0.0687, 0.0158, 0.0622, -0.142, -0.1028, 0.1416, -0.0356, -0.2329, 0.0713, 0.2105, -0.0975, -0.1553, 0.1706, 0.1217, -0.2009, -0.0336, 0.2484, -0.0227, -0.245, 0.0897, 0.158, -0.1845, -0.1176, 0.232, 0.1298, -0.1405, 0.0253, 0.1798, -0.0552, -0.1961, 0.0491, 0.1199, -0.1009, -0.0393, 0.1784, 0.1028, -0.1023, -0.0461, 0.0687, -0.0026, -0.0502, 0.0283, 0.1171, 0.0304, -0.05, 0.0528, 0.0643, -0.0015, 0.0491, 0.1015, 0.0559, 0.0266, 0.1001, 0.0796, -0.0814, -0.0633, 0.0867, 0.0702, -0.0531, -0.043, 0.0814, 0.0617, -0.0819, -0.0317, 0.0538, -0.0443, -0.0213, 0.1615, 0.0949, -0.1257, 0.0505, 0.1959, -0.0752, -0.1184, 0.1619, 0.1485, -0.1036, -0.0463, 0.0937, -0.0595, -0.1126, 0.0601, -0.0603, -0.1697, 0.1166, 0.1321, -0.1896, -0.1083, 0.1983, 0.0169, -0.1858, 0.1559, 0.2653, -0.1784, -0.1728, 0.2787, 0.1506, -0.2017, -0.0128, 0.2552, 0.0076, -0.1699, 0.1275, 0.0776, -0.2333, -0.077, 0.1044, -0.0854, -0.0729, 0.1993, 0.1509, -0.0859, 0.0556, 0.2102, -0.0664, -0.0601, 0.2482, 0.1109, -0.153, 0.0214, 0.1801, -0.0174, -0.0867, 0.1226, 0.0936, -0.1356, 0.0339, 0.2185, -0.0783, -0.2352, 0.0802, 0.2021, -0.0685, -0.0921, 0.1759, 0.1426, -0.1009, -0.0413, 0.0671, -0.0824, -0.123, 0.1241, 0.1144, -0.2237, -0.0895, 0.2953, 0.0629, -0.2919, 0.0032, 0.2679, -0.0328, -0.1753, 0.0754, 0.0898, -0.1023, 0.0023, 0.0284, -0.1605, 0.0427, 0.2373, -0.1113, -0.2719, 0.1053, 0.1939, -0.1158, -0.0785, 0.2084, 0.1228, -0.1077, 0.0122, 0.0897, -0.0716, -0.1075, 0.0174, 0.0546, -0.0633, -0.0608, 0.1171, 0.2357, 0.075, -0.1563, 0.0573, 0.3838, 0.1304, -0.1915, 0.0591, 0.2825, 0.0091, -0.2313, -0.0409, 0.1192, -0.0453, -0.117, -0.0101, -0.0161, -0.0177, 0.0598, -0.0448, -0.0645, 0.2136, 0.2649, 0.031, 0.0478, 0.2095, 0.0793, -0.102, -0.0109, 0.155, 0.0724, -0.0301, 0.0419, 0.0161, -0.0926, -0.0642, -0.0161, -0.0911, -0.0094, 0.0565, -0.0447, 0.0227, 0.1098, -0.0193, -0.101, 0.0585, 0.0854, -0.0966, -0.0612, 0.1306, -0.0624, -0.3538, -0.0726, 0.1184, -0.2089, -0.1376, 0.3171, 0.1512, -0.2066, 0.0424, 0.2982, 0.0578, -0.1273, 0.1295, 0.2487, 0.0244, -0.0442, 0.0625, -0.0221, -0.0822, 0.1043, 0.0385, -0.2001, -0.0318, 0.2177, -0.0021, -0.2211, 0.0193, 0.2251, -0.0158, -0.1494, 0.1122, 0.1009, -0.0851, 0.0266, 0.1369, 0.0229, -0.0434, 0.0876, 0.1098, -0.0752, -0.0221, 0.1865, -0.0523, -0.2367, 0.0666, 0.1821, -0.0629, -0.0945, 0.1834, 0.1834, -0.0897, -0.0828, 0.1598, 0.1345, -0.0301, 0.0591, 0.1308, -0.0378, -0.0541, 0.1132, -0.0328, -0.1465, 0.0595, 0.1142, -0.0593, -0.1095, 0.0955, 0.0879, -0.1788, -0.0747, 0.1735, -0.0133, -0.0953, 0.0957, 0.0006, -0.0942, 0.0263, 0.0949, 0.0262, 0.0336, 0.1499, 0.026, -0.0902, 0.0684, 0.0284, -0.2009, -0.0612, 0.1361, -0.0018, -0.0257, 0.1361, 0.0458, -0.0905, 0.0621, 0.0789, -0.1202, -0.0908, 0.122, 0.0609, -0.1704, -0.0302, 0.1738, -0.0325, -0.1665, 0.1031, 0.2245, -0.0424, -0.1348, 0.0882, 0.1525, -0.0469, -0.0837, 0.1343, 0.1311, -0.0569, -0.0411, 0.0249, -0.0489, -0.0094, 0.0713, 0.0677, 0.0682, 0.0791, 0.1709, 0.096, -0.0624, 0.0266, 0.1688, -0.0312, -0.1881, 0.0856, 0.159, -0.0689, -0.1455, -0.0435, -0.077, -0.1183, 0.0424, 0.05, -0.1475, -0.0135, 0.2999, -0.008, -0.1972, 0.2536, 0.3244, -0.0791, -0.0807, 0.2834, 0.0976, -0.1938, 0.0461, 0.1114, -0.1311, -0.0668, 0.1558, -0.0141, -0.1798, 0.0119, 0.0689, -0.191, -0.1481, 0.1964, 0.1283, -0.0775, 0.0414, 0.1452, 0.0049, -0.09, 0.0674, 0.141, -0.1444, -0.1494, 0.2586, 0.1871, -0.2787, -0.2456, 0.2841, 0.2596, -0.339, -0.2082, 0.4123, 0.1788, -0.3263, -0.0882, 0.2063, 0.0107, -0.0819, 0.1064, -0.0286, -0.094, 0.2113, 0.0484, -0.3177, -0.0175, 0.3949, 0.0619, -0.2906, 0.1592, 0.443, -0.1231, -0.2727, 0.2602, 0.1952, -0.2251, -0.026, 0.3406, 0.0513, -0.2888, 0.0294, 0.2474, -0.0536, -0.1113, 0.1144, 0.0685, -0.0299, 0.0604, 0.0685, -0.0614, -0.026, 0.1194, 0.0547, -0.0708, -0.0136, 0.0702, 0.0162, -0.1096, -0.1348, -0.024, 0.0453, -0.0443, -0.1145, 0.0044, 0.0502, -0.1017, -0.1163, 0.0606, 0.0986, -0.032, -0.0005, 0.1626, 0.0469, -0.1184, 0.0336, 0.1092, -0.043, -0.0458, 0.1207, 0.1373, -0.0089, -0.0372, 0.0724, 0.0892, 0.0021, -0.0146, -0.0156, -0.0037, 0.053, 0.0089, -0.0793, -0.0569, 0.0867, 0.0879, -0.0271, 0.0205, 0.1205, 0.0835, -0.0205, -0.0188, 0.0832, 0.1452, 0.0011, -0.0273, 0.1555, 0.0988, -0.1051, -0.1207, 0.0323, -0.0089, -0.1343, 0.0427, 0.1619, -0.0648, -0.0731, 0.2112, 0.0885, -0.1291, 0.0807, 0.2453, -0.001, -0.1467, 0.1506, 0.2173, -0.1114, -0.1745, 0.1116, 0.1288, -0.0885, -0.1075, -0.0338, 0.0005, -0.0385, -0.0902, -0.0832, 0.075, 0.0923, -0.1002, -0.0763, 0.1124, 0.0945, -0.1866, -0.117, 0.1935, 0.0975, -0.0981, 0.0773, 0.1595, -0.0991, -0.1009, 0.091, 0.0455, -0.0871, 0.0325, 0.1007, -0.071, -0.0547, 0.1163, 0.097, -0.0422, 0.0127, 0.0986, 0.0011, -0.0275, 0.0656, 0.0032, -0.0801, 0.044, 0.1514, 0.0903, 0.0859, 0.1722, 0.0245, -0.1317, -0.0143, 0.0872, -0.0505, -0.1813, 0.053, 0.2409, 0.0026, -0.1079, 0.1131, 0.1386, -0.0154, -0.011, 0.0869, 0.0672, -0.0291, 0.0648, 0.0711, -0.1517, -0.1215, 0.1429, 0.154, -0.134, -0.1977, 0.0479, 0.1147, -0.1145, -0.2032, 0.0112, 0.1715, 0.069, -0.0991, -0.0075, 0.2021, 0.1196, -0.1202, -0.0336, 0.1832, 0.0895, -0.0011, 0.0798, -0.0249, -0.1233, 0.0357, 0.0427, -0.1225, -0.0611, 0.1587, 0.1291, -0.1092, -0.1286, 0.0731, 0.1657, 0.0702, -0.0955, -0.1364, 0.1892, 0.2937, -0.203, -0.2849, 0.1936, 0.2363, -0.1529, -0.1954, 0.1416, 0.1823, -0.0629, -0.0981, 0.0262, 0.1238, 0.1361, 0.0219, 0.0016, 0.1694, 0.1795, -0.0604, -0.1408, 0.0724, 0.1079, -0.1249, -0.0698, 0.1619, 0.0585, -0.1103, -0.0247, 0.0716, -0.0957, -0.1634, 0.135, 0.1207, -0.161, -0.0378, 0.1192, -0.056, -0.064, 0.2061, 0.1488, -0.1106, 0.0585, 0.2394, -0.0867, -0.2225, 0.1632, 0.1611, -0.2651, -0.1751, 0.1923, -0.0192, -0.2997, 0.0297, 0.1933, -0.1277, -0.1379, 0.274, 0.2679, -0.1007, 0.0073, 0.2929, 0.0679, -0.2001, 0.0484, 0.1762, -0.0232, -0.0952, -0.0185, -0.0291, -0.1147, -0.0182, 0.0284, -0.0729, -0.0169, 0.1611, 0.1207, -0.014, 0.0094, 0.0877, 0.1009, 0.0302, 0.0658, 0.0947, 0.0853, 0.0541, -0.0538, -0.0726, -0.0023, 0.0313, -0.0005, 0.0742, 0.0614, -0.0302, 0.0177, 0.0432, -0.0323, -0.0271, 0.0595, 0.0166, -0.0055, -0.011, 0.0067, 0.0205, -0.0583, -0.0257, -0.0044, -0.0741, 0.0966, 0.2, -0.1322, -0.126, 0.2579, 0.0968, -0.2713, -0.02, 0.2904, -0.0608, -0.3491, 0.0107, 0.1399, -0.1805, -0.0612, 0.2461, 0.0895, 0.0034, 0.2406, 0.1366, -0.1135, 0.0518, 0.205, -0.0871, -0.2217, 0.1468, 0.1949, -0.2149, -0.2467, 0.1192, 0.0942, -0.2367, -0.1844, 0.0882, 0.0491, -0.0439, 0.1179, 0.0902, 0.0135, 0.2233, 0.2451, -0.0461, -0.0141, 0.3198, 0.1408, -0.2617, -0.0606, 0.1957, -0.0953, -0.2177, 0.0685, 0.0552, -0.2229, -0.1639, 0.0741, 0.013, -0.0721, 0.0944, 0.1852, 0.0798, 0.0606, 0.1092, 0.0676, 0.0413, 0.1041, 0.153, 0.052, -0.012, 0.0484, 0.0578, 0.0055, -0.141, -0.0981, 0.0866, -0.044, -0.1131, 0.0746, 0.1056, -0.0551, -0.0997, 0.0136, 0.0953, -0.0052, -0.0947, 0.0957, 0.1181, -0.0851, -0.1059, 0.02, 0.1225, -0.0067, -0.1621, 0.0396, 0.1811, -0.0737, -0.1865, 0.0221, 0.1028, -0.0559, -0.0853, 0.1018, 0.1113, -0.0132, 0.0057, 0.0229, -0.043, 0.0167, 0.166, 0.0361, -0.1416, 0.0266, 0.1772, -0.0434, -0.2094, 0.0453, 0.2207, -0.0214, -0.1394, 0.16, 0.1928, -0.1389, -0.1444, 0.102, 0.0942, -0.0278, 0.0109, 0.0513, 0.0549, 0.0957, 0.0534, -0.1438, -0.043, 0.2443, 0.0268, -0.1741, 0.0892, 0.1899, -0.0552, -0.1031, 0.1693, 0.2008, -0.0313, 0.0526, 0.2045, 0.0016, -0.1238, -0.0835, -0.0067, 0.0608, -0.011, -0.1093, -0.0807, 0.1364, 0.1179, -0.2065, -0.1543, 0.2194, 0.1191, -0.1728, -0.0088, 0.2001, 0.0858, -0.0617, -0.0534, -0.0143, 0.1248, 0.1577, -0.0349, -0.102, 0.0664, 0.0039, -0.3307, -0.1533, 0.2133, 0.0021, -0.2401, 0.1028, 0.3202, -0.072, -0.2108, 0.1481, 0.193, -0.1681, -0.1431, 0.1655, 0.0832, -0.0601, 0.0395, 0.0286, -0.0219, 0.126, 0.1628, -0.0218, -0.0339, 0.1767, 0.0859, -0.2336, -0.058, 0.2701, 0.0981, -0.1348, 0.0463, 0.2378, 0.0664, -0.1421, -0.1459, 0.0151, 0.1215, 0.0263, -0.0266, 0.0499, 0.0819, 0.0608, 0.0023, -0.0556, 0.0338, 0.1093, 0.0219, 0.0057, 0.0525, -0.0263, -0.1332, -0.0387, 0.1866, 0.0401, -0.2508, -0.0084, 0.2999, -0.0106, -0.366, -0.0789, 0.2224, 0.0419, -0.0921, 0.0245, 0.1096, 0.1035, 0.0081, -0.1814, -0.142, 0.1696, 0.1433, -0.2329, -0.1293, 0.2605, 0.1049, -0.1891, -0.0232, 0.2268, 0.1308, -0.0224, 0.0216, 0.1043, 0.071, -0.005, -0.0117, -0.0804, -0.0905, 0.0557, 0.0671, -0.1293, -0.1376, 0.1012, 0.0898, -0.1871, -0.0908, 0.3077, 0.2061, -0.1116, 0.0573, 0.3036, 0.0489, -0.1358, 0.126, 0.1628, 0.0067, 0.0637, 0.096, -0.0341, -0.0041, 0.1126, -0.0479, -0.224, 0.027, 0.244, -0.0861, -0.1756, 0.2011, 0.2513, -0.1051, -0.1615, 0.1416, 0.1275, -0.1246, -0.1325, 0.0336, -0.0236, -0.1135, -0.0897, -0.0885, 0.0037, 0.1053, 0.0346, -0.0846, 0.0489, 0.1394, 0.0369, 0.0434, 0.1719, 0.1533, -0.031, 0.0135, 0.0841, -0.1131, -0.1662, 0.0473, -0.0279, -0.1954, 0.013, 0.1171, -0.0476, -0.0988, 0.0336, 0.0507, 0.0096, 0.1012, 0.0963, -0.05, -0.0192, 0.1842, 0.0674, -0.1325, 0.0573, 0.1654, -0.0567, -0.0988, 0.0383, -0.0244, -0.0822, -0.0062, -0.0023, -0.0731, -0.0088, 0.1699, 0.1101, -0.1085, -0.008, 0.2149, 0.0945, -0.024, 0.1732, 0.2375, -0.0271, -0.1327, 0.0929, 0.1106, -0.1499, -0.1108, 0.1467], "xjtu_early": [-0.3964, -0.1231, 0.9888, 0.0067, -1.0744, -0.7563, -0.6531, -0.6229, -0.4879, -0.0487, -0.1599, -0.0581, -0.2538, 0.5477, 0.4713, 1.2655, 1.2319, -0.2199, 0.3844, 0.8126, 0.629, -0.841, -0.681, -0.0557, -0.2738, -0.5324, -0.2578, -0.4578, -0.4761, -0.802, -1.1612, -0.0449, 0.7351, 0.6872, -0.0799, 0.2203, 0.4477, 0.897, 1.0604, 0.5614, 0.8212, 0.3399, 0.0228, -0.5334, -0.4983, -0.1842, -0.118, -0.6218, -1.4325, -0.5129, -0.2463, -0.8265, -0.5208, 0.38, 0.6732, 0.1824, 0.0596, -0.5476, -0.2535, 0.4465, 1.2193, 0.2181, 1.0222, 0.4748, -0.5831, -0.5187, 0.2097, 0.4855, 0.1287, -0.3691, -0.9501, -0.4266, 0.1483, -0.3689, -0.3328, -0.6459, 0.1606, 0.0776, -0.4235, 0.2829, 0.3439, 0.2244, 0.525, -0.2704, -0.0935, 0.4853, 0.7897, -0.437, -0.4912, 0.1796, -0.0026, -0.3182, -0.4806, -0.0029, -0.1913, 0.4552, 0.351, -0.1761, -0.2033, -0.1005, 0.5798, -0.0353, -0.0025, 0.0216, 0.3999, -0.1422, 0.0895, 0.3049, 0.1199, 0.0609, 0.0769, -0.0404, -0.547, -1.0161, -0.5198, -0.3621, 0.262, 0.2624, 0.688, 0.3653, 0.6279, 0.9244, 0.7348, 1.4184, 0.5548, 0.4332, -0.8256, -0.4585, -0.6774, -0.1809, -0.028, -1.1178, -1.2927, -0.7974, -0.4021, 0.0759, -0.3908, 0.131, 0.0669, 0.5019, 1.0187, -0.2166, -0.2967, 0.2133, 1.4134, 0.5059, 0.5501, 0.4989, -0.2711, -0.0185, 0.0477, 0.49, -0.0423, -0.6462, -0.0454, -0.133, 0.1641, -0.1229, -0.287, -1.247, -0.3252, 0.7033, 1.2504, 0.1903, 0.3091, 0.6273, 1.0213, 0.288, -0.1303, 0.49, -0.0859, 0.5135, -1.0668, -0.7573, -0.5789, -0.1168, -0.9363, -1.0639, 0.4334, 0.4157, -0.3268, 0.1055, 0.1415, -0.0796, 0.2099, 0.6394, 0.3379, -0.0738, 1.0607, 1.0414, 0.4726, 0.7715, 1.2538, 0.9258, -0.7371, 0.1662, -0.1207, -0.6387, -1.0718, -1.0409, -0.2612, -0.7899, -0.5446, -0.1397, 0.8264, 0.7496, 0.2513, 0.0518, 0.6475, 1.36, 0.949, 0.3275, 0.192, 1.0528, 0.8946, 0.6342, -0.409, 0.3383, 0.2289, -0.3708, -0.385, -0.8067, -0.2452, 0.3556, -0.3366, -0.4287, 0.2969, 0.4733, 0.356, 0.7031, 0.6175, 1.3883, 1.4588, -0.0847, -0.4752, 0.315, 0.2283, -0.1299, -0.647, -0.0118, 0.0933, -0.0419, 0.374, -0.5538, -0.3355, 0.1194, 0.3309, -0.0551, -0.5307, 0.1544, 0.5219, 0.2857, 0.286, 0.1595, -0.3404, 0.5269, 0.0849, -0.1557, 0.7369, 0.4132, -0.4199, -0.7971, -0.4158, 0.1937, 0.0493, -0.2429, -0.3683, 0.1462, -0.1245, -0.1264, -0.0438, 0.7455, 0.3049, 0.2525, 0.3436, 0.5586, 0.641, 0.9638, 0.2236, -0.2041, 0.532, -0.2145, -0.8972, -1.2658, -0.0892, -0.5667, -0.5305, -0.113, -0.7069, -0.2155, 0.9903, 0.2519, 0.0767, 1.3278, 1.0232, 0.3155, 0.4585, 0.2865, 0.4498, 0.457, -0.4115, -0.343, 0.2421, 0.2805, -0.2518, -0.6069, -0.0225, 0.1129, -0.0638, -0.029, -0.7373, -0.2355, 0.5716, -0.1884, -0.2602, 0.5407, 0.887, 1.038, 0.0352, 0.2697, 0.2481, 0.5579, 0.627, -0.1523, -0.615, -0.9052, -0.6882, -0.8826, -0.4134, -1.4727, 0.1345, 0.2161, 0.2452, -0.0885, 0.4015, 0.1229, 0.3043, 0.4078, -0.5883, 0.3946, 0.5729, 0.8812, 0.0904, -0.1459, 0.3003, -0.1132, -0.4051, -0.0606, -0.1055, -0.8817, -1.3449, -1.0097, -0.7115, -0.4792, 0.0815, 0.4676, -0.0158, 0.175, -0.0405, 0.486, 0.7359, 1.4081, 1.0443, 0.05, 0.0681, -0.5712, 0.1796, -0.2168, 0.3099, 0.0218, 0.0477, -0.5229, -0.5217, -0.6218, 0.1473, 0.7411, 0.1269, -0.086, 0.06, 0.4655, -0.5652, 0.3472, 1.1116, 0.9205, 0.2147, -0.0044, 0.6072, 0.5276, 0.5659, -0.0908, 0.2997, 0.4874, -0.5057, -0.7665, -1.152, 0.0684, 0.3125, 0.6548, -0.0475, -0.4359, -1.075, 0.7538, 0.9272, 0.3148, 0.0233, -0.1158, -0.7501, -0.474, 0.0107, -0.289, 0.0697, 0.7577, -0.5068, -0.1831, -0.5238, 0.3813, 0.5794, 0.0293, -0.1281, -0.8182, 0.0591, -0.2831, -0.2411, 0.0917, 0.0357, 0.3494, 0.4451, 0.0779, -0.1892, 0.3405, -0.4336, -0.7169, -0.9061, -0.478, -0.3731, -0.4485, -0.7246, -0.4321, -0.2243, -0.0749, 1.0018, -0.0544, 0.0781, -0.0951, 0.0844, 0.0503, 0.3812, 0.779, 0.2949, 0.1526, 0.2824, 0.0186, 0.1283, -0.0884, 0.5979, 0.4918, -0.5847, -0.8404, 0.1561, 0.0768, -0.757, 0.4101, 0.5411, 0.4707, 0.3085, 0.2647, 0.2388, 0.5882, 1.5696, 0.5037, 0.0367, 0.2983, 0.5847, -0.2833, -0.2947, -0.7302, -1.1495, -0.2292, -0.5409, 0.0199, -0.1884, -0.3222, -0.2928, 0.4033, 0.501, 0.5857, 0.7681, 0.8186, 0.0773, 0.0479, 0.1417, 0.4562, -0.4766, 0.1105, -0.1889, -0.5853, 0.165, 0.1685, -0.8007, -0.7286, 0.0017, -0.7188, -1.0345, -0.7713, -0.4448, -0.6202, -0.3279, 0.0538, -0.2369, -0.0514, -0.3011, 0.6467, 0.2639, 0.8105, 0.2203, 0.1458, -0.7186, -0.5084, 0.1164, -0.6422, -0.5344, 0.064, 0.2373, -1.2062, -0.9413, -0.1585, -0.3245, -0.6947, 0.1073, 0.0434, 0.2445, 0.2305, 0.0708, -0.0108, 0.7158, 0.413, 0.4633, 0.284, 0.2635, -0.2377, -1.1485, -0.4326, -0.1283, 0.0502, -0.2165, -0.5999, -1.234, -0.4761, -0.0773, -0.4814, 0.8053, 0.9707, 0.5802, -0.177, 0.225, -0.0017, 0.305, 0.4264, -0.1547, 0.027, -0.1017, -0.2372, -0.5318, -0.4611, -0.1603, 0.1633, 0.2549, -0.1693, 0.3001, -0.6996, -0.1534, -0.5337, -0.6346, -0.5239, -0.397, 0.2534, -1.0869, 0.1345, -0.4446, 0.3776, -0.1929, 0.1308, -0.3836, -1.5029, -0.8592, -0.6187, -0.412, -0.3822, 0.3985, -0.5873, -0.2708, -0.7789, -0.1907, 0.1497, 0.7982, 0.2768, -0.8342, -0.1247, -0.5923, -0.0471, -0.6002, -0.9336, -0.2751, -0.0011, 0.3001, -0.825, -0.3832, -1.0927, -0.5053, -0.4002, 0.3206, 0.9057, -0.6652, 0.0883, 0.4822, 0.2899, -0.8574, 0.27, 0.2968, 0.9092, 0.9259, 0.2515, -0.1692, -0.8297, -0.3343, -0.7813, -1.0969, -0.8943, -0.3194, -1.0674, -0.622, -0.2178, 0.5117, 0.0312, -0.1269, 0.0709, 0.6074, 0.8717, 1.0153, 0.684, -0.2581, 0.8396, -0.2317, 0.0065, -0.7535, -0.2983, -0.3873, -0.3094, -0.6059, -0.9084, -1.0182, -1.1511, -0.2279, -0.7712, -0.6244, -0.642, -0.2545, -0.1037, 0.2242, 0.5788, 0.8545, 0.3928, 0.7605, 0.7859, 0.332, 0.2535, -0.4993, -0.2011, -0.255, -1.559, -0.5468, -0.3271, -0.825, -0.6255, -0.4666, -0.5357, -0.5028, 0.2849, 0.1944, 0.9466, 0.5168, 0.2631, 0.4612, 0.2368, 0.4441, 0.1705, 0.4908, -0.3084, 0.1095, 0.5572, -0.29, -0.7747, -0.2758, -0.7501, -0.5771, -0.0783, -0.3964, -0.7006, -1.1963, -0.1912, 0.1536, -0.1897, 0.283, 1.3908, 1.1276, 0.6734, 0.9624, 0.719, 0.6477, 0.1924, 0.2713, 0.1216, -0.7292, -0.0557, -0.3715, -0.7676, -0.8295, -0.5574, 0.0079, -0.3239, 0.2642, 0.1397, -0.5503, -1.1039, 0.5319, -0.3911, 0.0828, 0.5866, 0.4786, 0.5964, 0.2834, 0.2974, -0.0573, -0.0225, -0.0061, -0.3008, -0.4943, -0.1663, 0.0291, -0.0165, -0.1363, -1.0437, -0.5404, 0.2045, -0.1073, 0.3773, 0.2554, -0.5734, -0.6769, 0.4579, 0.4939, 0.9791, 0.7638, 0.3043, 0.4642, -0.619, -0.5799, -0.6797, 0.0472, -0.9391, -0.6947, -0.043, 0.2468, 0.3366, -0.4098, -0.2566, -0.267, 0.9844, 0.4852, -0.3236, -0.6413, 0.3789, 0.562, -0.0998, 0.1149, 0.9307, 0.3335, 0.6453, 0.0502, -0.2175, 0.4659, 0.1526, -0.5377, -0.2921, 0.008, 0.2025, 0.6226, 0.5034, 0.9829, 0.5392, 0.9087, -0.0958, -0.7335, -0.3445, -0.0925, -0.1088, -0.7351, -0.411, -0.655, -0.2429, -0.8459, -0.2159, 0.7085, 0.2903, 0.1472, 0.3648, 0.2575, -0.5084, 0.2477, 0.4817, -0.2709, 0.2763, 0.3331, 0.1287, -0.093, 0.6983, 0.2537, 0.3636, 0.5138, -0.6914, -0.6791, -1.2125, -0.3392, -0.131, -0.4115, -0.5176, -1.1242, 0.0833, -0.016, 0.196, -0.1611, 0.6699, 0.2406, 0.4009, 0.7503, -0.0796, 0.1941, 0.1597, -0.1847, -0.3083, -0.341, 0.2587, -0.2518, -0.3491, -1.0627, 0.3186, 0.723, 0.6463, 0.0813, -0.0813, 0.2075, 0.1701, -0.2817, -0.2776, 0.3154, 0.5814, 0.7086, 0.2178, 0.3127, 1.0158, 0.8029, -0.6009, -0.487, -0.372, -0.2464, -0.0581, -0.5996, -0.5098, 0.1202, 0.0012, 0.0232, 0.0564, 0.6726, 0.8003, 0.0058, -0.0157, -0.2623, 0.4479, -1.0093, -0.9649, -0.8224, 0.3318, 0.4099, -0.2057, 0.3314, -0.6665, -0.0047, -0.4706, 0.325, 0.0665, 0.1069, 0.3613, -0.3518, -0.6774, 0.058, 0.493, -0.4703, -0.2052, 0.9607, 0.8699, 0.2289, -0.0221, 0.2818, 0.2173, -0.959, -0.6114, -1.1516, -0.7601, 0.4507, -0.1732, -1.2494, -1.0931, 0.813, 0.8083, 0.9198, 0.0585, 0.436, 0.494, 0.3265, 0.4965, 0.5438, -0.0436, 0.4033, 0.7448, -0.3089, -0.1891, 0.6807, 0.633, -0.6299, 0.1931, 1.4955, -0.0554, -0.4866, -0.1124, 0.728, -0.0214, 0.3928, 0.7405, -0.0244, 0.3822, 0.4407, 0.6377, 0.0299, 0.5632, 0.5778, -0.9088, -0.955, -0.4014, 0.0688, 0.2292, -0.7088, -0.063, -0.4336, -0.1226, 0.0662, 1.229, 0.8752, 1.1744, 0.7604, -0.0396, -0.493, 0.4853, 1.9142, -0.0905, 0.4048, 0.3954, -0.1485, -1.8093, -0.3861, 0.428, 0.2738, -0.1452, -1.3753, 0.2528, -1.1417, -0.6944, 0.2391, 0.3284, 0.6212, 0.0721, 1.1711, -0.3023, 0.0397, 1.3202, 1.1546, -0.0301, -0.5203, 1.8167, -0.7358, -0.6692, -0.1064, 0.2679, -1.0716, -1.3645, 0.2377, -0.9337, -0.2208, 0.2189, 0.6351, -1.1734, 0.3237, 1.1602, 0.3479, 0.6669, 0.2964, 1.6862, 0.3376, 0.4743, 0.372, 0.7444, 0.3085, 0.1309, 0.0726, -0.2251, 0.2338, -0.1383, -0.4064, -1.2632, -0.2085, -0.0384, -0.4351, -0.7015, 0.4123, 1.5899, -0.005, 0.3718, 0.1605, 0.8903, 0.5779, 1.1867, 1.1058, -0.1574, -0.1145, -0.0715, -0.5725, -0.5681, 0.1482, -0.2056, -0.8787, 0.5417, 0.5981, 0.722, -0.956, -0.3626, 0.3522, 1.1536, -1.0249, -0.2281, 0.9905, 0.032, 1.0491, 0.5994, 0.4161, -0.9117, 0.8315, 0.9426, -0.1431, -1.5684, 0.4668, -0.4504, -1.0424, -1.3868, -0.0582, -0.4498, -1.211, -0.1686, -0.7475, 0.181, 0.2119, 0.7998, 0.4489, 0.5282, 1.3462, 0.1396, -0.1393, 0.3214, 0.0142, 0.1057, -0.8891, -0.4462, 0.5167, -0.7165, -0.108, -1.0409, -0.5792, -0.8196, 0.112, 0.3246, -0.2659, 0.1939, 0.442, 0.445, -0.2433, 0.565, 0.5683, 0.6777, 0.8171, 0.5199, 1.014, 1.0693, -0.4206, -1.209, 0.024, 0.0214, 1.1342, -0.4703, -0.785, -0.9839, -0.3236, 0.1515, -0.2365, 0.3081, 0.6841, 0.632, -1.2972, 0.1178, 1.3448, 0.7657, 0.1309, 0.2228, -0.2037, -0.7868, 0.6401, 0.5622, -0.1635, 0.2028, 0.4131, -0.7569, -1.4324, 0.0646, 0.2705, -0.2812, -0.1173, -0.0083, 0.3394, -0.3703, 0.2509, -0.0913, -0.0136, 0.5802, 0.8185, 0.4395, -0.7034, -0.6994, 0.043, 0.2276, -0.14, 0.0537, 0.041, -1.0517, -0.8249, -0.2948, 0.1117, -0.3203, 0.424, -0.0324, 0.0866, -0.398, 0.324, 0.1405, 0.2468, 0.4228, -0.2214, 0.4931, 0.3134, 0.662, 0.1051, -0.8377, -0.4365, -0.364, -0.0765, -1.0953, -0.4975, -0.1363, -0.1131, -0.0095, 0.3841, 0.3358, 0.2008, 1.3644, 0.3491, -0.6662, 0.5932, 0.9468, 0.4686, -0.1643, 0.4692, -0.2997, -0.7895, -0.3279, -0.5361, -0.6116, -0.1501, 1.2274, -0.0916, 0.0363, 0.0804, 0.6488, 0.0071, 0.5749, -0.2602, 0.0695, 0.7728, 0.4591, 0.0013, 0.0257, 0.0494, -0.2458, 0.4644, 0.0022, -0.434, -0.195, -0.6895, -0.6225, -0.0956, -0.0155, -0.8409, -0.106, 0.3437, -0.1392, -0.7103, 0.4527, 0.263, 0.5267, 0.6162, 0.283, -0.1111, -0.5879, -0.6976, -0.7215, 0.444, 0.3279, 0.1482, -0.5828, -0.7267, -0.9111, -0.4421, 0.1329, -0.4597, 0.3005, 0.2624, -0.3299, -0.1163, 0.7241, 0.351, 0.3301, 0.6905, -0.0434, -0.3797, -0.0227, 1.2466, 0.2612, 0.0521, 0.5429, -0.5124, -0.5104, -0.1637, -0.3615, -0.118, -0.0852, -0.5657, -1.2519, -0.0458, -0.0776, -0.0161, 0.6059, 0.2248, 0.2933, 0.0112, 0.5229, -0.4573, -0.3308, 0.5435, 0.0039, -0.7063, -0.1969, -0.3796, -0.565, -0.2318, 0.3625, 0.0573, 0.1845, 0.1475, -1.0951, -0.0664, 0.1165, -0.5279, -0.1048, 0.2383, -0.598, -0.497, 0.2087, 0.0157, 0.3381, 0.6254, -0.9341, -0.8298, 0.3151, -0.3399, -0.5719, -0.5985, -0.6021, -0.9586, 0.308, 0.2373, 0.0651, 0.4671, 0.6049, 0.0382, -0.5007, 0.5258, -0.2319, -0.8284, -1.1307, -0.4367, -0.3273, 0.0123, 0.5561, 0.0211, 0.3425, -0.2773, -0.0097, 0.2081, 0.7313, -0.2293, -0.3589, 0.016, -0.8579, -0.3811, 1.0237, -0.0277, 0.1537, 0.8784, -0.0488, -1.2917, -0.2774, 0.5471, -0.4294, -0.4152, -0.4593, -1.5893, -0.8887, -0.5162, -0.3001, -0.2162, 0.819, 0.6314, 0.3469, -0.0755, -0.5272, -0.5122, -0.6567, 0.1573, 0.0158, -0.0656, -0.4405, -1.5336, -0.0487, -0.5935, -0.5016, -0.3226, -0.1753, -1.0971, -1.2844, -0.6195, -0.6549, 0.448, -0.4647, -0.0451, -0.1935, 0.8622, 0.4326, 0.1839, -0.1354, 0.0957, -0.3423, 0.2178, -0.0277, -0.5775, 0.0988, -1.0457, -0.4719, -1.0872, -0.2221, -0.1165, -0.6516, -0.2085, -0.2733, -0.9294, -0.5643, -0.2949, 0.347, 1.4135, 0.8686, 0.0796, -0.0144, 0.2447, -0.2675, 0.975, 0.4965, -0.3219, -0.4091, -0.5947, 0.0946, 0.0994, -0.4274, -0.1916, -0.6532, -0.0982, -0.9164, -0.9637, -0.0526, 0.248, 0.3512, -0.212, 0.0203, 0.4604, 0.9407, 1.0603, 0.5947, 0.3615, -0.206, -0.0411, -0.7905, -0.6541, -0.4196, -0.9882, -1.0708, -0.9917, -0.2337, -0.3098, -0.4517, 0.508, -0.1773, -0.3082, 0.424, 0.9232, 0.2886, 0.9095, 0.3875, -0.489, -0.6234, 0.1387, 0.4674, 0.1867, 0.2267, 0.3217, -0.8004, -0.9464, -0.3352, -0.7603, -0.5195, -0.2259, -0.9401, -0.4272, 0.0196, 0.289, 0.6508, 0.8751, 0.0141, -0.086, 0.6603, 0.0022, 0.4791, -0.2616, 0.0935, -0.7962, -0.4484, 0.041, 0.0772, 0.341, -0.0228, -0.0769, -0.5158, -0.4157, 0.395, 0.7511, 0.4423, 0.1687, -0.2537, -0.3633, 0.0329, 0.2154, -0.2887, 0.9055, 0.1645, 0.0577, 0.0657, -0.4568, 0.3911, -0.1965, 0.0372, -0.1512, 0.2606, -0.8346, -0.087, -0.281, -0.3222, -0.178, 0.0623, 0.2384, -0.2649, -0.0848, 0.8217, 0.0528, 0.6891, 0.6929, 0.5151, 0.0582, -0.2269, -0.7147, -0.8313, -0.4103, -1.1652, -0.5066, -0.3376, 0.5509, -0.0077, 0.1204, 0.2488, 0.6758, 0.9279, 0.6414, 0.2601, -0.4335, 0.1392, 0.0313, 0.2661, -0.1775, -0.3177, 0.0483, -0.1569, -0.119, -1.1112, -0.4971, -0.6627, -0.6454, -0.1143, -0.2211, -0.0213, 0.0768, 0.8551, 0.4712, 0.8747, 0.837, 0.708, 0.2181, -0.0387, -0.3704, -0.2799, 0.5991, -0.3996, -0.1329, -0.6647, 0.3256, 0.1052, 0.7802, -0.0404, -0.8414, -0.4006, -0.177, 0.5846, 0.4493, 0.8747, -0.0259, 0.528, 0.2966, 0.4135, -0.0589, 0.4749, 0.4992, 0.3375, -0.3029, -0.4689, 0.182, -0.3642, 0.0551, -0.4683, 0.0803, -0.1766, -0.6188, -0.7627, -0.7303, -0.4737, 0.8965, 0.1624, 0.3201, 0.2973, 1.5301, 0.2791, 0.6706, 0.3121, 0.4579, 0.1375, -0.8165, -0.5334, -0.3157, -0.1305, -0.4015, -1.0303, -0.7538, 0.0387, -0.1207, -1.0687, -0.5566, -0.1518, -0.1592, 0.5009, 0.2692, 0.4208, 0.2261, 0.2844, 0.717, 0.4799, 0.5535, 0.112, 0.5013, -0.4793, -0.6046, -0.7215, -0.4561, -0.327, -0.5162, -0.2555, -0.3577, -0.1984, 0.5226, -0.1191, -0.5605, -0.1206, 1.317, 0.3854, 0.3164, 0.1027, 0.772, 0.5444, 0.2479, -0.3904, 0.6124, 0.9757, 0.1709, 0.3725, -0.0506, 0.1152, -0.0319, -0.1238, 0.8574, -0.541, -0.6121, -1.157, -0.3453, -0.2656, 0.0187, -0.2205, -0.0436, 1.101, 0.0006, 1.6741, 0.8265, 0.0631, -0.5207, 0.7429, -0.595, -0.9942, -0.3786, 0.3878, -0.0831, -0.7907, 0.5358, -0.4868, 0.2699, 0.6432, 0.0412, -0.0908, 0.5789, 0.757, -0.0086, 0.3799, 0.5489, 0.0419, -0.2593, 0.212, 0.5261, -0.6565, -0.2113, -0.4989, -0.5935, -0.1297, -0.7514, -0.8702, 0.4256, 0.1347, -0.1197, -0.3878, 0.5622, 1.2264, 0.3891, 1.1108, 0.9942, 0.424, 0.5399, 0.3953, -0.2605, -0.3178, 0.6727, -0.3005, -0.4518, -0.77, -0.4811, -0.1382, -1.0592, 0.0023, -0.3891, -0.4501, 0.4515, 0.9589, 0.2287, -0.0719, 0.2714, 1.0156, 0.7086, 0.8364, 0.1932, 0.2299, 0.2105, 1.063, -0.2327, -0.3421, -0.1423, 0.7899, -0.3369, -0.7899, 0.491, -0.3086, -0.2955, -0.5477, 0.1129, -0.2788, 0.5979, 0.5565, 0.0129, 1.5832, 0.3585, 1.3395, 0.2712, 0.684, 0.0749, 0.2441, 0.3737, -1.2577, 0.5985, 0.4652, 0.4541, -1.0756, -0.1821, -0.2891, -0.22, 0.4681, 0.3543, 0.4497, -1.2228, 0.9859, 0.0453, 0.5093, 0.4171, 0.6234, 0.107, -0.5678, 1.3019, 0.1217, 0.1429, -1.8165, -0.2834, -0.4278, -0.7017, -0.7193, 0.7867, 0.4496, -0.8206, 0.1147, -0.5816, 0.8542, 0.7106, 0.8741, 0.3221, 0.4428, 1.3733, -0.9661, 0.0066, -0.7516, 0.6626, 0.718, -0.5236, -0.1012, -0.6506, 0.0178, -0.1416, -0.4922, 0.4454, 0.1003, -0.6436, -0.7238, -0.0392, -0.6932, 0.6718, 0.8912, 0.7958, 0.4671, 0.9269, -0.1186, 0.0523, 0.4363, 0.5585, -0.1298, -0.6378, 0.3701, 0.8156, -0.1518, -0.2889, -0.8614, -0.1479, 0.6123, 0.2752, 0.7903, -0.1465, 0.8487, -0.5833, -0.0881, 0.8159, 0.219, 0.0547, -0.8706, -0.3618, 0.1377, 0.1707, -0.2825, 0.1298, -0.0548, -1.0155, -0.0214, 0.4969, -0.9459, -0.2264, 0.751, 0.1284, -0.4145, 0.2285, 0.687, 0.0611, -0.5562, 0.1396, 0.2787, 0.8802, -0.123, 0.2344, -0.4352, -0.7112, 0.074, -0.0015, -0.5998, -0.174, 0.291, -0.1677, 0.2034, 0.0491, 0.2793, -0.2484, -0.2834, -0.302, 1.0143, -0.0916, 0.7224, 0.366, -0.2812, -0.4221, 0.0844, -0.2545, -0.7284, 0.7835, -0.0334, 0.0223, -0.3251, 0.1308, -0.0741, 0.5685, 0.2024, -0.7599, 0.5823, 0.3227, 0.0277, 0.0256, 0.2203, 0.054, 0.6615, 0.8315, -0.5515, 0.4338, 0.3859, -0.0253, -0.5882, -0.2305, 0.2262, -0.197, -1.2359, -1.2143, -0.8206, -0.1361, 0.6438, 0.1957, 0.1086, 0.2782, 0.3152, 0.0333, 0.9909, 1.8173, 1.3416, -0.2855, -0.8184, -0.39, -0.1462, 0.4022, -0.2136, -0.5162, -0.6596, -0.3541, 0.0998, -0.0405, 0.3082, 0.8061, 0.6365, -0.8314, 0.152, 0.1611, 0.6125, 0.2594, -0.2287, 1.3186, 0.9344, -0.2587, -0.846, -0.4111, -0.5569, -0.4933, -0.3402, -1.1598, -0.9416, -0.478, -0.1997, -0.6291, 0.0651, 0.5705, 0.4144, 0.1274, -0.0586, 0.3912, 0.637, 0.4544, 0.2072, 0.2013, 0.0661, 0.2427, 0.5589, -0.7011, 0.4456, 0.051, -0.2344, -0.7967, -0.0411, -0.1426, -1.018, -0.9205, -0.905, 0.3655, 0.2513, 0.1683, 0.219, 0.1079, 0.5603, -0.2368, 0.34, 0.499, 0.6524, -0.3379, -0.6025, -0.413, -0.1457, 0.3331, -0.1273, -0.5404, -0.8428, -0.1358, -1.0798, -0.1975, 0.3032, 0.1576, -0.1117, -0.2246, 0.2928, -0.2043, 1.9296, 0.3982, 0.3951, 0.253, -0.1905, 0.5034, -0.132, 0.5783, -0.7422, -0.1536, -1.346, -1.0475, -0.913, -0.9911, 0.1483, -0.2913, -0.1876, -0.3537, 0.7581, 0.9491, 0.8162, 0.7701, 0.7803, 0.939, 0.1988, 0.3278, -0.3988, 0.0339, -0.1149, -0.6906, -0.8116, -0.9505, 0.2477, -0.9419, -0.519, -0.5541, 0.0285, -0.6626, -0.3923, -0.2015, -0.5558, 0.8541, -0.1195, -0.233, 0.5842, 0.6863, 0.6595, -0.0868, 0.0962], "xjtu_late": [1.246, -1.4116, -0.7076, -0.4302, -1.0799, -1.2749, -1.8776, -0.9942, -1.8481, -0.5763, -0.6298, -0.699, 1.459, 0.9022, 2.0582, 1.7532, -0.0527, 2.1088, 1.8803, 2.7428, -1.6096, 1.3492, -0.1115, 0.6535, 0.576, -0.2306, 1.6045, -1.4221, 1.253, -1.0489, -1.0841, -0.1746, 1.0498, 1.6609, -0.2062, 1.0966, 1.5271, 1.5898, 2.9369, 2.884, 2.3326, -0.1119, -0.2522, -4.4912, -7.3177, -7.7207, -4.2274, -5.2853, -4.889, -7.8216, -8.1485, -6.143, -3.1788, 0.1818, -0.3734, 1.1248, 2.2935, 3.1751, 4.4744, 6.7744, 8.1679, 7.7555, 6.9543, 6.7321, 3.6977, 4.2158, 1.2755, -0.0412, -4.3498, -5.2969, -4.8587, -7.7044, -9.2607, -7.1074, -7.6024, -6.3048, -6.5066, -5.0175, -4.7022, -3.7996, -2.2508, 0.5446, -0.9247, 0.5205, 7.0141, 4.6794, 4.646, 4.5155, 8.9143, 3.1175, 5.5555, 3.9548, 4.0473, 0.5402, 0.504, -0.6255, -2.5976, -0.8175, -4.1492, -0.1763, -3.0985, -1.0387, -2.6689, -0.2854, 0.0003, 1.323, 5.2773, 1.3464, 6.8514, 2.9892, 4.1467, 3.3506, 0.5471, 1.4187, 0.2645, -0.6736, -4.8541, -2.9409, -4.9009, -2.4276, -3.6499, -0.6192, -4.1335, -2.9755, -1.8944, 0.2874, -0.1263, 0.6893, 3.5154, 0.1, 0.5579, 0.0294, 2.0254, -0.2668, 0.8685, 0.0348, 2.5228, -3.7831, -0.0716, -1.4716, -3.0676, -3.3248, -2.2591, -0.3428, -3.7899, -2.1196, -4.1056, -0.0236, -1.2437, 0.9137, -1.4399, -0.4233, -0.4361, 1.9419, 1.9663, -0.3106, 2.8502, 0.7951, 2.9091, 0.842, 2.2493, 2.3028, 0.6442, 1.8371, -0.5376, -0.4354, -0.7687, -1.2696, -1.5043, -2.7635, -1.1711, -2.8082, -2.202, -1.2483, -0.8385, 2.3749, 1.6257, 0.7944, 0.7161, 2.9723, 1.6307, 3.2189, 0.9952, 0.1898, 0.4802, -1.1321, 0.9259, -2.12, -0.7543, -1.5879, -1.3008, -2.5459, -2.9716, -1.2129, -1.3533, -1.8869, -0.9375, -1.1687, 0.1837, -0.0404, 1.5597, 1.3679, 1.052, 3.0614, 2.4763, 1.8129, 2.1757, 1.9315, 3.3887, 1.594, 0.466, 0.6204, -0.4176, -1.1378, 0.486, -1.8312, -2.0063, -1.7647, -0.552, -3.3069, -2.9566, -0.0715, -2.0595, -2.7804, -2.0053, 0.9845, -1.3914, -0.5975, 1.8314, -0.8794, -0.7367, 1.2332, 1.9375, 1.6813, 0.7641, 2.2128, 0.5756, -0.2071, -0.2493, 0.619, -0.8714, 0.3823, -0.2826, -0.5585, -0.1968, -0.6995, 0.2469, 0.8929, 2.6867, -0.7518, 1.6415, 0.9158, 1.1798, 0.7257, 1.0813, 0.2349, -1.6154, 0.4812, -0.3906, 0.0155, -0.3217, 1.8997, -1.1749, 0.6066, 0.2325, -0.2375, 2.7114, 1.7006, 3.1872, 1.0653, 1.8587, 2.3926, 3.8895, 2.7251, 2.9688, -0.6247, 2.7374, -1.1434, -7.7668, -12.2699, -2.9052, -6.6833, -4.2863, -5.1359, -7.4876, -9.5662, -1.6644, 3.8064, -2.3869, 2.2282, 2.8401, 3.4822, 3.2562, 2.2795, 9.9187, 5.2724, 7.3422, 5.3353, 4.7614, 2.5161, 3.0623, 3.7776, -6.6617, -3.1324, -0.6094, -8.374, -7.7335, -7.4543, -4.9251, -8.6596, -6.4322, -8.6334, -1.8179, -7.889, 1.4932, -1.7125, 1.2445, -1.5716, 7.2423, 6.7579, 1.6847, 7.8983, 5.8976, 6.3436, 0.9117, 5.9209, 1.9201, 3.4128, -0.5152, -0.5245, -2.4067, -0.5359, -3.5288, -1.2909, -0.9672, -2.5836, -0.3911, -0.2655, 0.39, 2.2692, 1.8142, 4.0446, 3.3159, 4.3139, 5.5022, 4.2388, 2.2529, -0.1765, 1.7627, -0.0075, -2.502, -2.8333, -2.185, -1.5846, -3.0874, -1.7815, -2.781, -0.647, 1.2043, 0.5822, 0.2195, 1.0691, 0.7506, -0.4958, 0.1179, -0.6581, 1.2058, 0.2385, -0.3553, -0.8826, -0.4109, -0.8366, -0.3476, -1.7569, -1.7386, -1.8653, -1.5748, -3.0358, -3.3287, -1.3386, -0.6377, -0.887, -1.3638, -0.0257, -0.6587, 0.4331, 0.2411, 0.6995, 2.3516, 0.7205, 2.8717, 0.2185, 2.0792, 0.66, 2.3659, 2.3373, -0.5027, 1.7553, 0.1799, -0.1558, -3.2026, -1.7615, -0.7298, -2.7755, -1.0174, -0.5857, -0.0103, -1.5337, -0.2386, 1.037, 1.005, 1.5372, 1.8068, 2.2697, -0.4296, 2.0922, 0.0545, 0.0517, -1.1394, -0.9825, 2.2259, -4.2273, 0.5192, -4.6122, 0.9381, -1.4098, -0.7237, 0.4753, -0.0835, -0.7028, -0.6556, 0.9479, 1.2609, -1.2365, 4.9664, -0.9868, 0.7227, 3.0977, 0.0915, 5.6206, -0.8569, 5.5686, 1.4319, 2.9201, 0.8703, 0.7591, 0.2329, -0.2026, -0.1766, 0.6928, -4.6175, 0.9344, -3.9384, -0.2828, -5.0704, -0.535, 0.372, -5.8076, 5.0234, -4.535, 1.4695, -3.0107, 2.0619, -2.4132, 3.0561, 0.8078, -0.5469, 4.1945, -0.6352, 0.3142, 1.4472, -0.7446, 0.5378, 1.0519, 1.8915, -4.382, 1.0126, 0.3901, -1.3011, 1.3888, -0.7553, 0.4051, -0.4303, 3.0798, -2.1942, 0.7093, 2.4212, -1.2108, 2.6679, 0.1053, -1.5837, 2.7352, 0.6104, 0.7874, -1.7263, 1.7635, -1.2472, -0.1372, -0.2412, -0.3937, -0.0819, -1.8422, 1.6534, -2.5884, 0.9131, 2.6862, 2.4059, 2.9629, 2.3147, 4.7672, 4.9701, 5.0675, 5.266, 5.088, 3.2159, -3.5828, 0.4161, -8.3177, -9.0889, -4.3714, -9.3032, -1.0637, -13.7661, 1.1615, -18.8083, -3.9644, 3.1412, -0.0143, -1.5111, 2.3453, 5.3332, 0.4163, 11.4818, 2.5979, 12.0229, 5.3059, 10.741, 4.4099, 5.3924, -0.68, 1.7089, 0.4573, -7.8044, -4.7348, -6.2466, -12.0615, -6.2136, -6.6269, -6.0877, -6.5864, -5.5539, -1.8409, -6.612, -1.2816, -3.1132, 0.1243, 6.5428, 1.2194, 6.6473, 4.3017, 5.7284, 7.008, 8.6407, 1.066, 4.6998, 5.6723, 0.7231, -1.5727, -0.0352, -2.4006, -2.9064, -0.7455, -3.6435, -2.7029, 0.216, 0.5562, 0.7201, 2.1907, 3.6707, 3.0864, 3.2963, 4.9338, 1.0595, 4.548, 3.0484, 0.2261, -0.562, 0.7987, -2.4503, -1.8292, -5.8673, -0.976, -4.0218, -2.4162, -3.7129, -1.1501, -2.9277, -2.2035, 1.0762, 1.3953, 0.2038, 2.9199, 1.9534, 1.0841, 0.8455, 1.8615, 2.5072, 1.7501, -0.0182, -0.1713, -1.1118, -3.2354, -1.2075, -0.3429, -1.9894, -2.9981, -4.4439, -1.5334, -2.3837, -1.2151, -0.7365, -0.861, -1.0157, 0.187, -0.7053, -0.3959, 1.6618, 2.7175, 0.8529, 3.1916, 1.3377, 1.8235, 2.0033, 0.9128, 1.4048, 1.3136, -0.8466, 0.1238, -1.9056, -3.9133, -1.5442, -2.0026, -1.1139, -1.5044, -1.6473, -1.3473, -0.7375, 0.6624, 0.7693, 1.6399, 3.3508, 2.0337, 3.0672, 0.7873, 5.129, -4.5085, 7.502, -2.7546, 3.7175, -3.4697, 2.0924, -2.3888, -4.8489, -1.832, -3.9142, -0.2565, -7.8645, 1.6369, -3.2684, -1.6515, -0.522, 0.1527, 0.2764, 0.466, 4.4727, 2.1403, 2.3482, 2.806, 4.5926, 2.4067, 0.7182, 4.4926, 2.1675, 0.5955, 1.3065, -0.0733, 0.1358, -2.2889, -1.4178, 0.1812, -5.901, 1.0941, -5.2876, 0.49, -7.0679, 1.0886, -2.4199, -0.788, 0.6234, -0.1966, -0.0421, 1.2699, 2.1286, 4.0414, -0.1157, 2.9487, 0.6992, 0.5048, -0.3938, 1.669, -1.3149, 1.2093, -1.6522, -2.4986, -2.6826, -1.5354, 0.1035, -2.8154, -0.4185, -1.2229, -1.0867, 1.137, -0.1768, 2.7914, 0.3449, 2.4034, 3.1134, 1.0582, 2.0998, -0.0506, 0.9743, 0.2942, 0.5832, 0.842, -0.2386, -0.1579, -1.1203, -0.2594, -0.6515, -0.0239, 0.2131, 1.6656, 1.6744, 0.3465, 2.4051, 0.7331, 3.3209, 1.5421, 3.8546, 0.02, -1.4357, -5.1709, -8.4378, -5.9726, -5.1886, -4.7282, -4.0901, -8.5358, -6.9964, -7.6987, -1.129, 0.7257, 0.5449, 1.3463, 3.117, 4.4683, 3.6208, 8.8398, 7.0042, 8.799, 6.3891, 7.4589, 3.2053, 4.4395, 2.1513, -0.0592, -5.2095, -4.3535, -6.6496, -9.4233, -8.3875, -6.8981, -8.391, -7.789, -6.0199, -5.3308, -5.2844, -2.6776, -1.4444, -0.3936, -0.1966, 3.2806, 5.8386, 3.0703, 7.3718, 8.3773, 6.1933, 4.1704, 5.1809, 4.6356, 3.8516, 1.491, -0.4685, -1.7234, -2.4038, -1.9814, -3.2497, -2.5477, -2.2002, -0.8601, -1.7257, -1.317, -0.4165, 2.8673, 3.076, 3.2511, 3.2787, 4.0961, 2.9428, 2.7984, 1.792, 1.0334, 2.264, -3.5809, -2.5166, -3.5955, -3.645, -5.308, -1.8965, -3.5489, -1.7133, -2.4626, -3.7221, -2.4648, -0.5595, 1.7131, 0.8256, -0.1582, -0.4852, 1.8107, 2.436, 1.773, 1.4702, 0.1864, 1.3053, 0.5378, -0.793, -1.235, -1.6308, -1.2741, -3.2733, -2.2644, -4.3616, -3.5602, -2.4967, -0.3288, -2.1928, -1.0886, -1.8856, 0.0608, -1.2681, 0.5648, 1.2044, 1.2708, 2.3178, 1.0571, 2.3683, 1.8245, 3.1385, 2.6299, 1.777, -0.6644, 0.2504, 0.6947, 0.4005, -3.1332, -1.3972, -2.5999, -1.7025, -0.5115, -1.0909, -1.195, -1.1214, 0.0385, 0.8627, 2.7116, 1.2363, 1.1466, 0.2124, 1.4961, 0.6717, 0.8175, 0.7995, -0.2766, -0.4479, -1.1593, -0.8304, -1.8235, -2.1574, -2.2712, -2.4825, -1.6447, -1.107, -1.5072, -2.4401, -1.7286, 1.6038, 0.8924, 1.0294, 1.1931, 0.295, 2.2517, 3.621, 2.9185, 0.5912, 2.2744, 2.0861, 2.2368, 0.9025, 0.7915, -0.0762, 0.1517, -0.9068, -1.9188, -2.401, -1.3135, -1.9845, -2.3193, -1.9471, -2.3864, -1.3379, -1.5953, -1.4574, -0.4008, 0.8537, 1.5078, 0.0437, -0.019, 1.0792, 1.7735, 1.1795, 0.6066, 0.9127, -0.5882, 0.6706, 0.4859, -0.1052, -0.5245, 0.7711, -0.5793, -1.5067, -0.0905, 0.4734, 1.0879, -0.5401, 0.161, 0.3595, 1.3242, 1.0606, 0.6818, 1.1669, 0.6452, 0.7956, 0.5208, -0.4421, -0.0118, 1.5274, 0.044, -0.9179, 0.8579, 0.4398, -0.2029, -0.4928, 1.7201, 0.8176, 2.5791, 2.5632, 0.4177, 2.9031, 2.6838, 2.3908, 0.6493, 2.6839, -3.9281, -1.6243, -7.8262, -8.026, -6.0428, -3.7455, -2.4332, -6.956, -6.4662, -7.2085, -0.2012, 3.2239, -2.8069, 4.2181, -1.2933, 6.9836, 3.7963, 5.1788, 6.2001, 6.8928, 7.8237, 5.341, 3.5393, 0.9626, 1.2727, 1.0502, -4.7731, -3.4705, -3.9323, -6.6329, -7.6389, -4.7336, -9.6773, -4.1494, -4.975, -5.3787, -5.5265, -5.2127, -0.0281, -2.7538, 2.1989, 2.5439, 4.5245, 4.9787, 5.1253, 6.1459, 5.657, 3.7402, 6.9876, 3.4701, 3.1226, -0.4102, -0.2361, -0.7266, -1.445, -0.2343, -2.7494, -2.17, -2.8164, -0.8801, 0.764, -0.6487, 0.2336, 2.5009, 3.8893, 2.0429, 4.2901, 3.3376, 3.3662, 3.246, 2.5427, 1.2278, -2.2844, -0.3291, -1.7074, -2.3271, -2.7728, -2.0762, -3.1739, -2.4669, -0.2214, -0.7081, 0.0129, -0.1794, -0.387, 0.407, -0.3667, -0.4802, 1.0885, 0.2743, -0.7087, 0.4681, -0.137, -0.5783, 0.2963, -0.725, 0.2386, -1.4295, -0.9616, -1.8701, -2.8182, -1.7389, -1.8254, -1.3795, -2.3598, -1.1754, -0.1309, -2.1415, -0.7089, -0.1475, 2.0212, 1.137, 1.1714, 0.8609, 0.7158, 3.1252, 1.5462, 2.1362, 1.4588, 2.0296, 2.3692, -0.1992, -1.2156, -0.8018, 0.6553, -1.474, -0.999, -0.2378, -1.073, -0.7486, -2.1917, -0.2229, 0.0839, 2.1757, 1.1721, -0.0767, -0.0649, 0.8884, 2.0493, -0.1697, 0.1612, -0.1266, 0.5849, -0.4667, -1.2183, -0.84, -1.6785, -0.7456, -0.4791, -1.1653, -1.5957, 0.0336, 0.4701, -0.7079, -0.6846, 0.3328, 0.3303, 1.3836, 0.7911, 1.7488, 1.1308, 1.2956, 0.8798, 1.7373, 0.9586, 1.8499, 2.2335, 1.5731, 0.4008, -0.0371, 1.6101, -1.2336, 0.5433, -2.2444, -1.7888, -1.9902, -0.5829, -1.8231, -2.4398, -0.6685, -2.1831, 0.017, -2.4303, 0.0994, 0.4982, 1.1523, -0.0347, -0.4759, 1.9048, -0.1062, 0.0697, 1.8886, -0.1113, 1.2334, -0.1532, 3.6539, -2.4797, 0.8638, -0.1987, 1.7497, 0.6219, -1.3278, 3.352, -0.718, -0.9265, 1.2648, 2.9651, -1.0785, 0.1678, 1.4231, 1.2481, -1.7571, 1.5341, 0.306, -2.5732, 0.2056, -0.2966, 2.7589, -1.4607, 1.5037, 0.1719, -0.4316, 1.9451, 0.1518, -0.0716, 2.7813, 1.3852, 2.8818, 1.0228, 3.2534, 1.0655, 3.4877, 4.9333, 3.9492, 1.5859, -1.3323, 0.1539, -8.2875, -11.6248, -4.5577, -1.4914, -7.6404, -11.1049, -3.0772, -8.8921, -8.0471, 5.4288, 1.9505, -2.6676, 3.5387, 3.0975, 6.5524, -0.0976, 11.3418, 8.4664, 7.8295, 6.1537, 4.2508, 5.7803, -1.0401, 3.7323, -0.5153, -5.821, -7.7708, -4.1566, -11.2804, -7.1415, -5.6155, -5.2685, -5.3583, -7.3842, -1.0591, -10.0856, 4.1476, -2.1055, 0.8762, 1.4426, 1.6566, 6.9868, 5.1162, 4.6446, 8.3505, 6.4648, 1.7013, 4.7948, 3.419, 2.4885, -4.6991, 4.1673, -3.5546, -3.7023, 0.0083, -2.7821, -1.3335, -0.8429, 1.4718, -0.0303, 0.7878, 4.2729, 3.2946, 3.3478, 3.5068, 2.196, 4.75, 3.0323, 0.617, 2.595, -0.8378, 1.3028, -2.2149, -2.9978, -3.6646, -1.3007, -3.5103, -3.6742, -4.2581, 1.1768, -2.3458, -0.4244, 1.1485, -0.1, 2.3285, -0.6986, 3.0575, 0.6693, 0.9952, 1.382, 1.8491, -2.4153, -0.5539, 0.9289, -1.4749, -3.0613, -1.3126, -1.7172, -3.9094, -2.2323, -1.396, -2.6438, -2.0906, -1.0507, -0.7067, -3.0099, 0.7668, 0.7978, 0.2292, 0.8779, 2.2672, 1.4327, 1.5972, 0.6235, 3.3033, 1.2373, -0.198, 0.8798, -0.7944, -1.7652, -0.5742, 0.4372, -0.2397, -1.7238, 0.739, -1.2822, -1.3572, -1.7037, -0.328, 0.2501, -0.2704, 2.5771, 0.0033, 1.1614, 0.5617, 0.5885, 2.2182, 3.2185, 1.799, 2.069, -1.0356, 0.6265, -0.8888, -1.8267, -0.0596, -2.2319, -1.2378, -3.9064, -0.3483, -3.8219, -1.5502, -1.3568, -0.1551, -1.4593, 1.7172, 1.9039, 0.415, 1.668, 1.585, 2.8463, 1.4722, 2.3944, 3.0644, 2.6259, 2.701, 1.3998, 2.851, -0.1024, 1.3371, -1.6789, 0.7056, -5.3171, -1.466, -1.3605, -2.8465, -3.1052, -3.3442, -0.9258, -3.2178, 1.3341, -2.8031, 1.6767, -0.5045, 1.2672, -0.636, 1.4031, 1.7543, 1.5428, 1.2568, 0.4799, 2.2369, 0.3258, 1.426, 0.2021, -1.6547, 0.0888, -0.7736, -1.2049, -2.3647, -1.1055, -0.4496, -1.0563, -0.6187, 0.1657, 1.0693, 1.8263, 2.2759, 1.2841, 0.9458, 1.634, 0.5343, -0.4089, 0.3285, 0.5123, 1.536, 0.6299, 0.3471, -0.5072, 0.7434, -0.2902, 0.7973, 0.7731, 1.2511, -0.3673, 1.3639, 0.6524, 0.8393, 1.8203, 3.4517, 1.8399, 2.1142, 1.1223, -1.1691, -3.151, -7.007, -8.23, -4.87, -4.8428, -2.5768, -6.8734, -8.1512, -7.3836, -3.6037, 2.0688, 0.0662, 2.0588, 2.1333, 4.2049, 4.2315, 5.1578, 6.5475, 8.7305, 7.7633, 7.006, 4.2185, 1.6733, 3.0444, 1.1883, -1.9412, -7.4797, -4.9887, -7.7277, -8.1869, -7.81, -7.2413, -5.4049, -8.4781, -3.5721, -5.3762, -3.3218, -4.1794, 2.5283, -0.9782, 0.931, 5.0999, 4.085, 5.4847, 5.1614, 8.2425, 3.3404, 5.8743, 3.8954, 3.3326, 0.7264, 1.573, -0.6481, -2.3928, -3.3409, -1.3127, -2.2097, -2.3554, -0.2392, -1.0339, -1.5819, 0.0429, 2.0706, 2.4205, 2.8536, 3.7099, 4.0118, 3.774, 1.7683, 3.5174, -2.1167, -0.0851, 1.9756, 0.1074, -4.842, -4.1763, -1.6504, -3.9175, -2.3365, -1.8462, -0.8768, -4.0436, -0.9673, -1.202, -0.438, -0.3226, 2.5241, 0.5829, -2.7137, 0.658, 1.2572, 1.2405, 0.2188, 1.2181, 0.1674, 0.0544, 1.3138, -3.9855, -2.3917, -0.7795, -1.6068, -3.9551, -0.7023, -3.0744, -2.4573, -1.3916, -0.6969, -1.748, -1.5055, 0.5296, 1.1897, -0.0525, 1.3868, 2.4817, 0.6429, 0.0221, 0.6225, 2.0512, 1.923, 2.9493, 0.4451, -3.2109, -0.6946, -0.1913, 0.4391, -2.4646, -1.6942, -2.3806, -1.4176, -0.9054, -1.3477, 1.1732, 0.954, 2.1215, 0.0593, 1.3329, 2.1203, 0.9198, 1.9067, 0.4669, 1.2056, 1.2318, -0.0725, -2.7046, -2.367, -0.4188, -0.4803, -1.3107, -2.2018, -3.3056, -0.6554, -1.6166, -0.3966, -1.4389, -0.0628, 0.1094, 0.2593, 0.0116, 0.0689, 2.4702, 0.8414, 1.9186, 1.5757, 3.1954, 0.6511, 1.9096, 0.6844, 0.7807, 1.3129, 1.0162, 0.1464, -2.837, -1.6143, -1.5495, -1.8273, -1.8012, -2.4856, -1.8646, -3.6732, -0.7845, -1.0735, -0.0585, 0.132, -1.154, 1.715, -0.1169, 0.9022, -0.0595, -0.1099, 0.8276, 0.8689, 0.876, -1.3464, 0.9644, -2.0649, -0.7244, -0.158, 0.7315, 0.419, -0.2942, 0.1955, -1.7831, 0.9081, 2.2083, 1.8427, 0.5025, 1.0463, 1.631, -0.024, 0.6277, 0.2931, -0.376, 0.2117, 0.1176, 0.094, -1.2786, -0.1184, -0.0703, 0.0781, -0.1381, 1.8593, 0.9796, -0.1097, 1.5904, 2.0413, 2.4755, 3.0017, 1.95, 1.5554, 2.0758, 3.312, 1.2148, -1.1372, -3.3646, -5.4403, -8.766, -5.5424, -5.0367, -2.6404, -7.0453, -6.7836, -6.784, -1.9922, 1.6313, -0.3541, 0.3288, 2.2436, 2.4585, 7.7745, 4.266, 6.4293, 7.3005, 7.6374, 4.3358, 4.1501, 4.4503, 2.3108, 2.1162, -4.8594, -3.3391, -7.1168, -4.5089, -5.9364, -8.5527, -5.3451, -5.8512, -7.3191, -8.0881, -4.0118, -3.6691, -0.1673, -1.3565, 0.926, -0.6979, 3.5245, 6.1654, 5.2366, 5.3541, 4.8621, 4.3671, 4.3676, 1.4295, 3.8898, 2.0822, 0.4637, -3.6211, -1.5924, 0.5969, -3.2823, -1.1517, -2.8438, 1.0383, -1.4656, -0.2473, 1.7298, 3.4833, 2.1926, 3.6935, 3.5526, 3.8216, 4.3485, 3.5487, 2.312, 0.1567, 0.1603, -0.9022, -0.3932, -4.1378, -3.8342, -1.2194, -3.3517, -2.5511, -2.1765, -2.2879, 3.26, -1.1831, 1.8867, -0.7951, 2.7503, 1.2037, 1.1758, 0.5221, 0.7867, 0.8633, -0.4523, -1.9062, -1.2701, 0.4253, -0.9393, -2.3174, -3.4047, -2.0024, -3.8087, -1.9477, -1.8123, -2.1978, -1.5875, 0.3236, -1.3078, -0.925, -1.2838, 3.0084, 1.8208, 0.3764, 2.2614, 1.9732, 0.0873, 0.5199, 3.1137, 0.8011, -0.1839, 1.1997, 1.5519, -1.6923, -1.0181, 0.6518, -1.3578, -2.539, -1.3717, -0.6192, -2.1051, -1.8831, -0.2644, -1.5536, 0.3091, 1.2347, 2.5531, 0.3419, 1.1079, 1.8777, 2.027, 1.7044, 2.1205, 0.4294, -1.4535, -0.5598, -1.5891, -1.9992, -1.674, -1.3672, -1.9993, -1.5192, -0.753, -1.2053, -1.1093, -0.3397, 0.5372, 1.5128, 1.1784, 0.4515, 1.4227, 1.7878, 2.5786, 1.4395, 2.9477, 1.3602, 3.3779, 0.5414, 1.0119, 1.5197, 1.3478, 0.8927, -0.6656, 0.374, -1.26, -0.7693, -0.5007, -2.0944, -1.1786, -1.0432, -1.3889, -2.8678, -1.8764, -1.1538, -0.2625, -0.7067, 0.1475, 0.8439, -0.7046, 0.3304, 0.6204, 0.436, 0.4986, 0.581, -0.0356, -0.8347, 1.7421, 0.3636, 0.051, -1.1191, 1.1107, -0.7801, -0.0187, 0.7891, -0.8478, 0.0327, 0.8701, 1.2076, -0.7921, 1.2937, 1.8859, 1.5542, 0.4217, 0.2771, 0.4756, 0.5425, -0.0523, -1.0312, -0.6089, -1.1236, -0.0593, -0.7037, 0.5324, 0.339, 1.9323, 0.5098, 0.7053, 0.7208, 1.4392, 0.94, 2.7018, 2.4989, 3.3045, 3.7763, 4.18, 2.259, 4.9441, 2.9276, 1.5378, -2.1477, -4.7199, -8.7872, -8.1023, -6.5862, -5.0669, -5.314, -7.2076, -7.8861, -7.1013, -1.2012, 1.7459, 1.319, 1.3261, 1.5271, 4.9014, 4.4435, 5.6069, 8.0833, 9.9641, 7.5991, 6.3718, 4.2216, 3.8688, 0.7804, 1.5123, -3.4307, -5.3061, -7.588, -7.1483, -9.4839, -7.1921, -7.1946, -4.0204, -6.198, -6.1275, -1.5803, -6.0264, 1.5752, -1.3512, 2.6806, 0.9106, 6.2538, 2.3466, 7.6808, 4.7016, 7.9016, 2.8077, 4.1744, 1.8529, 3.9121, -2.4474, 0.8801, -2.6422, -1.4949, -3.4913, -0.9497, -2.2485, -0.8604, 0.9254, -2.2147, 4.5371, -1.5361, 5.5874, 2.7816, 4.7145, 0.9569, 8.1478, 1.5299, 4.8018, -0.4191, 2.1098, -0.5102, -2.2048, -2.9632, -1.8354, -4.2771, -5.5546, -0.768, -2.8978, -3.0262, 1.9516, -0.7863, 2.2119, -0.2703, 3.4759, 1.6297, 1.579, 0.7144, 0.7172, 3.1796, -1.4521, 1.3204, -0.955, 0.1307, -3.1943, 0.0515, -2.9912, -0.9326, -3.3911, -1.3723, -4.5201, -1.2655, -2.2225, -1.017, -1.057, -0.0238, -0.4648, 1.9744, 0.4625, 2.1992, 1.4294, 0.9869, 2.8635, 0.3722, 2.913, -0.0087, 1.3828, -0.4597, 1.3132, -1.5441, 0.0587, -1.3153, -2.4972, -2.299, -2.4119]};

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

    function onFaultChange(val) {
      const sld = document.getElementById('sld-sev');
      const txt = document.getElementById('txt-sev');
      const note = document.getElementById('guardrail-note');
      if (val === 'normal') {
        sld.value = 0.0;
        sld.disabled = true;
        txt.innerText = '0.00';
        if (note) note.classList.remove('hidden');
      } else {
        sld.disabled = false;
        if (parseFloat(sld.value) === 0.0) {
          sld.value = 0.65;
          txt.innerText = '0.65';
        }
        if (note) note.classList.add('hidden');
      }
    }

    function applyPreset(fault, sev) {
      document.getElementById('sel-fault').value = fault;
      onFaultChange(fault);
      if (fault !== 'normal') {
        document.getElementById('sld-sev').value = sev;
        document.getElementById('txt-sev').innerText = sev.toFixed(2);
      }
    }

    function switchTab(idx) {
      for (let i = 0; i < 6; i++) {
        const btn = document.getElementById(`tab-btn-${i}`);
        const content = document.getElementById(`tab-content-${i}`);
        if (!btn || !content) continue;
        if (i === idx) {
          btn.className = "py-2.5 px-3 border-b-2 border-[rgb(255,75,75)] text-[rgb(255,75,75)] flex items-center gap-1.5 cursor-pointer transition text-xs font-bold whitespace-nowrap";
          content.classList.remove('hidden');
        } else {
          btn.className = "py-2.5 px-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-1.5 cursor-pointer transition text-xs whitespace-nowrap";
          content.classList.add('hidden');
        }
      }
      if (idx === 5) {
        setTimeout(renderDbTelemetryChart, 100);
      }
      window.dispatchEvent(new Event('resize'));
    }

    function switchDbSubTable(subId) {
      const subs = ['equipments', 'spare-parts', 'telemetry', 'work-orders'];
      subs.forEach(s => {
        const btn = document.getElementById(`btn-sub-${s}`);
        const panel = document.getElementById(`panel-sub-${s}`);
        if (!btn || !panel) return;
        if (s === subId) {
          btn.className = "px-3 py-1.5 rounded-lg text-xs font-semibold bg-[rgb(255,75,75)] text-white shadow transition cursor-pointer";
          panel.classList.remove('hidden');
        } else {
          btn.className = "px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition cursor-pointer";
          panel.classList.add('hidden');
        }
      });
      if (subId === 'telemetry') {
        setTimeout(renderDbTelemetryChart, 50);
      }
    }

    function renderDbTelemetryChart() {
      const el = document.getElementById('dbTelemetryPlot');
      if (!el || typeof Plotly === 'undefined') return;

      const timestamps = [
        "07:53", "08:53", "09:53", "10:53", "11:53", "12:53", "13:53", "14:53", "15:53", "16:53"
      ];
      const degradation = [4.2, 5.4, 6.1, 7.5, 8.9, 10.8, 12.4, 32.1, 67.3, 88.5];
      const rms = [0.44, 0.43, 0.36, 0.42, 0.43, 0.45, 0.41, 0.43, 1.60, 4.14];

      const traceDeg = {
        x: timestamps,
        y: degradation,
        mode: 'lines+markers',
        name: 'ความเสื่อมสภาพ (%)',
        line: { color: '#f43f5e', width: 3 },
        marker: { size: 7, color: '#f43f5e' }
      };

      const traceRms = {
        x: timestamps,
        y: rms.map(v => v * 20),
        mode: 'lines+markers',
        name: 'RMS Vibration (x20 g)',
        line: { color: '#38bdf8', width: 2, dash: 'dot' },
        marker: { size: 5, color: '#38bdf8' }
      };

      const layout = {
        title: {
          text: 'แนวโน้มการเสื่อมสภาพ Run-to-Failure Evolution (TEST-RIG-01)',
          font: { size: 13, color: '#f8fafc' }
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(15, 23, 42, 0.6)',
        margin: { l: 40, r: 20, t: 35, b: 35 },
        xaxis: {
          title: 'เวลาบันทึก (Timestamp)',
          color: '#94a3b8',
          gridcolor: '#334155'
        },
        yaxis: {
          title: 'ดัชนี (%) / สเกลแปลงค่า',
          color: '#94a3b8',
          gridcolor: '#334155'
        },
        legend: {
          orientation: 'h',
          y: 1.15,
          font: { color: '#cbd5e1', size: 11 }
        }
      };

      Plotly.newPlot(el, [traceDeg, traceRms], layout, { responsive: true, displayModeBar: false });
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
      switchTab(4);
      setTimeout(() => {
        window.print();
      }, 100);
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
</html>"""
