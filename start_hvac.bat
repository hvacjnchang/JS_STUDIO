@echo off
cd /d "%~dp0"
echo ========================================
echo HVAC System is Starting...
echo ========================================
echo [1/2] Starting Python Engine...
echo [2/2] Web Browser will open in 3 seconds...

start "" cmd /c "timeout /t 3 >nul & start hvac_analyzer-pro.html"

python -m uvicorn main:app --reload
pause