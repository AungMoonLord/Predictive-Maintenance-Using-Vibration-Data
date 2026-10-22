# MechAgent Web Dashboard Launcher
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  MechAgent: Agentic AI Predictive Maintenance Dashboard" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting Streamlit Web UI on http://localhost:8501 ..." -ForegroundColor Yellow
Write-Host ""
& ".\.venv\Scripts\streamlit.exe" run demo\dashboard.py
