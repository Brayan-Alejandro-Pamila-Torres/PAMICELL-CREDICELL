# services/reportes_service.py
from database import conectar

def obtener_reporte_inventario_matematico(fecha_inicio, fecha_fin):
    """
    REPORTE DE INVENTARIO
    
    ALGEBRA RELACIONAL:
    π id_equipo, fecha, proveedor, imei, modelo, precio_compra, ram, almacenamiento, estatus, iva (
        σ fecha >= fecha_inicio ∧ fecha <= fecha_fin (
            equipos_fisicos bowtie productos bowtie proveedores
        )
    )
    
    CÁLCULO RELACIONAL BASADO EN TUPLAS (CRT):
    { t | ∃e ∈ equipos_fisicos ∃p ∈ productos ∃pv ∈ proveedores (
            e.id_producto = p.id_producto ∧ e.id_proveedor = pv.id_proveedor ∧
            e.fecha >= fecha_inicio ∧ e.fecha <= fecha_fin ∧
            t.id_equipo = e.id_equipo ∧ t.fecha = e.fecha ∧ t.proveedor = pv.proveedor ∧
            t.imei = e.imei ∧ t.modelo = p.modelo ∧ t.precio_compra = e.precio_compra ∧
            t.ram = p.ram ∧ t.almacenamiento = p.almacenamiento ∧ t.estatus = e.estatus ∧ t.iva = e.iva
    )}
    """
    conn = conectar()
    if not conn: return []
    cursor = conn.cursor()
    
    query = """
        SELECT 
            ef.id_equipo, ef.fecha, prv.proveedor, ef.imei, prd.modelo, 
            ef.precio_compra, prd.ram, prd.almacenamiento, 
            CASE WHEN ef.estatus = 'DISPONIBLE' THEN 1 ELSE 0 END, 
            ef.estatus, ef.iva
        FROM equipos_fisicos ef
        JOIN productos prd ON ef.id_producto = prd.id_producto
        JOIN proveedores prv ON ef.id_proveedor = prv.id_proveedor
        WHERE STR_TO_DATE(ef.fecha, '%d/%m/%Y') BETWEEN STR_TO_DATE(%s, '%d/%m/%Y') AND STR_TO_DATE(%s, '%d/%m/%Y')
        ORDER BY STR_TO_DATE(ef.fecha, '%d/%m/%Y') DESC
    """
    try:
        cursor.execute(query, (fecha_inicio, fecha_fin))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error en Álgebra Relacional de Inventario: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def obtener_reporte_ventas_matematico(fecha_inicio, fecha_fin):
    """
    REPORTE DE VENTAS
    
    ALGEBRA RELACIONAL:
    Extrae la cabecera económica de las transacciones ejecutadas en el rango.
    π id_venta, fecha_venta, modelo, nombre_cliente, imei, tag, nombre_vendedor, venta, ganancia_total (
        σ fecha_venta >= fecha_inicio ∧ fecha_venta <= fecha_fin (
            ventas bowtie clientes bowtie vendedores bowtie detalle_venta bowtie equipos_fisicos bowtie productos
        )
    )
    """
    conn = conectar()
    if not conn: return [], 0.0, 0.0
    cursor = conn.cursor()
    
    query = """
        SELECT 
            v.id_venta, v.fecha_venta, p.modelo, c.nombre_cliente, ef.imei, 
            IFNULL(cr.tag, 'CONTADO'), vend.nombre_vendedor, v.venta, v.ganancia_total
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        JOIN vendedores vend ON v.id_vendedor = vend.id_vendedor
        JOIN detalle_venta dv ON v.id_venta = dv.id_venta
        JOIN equipos_fisicos ef ON dv.id_equipo = ef.id_equipo
        JOIN productos p ON ef.id_producto = p.id_producto
        LEFT JOIN creditos cr ON v.id_venta = cr.id_venta
        WHERE STR_TO_DATE(v.fecha_venta, '%d/%m/%Y') BETWEEN STR_TO_DATE(%s, '%d/%m/%Y') AND STR_TO_DATE(%s, '%d/%m/%Y')
        ORDER BY STR_TO_DATE(v.fecha_venta, '%d/%m/%Y') DESC
    """
    try:
        cursor.execute(query, (fecha_inicio, fecha_fin))
        ventas = cursor.fetchall()
        
        total_monto = sum(float(v[7]) for v in ventas)
        total_ganancia = sum(float(v[8]) for v in ventas)
        
        return ventas, total_monto, total_ganancia
    except Exception as e:
        print(f"Error en Álgebra Relacional de Ventas: {e}")
        return [], 0.0, 0.0
    finally:
        cursor.close()
        conn.close()