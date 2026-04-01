import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
from database import conectar, crear_tabla

crear_tabla()

# ---------------- FUNCIONES ---------------- #

def mostrar_frame(frame):
    frame.tkraise()

def guardar_producto():
    try:
        fecha = entry_fecha.get()
        prov = valor_proveedor.get()
        imei = entry_imei.get()
        mod = entry_modelo.get()
        precio_texto = entry_precio_c.get()
        ram = valor_ram.get()
        alm = valor_almacenamiento.get()
        est = "DISPONIBLE"

        if not imei or not mod or not precio_texto:
            messagebox.showwarning("Atención", "IMEI, Modelo y Precio son obligatorios.")
            return

        if not imei.isdigit() or len(imei) != 15:
            messagebox.showwarning("Error", "El IMEI debe tener 15 dígitos.")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM productos WHERE imei = ?", (imei,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            messagebox.showerror("Error", "IMEI ya registrado")
            return

        precio = float(precio_texto)

        cursor.execute("""
            INSERT INTO productos 
            (fecha, proveedor, imei, modelo, precio_compra, ram, almacenamiento, estatus) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (fecha, prov, imei, mod, precio, ram, alm, est))

        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Producto guardado")
        limpiar_campos()
        mostrar_productos()

    except ValueError:
        messagebox.showerror("Error", "Precio inválido")

def mostrar_productos():
    for fila in tabla.get_children():
        tabla.delete(fila)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    for producto in cursor.fetchall():
        tabla.insert("", tk.END, values=producto)
    conn.close()

def limpiar_campos():
    entry_imei.delete(0, tk.END)
    entry_modelo.delete(0, tk.END)
    entry_precio_c.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)
    entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))

# ---------------- GUI ---------------- #

ventana = tk.Tk()
ventana.title("CREDICELL & PAMICELL")

try:
    ventana.state("zoomed")
except:
    ventana.attributes('-zoomed', True)

# ---- estilos ----
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11), padding=10)
style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

# ---- layout ----
contenedor = tk.Frame(ventana)
contenedor.pack(fill="both", expand=True)

contenedor.grid_rowconfigure(0, weight=1)
contenedor.grid_columnconfigure(1, weight=1)

# ---------------- SIDEBAR (APP REAL) ---------------- #

COLOR_BG = "#111417"
COLOR_HOVER = "#1f2a33"
COLOR_ACTIVE = "#2f3640"
COLOR_ACCENT = "#f1c40f"
COLOR_TEXT = "#ecf0f1"

sidebar = tk.Frame(contenedor, bg=COLOR_BG, width=280)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)  # 🔥 importante para respetar ancho

contenido = tk.Frame(contenedor)
contenido.grid(row=0, column=1, sticky="nsew")
contenido.grid_rowconfigure(0, weight=1)
contenido.grid_columnconfigure(0, weight=1)

# Header sidebar
header_sb = tk.Frame(sidebar, bg=COLOR_BG)
header_sb.pack(fill="x", pady=(20, 10))

tk.Label(header_sb, text="PAMICELL",
         bg=COLOR_BG, fg=COLOR_ACCENT,
         font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20)

tk.Label(header_sb, text="Sistema",
         bg=COLOR_BG, fg="#7f8c8d",
         font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=(2, 0))

# divisor
tk.Frame(sidebar, height=1, bg="#2c3e50").pack(fill="x", padx=15, pady=10)

# --- botones con indicador activo ---
botones_sidebar = []
indicadores = []

def activar_boton(btn, ind):
    for b in botones_sidebar:
        b.config(bg=COLOR_BG)
    for i in indicadores:
        i.config(bg=COLOR_BG)

    btn.config(bg=COLOR_ACTIVE)
    ind.config(bg=COLOR_ACCENT)

def hover_in(e):
    if e.widget["bg"] != COLOR_ACTIVE:
        e.widget.config(bg=COLOR_HOVER)

def hover_out(e):
    if e.widget["bg"] != COLOR_ACTIVE:
        e.widget.config(bg=COLOR_BG)

def boton_sidebar(texto, comando):
    cont = tk.Frame(sidebar, bg=COLOR_BG)
    cont.pack(fill="x")

    indicador = tk.Frame(cont, width=4, bg=COLOR_BG)
    indicador.pack(side="left", fill="y")

    btn = tk.Label(cont,
                   text="   " + texto,
                   bg=COLOR_BG,
                   fg=COLOR_TEXT,
                   font=("Segoe UI", 11),
                   anchor="w",
                   padx=20,
                   pady=12,
                   cursor="hand2")
    btn.pack(fill="x")

    btn.bind("<Enter>", hover_in)
    btn.bind("<Leave>", hover_out)

    def click():
        activar_boton(btn, indicador)
        comando()

    btn.bind("<Button-1>", lambda e: click())

    botones_sidebar.append(btn)
    indicadores.append(indicador)

    return btn, indicador

# botones
btn_inicio, ind_inicio = boton_sidebar("🏠  Inicio", lambda: mostrar_frame(frame_menu))
btn_inv, ind_inv = boton_sidebar("📦  Inventario", lambda: mostrar_frame(frame_inventario))
btn_ventas, ind_ventas = boton_sidebar("💰  Ventas", lambda: mostrar_frame(frame_ventas))

# ---------------- FRAMES ---------------- #

frame_menu = tk.Frame(contenido, bg="#f5f6fa")
frame_inventario = tk.Frame(contenido)
frame_ventas = tk.Frame(contenido)

for frame in (frame_menu, frame_inventario, frame_ventas):
    frame.grid(row=0, column=0, sticky="nsew")

# ---------------- MENU ---------------- #

contenedor_menu = tk.Frame(frame_menu, bg="#f5f6fa")
contenedor_menu.pack(expand=True)

try:
    img_logo = Image.open("logo.jpeg").resize((180, 180))
    logo = ImageTk.PhotoImage(img_logo)
    tk.Label(contenedor_menu, image=logo, bg="#f5f6fa").pack(pady=10)
except:
    tk.Label(contenedor_menu, text="LOGO").pack()

tk.Label(contenedor_menu, text="CREDICELL & PAMICELL",
         font=("Segoe UI", 26, "bold"),
         bg="#f5f6fa").pack()

tk.Label(contenedor_menu,
         text="Sistema Integral de Ventas e Inventario",
         font=("Segoe UI", 12),
         bg="#f5f6fa", fg="#666").pack(pady=5)

# ---------------- INVENTARIO ---------------- #

header = tk.Frame(frame_inventario, bg="#2f3640", height=60)
header.pack(fill="x")

tk.Label(header, text="Gestión de Inventario",
         bg="#2f3640", fg="white",
         font=("Segoe UI", 16, "bold")).pack(pady=10)

frame_form = tk.Frame(frame_inventario, bg="white", bd=1, relief="solid")
frame_form.pack(pady=15, padx=30, fill="x")

opciones_prov = ["GAMA PLUS", "SMART SHOP", "NANO SHOP", "TELESISTEM"]
valor_proveedor = tk.StringVar(value=opciones_prov[0])

opciones_ram = ["4GB", "8GB", "16GB"]
valor_ram = tk.StringVar(value=opciones_ram[0])

opciones_alm = ["64GB", "128GB", "256GB"]
valor_almacenamiento = tk.StringVar(value=opciones_alm[0])

tk.Label(frame_form, text="Fecha").grid(row=0, column=0, padx=5, pady=5)
entry_fecha = tk.Entry(frame_form)
entry_fecha.grid(row=0, column=1)
entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))

tk.Label(frame_form, text="Proveedor").grid(row=0, column=2)
tk.OptionMenu(frame_form, valor_proveedor, *opciones_prov).grid(row=0, column=3)

tk.Label(frame_form, text="IMEI").grid(row=1, column=0)
entry_imei = tk.Entry(frame_form)
entry_imei.grid(row=1, column=1)

tk.Label(frame_form, text="Modelo").grid(row=1, column=2)
entry_modelo = tk.Entry(frame_form)
entry_modelo.grid(row=1, column=3)

tk.Label(frame_form, text="Precio").grid(row=2, column=0)
entry_precio_c = tk.Entry(frame_form)
entry_precio_c.grid(row=2, column=1)

tk.Label(frame_form, text="RAM").grid(row=2, column=2)
tk.OptionMenu(frame_form, valor_ram, *opciones_ram).grid(row=2, column=3)

tk.Label(frame_form, text="Almacenamiento").grid(row=3, column=0)
tk.OptionMenu(frame_form, valor_almacenamiento, *opciones_alm).grid(row=3, column=1)

ttk.Button(frame_inventario, text="REGISTRAR EQUIPO", command=guardar_producto).pack(pady=10)

frame_tabla = tk.Frame(frame_inventario)
frame_tabla.pack(padx=30, fill="both", expand=True)

columnas = ("ID", "FECHA", "PROVEEDOR", "IMEI", "MODELO", "PRECIO", "RAM", "ALM", "ESTATUS")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, anchor="center", width=120)

scroll = ttk.Scrollbar(frame_tabla, command=tabla.yview)
tabla.configure(yscroll=scroll.set)

tabla.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

# ---------------- VENTAS ---------------- #

tk.Label(frame_ventas, text="Módulo de Ventas",
         font=("Segoe UI", 20)).pack(pady=20)

# ---------------- START ---------------- #

mostrar_productos()
mostrar_frame(frame_menu)
activar_boton(btn_inicio, ind_inicio)

ventana.mainloop()