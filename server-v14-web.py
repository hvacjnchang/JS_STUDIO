from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import json
import os

app = Flask(__name__)
CORS(app)  # 允許跨域請求

DB_FILE = 'quotes.db'

def init_db():
    """初始化 SQLite 資料庫"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 建立報價單資料表
    c.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            quoteNo TEXT PRIMARY KEY,
            date TEXT,
            clientName TEXT,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """直接從後端提供 HTML 網頁 (真正的 Web 模式)"""
    return send_from_directory('.', 'v14-web.html')

@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    """取得所有報價單列表"""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('SELECT quoteNo, date, clientName FROM quotes ORDER BY quoteNo DESC')
        rows = c.fetchall()
        conn.close()
        
        data =[{'quoteNo': r[0], 'date': r[1], 'clientName': r[2]} for r in rows]
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/save_quote', methods=['POST'])
def save_quote():
    """儲存或更新報價單"""
    try:
        record = request.json
        quoteNo = record.get('quoteNo')
        date = record.get('date', '')
        clientName = record.get('clientName', '')
        
        if not quoteNo:
            return jsonify({'status': 'error', 'message': '缺少報價單編號'})
            
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # 使用 REPLACE INTO 達成新增或覆蓋更新
        c.execute('''
            REPLACE INTO quotes (quoteNo, date, clientName, data)
            VALUES (?, ?, ?, ?)
        ''', (quoteNo, date, clientName, json.dumps(record)))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': f'報價單 {quoteNo} 儲存成功！'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/quotes/<quoteNo>', methods=['GET'])
def get_quote(quoteNo):
    """載入特定報價單內容"""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('SELECT data FROM quotes WHERE quoteNo = ?', (quoteNo,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return jsonify({'status': 'success', 'data': json.loads(row[0])})
        else:
            return jsonify({'status': 'error', 'message': '找不到該報價單'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/quotes/<quoteNo>', methods=['DELETE'])
def delete_quote(quoteNo):
    """刪除特定報價單"""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('DELETE FROM quotes WHERE quoteNo = ?', (quoteNo,))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': f'報價單 {quoteNo} 已刪除'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    init_db()
    print("====================================================")
    print("伺服器啟動成功！")
    print("請在您的電腦瀏覽器輸入以下網址來使用系統：")
    print("👉 http://192.168.18.17:5000")
    print("====================================================")
    # host='0.0.0.0' 代表允許所有外部 IP 連線
    app.run(host='0.0.0.0', port=5000, debug=False)