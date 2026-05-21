import tkinter as tk
from tkinter import ttk, messagebox
from services.inventario_service import obtener_productos, eliminar_producto_relacional
from services.ventas_service import obtener_ventas, eliminar_venta

FONT = "Ubuntu"

def crear_frame_datos(parent, actualizar_combos_ventas_callback=None):
    frame = tk.Frame(parent, bg="#f8fafc")

    # ---------------- HEADER ---------------- #
    header = tk.Frame(frame, bg="#1f2022", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Administración de Datos del Sistema",
        bg="#1f2022",
        fg="white",
        font=(FONT, 18, "bold")
    ).pack(expand=True)

    # ---------------- CONTENEDOR CONTENIDO ---------------- #
    cuerpo = tk.Frame(frame, bg="#f8fafc")
    cuerpo.pack(fill="both", expand=True, padx=24, pady=24)

    # Estilo del Notebook para que se vea moderno
    style = ttk.Style()
    style.configure("Datos.TNotebook", background="#f8fafc", borderwidth=0)
    style.configure("Datos.TNotebook.Tab", font=(FONT, 11, "bold"), padding=[20, 8])

    # Instanciar el contenedor de pestañas
    notebook = ttk.Notebook(cuerpo, style="Datos.TNotebook")
    notebook.pack(fill="both", expand=True)

    # Crear los contenedores de cada pestaña
    tab_inventario = tk.Frame(notebook, bg="white", bd=1, relief="solid")
    tab_ventas = tk.Frame(notebook, bg="white", bd=1, relief="solid")

    notebook.add(tab_inventario, text="📦 Tabla de Inventario")
    notebook.add(tab_ventas, text="💰 Tabla de Ventas")

    # =========================================================================
    # 📦 PESTAÑA 1: INVENTARIO COMPLETÓ
    # =========================================================================
    top_inv = tk.Frame(tab_inventario, bg="white")
    top_inv.pack(fill="x", padx=20, pady=(18, 10))
    
    tk.Label(top_inv, text="Historial de Inventario Registrado", bg="white", fg="#0f172a", font=("Segoe UI", 13, "bold")).pack(side="left")
    
    buscar_inv_frame = tk.Frame(top_inv, bg="white")
    buscar_inv_frame.pack(side="right")
    tk.Label(buscar_inv_frame, text="Buscar:", bg="white", fg="#334155", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
    entry_buscar_inv = ttk.Entry(buscar_inv_frame, width=28)
    entry_buscar_inv.pack(side="left")

    tabla_inv_wrap = tk.Frame(tab_inventario, bg="white")
    tabla_inv_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    columnas_inv = ("ID", "FECHA", "PROVEEDOR", "IMEI", "MODELO", "PRECIO", "RAM", "ALM", "STOCK", "ESTATUS", "IVA")
    tabla_inv = ttk.Treeview(tabla_inv_wrap, columns=columnas_inv, show="headings")
    anchos_inv = {"ID": 50, "FECHA": 110, "PROVEEDOR": 120, "IMEI": 150, "MODELO": 140, "PRECIO": 100, "RAM": 80, "ALM": 90, "STOCK": 60, "ESTATUS": 110, "IVA": 70}
    
    for col in columnas_inv:
        tabla_inv.heading(col, text=col)
        tabla_inv.column(col, width=anchos_inv[col], anchor="center")

    scroll_y_inv = ttk.Scrollbar(tabla_inv_wrap, orient="vertical", command=tabla_inv.yview)
    scroll_x_inv = ttk.Scrollbar(tabla_inv_wrap, orient="horizontal", command=tabla_inv.xview)
    tabla_inv.configure(yscrollcommand=scroll_y_inv.set, xscrollcommand=scroll_x_inv.set)
    tabla_inv.grid(row=0, column=0, sticky="nsew")
    scroll_y_inv.grid(row=0, column=1, sticky="ns")
    scroll_x_inv.grid(row=1, column=0, sticky="ew")
    tabla_inv_wrap.grid_rowconfigure(0, weight=1)
    tabla_inv_wrap.grid_columnconfigure(0, weight=1)

    # =========================================================================
    # 💰 PESTAÑA 2: VENTAS COMPLETO
    # =========================================================================
    top_ven = tk.Frame(tab_ventas, bg="white")
    top_ven.pack(fill="x", padx=20, pady=(18, 10))
    
    tk.Label(top_ven, text="Registro Histórico de Ventas", bg="white", fg="#0f172a", font=("Segoe UI", 13, "bold")).pack(side="left")
    
    buscar_ven_frame = tk.Frame(top_ven, bg="white")
    buscar_ven_frame.pack(side="right")
    tk.Label(buscar_ven_frame, text="Buscar:", bg="white", fg="#334155", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
    entry_buscar_ven = ttk.Entry(buscar_ven_frame, width=28)
    entry_buscar_ven.pack(side="left")

    tabla_ven_wrap = tk.Frame(tab_ventas, bg="white")
    tabla_ven_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    columnas_ven = ("ID", "FECHA", "CLIENTE", "IMEI", "TAG", "VENDEDOR", "VENTA", "PLATAFORMA", "GANANCIA", "PLAZO")
    tabla_ven = ttk.Treeview(tabla_ven_wrap, columns=columnas_ven, show="headings")
    anchos_ven = {"ID": 50, "FECHA": 110, "CLIENTE": 140, "IMEI": 140, "TAG": 110, "VENDEDOR": 130, "VENTA": 90, "PLATAFORMA": 110, "GANANCIA": 100, "PLAZO": 80}
    
    for col in columnas_ven:
        tabla_ven.heading(col, text=col)
        tabla_ven.column(col, width=anchos_ven[col], anchor="center")

    scroll_y_ven = ttk.Scrollbar(tabla_ven_wrap, orient="vertical", command=tabla_ven.yview)
    scroll_x_ven = ttk.Scrollbar(tabla_ven_wrap, orient="horizontal", command=tabla_ven.xview)
    tabla_ven.configure(yscrollcommand=scroll_y_ven.set, xscrollcommand=scroll_x_ven.set)
    tabla_ven.grid(row=0, column=0, sticky="nsew")
    scroll_y_ven.grid(row=0, column=1, sticky="ns")
    scroll_x_ven.grid(row=1, column=0, sticky="ew")
    tabla_ven_wrap.grid_rowconfigure(0, weight=1)
    tabla_ven_wrap.grid_columnconfigure(0, weight=1)

    # ---------------- LÓGICA DE CARGA Y BUSQUEDA ---------------- #
    
    def cargar_tabla_inventario(datos=None):
        for fila in tabla_inv.get_children(): tabla_inv.delete(fila)
        registros = datos if datos is not None else obtener_productos()
        for p in registros:
            tabla_inv.insert("", tk.END, values=(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]))

    def cargar_tabla_ventas(datos=None):
        for fila in tabla_ven.get_children(): tabla_ven.delete(fila)
        registros = datos if datos is not None else obtener_ventas()
        for v in registros:
            tabla_ven.insert("", tk.END, values=(v[0], v[1], v[3], v[4], v[5], v[6], v[9], v[10], v[12], v[15]))

    def buscar_inventario(_event=None):
        texto = entry_buscar_inv.get().strip().lower()
        if not texto:
            cargar_tabla_inventario()
            return
        resultados = [p for p in obtener_productos() if texto in " ".join(map(str, p)).lower()]
        cargar_tabla_inventario(resultados)

    def buscar_ventas(_event=None):
        texto = entry_buscar_ven.get().strip().lower()
        if not texto:
            cargar_tabla_ventas()
            return
        resultados = [v for v in obtener_ventas() if texto in " ".join(map(str, v)).lower()]
        cargar_tabla_ventas(resultados)

    def eliminar_inventario_ui():
        seleccion = tabla_inv.selection()
        if not seleccion:
            messagebox.showwarning("Selección vacía", "Selecciona un producto del listado para eliminarlo.")
            return
        valores = tabla_inv.item(seleccion[0], "values")
        if messagebox.askyesno("Confirmar eliminación", f"¿Deseas eliminar permanentemente el equipo ID {valores[0]} ({valores[4]})?"):
            if eliminar_producto_relacional(valores[0]):
                cargar_tabla_inventario()
                if actualizar_combos_ventas_callback:
                    actualizar_combos_ventas_callback()

    def eliminar_venta_ui():
        seleccion = tabla_ven.selection()
        if not seleccion:
            messagebox.showwarning("Selección vacía", "Selecciona una venta del listado para eliminarla.")
            return
        valores = tabla_ven.item(seleccion[0], "values")
        if messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente el registro de venta ID {valores[0]}?\nEsto devolverá el equipo a disponible."):
            eliminar_venta(valores[0])
            cargar_tabla_ventas()
            if actualizar_combos_ventas_callback:
                actualizar_combos_ventas_callback()

    # Botones de Acción colocados al pie de cada pestaña
    tk.Button(tab_inventario, text="Eliminar Equipo Seleccionado", bg="#dc2626", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=eliminar_inventario_ui, cursor="hand2", padx=16, pady=8).pack(anchor="w", padx=20, pady=(0, 15))
    tk.Button(tab_ventas, text="Eliminar Venta Seleccionada", bg="#dc2626", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=eliminar_venta_ui, cursor="hand2", padx=16, pady=8).pack(anchor="w", padx=20, pady=(0, 15))

    # Eventos de teclado para búsquedas instantáneas
    entry_buscar_inv.bind("<KeyRelease>", buscar_inventario)
    entry_buscar_ven.bind("<KeyRelease>", buscar_ventas)

    # Función global de actualización para el ruteador de app.py
    def refrescar_todo():
        entry_buscar_inv.delete(0, tk.END)
        entry_buscar_ven.delete(0, tk.END)
        cargar_tabla_inventario()
        cargar_tabla_ventas()

    refrescar_todo()
    frame.refrescar = refrescar_todo
    return frame