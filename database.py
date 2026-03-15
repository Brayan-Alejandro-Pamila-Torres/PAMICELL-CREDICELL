import sqlite3

def conectar():
    # Si inventario.db no existe, SQLite la crea automáticamente
    conn = sqlite3.connect("inventario.db")
    return conn


def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        marca TEXT,
        modelo TEXT,
        capacidad TEXT,
        color TEXT,
        precio REAL,
        stock INTEGER
    )
    """)

    conn.commit()
    conn.close()