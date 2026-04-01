import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
from database import conectar, crear_tabla

# Inicializar la base de datos al arrancar el programa
crear_tabla()

# ---------------- FUNCIONES DE LÓGICA ---------------- #

def mostrar_frame(frame):
    frame.tkraise()

def guardar_producto():
    try:
        # Extraer datos de los campos de texto y del OptionMenu
        fecha = entry_fecha.get()
        prov = valor_proveedor.get()
        imei = entry_imei.get()
        mod = entry_modelo.get()
        precio_texto = entry_precio_c.get()
        ram = valor_ram.get()
        alm = valor_almacenamiento.get()
        
        # El estatus siempre es DISPONIBLE al dar de alta
        est = "DISPONIBLE"

        # Validación básica de campos obligatorios
        if not imei or not mod or not precio_texto:
            messagebox.showwarning("Atención", "IMEI, Modelo y Precio son obligatorios.")
            return

        #validar que el IMEI tenga 15 dígitos exactos
        if not imei.isdigit() or len(imei) != 15:
            messagebox.showwarning("Error", "El IMEI debe contener exactamente 15 dígitos numéricos.")
            return

        #verificar que el imei no exista ya en la base de datos
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM productos WHERE imei = ?", (imei,))
        existe = cursor.fetchone()[0]
        
        if existe > 0:
            conn.close()
            messagebox.showerror("Error", "este IMEI ya esta registrado")
            return
        precio = float(precio_texto)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos 
            (fecha, proveedor, imei, modelo, precio_compra, ram, almacenamiento, estatus) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (fecha, prov, imei, mod, precio, ram, alm, est))
        
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Equipo {mod} (IMEI: {imei}) guardado como DISPONIBLE.")
        limpiar_campos()
        mostrar_productos()

    except ValueError:
        messagebox.showerror("Error", "En 'Precio Compra' debe ingresar un número (ej: 2500 o 2500.50).")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

def mostrar_productos():
    # Limpiar la tabla antes de cargar los datos actualizados
    for fila in tabla.get_children():
        tabla.delete(fila)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    for producto in cursor.fetchall():
        tabla.insert("", tk.END, values=producto)
    conn.close()

def limpiar_campos():
    # Limpiar los Entry de texto
    entry_imei.delete(0, tk.END)
    entry_modelo.delete(0, tk.END)
    entry_precio_c.delete(0, tk.END)
    
    # Reiniciar fecha a la actual
    entry_fecha.delete(0, tk.END)
    entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))

# ---------------- INTERFAZ GRÁFICA (GUI) ---------------- #

ventana = tk.Tk()
ventana.title("CREDICELL & PAMICELL - Gestión de Inventario")
ventana.geometry("1100x800")

contenedor = tk.Frame(ventana)
contenedor.pack(fill="both", expand=True)

# Frames para las diferentes pantallas
frame_menu = tk.Frame(contenedor)
frame_inventario = tk.Frame(contenedor)
frame_ventas = tk.Frame(contenedor)

for frame in (frame_menu, frame_inventario, frame_ventas):
    frame.grid(row=0, column=0, sticky="nsew")

# --- MENÚ PRINCIPAL ---
try:
    img_logo = Image.open("logo.jpeg").resize((200, 200))
    logo = ImageTk.PhotoImage(img_logo)
    tk.Label(frame_menu, image=logo).pack(pady=20)
except:
    tk.Label(frame_menu, text="[Logo: logo.jpeg no encontrado]", fg="grey", font=("Arial", 12)).pack(pady=20)

tk.Label(frame_menu, text="CREDICELL & PAMICELL", font=("Arial", 28, "bold")).pack(pady=5)
tk.Label(frame_menu, text="Sistema Integral de Ventas e Inventario", font=("Arial", 14), fg="#555").pack(pady=5)

btn_estilo = {"font": ("Arial", 14), "width": 30, "height": 2, "cursor": "hand2"}
tk.Button(frame_menu, text="GESTIÓN DE INVENTARIO", bg="#007bff", fg="white", **btn_estilo, 
          command=lambda: mostrar_frame(frame_inventario)).pack(pady=15)
tk.Button(frame_menu, text="MÓDULO DE VENTAS", **btn_estilo, 
          command=lambda: mostrar_frame(frame_ventas)).pack(pady=15)

# --- MÓDULO INVENTARIO ---
tk.Label(frame_inventario, text="Control de Stock / Entradas", font=("Arial", 20, "bold")).pack(pady=10)

frame_form = tk.LabelFrame(frame_inventario, text="Datos del Equipo (Nuevo Ingreso)", padx=15, pady=15)
frame_form.pack(pady=10, padx=30, fill="x")

# Configuración de Proveedores (Lista Desplegable)
opciones_prov = ["GAMA PLUS", "SMART SHOP", "NANO SHOP", "TELESISTEM"]
valor_proveedor = tk.StringVar(ventana)
valor_proveedor.set(opciones_prov[0])

opciones_ram = ["4GB", "8GB", "16GB", "32GB", "64GB", "128GB", "256GB"]
valor_ram = tk.StringVar(ventana)
valor_ram.set(opciones_ram[0])

opciones_alm = ["32GB", "64GB", "128GB", "256GB", "512GB", "1TB"]
valor_almacenamiento = tk.StringVar(ventana)
valor_almacenamiento.set(opciones_alm[0])

# --- GRID DEL FORMULARIO ---
# Fila 0
tk.Label(frame_form, text="Fecha (DD/MM/AAAA):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_fecha = tk.Entry(frame_form, width=25)
entry_fecha.grid(row=0, column=1, padx=5, pady=5)
entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))

tk.Label(frame_form, text="Proveedor:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
menu_prov = tk.OptionMenu(frame_form, valor_proveedor, *opciones_prov)
menu_prov.config(width=21)
menu_prov.grid(row=0, column=3, padx=5, pady=5)

# Fila 1
tk.Label(frame_form, text="IMEI:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_imei = tk.Entry(frame_form, width=25)
entry_imei.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Modelo:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
entry_modelo = tk.Entry(frame_form, width=25)
entry_modelo.grid(row=1, column=3, padx=5, pady=5)

# Fila 2
tk.Label(frame_form, text="Precio Compra ($):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_precio_c = tk.Entry(frame_form, width=25)
entry_precio_c.grid(row=2, column=1, padx=5, pady=5)

menu_ram = tk.OptionMenu(frame_form, valor_ram, *opciones_ram)
menu_ram.config(width=21)
menu_ram.grid(row=2, column=3, padx=5, pady=5)
tk.Label(frame_form, text="RAM:").grid(row=2, column=2, sticky="e", padx=5, pady=5)


# Fila 3
menu_alm = tk.OptionMenu(frame_form, valor_almacenamiento, *opciones_alm)
menu_alm.config(width=21)
menu_alm.grid(row=3, column=1, padx=5, pady=5)
tk.Label(frame_form, text="Almacenamiento:").grid(row=3, column=0, sticky="e", padx=5, pady=5)

# Botón Guardar
tk.Button(frame_inventario, text="REGISTRAR EQUIPO", bg="#28a745", fg="white", font=("Arial", 12, "bold"), 
          width=30, command=guardar_producto).pack(pady=10)

# --- TABLA DE INVENTARIO ---
frame_tabla = tk.Frame(frame_inventario)
frame_tabla.pack(pady=10, padx=30, fill="both", expand=True)

columnas_tabla = ("ID", "FECHA", "PROVEEDOR", "IMEI", "MODELO", "PRECIO COMPRA", "RAM", "INTERNO", "ESTATUS")
tabla = ttk.Treeview(frame_tabla, columns=columnas_tabla, show="headings")

for col in columnas_tabla:
    tabla.heading(col, text=col)
    tabla.column(col, width=105, anchor="center")

# Barra de desplazamiento
scroll_v = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scroll_v.set)
tabla.pack(side="left", fill="both", expand=True)
scroll_v.pack(side="right", fill="y")

tk.Button(frame_inventario, text="VOLVER AL MENÚ PRINCIPAL", font=("Arial", 10), command=lambda: mostrar_frame(frame_menu)).pack(pady=10)

# --- MÓDULO VENTAS (A DESARROLLAR) ---
tk.Label(frame_ventas, text="Módulo de Ventas y Créditos", font=("Arial", 20, "bold")).pack(pady=20)
tk.Label(frame_ventas, text="Aquí se gestionarán los abonos de los clientes de CREDICELL.", font=("Arial", 12)).pack()
tk.Button(frame_ventas, text="REGRESAR", command=lambda: mostrar_frame(frame_menu)).pack(pady=50)

# ---------------- ARRANQUE ---------------- #

mostrar_productos()
mostrar_frame(frame_menu)
ventana.mainloop()