import sqlite3

DB_NAME = "usuarios.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        telegram_id INTEGER UNIQUE NOT NULL,
                        first_name TEXT,
                        username TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                    """)
    conn.commit()
    conn.close()
    
def guardar_usuario(telegram_id, first_name, username):
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO usuarios (telegram_id, first_name, username)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                first_name = excluded.first_name,
                username = excluded.username
            """,
            (telegram_id, first_name, username),
        )
        conn.commit()
    finally:
        conn.close()
def obtener_todos_usuarios():
    conn = get_connection()
    try:
        filas = conn.execute(
            """
            SELECT telegram_id, first_name, username, created_at
            FROM usuarios
            """
        ).fetchall()
        # for fila in filas:
            # print(f"id:{fila['telegram_id']}, first_name: {fila['first_name']}, username: {fila['username']}, created_at: {fila['created_at']}")
        return [dict(fila) for fila in filas]
    finally:
        conn.close()                 