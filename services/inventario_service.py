from database import conectar

def guardar_producto(data):
    conn = conectar()
    cursor = conn.cursor()

    # Verificar IMEI duplicado
    cursor.execute("SELECT COUNT(*) FROM productos WHERE imei = ?", (data["imei"],))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return "existe"

    # INSERT CORREGIDO (ahora incluye stock y estatus)
    cursor.execute("""
        INSERT INTO productos 
        (fecha, proveedor, imei, modelo, precio_compra, ram, almacenamiento, stock, estatus)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["fecha"],
        data["proveedor"],
        data["imei"],
        data["modelo"],
        data["precio"],
        data["ram"],
        data["alm"],
        data["stock"],      
        data["estatus"]     
    ))

    conn.commit()
    conn.close()
    return "ok"


def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()

    conn.close()
    return datos