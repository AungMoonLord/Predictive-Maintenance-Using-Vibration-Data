@echo off
chcp 65001 >nul
echo ============================================================
echo   MechAgent: Agentic AI Predictive Maintenance Dashboard
echo ============================================================
echo Starting Streamlit Web UI on http://localhost:8501 ...
echo.
call .venv\Scripts\streamlit.exe run demo\dashboard.py
pause
