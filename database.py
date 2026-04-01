import sqlite3

def conectar():
    return sqlite3.connect("inventario.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        proveedor TEXT,
        imei TEXT UNIQUE,
        modelo TEXT,
        precio_compra REAL,
        ram TEXT,
        almacenamiento TEXT,
        estatus TEXT
    )
    """)

    conn.commit()
    conn.close()