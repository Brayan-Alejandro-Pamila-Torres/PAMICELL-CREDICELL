from database import conectar

def registrar_venta(data):
    conn = conectar()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_equipo FROM equipos_fisicos WHERE imei = %s", (data["imei"],))
        res_equipo = cursor.fetchone()
        if not res_equipo: return
        id_equipo = res_equipo[0]

        cursor.execute("SELECT id_cliente FROM clientes WHERE nombre_cliente = %s", (data["nombre_cliente"],))
        res_cliente = cursor.fetchone()
        id_cliente = res_cliente[0] if res_cliente else None
        if not id_cliente:
            cursor.execute("INSERT INTO clientes (nombre_cliente) VALUES (%s)", (data["nombre_cliente"],))
            id_cliente = cursor.lastrowid

        cursor.execute("SELECT id_vendedor FROM vendedores WHERE nombre_vendedor = %s", (data["nombre_vendedor"],))
        res_vendedor = cursor.fetchone()
        id_vendedor = res_vendedor[0] if res_vendedor else None
        if not id_vendedor:
            cursor.execute("INSERT INTO vendedores (nombre_vendedor) VALUES (%s)", (data["nombre_vendedor"],))
            id_vendedor = cursor.lastrowid

        cursor.execute("""
            INSERT INTO ventas (id_cliente, id_vendedor, fecha_venta, venta, costo_equipo, ganancia_total)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_cliente, id_vendedor, data["fecha_venta"], data["venta"], data["costo_equipo"], data["ganancia_total"]))
        id_venta = cursor.lastrowid

        cursor.execute("INSERT INTO detalle_venta (id_venta, id_equipo) VALUES (%s, %s)", (id_venta, id_equipo))
        cursor.execute("UPDATE equipos_fisicos SET estatus = 'AGOTADO' WHERE id_equipo = %s", (id_equipo,))

        if data.get("plataforma") and data["plataforma"].strip() != "":
            cursor.execute("SELECT id_compania FROM companias_credito WHERE plataforma = %s", (data["plataforma"],))
            res_comp = cursor.fetchone()
            id_compania = res_comp[0] if res_comp else None
            if not id_compania:
                cursor.execute("INSERT INTO companias_credito (plataforma) VALUES (%s)", (data["plataforma"],))
                id_compania = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO creditos (id_venta, id_compania, tag, enganche_consola, enganche_cliente, ganancia_plataforma, pagara_plataforma, plazo_semanas)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_venta, id_compania, data["tag"], data["enganche_consola"], data["enganche_cliente"],
                data["ganancia_plataforma"], data["pagara_plataforma"], data["plazo_semanas"]))

        conn.commit()
    except Exception as e:
        print(f"Error al registrar venta: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def obtener_ventas():
    conn = conectar()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            v.id_venta, v.fecha_venta, p.modelo, c.nombre_cliente, ef.imei, 
            IFNULL(cr.tag, ''), vend.nombre_vendedor, 
            IFNULL(cr.enganche_consola, 0.0), IFNULL(cr.enganche_cliente, 0.0),
            v.venta, IFNULL(cc.plataforma, ''), IFNULL(cr.ganancia_plataforma, 0.0), 
            v.ganancia_total, IFNULL(cr.pagara_plataforma, 0.0), v.costo_equipo, 
            IFNULL(cr.plazo_semanas, 0)
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        JOIN vendedores vend ON v.id_vendedor = vend.id_vendedor
        JOIN detalle_venta dv ON v.id_venta = dv.id_venta
        JOIN equipos_fisicos ef ON dv.id_equipo = ef.id_equipo
        JOIN productos p ON ef.id_producto = p.id_producto
        LEFT JOIN creditos cr ON v.id_venta = cr.id_venta
        LEFT JOIN companias_credito cc ON cr.id_compania = cc.id_compania
        ORDER BY v.id_venta DESC
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def eliminar_venta(id_venta):
    conn = conectar()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_equipo FROM detalle_venta WHERE id_venta = %s", (id_venta,))
        fila = cursor.fetchone()
        if fila:
            id_equipo = fila[0]
            cursor.execute("DELETE FROM ventas WHERE id_venta = %s", (id_venta,))
            cursor.execute("UPDATE equipos_fisicos SET estatus = 'DISPONIBLE' WHERE id_equipo = %s", (id_equipo,))
        conn.commit()
    except Exception as e:
        print(f"Error al eliminar venta: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def obtener_vendedores():
    conn = conectar()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute("SELECT nombre_vendedor FROM vendedores ORDER BY nombre_vendedor ASC")
    vendedores = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    conn.close()
    return vendedores

def agregar_vendedor(nombre):
    nombre = nombre.strip()
    if not nombre: return False
    conn = conectar()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM vendedores WHERE nombre_vendedor = %s", (nombre,))
        if cursor.fetchone()[0] > 0: return False
        cursor.execute("INSERT INTO vendedores (nombre_vendedor) VALUES (%s)", (nombre,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def eliminar_vendedor(nombre):
    conn = conectar()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM vendedores WHERE nombre_vendedor = %s", (nombre,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()