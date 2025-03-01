import sqlite3
from datetime import datetime

DB_PATH = "history.db"

def init_db():
    """
    Initialize the SQLite database and create the users and history tables if they do not exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # Create history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            original_text TEXT NOT NULL,
            translated_text TEXT NOT NULL,
            source_lang TEXT NOT NULL,
            target_lang TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, hashed_password):
    """
    Register a new user in the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

def get_user(username):
    """
    Retrieve a user record from the database.
    Returns a tuple: (id, username, password) or None if not found.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def insert_history(username, original_text, translated_text, source_lang, target_lang):
    """
    Insert a new translation record into the history database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO history (username, timestamp, original_text, translated_text, source_lang, target_lang)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, timestamp, original_text, translated_text, source_lang, target_lang))
    conn.commit()
    conn.close()

def get_history(username):
    """
    Retrieve all translation history records for a given username.
    Returns a list of dictionaries.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, original_text, translated_text, source_lang, target_lang
        FROM history WHERE username = ? ORDER BY timestamp DESC
    """, (username,))
    rows = cursor.fetchall()
    conn.close()
    history = []
    for row in rows:
        history.append({
            "timestamp": row[0],
            "original_text": row[1],
            "translated_text": row[2],
            "source_lang": row[3],
            "target_lang": row[4]
        })
    return history
