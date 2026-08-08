import sqlite3
from datetime import datetime

DB_PATH = "app/database/nexdoc.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_recent_searches_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recent_searches(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT UNIQUE NOT NULL,
            searched_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    

def save_recent_search(query: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO recent_searches(query, searched_at)
        VALUES(?, ?)
    """, (query, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()


def get_recent_searches(limit: int = 50):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM recent_searches
    ORDER BY searched_at DESC
    LIMIT ?
""", (limit,))
    
    recent_searches = cursor.fetchall()
    
    conn.close()
    return [dict(row) for row in recent_searches]


def delete_recent_search(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM recent_searches
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()


def clear_recent_searches():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM recent_searches
    """)

    conn.commit()
    conn.close()