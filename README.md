# ❄️ HVAC & R 專業冷媒熱力學與循環分析系統

這是一個結合 Python (CoolProp) 後端與 HTML/JS 前端的專業冷凍空調循環分析工具。

## ⚠️ 重要提示：無法直接在網頁上運行
因為本系統需要進行複雜的熱力學計算，**必須依賴 Python 後端伺服器**。您無法直接在 GitHub 網頁上預覽並執行計算。

## 🚀 如何在您的電腦上運行 (Windows)

1. **下載專案**：
   - 點擊本頁面右上角的綠色按鈕 **`<> Code`**。
   - 選擇 **`Download ZIP`**。
   - 將下載的檔案解壓縮到您的電腦中。

2. **環境準備**：
   - 請確保您的電腦已經安裝了 [Python](https://www.python.org/downloads/) (建議版本 3.8 以上)。
   - 安裝 Python 時，請務必勾選 **"Add Python to PATH"**。

3. **一鍵啟動**：
   - 進入解壓縮後的資料夾。
   - 雙擊執行 **`start_hvac.bat`**。
   - 腳本會自動為您安裝所需的套件 (`fastapi`, `uvicorn`, `CoolProp`)，啟動後端伺服器，並自動在瀏覽器中開啟分析系統網頁。

## 🛠️ 系統架構
- `hvac_analyzer-pro.html`: 前端使用者介面與圖表渲染 (Plotly.js)。
- `main.py`: FastAPI 後端，負責接收參數並呼叫 CoolProp 進行熱力學狀態計算。
- `start_hvac.bat`: Windows 環境下的一鍵啟動腳本。