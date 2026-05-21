from database import conectar

def guardar_producto(data):
    conn = conectar()
    if not conn: return "error"
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM equipos_fisicos WHERE imei = %s", (data["imei"],))
        if cursor.fetchone()[0] > 0:
            return "existe"

        cursor.execute("SELECT id_proveedor FROM proveedores WHERE proveedor = %s", (data["proveedor"],))
        res_prov = cursor.fetchone()
        id_proveedor = res_prov[0] if res_prov else None
        if not id_proveedor:
            cursor.execute("INSERT INTO proveedores (proveedor) VALUES (%s)", (data["proveedor"],))
            id_proveedor = cursor.lastrowid

        cursor.execute("SELECT id_producto FROM productos WHERE modelo = %s AND ram = %s AND almacenamiento = %s", 
                       (data["modelo"], data["ram"], data["alm"]))
        res_prod = cursor.fetchone()
        id_producto = res_prod[0] if res_prod else None
        if not id_producto:
            cursor.execute("INSERT INTO productos (modelo, ram, almacenamiento) VALUES (%s, %s, %s)", 
                           (data["modelo"], data["ram"], data["alm"]))
            id_producto = cursor.lastrowid

        cursor.execute("""
            INSERT INTO equipos_fisicos (id_producto, id_proveedor, fecha, imei, precio_compra, iva, estatus)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_producto, id_proveedor, data["fecha"], data["imei"], data["precio"], data["iva"], data["estatus"]))
        
        conn.commit()
        return "ok"
    except Exception as e:
        print(f"Error: {e}")
        return "error"
    finally:
        cursor.close()
        conn.close()

def actualizar_producto_relacional(id_equipo, data):
    conn = conectar()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_proveedor FROM proveedores WHERE proveedor = %s", (data["proveedor"],))
        res_prov = cursor.fetchone()
        id_proveedor = res_prov[0] if res_prov else None
        if not id_proveedor:
            cursor.execute("INSERT INTO proveedores (proveedor) VALUES (%s)", (data["proveedor"],))
            id_proveedor = cursor.lastrowid

        cursor.execute("INSERT INTO productos (modelo, ram, almacenamiento) \
                        SELECT %s, %s, %s WHERE NOT EXISTS \
                        (SELECT 1 FROM productos WHERE modelo=%s AND ram=%s AND almacenamiento=%s)", 
                       (data["modelo"], data["ram"], data["alm"], data["modelo"], data["ram"], data["alm"]))
        
        cursor.execute("SELECT id_producto FROM productos WHERE modelo = %s AND ram = %s AND almacenamiento = %s", 
                       (data["modelo"], data["ram"], data["alm"]))
        id_producto = cursor.fetchone()[0]

        cursor.execute("""
            UPDATE equipos_fisicos 
            SET fecha = %s, id_proveedor = %s, imei = %s, id_producto = %s, precio_compra = %s, iva = %s
            WHERE id_equipo = %s
        """, (data["fecha"], id_proveedor, data["imei"], id_producto, data["precio"], data["iva"], id_equipo))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar producto: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def eliminar_producto_relacional(id_equipo):
    conn = conectar()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM equipos_fisicos WHERE id_equipo = %s", (id_equipo,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def obtener_productos():
    conn = conectar()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ef.id_equipo, ef.fecha, prv.proveedor, ef.imei, prd.modelo, 
            ef.precio_compra, prd.ram, prd.almacenamiento, 
            CASE WHEN ef.estatus = 'DISPONIBLE' THEN 1 ELSE 0 END, 
            ef.estatus, ef.iva
        FROM equipos_fisicos ef
        JOIN productos prd ON ef.id_producto = prd.id_producto
        JOIN proveedores prv ON ef.id_proveedor = prv.id_proveedor
        ORDER BY ef.id_equipo DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return datos