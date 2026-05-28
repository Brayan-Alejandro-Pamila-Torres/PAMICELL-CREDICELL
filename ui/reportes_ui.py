# ui/reportes_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from services.reportes_service import obtener_reporte_inventario_matematico, obtener_reporte_ventas_matematico
from services.reporte_pdf_service import exportar_treeview_a_pdf

FONT = "Ubuntu"

def crear_frame_reportes(parent):
    frame = tk.Frame(parent, bg="#f8fafc")

    # ---------------- HEADER ---------------- #
    header = tk.Frame(frame, bg="#1f2022", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Módulo Analítico (Álgebra y Cálculo Relacional)",
        bg="#1f2022",
        fg="white",
        font=(FONT, 18, "bold")
    ).pack(expand=True)

    cuerpo = tk.Frame(frame, bg="#f8fafc")
    cuerpo.pack(fill="both", expand=True, padx=24, pady=24)

    # ---------------- CARD DE FILTROS TEMPORALES (σ) ---------------- #
    card_filtros = tk.Frame(cuerpo, bg="white", bd=1, relief="solid")
    card_filtros.pack(fill="x", pady=(0, 10))

    top_filtro = tk.Frame(card_filtros, bg="white")
    top_filtro.pack(fill="x", padx=20, pady=12)

    tk.Label(
        top_filtro, 
        text="Rango de Evaluación Relacional (σ):", 
        bg="white", 
        fg="#0f172a", 
        font=("Segoe UI", 11, "bold")
    ).pack(side="left")

    temporalidad_var = tk.StringVar(value="semanal")

    # ---------------- BARRA DE ACCIONES (BOTÓN PDF ARRIBA) ---------------- #
    barra_acciones = tk.Frame(cuerpo, bg="#f8fafc")
    barra_acciones.pack(fill="x", pady=(0, 15))

    # ---------------- INTERFAZ DE IMPRESIÓN PDF (DINÁMICA) ---------------- #
    def imprimir_reporte_actual():
        pestaña_activa = notebook.index(notebook.select())
        temp_texto = "Semanal (Últimos 7 Días)" if temporalidad_var.get() == "semanal" else "Mensual (Mes en Curso)"
        
        if pestaña_activa == 0:
            # Caso Inventario (Pestaña 1)
            formula = "π id_equipo, fecha, proveedor, imei, modelo, precio_compra (σ rango_tiempo (equipos ⋈ productos))"
            exportar_treeview_a_pdf(
                tabla_inv, 
                titulo_reporte=f"Reporte de Inventario - {temp_texto}", 
                expresion_algebraica=formula
            )
        else:
            # Caso Ventas (Pestaña 2)
            formula = "π id_venta, fecha_venta, cliente, venta, ganancia (σ rango_tiempo (ventas ⋈ clientes ⋈ vendedores))"
            exportar_treeview_a_pdf(
                tabla_ven, 
                titulo_reporte=f"Reporte Financiero de Ventas - {temp_texto}", 
                expresion_algebraica=formula
            )

    # Botón único superior de exportación que detecta qué tabla estás viendo
    btn_pdf_superior = tk.Button(
        barra_acciones, 
        text="🖨️ Exportar Tabla Actual a PDF Formal", 
        bg="#1e293b", 
        fg="white", 
        font=("Segoe UI", 10, "bold"), 
        relief="flat", 
        command=imprimir_reporte_actual, 
        cursor="hand2", 
        padx=15, 
        pady=8
    )
    btn_pdf_superior.pack(side="left")

    # ---------------- CONTENEDOR DE METRICAS (KPIs) ---------------- #
    lbl_total_ventas = tk.Label(barra_acciones, text="VENTAS ACUMULADAS: $0.00", bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=8)
    lbl_total_ventas.pack(side="right", padx=5)

    lbl_ganancia_total = tk.Label(barra_acciones, text="GANANCIA LÍQUIDA: $0.00", bg="#16a34a", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=8)
    lbl_ganancia_total.pack(side="right", padx=5)

    # ---------------- NOTEBOOK DE REPORTES ---------------- #
    notebook = ttk.Notebook(cuerpo)
    notebook.pack(fill="both", expand=True)

    tab_inventario = tk.Frame(notebook, bg="white")
    tab_ventas = tk.Frame(notebook, bg="white")

    notebook.add(tab_inventario, text=" 📦 Reporte de Inventario (σ ∧ ⋈) ")
    notebook.add(tab_ventas, text=" 💰 Reporte de Ventas (σ ∧ ⋈) ")

    # =========================================================================
    # PESTAÑA 1: INVENTARIO
    # =========================================================================
    tabla_inv_wrap = tk.Frame(tab_inventario, bg="white")
    tabla_inv_wrap.pack(fill="both", expand=True, padx=15, pady=15)
    
    columnas_inv = ("ID", "FECHA", "PROVEEDOR", "IMEI", "MODELO", "PRECIO COMPRA", "RAM", "A INTERNO", "STOCK", "ESTATUS", "IVA")
    tabla_inv = ttk.Treeview(tabla_inv_wrap, columns=columnas_inv, show="headings")
    
    anchos_inv = {"ID": 50, "FECHA": 90, "PROVEEDOR": 110, "IMEI": 140, "MODELO": 120, "PRECIO COMPRA": 110, "RAM": 60, "A INTERNO": 90, "STOCK": 60, "ESTATUS": 100, "IVA": 70}
    for col in columnas_inv:
        tabla_inv.heading(col, text=col)
        tabla_inv.column(col, width=anchos_inv[col], anchor="center")
    tabla_inv.pack(fill="both", expand=True)

    # =========================================================================
    # PESTAÑA 2: VENTAS
    # =========================================================================
    tabla_ven_wrap = tk.Frame(tab_ventas, bg="white")
    tabla_ven_wrap.pack(fill="both", expand=True, padx=15, pady=15)
    
    columnas_ven = ("ID", "FECHA", "MODELO", "CLIENTE", "IMEI", "TAG / CRÉDITO", "VENDEDOR", "VENTA", "GANANCIA TOTAL")
    tabla_ven = ttk.Treeview(tabla_ven_wrap, columns=columnas_ven, show="headings")
    
    anchos_ven = {"ID": 50, "FECHA": 100, "MODELO": 130, "CLIENTE": 150, "IMEI": 140, "TAG / CRÉDITO": 120, "VENDEDOR": 120, "VENTA": 90, "GANANCIA TOTAL": 110}
    for col in columnas_ven:
        tabla_ven.heading(col, text=col)
        tabla_ven.column(col, width=anchos_ven[col], anchor="center")
    tabla_ven.pack(fill="both", expand=True)

    # ---------------- LÓGICA DE CARGA ---------------- #
    def ejecutar_consulta_relacional():
        for fila in tabla_inv.get_children(): tabla_inv.delete(fila)
        for fila in tabla_ven.get_children(): tabla_ven.delete(fila)

        hoy = datetime.now()
        fecha_fin_str = hoy.strftime("%d/%m/%Y")

        if temporalidad_var.get() == "semanal":
            inicio = hoy - timedelta(days=7)
            fecha_inicio_str = inicio.strftime("%d/%m/%Y")
        else:
            fecha_inicio_str = hoy.strftime("01/%m/%Y")

        inventario_rows = obtener_reporte_inventario_matematico(fecha_inicio_str, fecha_fin_str)
        for r in inventario_rows:
            tabla_inv.insert("", tk.END, values=r)

        ventas_rows, total_monto, total_ganancia = obtener_reporte_ventas_matematico(fecha_inicio_str, fecha_fin_str)
        for v in ventas_rows:
            tabla_ven.insert("", tk.END, values=v)

        lbl_total_ventas.config(text=f"VENTAS ACUMULADAS: ${total_monto:,.2f}")
        lbl_ganancia_total.config(text=f"GANANCIA LÍQUIDA: ${total_ganancia:,.2f}")

    # Selectores dinámicos (Radiobuttons)
    tk.Radiobutton(top_filtro, text="Evaluación Semanal (Últimos 7 Días)", variable=temporalidad_var, value="semanal", bg="white", font=("Segoe UI", 10), command=ejecutar_consulta_relacional).pack(side="left", padx=20)
    tk.Radiobutton(top_filtro, text="Evaluación Mensual (Mes en Curso)", variable=temporalidad_var, value="mensual", bg="white", font=("Segoe UI", 10), command=ejecutar_consulta_relacional).pack(side="left", padx=20)

    frame.refrescar = ejecutar_consulta_relacional
    ejecutar_consulta_relacional()

    return frame