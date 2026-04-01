import sqlite3

def conectar():
    # Establece la conexión con la base de datos local
    return sqlite3.connect("inventario.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    # Estructura basada exactamente en las columnas del Excel de CREDICELL & PAMICELL
    # El campo 'estatus' se usará para rastrear si el equipo está disponible o vendido
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