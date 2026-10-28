@echo off
title CupidOS - Autonomous Agent Dating Protocol
echo ========================================================
echo    CupidOS: Autonomous Agent-to-Agent Dating Protocol
echo    Starting Local Server & Apify Store Integration...
echo ========================================================

set PYTHON_CMD=python
where python >nul 2>nul
if %errorlevel% neq 0 (
    if exist "C:\Users\SURYA\AppData\Local\Programs\Python\Python312\python.exe" (
        set PYTHON_CMD="C:\Users\SURYA\AppData\Local\Programs\Python\Python312\python.exe"
    ) else if exist "py.exe" (
        set PYTHON_CMD=py
    )
)

echo Starting Python server on port 8080...
start "" %PYTHON_CMD% server.py

timeout /t 2 /nobreak >nul
echo Opening Web Application in your default browser...
start http://localhost:8080

echo Server is running. Press any key to close this launcher window (server stays in background).
pause
