import sqlite3
from datetime import datetime

DB_PATH = "mcp_chat.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            sender TEXT,
            question TEXT,
            response TEXT,
            model TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(message_id, sender, question, response, model):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?)",
              (message_id, datetime.now().isoformat(), sender, question, response, model))
    conn.commit()
    conn.close()

def load_messages():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, sender, question, response FROM messages ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows
