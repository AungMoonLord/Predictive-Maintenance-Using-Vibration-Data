# Predictive Maintenance Using Vibration Data (MechAgent)

[![AWS Serverless](https://img.shields.io/badge/AWS-Serverless_100%25-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org)
[![Amazon Bedrock](https://img.shields.io/badge/Amazon_Bedrock-GenAI_Agent-0073BB?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/bedrock)
[![Amazon SageMaker](https://img.shields.io/badge/SageMaker-Serverless_Inference-232F3E?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/sagemaker)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Autonomous Physics-Informed Multitask AI Agent for Bearing Fault Diagnosis, Degradation Tracking & Autonomous Maintenance Planning on AWS 100% Serverless Architecture.**

---

## 🌐 Live Demonstrations & Cloud Endpoints

The system is deployed and publicly accessible in **AWS Region `ap-southeast-1` (Asia Pacific - Singapore)** with 100% Serverless Architecture (Zero EC2, Zero Idle Cost):

- **🖥️ Production Web Dashboard (CloudFront CDN):**  
  [https://d38e5nijdx3gmh.cloudfront.net](https://d38e5nijdx3gmh.cloudfront.net)
- **⚡ Backend REST API Gateway:**  
  [https://jynfhl5nc9.execute-api.ap-southeast-1.amazonaws.com](https://jynfhl5nc9.execute-api.ap-southeast-1.amazonaws.com)

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Key Innovations & Technical Highlights](#-key-innovations--technical-highlights)
3. [System Architecture](#-system-architecture)
4. [Tech Stack](#-tech-stack)
5. [Prerequisites](#-prerequisites)
6. [Local Setup & Running Guide](#-local-setup--running-guide)
7. [API Reference & Endpoints](#-api-reference--endpoints)
8. [Dataset & Benchmark Support](#-dataset--benchmark-support)
9. [Cost Optimization & Serverless Economics](#-cost-optimization--serverless-economics)
10. [Security & Best Practices](#-security--best-practices)
11. [Project Structure](#-project-structure)
12. [License & Acknowledgments](#-license--acknowledgments)

---

## 🎯 Project Overview

In industrial manufacturing, **rolling element bearing failures account for over 40–50% of all rotating equipment breakdowns** (electric motors, centrifugal pumps, gearboxes, and compressors). Traditional maintenance strategies suffer from critical shortcomings:
- **Preventive Maintenance (Time-based):** Machines are inspected or bearings replaced every 30–90 days. Sudden defects developing between cycles cause catastrophic unplanned downtime costing \$5,000–\$50,000/hour.
- **Manual Spectrum Analysis:** Interpreting FFT, envelope analysis, and harmonic peaks requires scarce and expensive vibration specialists.
- **Disconnected Workflows:** Vibration analysis, spare part inventory checks, production scheduling, and work order creation are siloed, requiring 2 to 4 hours of manual coordination per incident.

### The MechAgent Solution
**MechAgent** bridges deterministic physics, deep multitask learning, and generative AI orchestration:
1. **Signal Processing & Feature Extraction:** Bandpass filtering (1–5 kHz) and Hilbert transform calculate the envelope spectrum in the **order domain (orders = Hz / shaft RPS)**, making diagnosis independent of machine operating speed.
2. **Multitask Deep Learning:** A fine-tuned DistilHuBERT backbone simultaneously predicts:
   - **Fault Location:** Normal, Inner Race (BPFI), Outer Race (BPFO), Ball defect (BSF), or Cage defect (FTF).
   - **Degradation Level:** 0.0% (healthy) to 100.0% (total failure).
   - **Remaining Useful Life (RUL):** Exact remaining hours with $P_5 / P_{50} / P_{95}$ confidence intervals via Gaussian Negative Log-Likelihood (NLL).
3. **Physics Verification:** Cross-validates neural network predictions against deterministic kinematic bearing defect frequencies.
4. **Autonomous AI Maintenance Agent:** Built on **Amazon Bedrock (Nova Pro)** with tool-use capability. The agent queries machine profiles, checks warehouse spare parts, inspects production schedules, reviews maintenance manuals, drafts an optimal work order before the safety deadline, and dispatches 1-click approval links to engineering supervisors.

---

## 💡 Key Innovations & Technical Highlights

- **Speed-Invariant Order Tracking:** Physics-based order domain analysis allows zero-shot evaluation across variable-speed motors and different bearing geometries (e.g., 6205, 6208, 6310).
- **Multitask Learning with Uncertainty Weighting:** 1 shared feature extractor with 3 specialized heads trained with Kendall et al. adaptive homoscedastic uncertainty loss, preventing negative transfer.
- **Safety-First Deadline Enforcement:** The AI agent uses the conservative $P_5$ (worst-case 5th percentile) RUL as a hard guardrail. It is strictly forbidden from scheduling maintenance past this safety window.
- **Two-Tier Cost-Aware Gatekeeper:** 95%+ of normal sensor readings are filtered out at the deterministic compute layer. Amazon Bedrock is invoked **only when true anomalies are confirmed**, keeping LLM costs to ~1 THB (\$0.03) per incident.
- **100% Serverless First:** Built entirely on Amazon S3, CloudFront, API Gateway, AWS Lambda, DynamoDB, SageMaker Serverless Inference, and Bedrock. **Zero compute charge when idle.**

---

## 🏗️ System Architecture

### Multi-Server MCP & Multi-Agent Collaborative Architecture
```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  MECHAGENT: END-TO-END SYSTEM ARCHITECTURE                                 │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  ┌── 1. INDUSTRIAL VIBRATION TELEMETRY LAYER ─────────────────────────────────────────────────────────────┐
  │                                                                                                        │
  │   ┌──────────────────────────┐   Raw Vibration   ┌──────────────────────────┐                          │
  │   │ 📊 Accelerometer Stream  ├──────────────────►│                          │                          │
  │   │    (16 kHz High-Freq)    │                   │ ⚡ Signal Conditioning   │                          │
  │   └──────────────────────────┘                   │ (Bandpass & Envelope FFT)│                          │
  │   ┌──────────────────────────┐ Replay Life-Cycle │                          │                          │
  │   │ 🧪 Benchmark Lab Dataset ├──────────────────►│                          │                          │
  │   │    (CWRU & XJTU-SY RTF)  │                   └────────────┬─────────────┘                          │
  │   └──────────────────────────┘                                │                                        │
  └───────────────────────────────────────────────────────────────┼────────────────────────────────────────┘
                                    ┌─────────────────────────────┴────────────────────────────┐
                                    │ Envelope Orders                    1D Signal Windows     │
                                    ▼                                                          ▼
  ┌── 2. PHYSICS-INFORMED MULTITASK AI LAYER ────────────────────────────────────────────────────────────────┐
  │                                                                                                          │
  │   ┌──────────────────────────┐                           ┌──────────────────────────┐                    │
  │   │ 📐 Kinematic Tracking    │                           │ 🤖 1D-CNN Multi-Task     │                    │
  │   │ (BPFO/BPFI/BSF/FTF Peaks)│                           │ (Fault Head: S0 to S4)   │                    │
  │   └────────────┬─────────────┘                           └────────────┬─────────────┘                    │
  │                │ Physics Guardrail                                    │ Health Index                     │
  │                └───────────────────────────────┬──────────────────────┘                                  │
  │                                                ▼                                                         │
  │                                  ┌──────────────────────────┐                                            │
  │                                  │ ⏳ Monte Carlo RUL Engine│                                            │
  │                                  │ (P05 Safety Bounds / RUL)│                                            │
  │                                  └─────────────┬────────────┘                                            │
  └────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┘
                                                   │ Supply P05 Metrics
                                                   ▼
  ┌── 3. MODEL CONTEXT PROTOCOL (MCP) TOOL SERVERS ──────────────────────────────────────────────────────────┐
  │                                                                                                          │
  │   ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐   │
  │   │ 🔬 physics_diagnostic│ │ 📦 cmms_inventory    │ │ ⚙️ scada_production │ │ 🛡️ safety_sop_server │   │
  │   │  (Envelope Matching) │ │ (Spare Bearing Stock)│ │ (VFD Derating / Cost)│ │ (Zero-Energy LOTO SOP)│   │
  │   └──────────┬───────────┘ └──────────┬───────────┘ └──────────┬───────────┘ └──────────┬───────────┘   │
  └──────────────┼────────────────────────┼────────────────────────┼────────────────────────┼────────────────┘
                 └────────────────────────┴───────────┬────────────┴────────────────────────┘
                                                      │ Standardized MCP Tool Protocol
                                                      ▼
  ┌── 4. AUTONOMOUS MULTI-AGENT DEBATE (AMAZON BEDROCK) ─────────────────────────────────────────────────────┐
  │                                                                                                          │
  │          ┌──────────────────────────┐   Trade-off Debate   ┌──────────────────────────┐                  │
  │          │     🛡️ Safety Agent      │◄────────────────────►│   ⚙️ Operations Agent    │                  │
  │          │(ISO 10816 / LOTO Boundary│                      │(VFD Derating Strategy -$45k)                │
  │          └────────────┬─────────────┘                      └────────────┬─────────────┘                  │
  │                       │                                                 │                                │
  │                       │ Enforce Safety Boundaries                       │ Propose Derated Run Strategy   │
  │                       └────────────────────────┬────────────────────────┘                                │
  │                                                ▼                                                         │
  │                                  ┌──────────────────────────┐                                            │
  │                                  │     ⚖️ Arbiter Agent     │                                            │
  │                                  │(Consensus & Action Plan) │                                            │
  │                                  └─────────────┬────────────┘                                            │
  └────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┘
                                                   │
             ┌─────────────────────────────────────┼─────────────────────────────────────┐
             │ Reserve Spares & Log WO             │ Compile Thai Report PDF             │ Dispatch Urgent Alert
             ▼                                     ▼                                     ▼
  ┌── 5. 100% SERVERLESS AWS INFRASTRUCTURE & OPERATIONS ────────────────────────────────────────────────────┐
  │                                                                                                          │
  │   ┌──────────────────────────┐           ┌──────────────────────────┐           ┌──────────────────────┐ │
  │   │ 💾 Amazon DynamoDB       │           │ 📦 Amazon S3 Storage     │           │ 🔔 Amazon SNS Gateway│ │
  │   │ (Dual-Engine / 4 Tables) │           │ (OEM Manuals & PDF Reps) │           │ (Instant SMS / Email)│ │
  │   └────────────┬─────────────┘           └──────────────────────────┘           └──────────┬───────────┘ │
  │                │ Feed Data                                                                 │ 1-Click     │
  │                ▼                                                                           ▼ Approval    │
  │   ┌──────────────────────────┐                                                  ┌──────────────────────┐ │
  │   │ 🌐 CloudFront + S3 SPA   │                                                  │ 👤 Plant Supervisor  │ │
  │   │ (Zero-Idle Web Dashboard)│                                                  │ (Human-in-the-Loop)  │ │
  │   └──────────────────────────┘                                                  └──────────────────────┘ │
  └──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Multi-Agent Debate & Decision Workflow
```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              MULTI-AGENT DEBATE & WORK ORDER DECISION SEQUENCE                              │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  📡 Sensor    🧠 MTL & Phys    🛡️ Safety       ⚙️ Ops Agent     ⚖️ Arbiter       🗄️ CMMS/S3     👤 Supervisor
     │               │              │               │               │               │               │
  ───┼───────────────┼──────────────┼───────────────┼───────────────┼───────────────┼───────────────┼───
  PHASE 1: INGESTION & FAULT PREDICTION
  ───┼───────────────┼──────────────┼───────────────┼───────────────┼───────────────┼───────────────┼───
     │ 1. Raw 16 kHz │              │               │               │               │               │
     ├──────────────►│              │               │               │               │               │
     │               │ 2. S3 / RUL  │               │               │               │               │
     │               ├─────────────►│               │               │               │               │
     │               │              │               │               │               │               │
  ───┼───────────────┼──────────────┼───────────────┼───────────────┼───────────────┼───────────────┼───
  PHASE 2: MULTI-AGENT TRADE-OFF DEBATE (AMAZON BEDROCK)
  ───┼───────────────┼──────────────┼───────────────┼───────────────┼───────────────┼───────────────┼───
     │               │              │ 3. Spalling   │               │               │               │
     │               │              ├──────────────►│               │               │               │
     │               │              │               │ 4. Derate     │               │               │
     │               │              │               │──┐ -15% RPM   │               │               │
     │               │              │               │◄─┘            │               │               │
     │               │              │               │ 5. Save $45k  │               │               │
     │               │              │               ├──────────────►│               │               │
     │               │              │ 6. Enforce ISO 10816 & LOTO   │               │               │
     │               │              ├──────────────────────────────►│               │               │
     │               │              │               │               │ 7. Consensus  │               │
     │               │              │               │               │──┐ Approve    │               │
     │               │              │               │               │◄─┘ Derated Run│               │
     │               │              │               │               │               │               │
  ───┼───────────────┼──────────────┼───────────────┼───────────────┼───────────────┼───────────────┼───
  PHASE 3: ACTION PLAN & HUMAN-IN-THE-LOOP APPROVAL
  ───┼───────────────┼──────────────┼───────────────┼───────────────┼───────────────┼───────────────┼───
     │               │              │               │               │ 8. Reserve WO │               │
     │               │              │               │               ├──────────────►│               │
     │               │              │               │               │ 9. Save PDF   │               │
     │               │              │               │               ├──────────────►│               │
     │               │              │               │               │ 10. Dispatch SMS / Email      │
     │               │              │               │               ├──────────────────────────────►│
     │               │              │               │               │               │ 11. 1-Click OK│
     │               │              │               │               │               │◄──────────────┤
     ▼               ▼              ▼               ▼               ▼               ▼               ▼
```

### AWS Services & Roles
| AWS Service | Architectural Function |
|---|---|
| **Amazon S3 & CloudFront** | Hosts and accelerates the responsive Industrial Dark Web Dashboard SPA worldwide via HTTPS. |
| **Amazon API Gateway** | Provides managed, low-latency HTTP REST API endpoints (`/analyze`, `/reports/{id}`, `/approve`). |
| **AWS Lambda** | Serverless orchestrator executing signal preprocessing, gatekeeper logic, Bedrock agent loop, and reporting. |
| **Amazon SageMaker Serverless** | On-demand ML inference for DistilHuBERT-MTL (Fault classification, Deg%, RUL). Auto-scales to zero. |
| **Amazon Bedrock (Nova Pro)** | Reasoning AI Agent with tool-use (RAG manual lookup, inventory query, schedule optimization). |
| **Amazon DynamoDB** | Ultra-fast single-table NoSQL store for machine profiles, sensor readings, parts inventory, schedules, and audit trails. |
| **Amazon SNS** | Instant notifications, human-in-the-loop email action triggers, and work order dispatching. |

---

## 🛠️ Tech Stack

- **Core & Runtime:** Python 3.10+, PyTorch 2.1+, Hugging Face Transformers (`DistilHuBERT`), NumPy, SciPy (Signal & FFT), Pandas
- **Cloud & Serverless:** AWS Lambda, Amazon API Gateway, Amazon S3, Amazon CloudFront, Amazon DynamoDB, Amazon SageMaker Serverless, Amazon Bedrock
- **Frontend / Dashboard:** Vanilla HTML5 / JavaScript (ES6+), Tailwind CSS, Plotly.js, Sarabun typography
- **Local Prototyping:** Streamlit 1.30+, Plotly, ReportLab (PDF generation)
- **Testing & Quality Assurance:** PyTest 8.0+, Boto3, Botocore

---

## 📦 Prerequisites

Ensure the following tools are installed on your workstation:
1. **Python:** Version `3.10`, `3.11`, or `3.12` ([Download Python](https://www.python.org/downloads/))
2. **Git:** ([Download Git](https://git-scm.com/))
3. **AWS CLI v2:** Configured with administrative or deployment IAM permissions ([Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
4. **(Optional) Node.js & Docker:** Required only if modifying CDK or SAM container images.

---

## 🚀 Local Setup & Running Guide

### 1. Clone Repository & Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/AungMoonLord/Predictive-Maintenance-Using-Vibration-Data.git
cd Predictive-Maintenance-Using-Vibration-Data

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Windows (Command Prompt):
.\.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate
```

### 2. Install Project Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the `.env.example` template to create your local `.env` file:
```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```
Open `.env` and fill in your AWS credentials and resource names:
```env
AWS_REGION=ap-southeast-1
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
TABLE_NAME=mechagent-table
SAGEMAKER_ENDPOINT_NAME=mechagent-endpoint
BEDROCK_MODEL_ID=apac.amazon.nova-pro-v1:0
APPROVAL_SECRET=your-random-hmac-secret-string
```

### 4. Run Interactive Local Dashboard (Streamlit)
For local testing and offline experimentation:
```bash
# Option A: Run Streamlit directly
streamlit run demo/dashboard.py

# Option B: Quick-start batch script (Windows)
run_demo.bat
```
Open your browser at **`http://localhost:8501`** to interact with the local control center.

### 5. Run ML Pipeline Smoke Test
Verify the synthetic signal generator, feature extraction, model inference, and report generator:
```bash
python src/pipeline.py --quick
```

### 6. Run Automated Test Suite
Execute the unit and integration tests:
```bash
pytest
```
*(All 23 core test cases will validate physical frequency calculations, envelope analysis, multitask outputs, DynamoDB serializers, and HMAC approval generation).*

---

## 📡 API Reference & Endpoints

Base URL: `https://jynfhl5nc9.execute-api.ap-southeast-1.amazonaws.com`

### 1. `GET /` — Web Dashboard SPA
Returns the complete responsive single-page application for monitoring and manual signal diagnosis.

---

### 2. `POST /analyze` — Ingest & Analyze Vibration Signal
Processes vibration signals, triggers SageMaker inference, runs physics verification, checks gatekeeper conditions, and invokes the Bedrock agent if degradation is detected.

**Request Body (JSON):**
```json
{
  "machine_id": "PUMP-01",
  "bearing_model": "6205",
  "rpm": 1797.0,
  "sampling_rate": 16000,
  "signal": [0.012, -0.045, 0.123, 0.089, "... (min 4,000 samples) ..."]
}
```

**Response (JSON - HTTP 200 / 202):**
```json
{
  "job_id": "f48c3b71-705a-4ba9-9e8c-851508db8c0b",
  "status": "COMPLETED",
  "fault": "OUTER_RACE",
  "degradation_pct": 47.8,
  "rul_hours": 142.5,
  "safety_deadline": "2026-10-28T09:30:00+07:00",
  "action_required": true,
  "report_url": "/reports/f48c3b71-705a-4ba9-9e8c-851508db8c0b"
}
```

---

### 3. `GET /reports/{job_id}` — Retrieve Diagnostic Report & Audit Trail
Fetches full analysis results, physical spectrum peaks, agent reasoning trace, inventory allocations, and timeline history.

**Response (JSON):**
```json
{
  "job_id": "f48c3b71-705a-4ba9-9e8c-851508db8c0b",
  "machine_id": "PUMP-01",
  "fault_class": "OUTER_RACE",
  "degradation_pct": 47.8,
  "rul_prediction": {
    "p5": 98.4,
    "p50": 142.5,
    "p95": 195.2
  },
  "physics_verification": {
    "bpfo_detected": true,
    "bpfo_order": 3.58,
    "peak_amplitude": 0.42
  },
  "agent_recommendation": "Bearing 6205 replacement scheduled for next planned stop...",
  "status": "AWAITING_APPROVAL"
}
```

---

### 4. `GET /approve?action={action}&job_id={id}&token={token}` — Human-in-the-Loop Review
Foreman approval portal with cryptographically verified HMAC-SHA256 signature tokens. Supported actions:
- `approve`: Approves maintenance schedule and reserves spare parts in DynamoDB.
- `postpone`: Postpones action by 24 hours (with safety guardrail check).
- `reject`: Rejects the proposed work order.

---

## 📊 Dataset & Benchmark Support

MechAgent includes comprehensive support for both synthetic physics simulations and premier global benchmark vibration datasets:

1. **Synthetic Physics-Based Simulator (`src/simulate.py`):**
   - Implements non-linear multi-body bearing dynamics, defect impact modeling, Gaussian background noise, harmonics, and exponential wear degradation curves.
2. **CWRU Bearing Data (Case Western Reserve University):**
   - 12k/48k Drive End / Fan End bearing tests. Inner race, outer race, and ball fault verification.
3. **XJTU-SY Bearing Dataset (Xi'an Jiaotong University):**
   - Complete run-to-failure fatigue lifecycles across diverse radial loads and RPMs.
4. **IMS Bearing Dataset (University of Cincinnati):**
   - Multi-day continuous run-to-failure vibration data.

---

## 💰 Cost Optimization & Serverless Economics

Operating cost estimate for a typical manufacturing plant with **50 monitored machines** taking vibration readings every 10 minutes (**216,000 monthly inferences**):

| AWS Service | Monthly Usage Specification | Estimated Cost (USD) |
|---|---|---|
| **SageMaker Serverless Inference** | 216,000 inferences × 0.5s duration @ 4 GB RAM | \$9.00 |
| **AWS Lambda (arm64 Graviton)** | ~430,000 invocations × 1.5s @ 512 MB | \$2.50 |
| **Amazon Bedrock (Nova Pro)** | ~20 true anomaly incidents × 30k input / 3k output tokens | \$0.70 |
| **Amazon S3 & CloudFront** | 10 GB storage (7-day signal lifecycle) + CDN data transfer | \$2.00 |
| **Amazon DynamoDB (On-Demand)** | ~650,000 writes / 300,000 reads | \$1.00 |
| **Amazon API Gateway (HTTP API)** | ~250,000 requests | \$0.30 |
| **Amazon SNS & CloudWatch Logs** | Incident alerts + 3 GB log retention | \$2.00 |
| **Total Monthly Operating Cost** | | **~\$17.50 – \$19.50 / Month (~650 THB)** |

> 💡 **Cost Savings Impact:** Compared to a single unplanned catastrophic breakdown causing \$15,000+ in production losses, MechAgent provides 24/7 autonomous monitoring at **less than \$20/month**.

---

## 🔒 Security & Best Practices

- **Zero Hardcoded Credentials:** All credentials, AWS keys, and secrets are strictly retrieved from environment variables or AWS Systems Manager (SSM) Parameter Store.
- **Strict `.gitignore` Policy:** Multi-gigabyte benchmark datasets (`real_dataset_from_lab/`), heavy binary weights (`*.pt`, `model.tar.gz`), `.env` files, and temporary test artifacts are strictly barred from version control.
- **HMAC-SHA256 Signed Approval Links:** Action links dispatched via email/Telegram are protected by time-stamped HMAC tokens, preventing unauthorized approvals or tampering.
- **IAM Least Privilege:** Dedicated IAM roles for Lambda execution restrict write access solely to DynamoDB table items scoped by machine partition keys.
- **Encrypted Communication:** Full end-to-end TLS 1.3 encryption for S3, CloudFront, API Gateway, and inter-service AWS communication.

---

## 📁 Project Structure

```
Predictive-Maintenance-Using-Vibration-Data/
├── .env.example                  # Environment variables template
├── .gitignore                    # Comprehensive security & dataset exclusion rules
├── README.md                     # Project documentation & reference guide
├── PRESENTATION.md               # NTT DATA Hackathon presentation slides & script
├── requirements.txt              # Production Python dependencies
├── template.yaml                 # AWS SAM CloudFormation template (100% Serverless)
│
├── site/                         # Frontend Single Page Application
│   └── index.html                # Industrial Dark Dashboard (Tailwind CSS + Plotly.js)
│
├── src/                          # Physics & Deep Learning Pipeline
│   ├── bearing_physics.py        # Kinematic defect frequencies & order envelope analysis
│   ├── dataset.py                # PyTorch dataset & data loaders
│   ├── inference.py              # SageMaker Serverless model handler & inference logic
│   ├── mech_config.py            # Bearing geometries (6205, 6208, 6310) & sampling specs
│   ├── mtl_model.py              # DistilHuBERT-MTL multitask model architecture
│   ├── pipeline.py               # End-to-end execution pipeline (simulate -> train -> infer)
│   ├── simulate.py               # Physics-based synthetic vibration generator
│   └── train.py                  # PyTorch multitask model fine-tuning with uncertainty loss
│
├── agent/                        # AWS Lambda Serverless Orchestration
│   ├── agent_core.py             # Amazon Bedrock Converse API tool-use loop
│   ├── dashboard_html.py         # Embedded dashboard fallback string
│   ├── handler.py                # Lambda entrypoint & API Gateway router
│   ├── report.py                 # Markdown & PDF maintenance report builder
│   └── tools.py                  # 7 Agent tools (DynamoDB, inventory, schedules, SNS)
│
├── demo/                         # Local Prototyping & Demos
│   ├── client.py                 # CLI demonstration client
│   └── dashboard.py              # Local Streamlit industrial control center
│
├── aws/                          # AWS Deployment Scripts & Seeding
│   ├── sagemaker_train.py        # SageMaker training job & serverless endpoint creation
│   └── seed_data.py              # DynamoDB seed data (machines, spare parts, schedules)
│
└── tests/                        # Automated PyTest Test Suite
    ├── test_agent.py             # Unit tests for Bedrock agent & tool dispatching
    ├── test_bearing_physics.py   # Unit tests for envelope spectrum & BPFI/BPFO physics
    ├── test_models.py            # Unit tests for PyTorch MTL architecture
    └── test_report.py            # Unit tests for report generation & HMAC approval links
```

---

## 📄 License & Acknowledgments

This project is open-source under the [MIT License](LICENSE).

Developed for the **NTT DATA Hackathon** — *Predictive Maintenance Using Vibration Data & Agentic AI on AWS*.
