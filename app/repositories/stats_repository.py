import sqlite3
import os

DB_PATH = "app/database/stats.db"

os.makedirs("app/database", exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_stats_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY,

            total_files INTEGER DEFAULT 0,
            today_files INTEGER DEFAULT 0,

            total_searches INTEGER DEFAULT 0,
            total_downloads INTEGER DEFAULT 0,

            pdf_count INTEGER DEFAULT 0,
            pdf_today INTEGER DEFAULT 0,

            xls_count INTEGER DEFAULT 0,
            xls_today INTEGER DEFAULT 0,

            pptx_count INTEGER DEFAULT 0,
            pptx_today INTEGER DEFAULT 0,

            txt_count INTEGER DEFAULT 0,
            txt_today INTEGER DEFAULT 0,

            png_count INTEGER DEFAULT 0,
            png_today INTEGER DEFAULT 0,

            jpg_count INTEGER DEFAULT 0,
            jpg_today INTEGER DEFAULT 0,

            jpeg_count INTEGER DEFAULT 0,
            jpeg_today INTEGER DEFAULT 0,

            stats_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO stats(id, stats_date)
        VALUES (1, DATE('now'))
    """)

    conn.commit()
    conn.close()
    
    
def get_stats():
    conn = get_connection() # connection establed for this function
    conn.row_factory = sqlite3.Row # now the result will be returned as row
    cursor = conn.cursor() # here cursor got the db connection
    
    cursor.execute("SELECT * FROM stats WHERE id = 1") # cursor now executes the given sql commands
    stats = cursor.fetchone() # now its fetches the got result after executing the sql command
    
    conn.close()
    return dict(stats)


def reset_today_counts(today: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE stats
        SET
            today_files = 0,

            pdf_today = 0,
            xls_today = 0,
            pptx_today = 0,
            txt_today = 0,

            png_today = 0,
            jpg_today = 0,
            jpeg_today = 0,

            stats_date = ?
        WHERE id = 1
    """, (today,))

    conn.commit()
    conn.close()
    
    
def increment_file_stats(file_type: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    allowed = {"pdf", "xls", "xlsx", "pptx", "txt", "png", "jpg", "jpeg"}

    if file_type not in allowed:
      raise ValueError("Invalid file type")

    cursor.execute(f"""
        UPDATE stats
        SET
            total_files = total_files + 1,
            today_files = today_files + 1,
            {file_type}_count = {file_type}_count + 1,
            {file_type}_today = {file_type}_today + 1
        WHERE id = 1
    """)

    conn.commit()
    conn.close()


def increment_search_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE stats
        SET total_searches = total_searches + 1
        WHERE id = 1
    """)

    conn.commit()
    conn.close()


def increment_download_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE stats
        SET total_downloads = total_downloads + 1
        WHERE id = 1
    """)

    conn.commit()
    conn.close()