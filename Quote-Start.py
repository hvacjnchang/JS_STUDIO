import subprocess
import os
import time
import webbrowser

# 取得目前檔案所在的資料夾路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# 1. 啟動後端伺服器 (不顯示黑色視窗，或開啟新視窗)
print("正在啟動後端伺服器...")
subprocess.Popen(["python", "server-v14-web.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)

# 2. 等待 3 秒讓伺服器準備好
time.sleep(3)

# 3. 開啟網頁
print("正在開啟網頁介面...")
webbrowser.open("v14-web.html")
