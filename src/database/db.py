import sqlite3

DB_NAME = "usuarios.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
                 CREATE TABLE IF NOT EXIST usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        telegram_id INTEGER UINIQUE NOT NULL,
                        first_name TEXT,
                        username TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                    """)
    conn.commit()
    conn.close()
    

                 