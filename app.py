import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar, crear_tabla

crear_tabla()

# ---------------- FUNCIONES ---------------- #

def mostrar_frame(frame):
    frame.tkraise()

def guardar_producto():

    try:
        nombre = entry_nombre.get()
        marca = entry_marca.get()
        modelo = entry_modelo.get()
        capacidad = entry_capacidad.get()
        color = entry_color.get()
        precio = float(entry_precio.get())
        stock = int(entry_stock.get())

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO productos
        (nombre, marca, modelo, capacidad, color, precio, stock)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (nombre, marca, modelo, capacidad, color, precio, stock))

        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Teléfono agregado al inventario")

        limpiar_campos()
        mostrar_productos()

    except:
        messagebox.showerror("Error", "Datos inválidos")


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

    entry_nombre.delete(0, tk.END)
    entry_marca.delete(0, tk.END)
    entry_modelo.delete(0, tk.END)
    entry_capacidad.delete(0, tk.END)
    entry_color.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)


# ---------------- VENTANA PRINCIPAL ---------------- #

ventana = tk.Tk()
ventana.title("Sistema Credicell & Pamicell")
ventana.geometry("850x600")

contenedor = tk.Frame(ventana)
contenedor.pack(fill="both", expand=True)

frame_menu = tk.Frame(contenedor)
frame_inventario = tk.Frame(contenedor)
frame_ventas = tk.Frame(contenedor)

for frame in (frame_menu, frame_inventario, frame_ventas):
    frame.grid(row=0, column=0, sticky="nsew")

# ---------------- MENU PRINCIPAL ---------------- #

titulo = tk.Label(
    frame_menu,
    text="Sistema Credicell & Pamicell",
    font=("Arial", 24)
)
titulo.pack(pady=50)

boton_inventario = tk.Button(
    frame_menu,
    text="INVENTARIO",
    font=("Arial", 16),
    width=20,
    height=2,
    command=lambda: mostrar_frame(frame_inventario)
)
boton_inventario.pack(pady=20)

boton_ventas = tk.Button(
    frame_menu,
    text="VENTAS",
    font=("Arial", 16),
    width=20,
    height=2,
    command=lambda: mostrar_frame(frame_ventas)
)
boton_ventas.pack(pady=20)

# ---------------- MODULO INVENTARIO ---------------- #

titulo_inv = tk.Label(
    frame_inventario,
    text="Control de Inventario",
    font=("Arial", 18)
)
titulo_inv.pack(pady=10)

frame_form = tk.LabelFrame(frame_inventario, text="Alta de Teléfono")
frame_form.pack(pady=10, padx=10, fill="x")

tk.Label(frame_form, text="Nombre").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(frame_form)
entry_nombre.grid(row=0, column=1)

tk.Label(frame_form, text="Marca").grid(row=1, column=0, padx=5, pady=5)
entry_marca = tk.Entry(frame_form)
entry_marca.grid(row=1, column=1)

tk.Label(frame_form, text="Modelo").grid(row=2, column=0, padx=5, pady=5)
entry_modelo = tk.Entry(frame_form)
entry_modelo.grid(row=2, column=1)

tk.Label(frame_form, text="Capacidad").grid(row=3, column=0, padx=5, pady=5)
entry_capacidad = tk.Entry(frame_form)
entry_capacidad.grid(row=3, column=1)

tk.Label(frame_form, text="Color").grid(row=4, column=0, padx=5, pady=5)
entry_color = tk.Entry(frame_form)
entry_color.grid(row=4, column=1)

tk.Label(frame_form, text="Precio contado").grid(row=5, column=0, padx=5, pady=5)
entry_precio = tk.Entry(frame_form)
entry_precio.grid(row=5, column=1)

tk.Label(frame_form, text="Stock").grid(row=6, column=0, padx=5, pady=5)
entry_stock = tk.Entry(frame_form)
entry_stock.grid(row=6, column=1)

boton_guardar = tk.Button(
    frame_inventario,
    text="Guardar teléfono",
    command=guardar_producto
)
boton_guardar.pack(pady=10)

# TABLA INVENTARIO

frame_tabla = tk.Frame(frame_inventario)
frame_tabla.pack(pady=10)

columnas = (
    "ID",
    "Nombre",
    "Marca",
    "Modelo",
    "Capacidad",
    "Color",
    "Precio",
    "Stock"
)

tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=90)

tabla.pack()

boton_menu = tk.Button(
    frame_inventario,
    text="Volver al menú",
    command=lambda: mostrar_frame(frame_menu)
)
boton_menu.pack(pady=10)

# ---------------- MODULO VENTAS ---------------- #

titulo_ventas = tk.Label(
    frame_ventas,
    text="Módulo de Ventas",
    font=("Arial", 18)
)
titulo_ventas.pack(pady=20)

texto = tk.Label(
    frame_ventas,
    text="Aquí irá el sistema de ventas a crédito",
    font=("Arial", 12)
)
texto.pack(pady=10)

boton_menu2 = tk.Button(
    frame_ventas,
    text="Volver al menú",
    command=lambda: mostrar_frame(frame_menu)
)
boton_menu2.pack(pady=20)

# ---------------- INICIO ---------------- #

mostrar_productos()
mostrar_frame(frame_menu)

ventana.mainloop()