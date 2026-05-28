import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

from database import inicializar_db
from ui.menu_ui import crear_frame_menu
from ui.inventario_ui import crear_frame_inventario
from ui.ventas_ui import crear_frame_ventas
from ui.seguridad_ui import crear_frame_seguridad
from ui.datos_ui import crear_frame_datos  
from services.seguridad_service import validar_password
from ui.reportes_ui import crear_frame_reportes 

# ---------------- SOPORTE PARA EMPAQUETADO MULTIPLATAFORMA ---------------- #
def resolver_ruta(ruta_relativa):
    """ 
    Obtiene la ruta absoluta para los recursos del sistema.
    Funciona de forma transparente tanto en Linux Mint como en Windows.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath("."), ruta_relativa)

# Inicializar base de datos MySQL en Docker
inicializar_db()

# ---------------- VENTANA PRINCIPAL ---------------- #
ventana = tk.Tk()
ventana.title("CREDICELL & PAMICELL")
ventana.minsize(1200, 750)

# Carga del ícono usando el resolvedor de rutas multiplataforma
try:
    ruta_icono = resolver_ruta("logo3.png")
    mi_icono = tk.PhotoImage(file=ruta_icono)
    ventana.iconphoto(False, mi_icono)
except Exception as e:
    print(f"Advertencia: No se pudo cargar el ícono: {e}")

# Forzar el maximizado nativo adaptativo
def forzar_pantalla_completa():
    try:
        ventana.attributes("-zoomed", True)  # Maximizado para servidores X11/Linux
    except:
        try:
            ventana.state("zoomed")          # Respaldo para entornos Windows
        except:
            pass

# Ejecuta el maximizado 100 milisegundos después de arrancar
ventana.after(100, forzar_pantalla_completa)

FONT = "Ubuntu"

# ---------------- COLORES DE LA APP ---------------- #
COLOR_SIDEBAR = "#1f2022"
COLOR_SIDEBAR_HOVER = "#2a2b2e"
COLOR_SIDEBAR_ACTIVE = "#2a2b2e"
COLOR_ACCENT = "#ffffff"
COLOR_TEXT = "#e5e7eb"
COLOR_BG = "#f8fafc"

# Estilos globales de componentes (TTK)
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", foreground="#111827", rowheight=30, fieldbackground="white", bordercolor="#e5e7eb")
style.configure("Treeview.Heading", background="#0f172a", foreground="white", font=(FONT, 10, "bold"))
style.map("Treeview", background=[("selected", "#2563eb")], foreground=[("selected", "white")])
style.configure("TEntry", fieldbackground="white", foreground="#111827")
style.configure("TCombobox", fieldbackground="white", foreground="#111827")

# ---------------- LAYOUT GLOBAL ---------------- #
contenedor = tk.Frame(ventana, bg=COLOR_BG)
contenedor.pack(fill="both", expand=True)
contenedor.grid_rowconfigure(0, weight=1)
contenedor.grid_columnconfigure(1, weight=1)

sidebar = tk.Frame(contenedor, bg=COLOR_SIDEBAR, width=280)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)

contenido = tk.Frame(contenedor, bg=COLOR_BG)
contenido.grid(row=0, column=1, sticky="nsew")
contenido.grid_rowconfigure(0, weight=1)
contenido.grid_columnconfigure(0, weight=1)

# ---------------- CONTROL ACCESO (LOGIN) ---------------- #
def intentar_acceso(event=None):
    pwd = entry_login.get()
    if validar_password(pwd):
        frame_bloqueo.destroy() 
    else:
        messagebox.showerror("Error", "Contraseña incorrecta")
        entry_login.delete(0, tk.END)

def mostrar_bloqueo():
    global frame_bloqueo, entry_login, timer_id
    if timer_id:
        ventana.after_cancel(timer_id)
        timer_id = None
    
    frame_bloqueo = tk.Frame(ventana, bg=COLOR_SIDEBAR)
    frame_bloqueo.place(relx=0, rely=0, relwidth=1, relheight=1)

    login_card = tk.Frame(frame_bloqueo, bg=COLOR_SIDEBAR)
    login_card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(login_card, text="PAMICELL", bg=COLOR_SIDEBAR, fg="white", font=(FONT, 35, "bold")).pack(pady=10)
    tk.Label(login_card, text="Sistema Protegido", bg=COLOR_SIDEBAR, fg="#94a3b8", font=(FONT, 12)).pack(pady=(0, 20))

    entry_login = ttk.Entry(login_card, show="*", font=(FONT, 14), justify="center", width=25)
    entry_login.pack(pady=10, ipady=5)
    entry_login.focus_set()

    btn_entrar = tk.Button(login_card, text="DESBLOQUEAR SISTEMA", bg="#2563eb", fg="white", font=(FONT, 11, "bold"), relief="flat", padx=20, pady=10, cursor="hand2", command=intentar_acceso)
    btn_entrar.pack(pady=20, fill="x")
    entry_login.bind("<Return>", intentar_acceso)

# ---------------- DETECCIÓN INACTIVIDAD ---------------- #
TIEMPO_INACTIVIDAD = 600000 
timer_id = None

def reset_inactividad(event=None):
    global timer_id
    if timer_id:
        ventana.after_cancel(timer_id)
    try:
        if frame_bloqueo.winfo_exists(): return
    except: pass
    timer_id = ventana.after(TIEMPO_INACTIVIDAD, mostrar_bloqueo)

ventana.bind_all("<Any-KeyPress>", reset_inactividad)
ventana.bind_all("<Motion>", reset_inactividad)
ventana.bind_all("<Button-1>", reset_inactividad)

# ---------------- CARGA DINÁMICA DE VISTAS ---------------- #
def mostrar(frame):
    frame.tkraise()
    if hasattr(frame, "refrescar"):
        frame.refrescar()

frame_menu = crear_frame_menu(contenido)
frame_ventas = crear_frame_ventas(contenido)

def ir_a_tabla_datos():
    mostrar(frame_datos)
    activar(btn_datos, ind_datos)

frame_inv = crear_frame_inventario(contenido, ir_a_tabla_datos)

def recargar_combo_ventas_externo():
    if hasattr(frame_ventas, "refrescar"):
        frame_ventas.refrescar()

frame_datos = crear_frame_datos(contenido, recargar_combo_ventas_externo)
frame_seguridad = crear_frame_seguridad(contenido, mostrar_bloqueo)
frame_reportes = crear_frame_reportes(contenido)

for f in (frame_menu, frame_inv, frame_ventas, frame_datos, frame_reportes, frame_seguridad):
    f.grid(row=0, column=0, sticky="nsew")

# ---------------- CONSTRUCCIÓN SIDEBAR MENÚ ---------------- #
header = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
header.pack(fill="x", pady=(25, 10), padx=20)

tk.Label(header, text="PAMICELL", bg=COLOR_SIDEBAR, fg=COLOR_ACCENT, font=(FONT, 24, "bold")).pack(anchor="w")
tk.Label(header, text="Sistema de ventas", bg=COLOR_SIDEBAR, fg="#94a3b8", font=(FONT, 11)).pack(anchor="w", pady=(5, 0))
tk.Frame(sidebar, height=1, bg="#1e293b").pack(fill="x", padx=20, pady=15)

botones = []
indicadores = []

def activar(btn, indicador):
    for b in botones: 
        b.config(bg=COLOR_SIDEBAR, fg=COLOR_TEXT)
    for ind in indicadores: 
        ind.config(bg=COLOR_SIDEBAR)
    btn.config(bg=COLOR_SIDEBAR_ACTIVE, fg="white")
    indicador.config(bg=COLOR_ACCENT)

def crear_boton(texto, comando):
    cont = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
    cont.pack(fill="x")
    indicador = tk.Frame(cont, width=5, bg=COLOR_SIDEBAR)
    indicador.pack(side="left", fill="y")

    btn = tk.Label(cont, text="   " + texto, bg=COLOR_SIDEBAR, fg=COLOR_TEXT, font=(FONT, 13, "bold"), anchor="w", padx=25, pady=14, cursor="hand2")
    btn.pack(side="left", fill="both", expand=True)

    btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_SIDEBAR_HOVER) if btn["bg"] != COLOR_SIDEBAR_ACTIVE else None)
    btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_SIDEBAR) if btn["bg"] != COLOR_SIDEBAR_ACTIVE else None)
    btn.bind("<Button-1>", lambda e: (activar(btn, indicador), comando()))

    botones.append(btn)
    indicadores.append(indicador)
    return btn, indicador

# Instanciar botones del menú lateral izquierdo
btn_inicio, ind1 = crear_boton("Inicio", lambda: mostrar(frame_menu))
btn_inv, ind2 = crear_boton("Registrar Inventario", lambda: mostrar(frame_inv))
btn_ventas, ind3 = crear_boton("Nueva Venta", lambda: mostrar(frame_ventas))
btn_datos, ind_datos = crear_boton("Administrar Datos", lambda: mostrar(frame_datos))
btn_reportes, ind_reportes = crear_boton("Reportes Relacionales", lambda: mostrar(frame_reportes)) 
btn_seguridad, ind4 = crear_boton("Configuración", lambda: mostrar(frame_seguridad))

# --- ESPACIADOR DINÁMICO ---
spacer = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
spacer.pack(fill="both", expand=True)

# --- BOTÓN CERRAR SESIÓN ---
def cerrar_sesion():
    if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas cerrar la sesión?"):
        mostrar_bloqueo()
        activar(btn_inicio, ind1)
        mostrar(frame_menu)

cont_cerrar = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
cont_cerrar.pack(fill="x", side="bottom", pady=20)

btn_cerrar = tk.Label(cont_cerrar, text="   Cerrar Sesión", bg="#dc2626", fg="white", font=(FONT, 12, "bold"), anchor="w", padx=25, pady=12, cursor="hand2")
btn_cerrar.pack(fill="x", padx=20, pady=10)
btn_cerrar.bind("<Enter>", lambda e: btn_cerrar.config(bg="#b91c1c"))
btn_cerrar.bind("<Leave>", lambda e: btn_cerrar.config(bg="#dc2626"))
btn_cerrar.bind("<Button-1>", lambda e: cerrar_sesion())

# Arranque por defecto
if __name__ == "__main__":
    mostrar(frame_menu)
    activar(btn_inicio, ind1)
    reset_inactividad()
    mostrar_bloqueo()
    ventana.mainloop()