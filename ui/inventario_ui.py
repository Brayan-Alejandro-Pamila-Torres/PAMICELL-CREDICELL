import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from services.inventario_service import guardar_producto, obtener_productos
from database import conectar

def crear_frame_inventario(parent):
    frame = tk.Frame(parent, bg="#f8fafc")

    # ---------------- HEADER ---------------- #

    header = tk.Frame(frame, bg="#1f2022", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Gestión de Inventario",
        bg="#1f2022",
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(expand=True)

    # ---------------- CONTENIDO ---------------- #

    cont = tk.Frame(frame, bg="#f8fafc")
    cont.pack(fill="both", expand=True, padx=24, pady=24)

    # ---------------- TARJETA FORMULARIO ---------------- #

    card_form = tk.Frame(cont, bg="white", bd=1, relief="solid")
    card_form.pack(fill="x", pady=(0, 18))

    tk.Label(
        card_form,
        text="Registrar equipo",
        bg="white",
        fg="#0f172a",
        font=("Segoe UI", 13, "bold")
    ).pack(anchor="w", padx=20, pady=(18, 8))

    form = tk.Frame(card_form, bg="white")
    form.pack(fill="x", padx=20, pady=(0, 18))

    proveedor = tk.StringVar(value="GAMA PLUS")
    ram = tk.StringVar(value="4GB")
    almacenamiento = tk.StringVar(value="64GB")

    def crear_label(texto, row, col):
        tk.Label(
            form,
            text=texto,
            bg="white",
            fg="#334155",
            font=("Segoe UI", 10, "bold")
        ).grid(row=row, column=col, sticky="w", padx=10, pady=(8, 4))

    entry_fecha = ttk.Entry(form, width=24)
    entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))

    combo_proveedor = ttk.Combobox(
        form,
        textvariable=proveedor,
        values=["GAMA PLUS", "SMART SHOP", "NANO SHOP", "TELESISTEM"],
        state="readonly",
        width=22
    )

    entry_imei = ttk.Entry(form, width=24)
    entry_modelo = ttk.Entry(form, width=24)
    entry_precio = ttk.Entry(form, width=24)

    combo_ram = ttk.Combobox(
        form,
        textvariable=ram,
        values=["4GB", "8GB", "16GB", "32GB", "64GB", "128GB", "256GB"],
        state="readonly",
        width=22
    )

    combo_alm = ttk.Combobox(
        form,
        textvariable=almacenamiento,
        values=["32GB", "64GB", "128GB", "256GB", "512GB", "1TB"],
        state="readonly",
        width=22
    )

    for i in range(3):
        form.grid_columnconfigure(i, weight=1)

    crear_label("Fecha", 0, 0)
    crear_label("Proveedor", 0, 1)
    crear_label("IMEI", 0, 2)

    entry_fecha.grid(row=1, column=0, padx=10, pady=(0, 8), sticky="ew")
    combo_proveedor.grid(row=1, column=1, padx=10, pady=(0, 8), sticky="ew")
    entry_imei.grid(row=1, column=2, padx=10, pady=(0, 8), sticky="ew")

    crear_label("Modelo", 2, 0)
    crear_label("Precio de compra", 2, 1)
    crear_label("RAM", 2, 2)

    entry_modelo.grid(row=3, column=0, padx=10, pady=(0, 8), sticky="ew")
    entry_precio.grid(row=3, column=1, padx=10, pady=(0, 8), sticky="ew")
    combo_ram.grid(row=3, column=2, padx=10, pady=(0, 8), sticky="ew")

    crear_label("Almacenamiento", 4, 0)
    combo_alm.grid(row=5, column=0, padx=10, pady=(0, 8), sticky="ew")

    barra_acciones = tk.Frame(card_form, bg="white")
    barra_acciones.pack(fill="x", padx=20, pady=(0, 18))

    # ---------------- TARJETA TABLA ---------------- #

    card_tabla = tk.Frame(cont, bg="white", bd=1, relief="solid")
    card_tabla.pack(fill="both", expand=True)

    top_tabla = tk.Frame(card_tabla, bg="white")
    top_tabla.pack(fill="x", padx=20, pady=(18, 10))

    tk.Label(
        top_tabla,
        text="Inventario registrado",
        bg="white",
        fg="#0f172a",
        font=("Segoe UI", 13, "bold")
    ).pack(side="left")

    buscador_frame = tk.Frame(top_tabla, bg="white")
    buscador_frame.pack(side="right")

    tk.Label(
        buscador_frame,
        text="Buscar:",
        bg="white",
        fg="#334155",
        font=("Segoe UI", 10, "bold")
    ).pack(side="left", padx=(0, 8))

    entry_buscar = ttk.Entry(buscador_frame, width=28)
    entry_buscar.pack(side="left")

    acciones_tabla = tk.Frame(card_tabla, bg="white")
    acciones_tabla.pack(fill="x", padx=20, pady=(0, 10))

    tabla_wrap = tk.Frame(card_tabla, bg="white")
    tabla_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    columnas = ("ID", "FECHA", "PROVEEDOR", "IMEI", "MODELO", "PRECIO", "RAM", "ALM", "ESTATUS")

    tabla = ttk.Treeview(tabla_wrap, columns=columnas, show="headings")

    anchos = {
        "ID": 60,
        "FECHA": 110,
        "PROVEEDOR": 130,
        "IMEI": 150,
        "MODELO": 150,
        "PRECIO": 110,
        "RAM": 90,
        "ALM": 100,
        "ESTATUS": 120
    }

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=anchos[col], anchor="center", stretch=True)

    scroll_y = ttk.Scrollbar(tabla_wrap, orient="vertical", command=tabla.yview)
    scroll_x = ttk.Scrollbar(tabla_wrap, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabla.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    tabla_wrap.grid_rowconfigure(0, weight=1)
    tabla_wrap.grid_columnconfigure(0, weight=1)

    # ---------------- FUNCIONES ---------------- #

    producto_editando_id = {"valor": None}

    def limpiar():
        producto_editando_id["valor"] = None
        entry_imei.delete(0, tk.END)
        entry_modelo.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        proveedor.set("GAMA PLUS")
        ram.set("4GB")
        almacenamiento.set("64GB")
        btn_guardar.config(text="Guardar equipo")

    def cargar_tabla(datos=None):
        for fila in tabla.get_children():
            tabla.delete(fila)

        registros = datos if datos is not None else obtener_productos()

        for p in registros:
            tabla.insert(
                "",
                tk.END,
                values=(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])
            )

    def guardar():
        try:
            if not entry_imei.get() or not entry_modelo.get() or not entry_precio.get():
                messagebox.showwarning("Campos obligatorios", "IMEI, Modelo y Precio son obligatorios.")
                return

            if not entry_imei.get().isdigit() or len(entry_imei.get()) != 15:
                messagebox.showerror("IMEI inválido", "El IMEI debe contener exactamente 15 dígitos.")
                return

            precio = float(entry_precio.get())

            if producto_editando_id["valor"] is None:
                data = {
                    "fecha": entry_fecha.get(),
                    "proveedor": proveedor.get(),
                    "imei": entry_imei.get(),
                    "modelo": entry_modelo.get(),
                    "precio": precio,
                    "ram": ram.get(),
                    "alm": almacenamiento.get()
                }

                res = guardar_producto(data)

                if res == "existe":
                    messagebox.showerror("Error", "Ese IMEI ya está registrado.")
                    return

                messagebox.showinfo("Correcto", "Producto guardado correctamente.")
            else:
                conn = conectar()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    UPDATE productos
                    SET fecha = ?, proveedor = ?, imei = ?, modelo = ?, precio_compra = ?, ram = ?, almacenamiento = ?
                    WHERE id = ?
                    """,
                    (
                        entry_fecha.get(),
                        proveedor.get(),
                        entry_imei.get(),
                        entry_modelo.get(),
                        precio,
                        ram.get(),
                        almacenamiento.get(),
                        producto_editando_id["valor"]
                    )
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Correcto", "Producto actualizado correctamente.")

            limpiar()
            cargar_tabla()

        except ValueError:
            messagebox.showerror("Precio inválido", "Ingresa un número válido en el precio.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def buscar(_event=None):
        texto = entry_buscar.get().strip().lower()

        if not texto:
            cargar_tabla()
            return

        resultados = []
        for p in obtener_productos():
            if texto in " ".join(map(str, p)).lower():
                resultados.append(p)

        cargar_tabla(resultados)

    def editar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona un registro", "Primero selecciona un producto de la tabla.")
            return

        valores = tabla.item(seleccion[0], "values")

        producto_editando_id["valor"] = valores[0]

        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, valores[1])

        proveedor.set(valores[2])

        entry_imei.delete(0, tk.END)
        entry_imei.insert(0, valores[3])

        entry_modelo.delete(0, tk.END)
        entry_modelo.insert(0, valores[4])

        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, valores[5])

        ram.set(valores[6])
        almacenamiento.set(valores[7])

        btn_guardar.config(text="Actualizar equipo")

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona un registro", "Primero selecciona un producto de la tabla.")
            return

        valores = tabla.item(seleccion[0], "values")
        producto_id = valores[0]
        modelo = valores[4]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar el producto '{modelo}'?"
        )

        if not confirmar:
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conn.commit()
        conn.close()

        limpiar()
        cargar_tabla()

    # ---------------- BOTONES COLOREADOS ---------------- #

    btn_guardar = tk.Button(
        barra_acciones,
        text="Guardar equipo",
        bg="#f3d971",
        fg="#111827",
        activebackground="#f5d060",
        activeforeground="#111827",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        bd=0,
        padx=18,
        pady=10,
        cursor="hand2",
        command=guardar
    )
    btn_guardar.pack(side="left")

    btn_limpiar = tk.Button(
        barra_acciones,
        text="Limpiar",
        bg="#e2e8f0",
        fg="#0f172a",
        activebackground="#cbd5e1",
        activeforeground="#0f172a",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=16,
        pady=10,
        cursor="hand2",
        command=limpiar
    )
    btn_limpiar.pack(side="left", padx=(10, 0))

    btn_editar = tk.Button(
        acciones_tabla,
        text="Editar",
        bg="#92a9da",
        fg="white",
        activebackground="#89a6f5",
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=14,
        pady=8,
        cursor="hand2",
        command=editar
    )
    btn_editar.pack(side="left")

    btn_eliminar = tk.Button(
        acciones_tabla,
        text="Eliminar",
        bg="#dc2626",
        fg="white",
        activebackground="#b91c1c",
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=14,
        pady=8,
        cursor="hand2",
        command=eliminar
    )
    btn_eliminar.pack(side="left", padx=(10, 0))

    entry_buscar.bind("<KeyRelease>", buscar)

    cargar_tabla()

    return frame