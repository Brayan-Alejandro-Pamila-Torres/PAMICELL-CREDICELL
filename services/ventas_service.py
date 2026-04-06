from database import conectar

# ---------------- VENTAS ---------------- #

def registrar_venta(data):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ventas (
        fecha_venta, equipo, nombre_cliente, imei, tag,
        nombre_vendedor, enganche_consola, enganche_cliente,
        venta, plataforma, ganancia_plataforma, ganancia_total,
        pagara_plataforma, costo_equipo, plazo_semanas
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["fecha_venta"],
        data["equipo"],
        data["nombre_cliente"],
        data["imei"],
        data["tag"],
        data["nombre_vendedor"],
        data["enganche_consola"],
        data["enganche_cliente"],
        data["venta"],
        data["plataforma"],
        data["ganancia_plataforma"],
        data["ganancia_total"],
        data["pagara_plataforma"],
        data["costo_equipo"],
        data["plazo_semanas"]
    ))

    # Reducir stock
    cursor.execute("""
    UPDATE productos
    SET stock = stock - 1
    WHERE imei = ? AND stock > 0
    """, (data["imei"],))

    # Actualizar estatus
    cursor.execute("""
    UPDATE productos
    SET estatus = CASE
        WHEN stock <= 0 THEN 'AGOTADO'
        ELSE 'DISPONIBLE'
    END
    WHERE imei = ?
    """, (data["imei"],))

    conn.commit()
    conn.close()


def obtener_ventas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, fecha_venta, equipo, nombre_cliente, imei, tag,
           nombre_vendedor, enganche_consola, enganche_cliente,
           venta, plataforma, ganancia_plataforma, ganancia_total,
           pagara_plataforma, costo_equipo, plazo_semanas
    FROM ventas
    ORDER BY id DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def eliminar_venta(id_venta):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT imei FROM ventas WHERE id = ?", (id_venta,))
    fila = cursor.fetchone()

    if fila:
        imei = fila[0]

        cursor.execute("DELETE FROM ventas WHERE id = ?", (id_venta,))

        # Regresar stock al eliminar la venta
        cursor.execute("""
        UPDATE productos
        SET stock = stock + 1
        WHERE imei = ?
        """, (imei,))

        cursor.execute("""
        UPDATE productos
        SET estatus = CASE
            WHEN stock <= 0 THEN 'AGOTADO'
            ELSE 'DISPONIBLE'
        END
        WHERE imei = ?
        """, (imei,))

    conn.commit()
    conn.close()


# ---------------- VENDEDORES ---------------- #

def obtener_vendedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM vendedores ORDER BY nombre ASC")
    vendedores = [fila[0] for fila in cursor.fetchall()]
    conn.close()
    return vendedores


def agregar_vendedor(nombre):
    nombre = nombre.strip()
    if not nombre:
        return False

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO vendedores (nombre) VALUES (?)", (nombre,))
    conn.commit()
    agregado = cursor.rowcount > 0
    conn.close()
    return agregado


def eliminar_vendedor(nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vendedores WHERE nombre = ?", (nombre,))
    conn.commit()
    eliminado = cursor.rowcount > 0
    conn.close()
    return eliminado