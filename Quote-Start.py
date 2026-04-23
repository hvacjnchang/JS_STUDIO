import subprocess
import os
import sys

def install_requirements():
    """自動檢查並安裝必要的 Web 套件"""
    try:
        import flask
        import flask_cors
    except ImportError:
        print("首次執行，正在安裝必要的 Web 套件 (Flask, Flask-CORS)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors"])

# 1. 檢查套件
install_requirements()

# 取得目前檔案所在的資料夾路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# 2. 啟動後端伺服器
print("正在啟動後端伺服器...")
print("請注意：在 Ubuntu 伺服器上，請保持此 SSH 終端機視窗開啟。")
print("若要停止伺服器，請按 Ctrl+C。")
print("-" * 50)

try:
    # 在 Linux 伺服器上直接運行，方便查看連線 Log
    subprocess.run([sys.executable, "server-v14-web.py"])
except KeyboardInterrupt:
    print("\n伺服器已手動關閉。")