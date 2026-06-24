import sqlite3
from datetime import datetime

DB_NAME = "greenhouse_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            temperature REAL,
            humidity REAL,
            light REAL,
            mode TEXT
        )
    ''')
    conn.commit()
    conn.close()
    

def log_data(temp, hum, light, mode):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_logs (timestamp, temperature, humidity, light, mode)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now(), temp, hum, light, mode))
    conn.commit()
    conn.close()