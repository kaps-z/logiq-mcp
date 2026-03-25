import sqlite3
import json
import os

DB_PATH = os.environ.get("DB_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), '../../db/database.sqlite')))

def fetch_logs(level=None, service=None, limit=50):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM logs WHERE 1=1"
        params = []
        
        if level:
            query += " AND level = ?"
            params.append(level.upper())
            
        if service:
            query += " AND service = ?"
            params.append(service)
            
        query += " ORDER BY timestamp DESC LIMIT ?"
        try:
            params.append(int(limit))
        except (ValueError, TypeError):
            params.append(50)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        logs = [dict(row) for row in rows]
        conn.close()
        return json.dumps(logs)
    except Exception as e:
        return json.dumps({"error": str(e)})
