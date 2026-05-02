@echo off
:: 設定 CMD 編碼為 UTF-8，避免中文亂碼
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo ❄️ HVAC System is Starting...
echo ========================================

echo [1/3] 檢查並安裝必要的 Python 套件 (FastAPI, Uvicorn, CoolProp)...
pip install fastapi uvicorn CoolProp >nul 2>&1

echo [2/3] 啟動 Python 後端引擎...
echo [3/3] 網頁瀏覽器將在 3 秒後自動開啟...

:: 延遲 3 秒後開啟網頁，確保後端有足夠時間啟動
start "" cmd /c "timeout /t 3 >nul & start hvac_analyzer-pro.html"

:: 啟動 FastAPI 伺服器
python -m uvicorn main:app --reload

:: 如果伺服器意外關閉，暫停視窗讓使用者看得到錯誤訊息
pause