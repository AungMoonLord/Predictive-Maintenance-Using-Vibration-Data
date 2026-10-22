@echo off
chcp 65001 >nul
echo ============================================================
echo   MechAgent: Automated AWS Cloud Deployment
echo ============================================================
call .venv\Scripts\python.exe aws_deploy.py
pause
