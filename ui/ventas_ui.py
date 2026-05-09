import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from services.ventas_service import (
    registrar_venta,
    obtener_ventas,
    eliminar_venta,
    obtener_vendedores,
    agregar_vendedor,
    eliminar_vendedor,
)
from services.inventario_service import obtener_productos


def crear_frame_ventas(parent):
    frame = tk.Frame(parent, bg="#f8fafc")

    # ---------------- HEADER ---------------- #
    header = tk.Frame(frame, bg="#1f2022", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Modulo de Ventas",
        bg="#1f2022",
        fg="white",
        font=("Ubuntu", 18, "bold")
    ).pack(expand=True)

    # ---------------- CUERPO ---------------- #
    cuerpo = tk.Frame(frame, bg="#f8fafc")
    cuerpo.pack(fill="both", expand=True, padx=24, pady=24)

    # ---------------- TARJETA FORMULARIO ---------------- #
    card_form = tk.Frame(cuerpo, bg="white", bd=1, relief="solid")
    card_form.pack(fill="x", pady=(0, 18))

    tk.Label(
        card_form,
        text="Registrar venta",
        bg="white",
        fg="#0f172a",
        font=("Segoe UI", 13, "bold")
    ).pack(anchor="w", padx=20, pady=(18, 8))

    form = tk.Frame(card_form, bg="white")
    form.pack(fill="x", padx=20, pady=(0, 18))

    def crear_label(texto, row, col):
        tk.Label(
            form,
            text=texto,
            bg="white",
            fg="#334155",
            font=("Segoe UI", 10, "bold")
        ).grid(row=row, column=col, sticky="w", padx=10, pady=(8, 4))

    for i in range(3):
        form.grid_columnconfigure(i, weight=1)

    # Variables de control
    fecha_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
    equipo_var = tk.StringVar()
    nombre_cliente_var = tk.StringVar()
    imei_var = tk.StringVar()
    tag_var = tk.StringVar(value="V" + datetime.now().strftime("%H%M%S"))
    vendedor_var = tk.StringVar()
    enganche_consola_var = tk.StringVar(value="0")
    enganche_cliente_var = tk.StringVar(value="0")
    venta_var = tk.StringVar(value="0")
    plataforma_var = tk.StringVar(value="PAYJOY")
    ganancia_plataforma_var = tk.StringVar(value="0.00")
    ganancia_total_var = tk.StringVar(value="0.00")
    pagara_plataforma_var = tk.StringVar(value="0.00")
    costo_equipo_var = tk.StringVar(value="0")
    plazo_var = tk.StringVar(value="0")

    # ---------------- CÁLCULOS AUTOMÁTICOS ---------------- #
    def valor_float(var):
        try:
            val = var.get().strip()
            return float(val) if val else 0.0
        except:
            return 0.0

    def valor_int(var):
        try:
            val = var.get().strip()
            return int(val) if val else 0
        except:
            return 0

    def recalcular(*args):
        venta = valor_float(venta_var)
        enganche_consola = valor_float(enganche_consola_var)
        enganche_cliente = valor_float(enganche_cliente_var)
        costo_equipo = valor_float(costo_equipo_var)

        # Fórmulas solicitadas:
        # 1. Pagar plataforma = venta - enganche consola
        pagara_plat = venta - enganche_consola
        
        # 2. Ganancia plataforma = pagara plataforma - costo equipo
        ganancia_plat = pagara_plat - costo_equipo
        
        # 3. Ganancia total = ganancia plataforma + enganche cliente
        ganancia_tot = ganancia_plat + enganche_cliente

        # Actualizar variables
        pagara_plataforma_var.set(f"{pagara_plat:.2f}")
        ganancia_plataforma_var.set(f"{ganancia_plat:.2f}")
        ganancia_total_var.set(f"{ganancia_tot:.2f}")

    # Vincular rastreadores para cálculo en tiempo real
    for var in (venta_var, enganche_consola_var, enganche_cliente_var, costo_equipo_var):
        var.trace_add("write", recalcular)

    # ---------------- PRODUCTOS Y VENDEDORES ---------------- #
    def productos_disponibles():
        productos = obtener_productos()
        return [p for p in productos if p[8] > 0 and p[9] == "DISPONIBLE"]

    def actualizar_combo_imei():
        combo_imei["values"] = [p[3] for p in productos_disponibles()]

    def filtrar_imei(event=None):
        texto = imei_var.get()
        lista = [str(p[3]) for p in productos_disponibles()]
        coincidencias = [imei for imei in lista if imei.startswith(texto)]
        combo_imei["values"] = coincidencias
        if event and event.keysym in ("BackSpace", "Delete"): return
        if texto == "": 
            actualizar_combo_imei()
            return
        if coincidencias:
            primer = coincidencias[0]
            if texto != primer:
                imei_var.set(primer)
                combo_imei.icursor(len(texto))
                combo_imei.select_range(len(texto), tk.END)

    def seleccionar_imei(event=None):
        for p in productos_disponibles():
            if p[3] == imei_var.get():
                equipo_var.set(p[4])
                costo_equipo_var.set("0") 
                recalcular()
                break

    def refrescar_vendedores():
        combo_vendedor["values"] = obtener_vendedores()

    def agregar_vendedor_ui():
        nombre = entry_nuevo_vendedor.get().strip()
        if not nombre:
            messagebox.showwarning("Dato faltante", "Escribe el nombre del vendedor.")
            return
        if agregar_vendedor(nombre):
            messagebox.showinfo("Correcto", "Vendedor agregado.")
        else:
            messagebox.showwarning("Aviso", "Ese vendedor ya existe.")
        entry_nuevo_vendedor.delete(0, tk.END)
        refrescar_vendedores()

    def eliminar_vendedor_ui():
        nombre = vendedor_var.get().strip()
        if not nombre:
            messagebox.showwarning("Selecciona un vendedor", "Elige un vendedor de la lista.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Deseas eliminar al vendedor '{nombre}'?"): return
        if eliminar_vendedor(nombre):
            messagebox.showinfo("Correcto", "Vendedor eliminado.")
        vendedor_var.set("")
        refrescar_vendedores()

    # ---------------- DIBUJAR CAMPOS ---------------- #
    crear_label("Fecha venta", 0, 0)
    ttk.Entry(form, textvariable=fecha_var).grid(row=1, column=0, padx=10, sticky="ew")

    crear_label("Equipo", 0, 1)
    ttk.Entry(form, textvariable=equipo_var, state="readonly").grid(row=1, column=1, padx=10, sticky="ew")

    crear_label("Nombre cliente", 0, 2)
    ttk.Entry(form, textvariable=nombre_cliente_var).grid(row=1, column=2, padx=10, sticky="ew")

    crear_label("IMEI", 2, 0)
    combo_imei = ttk.Combobox(form, textvariable=imei_var)
    combo_imei.grid(row=3, column=0, padx=10, sticky="ew")

    crear_label("TAG", 2, 1)
    ttk.Entry(form, textvariable=tag_var, state="readonly").grid(row=3, column=1, padx=10, sticky="ew")

    crear_label("Nombre vendedor", 2, 2)
    combo_vendedor = ttk.Combobox(form, textvariable=vendedor_var, state="readonly")
    combo_vendedor.grid(row=3, column=2, padx=10, sticky="ew")

    crear_label("Enganche consola", 4, 0)
    ttk.Entry(form, textvariable=enganche_consola_var).grid(row=5, column=0, padx=10, sticky="ew")

    crear_label("Enganche cliente", 4, 1)
    ttk.Entry(form, textvariable=enganche_cliente_var).grid(row=5, column=1, padx=10, sticky="ew")

    crear_label("Venta", 4, 2)
    ttk.Entry(form, textvariable=venta_var).grid(row=5, column=2, padx=10, sticky="ew")

    crear_label("Plataforma", 6, 0)
    ttk.Combobox(form, textvariable=plataforma_var, values=["PAYJOY", "CREDICELL", "KREDIYA", "LES PAGO"], state="readonly").grid(row=7, column=0, padx=10, sticky="ew")

    # Campos de solo lectura (Calculados)
    crear_label("Ganancia plataforma", 6, 1)
    ttk.Entry(form, textvariable=ganancia_plataforma_var, state="readonly").grid(row=7, column=1, padx=10, sticky="ew")

    crear_label("Ganancia total", 6, 2)
    ttk.Entry(form, textvariable=ganancia_total_var, state="readonly").grid(row=7, column=2, padx=10, sticky="ew")

    crear_label("Pagará plataforma", 8, 0)
    ttk.Entry(form, textvariable=pagara_plataforma_var, state="readonly").grid(row=9, column=0, padx=10, sticky="ew")

    crear_label("Costo del equipo", 8, 1)
    ttk.Entry(form, textvariable=costo_equipo_var).grid(row=9, column=1, padx=10, sticky="ew")

    crear_label("Plazo (semanas)", 8, 2)
    ttk.Entry(form, textvariable=plazo_var).grid(row=9, column=2, padx=10, sticky="ew")

    combo_imei.bind("<<ComboboxSelected>>", seleccionar_imei)
    combo_imei.bind("<KeyRelease>", filtrar_imei)

    # ---------------- BARRA VENDEDORES ---------------- #
    barra_vendedores = tk.Frame(card_form, bg="white")
    barra_vendedores.pack(fill="x", padx=20, pady=(0, 10))

    tk.Label(barra_vendedores, text="Nuevo vendedor:", bg="white", fg="#334155", font=("Segoe UI", 10, "bold")).pack(side="left")
    entry_nuevo_vendedor = ttk.Entry(barra_vendedores, width=25)
    entry_nuevo_vendedor.pack(side="left", padx=10)

    tk.Button(barra_vendedores, text="Agregar vendedor", bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=agregar_vendedor_ui, cursor="hand2", padx=14, pady=8).pack(side="left", padx=(0, 10))
    tk.Button(barra_vendedores, text="Eliminar vendedor", bg="#dc2626", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=eliminar_vendedor_ui, cursor="hand2", padx=14, pady=8).pack(side="left")

    # ---------------- ACCIONES ---------------- #
    barra_acciones = tk.Frame(card_form, bg="white")
    barra_acciones.pack(fill="x", padx=20, pady=(0, 18))

    def limpiar():
        fecha_var.set(datetime.now().strftime("%d/%m/%Y"))
        equipo_var.set("")
        nombre_cliente_var.set("")
        imei_var.set("")
        tag_var.set("V" + datetime.now().strftime("%H%M%S"))
        vendedor_var.set("")
        enganche_consola_var.set("0")
        enganche_cliente_var.set("0")
        venta_var.set("0")
        plataforma_var.set("PAYJOY")
        costo_equipo_var.set("0")
        plazo_var.set("0")
        recalcular()

    def guardar():
        try:
            if not imei_var.get() or not nombre_cliente_var.get().strip() or not vendedor_var.get().strip():
                messagebox.showwarning("Campos obligatorios", "Completa IMEI, Cliente y Vendedor.")
                return
            data = {
                "fecha_venta": fecha_var.get(),
                "equipo": equipo_var.get(),
                "nombre_cliente": nombre_cliente_var.get().strip(),
                "imei": imei_var.get(),
                "tag": tag_var.get(),
                "nombre_vendedor": vendedor_var.get().strip(),
                "enganche_consola": valor_float(enganche_consola_var),
                "enganche_cliente": valor_float(enganche_cliente_var),
                "venta": valor_float(venta_var),
                "plataforma": plataforma_var.get(),
                "ganancia_plataforma": valor_float(ganancia_plataforma_var),
                "ganancia_total": valor_float(ganancia_total_var),
                "pagara_plataforma": valor_float(pagara_plataforma_var),
                "costo_equipo": valor_float(costo_equipo_var),
                "plazo_semanas": valor_int(plazo_var),
            }
            registrar_venta(data)
            messagebox.showinfo("Correcto", "Venta registrada.")
            limpiar()
            cargar_tabla()
            actualizar_combo_imei()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    tk.Button(barra_acciones, text="Registrar venta", bg="#e2c346", font=("Segoe UI", 11, "bold"), command=guardar, cursor="hand2", padx=18, pady=10, relief="flat").pack(side="left")
    tk.Button(barra_acciones, text="Limpiar", bg="#e2e8f0", font=("Segoe UI", 10, "bold"), command=limpiar, cursor="hand2", padx=16, pady=10, relief="flat").pack(side="left", padx=(10, 0))

    # ---------------- TABLA ---------------- #
    card_tabla = tk.Frame(cuerpo, bg="white", bd=1, relief="solid")
    card_tabla.pack(fill="both", expand=True)

    top_tabla = tk.Frame(card_tabla, bg="white")
    top_tabla.pack(fill="x", padx=20, pady=(18, 10))

    tk.Label(top_tabla, text="Ventas registradas", bg="white", font=("Segoe UI", 13, "bold")).pack(side="left")
    buscador_frame = tk.Frame(top_tabla, bg="white")
    buscador_frame.pack(side="right")
    tk.Label(buscador_frame, text="Buscar:", bg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
    entry_buscar = ttk.Entry(buscador_frame, width=28)
    entry_buscar.pack(side="left")

    tabla_wrap = tk.Frame(card_tabla, bg="white")
    tabla_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    columnas = ("ID", "FECHA", "CLIENTE", "IMEI", "TAG", "VENDEDOR", "VENTA", "PLATAFORMA", "GANANCIA", "PLAZO")
    tabla = ttk.Treeview(tabla_wrap, columns=columnas, show="headings")
    anchos = {"ID": 60, "FECHA": 110, "CLIENTE": 140, "IMEI": 140, "TAG": 110, "VENDEDOR": 130, "VENTA": 100, "PLATAFORMA": 120, "GANANCIA": 110, "PLAZO": 90}

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=anchos[col], anchor="center")

    scroll_y = ttk.Scrollbar(tabla_wrap, orient="vertical", command=tabla.yview)
    scroll_x = ttk.Scrollbar(tabla_wrap, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    tabla.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    tabla_wrap.grid_rowconfigure(0, weight=1)
    tabla_wrap.grid_columnconfigure(0, weight=1)

    def cargar_tabla(datos=None):
        for fila in tabla.get_children(): tabla.delete(fila)
        registros = datos if datos is not None else obtener_ventas()
        for v in registros:
            tabla.insert("", tk.END, values=(v[0], v[1], v[3], v[4], v[5], v[6], v[9], v[10], v[12], v[15]))

    def buscar(_event=None):
        texto = entry_buscar.get().strip().lower()
        if not texto: 
            cargar_tabla()
            return
        resultados = [v for v in obtener_ventas() if texto in " ".join(map(str, v)).lower()]
        cargar_tabla(resultados)

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion: return
        valores = tabla.item(seleccion[0], "values")
        if messagebox.askyesno("Confirmar", f"¿Eliminar venta ID {valores[0]}?"):
            eliminar_venta(valores[0])
            cargar_tabla()
            actualizar_combo_imei()

    tk.Button(card_tabla, text="Eliminar", bg="#dc2626", fg="white", font=("Segoe UI", 10, "bold"), command=eliminar, cursor="hand2", padx=14, pady=8, relief="flat").pack(anchor="w", padx=20, pady=(0,10))
    
    entry_buscar.bind("<KeyRelease>", buscar)
    
    def refrescar():
        refrescar_vendedores()
        actualizar_combo_imei()
        cargar_tabla()

    refrescar()
    frame.refrescar = refrescar
    return frame