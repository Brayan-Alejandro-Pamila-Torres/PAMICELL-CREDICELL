# ui/ventas_ui.py
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from services.ventas_service import registrar_venta, obtener_vendedores, agregar_vendedor, eliminar_vendedor
from services.inventario_service import obtener_productos

def crear_frame_ventas(parent):
    # Frame principal contenedor
    frame = tk.Frame(parent, bg="#f8fafc")

    # ---------------- HEADER FIXED (SIEMPRE VISIBLE) ---------------- #
    header = tk.Frame(frame, bg="#1f2022", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Módulo de Ventas y Financiamientos",
        bg="#1f2022",
        fg="white",
        font=("Ubuntu", 18, "bold")
    ).pack(expand=True)

    # ---------------- CONTENEDOR CON SCROLLBAR ---------------- #
    # Creamos un Canvas para permitir el desplazamiento vertical
    canvas = tk.Canvas(frame, bg="#f8fafc", highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    
    # Este frame interno contendrá todo el diseño original
    cuerpo_scrollable = tk.Frame(canvas, bg="#f8fafc")
    
    # Configurar el Canvas para que renderice el frame interno
    window_id = canvas.create_window((0, 0), window=cuerpo_scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Empaquetamos el sistema de scrollbar a la derecha y el canvas al centro
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Lógica adaptativa para ajustar el ancho automáticamente al redimensionar la ventana
    def al_redimensionar_canvas(event):
        canvas.itemconfig(window_id, width=event.width)
    canvas.bind("<Configure>", al_redimensionar_canvas)

    def actualizar_region_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    cuerpo_scrollable.bind("<Configure>", actualizar_region_scroll)

    # SOPORTE PARA LA RUEDA DEL MOUSE (Soporta Linux Mint y Windows)
    def_on_mousewheel = lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") if os.name == 'nt' else lambda event: canvas.yview_scroll(int(-1 * event.num), "units")
    
    # En Linux Mint (X11) se usan los eventos Button-4 y Button-5
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
    # En Windows se usa MouseWheel
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    # ---------------- CUERPO DEL FORMULARIO ---------------- #
    cuerpo = tk.Frame(cuerpo_scrollable, bg="#f8fafc")
    cuerpo.pack(fill="both", expand=True, padx=24, pady=24)

    card_form = tk.Frame(cuerpo, bg="white", bd=1, relief="solid")
    card_form.pack(fill="both", expand=True, pady=10)

    tk.Label(card_form, text="Registrar Nueva Operación", bg="white", fg="#0f172a", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=(18, 8))

    form = tk.Frame(card_form, bg="white")
    form.pack(fill="x", padx=20, pady=(0, 10))

    def crear_label(texto, row, col):
        tk.Label(form, text=texto, bg="white", fg="#334155", font=("Segoe UI", 10, "bold")).grid(row=row, column=col, sticky="w", padx=10, pady=(6, 2))

    for i in range(3): form.grid_columnconfigure(i, weight=1)

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

    def valor_float(var):
        try: return float(var.get().strip()) if var.get() else 0.0
        except: return 0.0

    def valor_int(var):
        try: return int(var.get().strip()) if var.get() else 0
        except: return 0

    def recalcular(*args):
        venta = valor_float(venta_var)
        enganche_consola = valor_float(enganche_consola_var)
        enganche_cliente = valor_float(enganche_cliente_var)
        costo_equipo = valor_float(costo_equipo_var)

        pagara_plat = venta - enganche_consola
        ganancia_plat = pagara_plat - costo_equipo
        ganancia_tot = ganancia_plat + enganche_cliente

        pagara_plataforma_var.set(f"{pagara_plat:.2f}")
        ganancia_plataforma_var.set(f"{ganancia_plat:.2f}")
        ganancia_total_var.set(f"{ganancia_tot:.2f}")

    for var in (venta_var, enganche_consola_var, enganche_cliente_var, costo_equipo_var):
        var.trace_add("write", recalcular)

    def productos_disponibles():
        return [p for p in obtener_productos() if p[8] > 0 and p[9] == "DISPONIBLE"]

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
        if coincidencias and texto != coincidencias[0]:
            imei_var.set(coincidencias[0])
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
        if not nombre: return
        if agregar_vendedor(nombre):
            messagebox.showinfo("Éxito", "Vendedor añadido.")
        else:
            messagebox.showwarning("Aviso", "El vendedor ya existe.")
        entry_nuevo_vendedor.delete(0, tk.END)
        refrescar_vendedores()

    def eliminar_vendedor_ui():
        nombre = vendedor_var.get().strip()
        if not nombre: return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar al vendedor '{nombre}'?"): return
        if eliminar_vendedor(nombre):
            messagebox.showinfo("Éxito", "Vendedor eliminado.")
        vendedor_var.set("")
        refrescar_vendedores()

    # RENGALÓN 1: FECHA, EQUIPO, NOMBRE DEL CLIENTE
    crear_label("FECHA", 0, 0)
    ttk.Entry(form, textvariable=fecha_var).grid(row=1, column=0, padx=10, sticky="ew")
    crear_label("EQUIPO", 0, 1)
    ttk.Entry(form, textvariable=equipo_var, state="readonly").grid(row=1, column=1, padx=10, sticky="ew")
    crear_label("NOMBRE DEL CLIENTE", 0, 2)
    ttk.Entry(form, textvariable=nombre_cliente_var).grid(row=1, column=2, padx=10, sticky="ew")

    # RENGLÓN 2: IMEI, TAG, VENDIÓ
    crear_label("IMEI", 2, 0)
    combo_imei = ttk.Combobox(form, textvariable=imei_var)
    combo_imei.grid(row=3, column=0, padx=10, sticky="ew")
    crear_label("TAG", 2, 1)
    ttk.Entry(form, textvariable=tag_var, state="readonly").grid(row=3, column=1, padx=10, sticky="ew")
    crear_label("VENDIÓ", 2, 2)
    combo_vendedor = ttk.Combobox(form, textvariable=vendedor_var, state="readonly")
    combo_vendedor.grid(row=3, column=2, padx=10, sticky="ew")

    # RENGLÓN 3: ENGANCHE CONSOLA, ENGANCHE CLIENTE, VENTA
    crear_label("ENGANCHE CONSOLA", 4, 0)
    ttk.Entry(form, textvariable=enganche_consola_var).grid(row=5, column=0, padx=10, sticky="ew")
    crear_label("ENGANCHE CLIENTE", 4, 1)
    ttk.Entry(form, textvariable=enganche_cliente_var).grid(row=5, column=1, padx=10, sticky="ew")
    crear_label("VENTA", 4, 2)
    ttk.Entry(form, textvariable=venta_var).grid(row=5, column=2, padx=10, sticky="ew")

    # RENGLÓN 4: PLATAFORMA, GANANCIA PLATAFORMA, GANANCIA TOTAL
    crear_label("PLATAFORMA", 6, 0)
    ttk.Combobox(form, textvariable=plataforma_var, values=["PAYJOY", "CREDICELL", "KREDIYA", "LES PAGO"], state="readonly").grid(row=7, column=0, padx=10, sticky="ew")
    crear_label("GANANCIA PLATAFORMA", 6, 1)
    ttk.Entry(form, textvariable=ganancia_plataforma_var, state="readonly").grid(row=7, column=1, padx=10, sticky="ew")
    crear_label("GANANCIA TOTAL", 6, 2)
    ttk.Entry(form, textvariable=ganancia_total_var, state="readonly").grid(row=7, column=2, padx=10, sticky="ew")

    # RENGLÓN 5: PAGARA PLATAFORMA , COSTO DE EQUIPO, PLAZO
    crear_label("PAGARA PLATAFORMA", 8, 0)
    ttk.Entry(form, textvariable=pagara_plataforma_var, state="readonly").grid(row=9, column=0, padx=10, sticky="ew")
    crear_label("COSTO DE EQUIPO", 8, 1)
    ttk.Entry(form, textvariable=costo_equipo_var).grid(row=9, column=1, padx=10, sticky="ew")
    crear_label("PLAZO", 8, 2)
    ttk.Entry(form, textvariable=plazo_var).grid(row=9, column=2, padx=10, sticky="ew")

    combo_imei.bind("<<ComboboxSelected>>", seleccionar_imei)
    combo_imei.bind("<KeyRelease>", filtrar_imei)

    # Panel de Operadores
    barra_vendedores = tk.Frame(card_form, bg="#f1f5f9", bd=1, relief="solid")
    barra_vendedores.pack(fill="x", padx=20, pady=15, ipady=5)
    tk.Label(barra_vendedores, text="  Alta Operadores: ", bg="#f1f5f9", fg="#334155", font=("Segoe UI", 10, "bold")).pack(side="left", pady=8)
    entry_nuevo_vendedor = ttk.Entry(barra_vendedores, width=25)
    entry_nuevo_vendedor.pack(side="left", padx=10, pady=8)
    tk.Button(barra_vendedores, text="Agregar", bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", command=agregar_vendedor_ui, cursor="hand2", padx=10).pack(side="left", padx=5)
    tk.Button(barra_vendedores, text="Eliminar", bg="#dc2626", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", command=eliminar_vendedor_ui, cursor="hand2", padx=10).pack(side="left")

    # ---------------- BARRA DE ACCIONES FINALES (BOTÓN GUARDAR SEGURO) ---------------- #
    barra_acciones = tk.Frame(card_form, bg="white")
    barra_acciones.pack(fill="x", padx=20, pady=(10, 20))

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
                messagebox.showwarning("Campos obligatorios", "Determina el IMEI, Cliente y Vendedor para continuar con la venta.")
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
            messagebox.showinfo("Éxito", "Venta y/o crédito asentado exitosamente.")
            limpiar()
            refrescar()
        except Exception as e:
            messagebox.showerror("Error", f"Fallo de persistencia: {e}")

    # Botón de Guardar Operación fijado visiblemente al final del layout interno
    tk.Button(
        barra_acciones, 
        text="💾 REGISTRAR NUEVA VENTA / FINANCIAMIENTO", 
        bg="#2563eb", 
        fg="white", 
        font=("Segoe UI", 12, "bold"), 
        relief="flat", 
        command=guardar, 
        cursor="hand2", 
        pady=10
    ).pack(fill="x", expand=True)

    def refrescar():
        refrescar_vendedores()
        actualizar_combo_imei()

    refrescar()
    frame.refrescar = refrescar
    return frame