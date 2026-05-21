import mysql.connector
from mysql.connector import Error
import hashlib

# ---------------- CONEXIÓN A DOCKER ---------------- #

def conectar():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3307,               # Puerto configurado para evitar el conflicto local
            user='root',
            password='root_password_123',
            database='pamicell_credicell',
            autocommit=True          # Guarda automáticamente las transacciones en disco
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL en Docker: {e}")
        return None


# ---------------- CREACIÓN DE TABLAS NORMALIZADAS ---------------- #

def crear_tablas():
    conn = conectar()
    if conn is None: return
    cursor = conn.cursor()

    # Asegurar codificación correcta en la base de datos para soportar acentos y la Ñ
    cursor.execute("ALTER DATABASE pamicell_credicell CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")

    # 1. Tabla Clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INT AUTO_INCREMENT,
        nombre_cliente VARCHAR(100) NOT NULL,
        CONSTRAINT pk_clientes PRIMARY KEY (id_cliente)
    ) ENGINE=InnoDB;
    """)

    # 2. Tabla Vendedores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendedores (
        id_vendedor INT AUTO_INCREMENT,
        nombre_vendedor VARCHAR(100) NOT NULL,
        CONSTRAINT pk_vendedores PRIMARY KEY (id_vendedor)
    ) ENGINE=InnoDB;
    """)

    # 3. Tabla Proveedores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proveedores (
        id_proveedor INT AUTO_INCREMENT,
        proveedor VARCHAR(100) NOT NULL,
        CONSTRAINT pk_proveedores PRIMARY KEY (id_proveedor)
    ) ENGINE=InnoDB;
    """)

    # 4. Tabla Compañías de Crédito
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companias_credito (
        id_compania INT AUTO_INCREMENT,
        plataforma VARCHAR(100) NOT NULL,
        CONSTRAINT pk_companias_credito PRIMARY KEY (id_compania)
    ) ENGINE=InnoDB;
    """)

    # 5. Tabla Catálogo de Productos (Modelo de catálogo sugerido por tu maestra)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id_producto INT AUTO_INCREMENT,
        modelo VARCHAR(100) NOT NULL,
        ram VARCHAR(20) NOT NULL,
        almacenamiento VARCHAR(20) NOT NULL,
        CONSTRAINT pk_productos PRIMARY KEY (id_producto)
    ) ENGINE=InnoDB;
    """)

    # 6. Tabla Equipos Físicos (Inventario real donde vive cada IMEI único)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipos_fisicos (
        id_equipo INT AUTO_INCREMENT,
        id_producto INT NOT NULL,
        id_proveedor INT NOT NULL,
        fecha TEXT,
        imei VARCHAR(15) NOT NULL,
        precio_compra DECIMAL(10,2) NOT NULL,
        iva DECIMAL(10,2) NOT NULL,
        estatus VARCHAR(20) DEFAULT 'DISPONIBLE',
        CONSTRAINT pk_equipos_fisicos PRIMARY KEY (id_equipo),
        CONSTRAINT uq_imei UNIQUE (imei),
        CONSTRAINT fk_equipos_productos FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_equipos_proveedores FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 7. Tabla Ventas (Cabecera general de la transacción)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id_venta INT AUTO_INCREMENT,
        id_cliente INT NOT NULL,
        id_vendedor INT NOT NULL,
        fecha_venta TEXT,
        venta DECIMAL(10,2) NOT NULL,
        costo_equipo DECIMAL(10,2) NOT NULL,
        ganancia_total DECIMAL(10,2) NOT NULL,
        CONSTRAINT pk_ventas PRIMARY KEY (id_venta),
        CONSTRAINT fk_ventas_clientes FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_ventas_vendedores FOREIGN KEY (id_vendedor) REFERENCES vendedores(id_vendedor) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 8. Tabla Detalle Venta (Vincula el artículo con IMEI único al ticket de venta)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_venta (
        id_detalle INT AUTO_INCREMENT,
        id_venta INT NOT NULL,
        id_equipo INT NOT NULL,
        CONSTRAINT pk_detalle_venta PRIMARY KEY (id_detalle),
        CONSTRAINT uq_equipo_vendido UNIQUE (id_equipo),
        CONSTRAINT fk_detalle_ventas FOREIGN KEY (id_venta) REFERENCES ventas(id_venta) ON DELETE CASCADE,
        CONSTRAINT fk_detalle_equipos FOREIGN KEY (id_equipo) REFERENCES equipos_fisicos(id_equipo) ON DELETE RESTRICT
    ) ENGINE=InnoDB;
    """)

    # 9. Tabla Créditos (Datos complementarios si la plataforma de venta fue financiada)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS creditos (
        id_credito INT AUTO_INCREMENT,
        id_venta INT NOT NULL,
        id_compania INT NOT NULL,
        tag VARCHAR(50),
        enganche_consola DECIMAL(10,2) NOT NULL,
        enganche_cliente DECIMAL(10,2) NOT NULL,
        ganancia_plataforma DECIMAL(10,2) NOT NULL,
        pagara_plataforma DECIMAL(10,2) NOT NULL,
        plazo_semanas INT NOT NULL,
        CONSTRAINT pk_creditos PRIMARY KEY (id_credito),
        CONSTRAINT uq_venta_credito UNIQUE (id_venta),
        CONSTRAINT fk_creditos_ventas FOREIGN KEY (id_venta) REFERENCES ventas(id_venta) ON DELETE CASCADE,
        CONSTRAINT fk_creditos_companias FOREIGN KEY (id_compania) REFERENCES companias_credito(id_compania) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 10. Tabla de Configuración de Seguridad
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracion (
        id INT AUTO_INCREMENT,
        clave VARCHAR(50) NOT NULL,
        valor VARCHAR(255) NOT NULL,
        CONSTRAINT pk_configuracion PRIMARY KEY (id)
    ) ENGINE=InnoDB;
    """)

    conn.commit()
    cursor.close()
    conn.close()


# ---------------- INSERTS INICIALES / SEMILLAS ---------------- #

def insertar_datos_iniciales():
    conn = conectar()
    if conn is None: return
    cursor = conn.cursor()

    # Insertar a Ana Lilia como vendedora por defecto si no está registrada
    cursor.execute("""
        INSERT INTO vendedores (nombre_vendedor) 
        SELECT * FROM (SELECT 'Ana Lilia') AS tmp 
        WHERE NOT EXISTS (SELECT nombre_vendedor FROM vendedores WHERE nombre_vendedor = 'Ana Lilia') LIMIT 1;
    """)

    # Insertar la contraseña del sistema "1234" hasheada por defecto si no existe
    cursor.execute("SELECT * FROM configuracion WHERE clave = 'password_sistema'")
    if not cursor.fetchone():
        password_inicial = hashlib.sha256("1234".encode()).hexdigest()
        cursor.execute("INSERT INTO configuracion (clave, valor) VALUES (%s, %s)", 
                       ("password_sistema", password_inicial))
    
    conn.commit()
    cursor.close()
    conn.close()


# ---------------- INIT GLOBAL ---------------- #

def inicializar_db():
    crear_tablas()
    insertar_datos_iniciales()