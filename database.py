import sqlite3
import os
import hashlib

# ---------------- CONEXIÓN ---------------- #

def conectar():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "inventario.db")
    return sqlite3.connect(db_path)


# ---------------- PRODUCTOS ---------------- #

def crear_tabla_productos():
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
        stock INTEGER DEFAULT 1,
        estatus TEXT DEFAULT 'DISPONIBLE',
        iva REAL
    )
    """)

    conn.commit()
    conn.close()


# ---------------- VENTAS ---------------- #

def crear_tabla_ventas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_venta TEXT,
        equipo TEXT,
        nombre_cliente TEXT,
        imei TEXT,
        tag TEXT,
        nombre_vendedor TEXT,
        enganche_consola REAL,
        enganche_cliente REAL,
        venta REAL,
        plataforma TEXT,
        ganancia_plataforma REAL,
        ganancia_total REAL,
        pagara_plataforma REAL,
        costo_equipo REAL,
        plazo_semanas INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ---------------- VENDEDORES ---------------- #

def crear_tabla_vendedores():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE
    )
    """)

    cursor.execute("INSERT OR IGNORE INTO vendedores (nombre) VALUES (?)", ("Obed",))

    conn.commit()
    conn.close()

# ---------------- SEGURIDAD ---------------- #

def crear_tabla_config():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clave TEXT,
        valor TEXT
    )
    """)
    
    cursor.execute("SELECT * FROM configuracion WHERE clave = 'password_sistema'")
    if not cursor.fetchone():
        password_inicial = hashlib.sha256("1234".encode()).hexdigest()
        cursor.execute("INSERT INTO configuracion (clave, valor) VALUES (?, ?)", 
                       ("password_sistema", password_inicial))
    
    conn.commit()
    conn.close()
# ---------------- INIT ---------------- #

def inicializar_db():
    crear_tabla_productos()
    crear_tabla_ventas()
    crear_tabla_vendedores()
    crear_tabla_config()