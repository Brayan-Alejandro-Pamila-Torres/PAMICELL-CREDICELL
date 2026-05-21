import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from services.inventario_service import guardar_producto

def crear_frame_inventario(parent, cambiar_a_datos_callback=None):
    frame = tk.Frame(parent, bg="#f8fafc")

    # ---------------- HEADER ---------------- #
    header = tk.Frame(frame, bg="#1f2022", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Registro de Nuevo Inventario",
        bg="#1f2022",
        fg="white",
        font=("Ubuntu", 18, "bold")
    ).pack(expand=True)

    cont = tk.Frame(frame, bg="#f8fafc")
    cont.pack(fill="both", expand=True, padx=24, pady=24)

    card_form = tk.Frame(cont, bg="white", bd=1, relief="solid")
    card_form.pack(fill="x", pady=40)

    tk.Label(card_form, text="Formulario de Alta de Equipos Celulares", bg="white", fg="#0f172a", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=(18, 8))

    form = tk.Frame(card_form, bg="white")
    form.pack(fill="x", padx=20, pady=(0, 18))

    proveedor = tk.StringVar(value="GAMA PLUS")
    ram = tk.StringVar(value="4GB")
    almacenamiento = tk.StringVar(value="64GB")

    def crear_label(texto, row, col):
        tk.Label(form, text=texto, bg="white", fg="#334155", font=("Segoe UI", 10, "bold")).grid(row=row, column=col, sticky="w", padx=10, pady=(8, 4))

    entry_fecha = ttk.Entry(form, width=24)
    entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))

    combo_proveedor = ttk.Combobox(form, textvariable=proveedor, values=["GAMA PLUS", "SMART SHOP", "NANO SHOP", "TELESISTEM"], state="readonly", width=22)
    entry_imei = ttk.Entry(form, width=24)
    entry_modelo = ttk.Entry(form, width=24)
    entry_precio = ttk.Entry(form, width=24)
    combo_ram = ttk.Combobox(form, textvariable=ram, values=["4GB", "8GB", "16GB", "32GB"], state="readonly", width=22)
    combo_alm = ttk.Combobox(form, textvariable=almacenamiento, values=["32GB", "64GB", "128GB", "256GB", "512GB", "1TB"], state="readonly", width=22)

    for i in range(3): form.grid_columnconfigure(i, weight=1)

    # FILA 1: FECHA, PROVEEDOR, IMEI
    crear_label("FECHA", 0, 0)
    crear_label("PROVEEDOR", 0, 1)
    crear_label("IMEI", 0, 2)

    entry_fecha.grid(row=1, column=0, padx=10, pady=(0, 8), sticky="ew")
    combo_proveedor.grid(row=1, column=1, padx=10, pady=(0, 8), sticky="ew")
    entry_imei.grid(row=1, column=2, padx=10, pady=(0, 8), sticky="ew")

    # FILA 2: MODELO, PRECIO COMPRA, RAM
    crear_label("MODELO", 2, 0)
    crear_label("PRECIO COMPRA", 2, 1)
    crear_label("RAM", 2, 2)

    entry_modelo.grid(row=3, column=0, padx=10, pady=(0, 8), sticky="ew")
    entry_precio.grid(row=3, column=1, padx=10, pady=(0, 8), sticky="ew")
    combo_ram.grid(row=3, column=2, padx=10, pady=(0, 8), sticky="ew")

    # FILA 3: A INTERNO, CANTIDAD LOTE, IVA
    crear_label("A INTERNO", 4, 0)
    combo_alm.grid(row=5, column=0, padx=10, pady=(0, 8), sticky="ew")

    crear_label("CANTIDAD LOTE", 4, 1)
    entry_stock = ttk.Entry(form, width=24)
    entry_stock.insert(0, "1")
    entry_stock.grid(row=5, column=1, padx=10, pady=(0, 8), sticky="ew")
    
    crear_label("IVA", 4, 2)
    entry_iva = ttk.Entry(form, width=24, state="readonly")
    entry_iva.grid(row=5, column=2, padx=10, pady=(0, 8), sticky="ew")

    def calcular_iva(event=None):
        try:
            precio = float(entry_precio.get())
            iva = precio * 0.16
            entry_iva.config(state="normal")
            entry_iva.delete(0, tk.END)
            entry_iva.insert(0, f"{iva:.2f}")
            entry_iva.config(state="readonly")
        except:
            entry_iva.config(state="normal")
            entry_iva.delete(0, tk.END)
            entry_iva.config(state="readonly")
            
    entry_precio.bind("<KeyRelease>", calcular_iva)

    barra_acciones = tk.Frame(card_form, bg="white")
    barra_acciones.pack(fill="x", padx=20, pady=(20, 18))

    def limpiar():
        entry_imei.delete(0, tk.END)
        entry_modelo.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        entry_stock.delete(0, tk.END)
        entry_stock.insert(0, "1")
        entry_iva.config(state="normal")
        entry_iva.delete(0, tk.END)
        entry_iva.config(state="readonly")
        proveedor.set("GAMA PLUS")
        ram.set("4GB")
        almacenamiento.set("64GB")

    def guardar():
        try:
            if not entry_imei.get() or not entry_modelo.get() or not entry_precio.get():
                messagebox.showwarning("Campos vacíos", "IMEI, MODELO y PRECIO COMPRA son obligatorios.")
                return

            imei_base_str = entry_imei.get().strip()
            if not imei_base_str.isdigit() or len(imei_base_str) != 15:
                messagebox.showerror("IMEI inválido", "El IMEI base debe contener exactamente 15 dígitos numéricos.")
                return

            precio = float(entry_precio.get())
            iva = precio * 0.16
            cantidad_lote = int(entry_stock.get())

            if cantidad_lote <= 0:
                messagebox.showwarning("Cantidad inválida", "La cantidad de equipos en el lote debe ser mayor a 0.")
                return

            imei_base_int = int(imei_base_str)
            imeis_duplicados = []
            registrados_con_exito = 0

            for i in range(cantidad_lote):
                nuevo_imei = str(imei_base_int + i).zfill(15)
                data = {
                    "fecha": entry_fecha.get(),
                    "proveedor": proveedor.get(),
                    "imei": nuevo_imei,
                    "modelo": entry_modelo.get(),
                    "precio": precio,
                    "ram": ram.get(),
                    "alm": almacenamiento.get(),
                    "iva": iva,
                    "stock": 1,
                    "estatus": "DISPONIBLE"
                }
                res = guardar_producto(data)
                if res == "existe": imeis_duplicados.append(nuevo_imei)
                elif res == "ok": registrados_con_exito += 1

            if registrados_con_exito == cantidad_lote:
                messagebox.showinfo("Éxito Total", f"Se registraron correctamente las {cantidad_lote} piezas.")
            else:
                msg_alerta = f"Se registraron {registrados_con_exito} de {cantidad_lote} equipos.\n\n"
                if imeis_duplicados:
                    msg_alerta += f"IMEIs duplicados omitidos:\n" + "\n".join(imeis_duplicados[:5])
                messagebox.showwarning("Registro Parcial", msg_alerta)

            limpiar()
            if cambiar_a_datos_callback: cambiar_a_datos_callback()
        except ValueError:
            messagebox.showerror("Error de conversión", "Ingresa formatos numéricos válidos.")

    tk.Button(barra_acciones, text="Guardar equipo en Inventario", bg="#e2c346", fg="#111827", font=("Segoe UI", 11, "bold"), relief="flat", command=guardar, cursor="hand2", padx=18, pady=10).pack(side="left")
    tk.Button(barra_acciones, text="Limpiar Formulario", bg="#e2e8f0", fg="#0f172a", font=("Segoe UI", 10, "bold"), relief="flat", command=limpiar, cursor="hand2", padx=16, pady=10).pack(side="left", padx=(10, 0))

    frame.refrescar = limpiar
    return frame