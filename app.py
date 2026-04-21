import tkinter as tk
from tkinter import ttk

from database import inicializar_db
from ui.menu_ui import crear_frame_menu
from ui.inventario_ui import crear_frame_inventario
from ui.ventas_ui import crear_frame_ventas
from tkinter import simpledialog
from services.seguridad_service import validar_password, actualizar_password
from ui.seguridad_ui import crear_frame_seguridad
from tkinter import ttk, messagebox

# Inicializar base de datos
inicializar_db()

# ---------------- VENTANA ---------------- #

ventana = tk.Tk()
ventana.title("CREDICELL & PAMICELL")
ventana.minsize(1200, 750)

try:
    ventana.state("zoomed")
except:
    ventana.attributes("-zoomed", True)

# ---------------- FUENTE ---------------- #

FONT = "Ubuntu"

# ---------------- COLORES ---------------- #

COLOR_SIDEBAR = "#1f2022"
COLOR_SIDEBAR_HOVER = "#2a2b2e"
COLOR_SIDEBAR_ACTIVE = "#2a2b2e"
COLOR_ACCENT = "#ffffff"
COLOR_TEXT = "#e5e7eb"
COLOR_BG = "#f8fafc"

# ---------------- ESTILOS ---------------- #

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="#111827",
    rowheight=30,
    fieldbackground="white",
    bordercolor="#e5e7eb"
)

style.configure(
    "Treeview.Heading",
    background="#0f172a",
    foreground="white",
    font=(FONT, 10, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#2563eb")],
    foreground=[("selected", "white")]
)

style.configure("TEntry", fieldbackground="white", foreground="#111827")
style.configure("TCombobox", fieldbackground="white", foreground="#111827")

# ---------------- LAYOUT ---------------- #

contenedor = tk.Frame(ventana, bg=COLOR_BG)
contenedor.pack(fill="both", expand=True)

contenedor.grid_rowconfigure(0, weight=1)
contenedor.grid_columnconfigure(1, weight=1)

sidebar = tk.Frame(contenedor, bg=COLOR_SIDEBAR, width=380)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)

contenido = tk.Frame(contenedor, bg=COLOR_BG)
contenido.grid(row=0, column=1, sticky="nsew")
contenido.grid_rowconfigure(0, weight=1)
contenido.grid_columnconfigure(0, weight=1)

# ---------------- LÓGICA DE ACCESO (LOGIN) ---------------- #
def intentar_acceso(event=None):
    # Ahora usamos la función del SERVICE (que ya tiene Hashing)
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
    
    # Crear el Frame de bloqueo que tapa todo
    frame_bloqueo = tk.Frame(ventana, bg=COLOR_SIDEBAR)
    frame_bloqueo.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Contenedor central del login
    login_card = tk.Frame(frame_bloqueo, bg=COLOR_SIDEBAR)
    login_card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(login_card, text="PAMICELL", bg=COLOR_SIDEBAR, fg="white", font=(FONT, 35, "bold")).pack(pady=10)
    tk.Label(login_card, text="Sistema Protegido", bg=COLOR_SIDEBAR, fg="#94a3b8", font=(FONT, 12)).pack(pady=(0, 20))

    # Campo de entrada
    entry_login = ttk.Entry(login_card, show="*", font=(FONT, 14), justify="center", width=25)
    entry_login.pack(pady=10, ipady=5)
    entry_login.focus_set()

    # Botón de entrada
    btn_entrar = tk.Button(
        login_card,
        text="DESBLOQUEAR SISTEMA",
        bg="#2563eb",
        fg="white",
        font=(FONT, 11, "bold"),
        relief="flat",
        padx=20,
        pady=10,
        cursor="hand2",
        command=intentar_acceso
    )
    btn_entrar.pack(pady=20, fill="x")
    entry_login.bind("<Return>", intentar_acceso)

# ---------------- LÓGICA DE INACTIVIDAD ---------------- #
TIEMPO_INACTIVIDAD = 600000 # 10 minutos en milisegundos
timer_id = None

def reset_inactividad(event=None):
    global timer_id
    
    # Cancelar el temporizador anterior si existe
    if timer_id:
        ventana.after_cancel(timer_id)
    
    # Verificar si el sistema ya está bloqueado para no acumular procesos
    try:
        # Intentamos ver si el frame de bloqueo existe y es visible
        if frame_bloqueo.winfo_exists():
            return
    except:
        pass
    
    # Iniciar un nuevo temporizador de 10 minutos
    timer_id = ventana.after(TIEMPO_INACTIVIDAD, mostrar_bloqueo)

# Vincular todos los eventos de interacción a la función de reinicio
ventana.bind_all("<Any-KeyPress>", reset_inactividad)
ventana.bind_all("<Motion>", reset_inactividad)
ventana.bind_all("<Button-1>", reset_inactividad)

# ---------------- FRAMES ---------------- #

frame_menu = crear_frame_menu(contenido)
frame_inv = crear_frame_inventario(contenido)
frame_ventas = crear_frame_ventas(contenido)
frame_seguridad = crear_frame_seguridad(contenido, mostrar_bloqueo)

for f in (frame_menu, frame_inv, frame_ventas, frame_seguridad):
    f.grid(row=0, column=0, sticky="nsew")

def mostrar(frame):
    frame.tkraise()
    if hasattr(frame, "refrescar"):
        frame.refrescar()

# ---------------- HEADER ---------------- #

header = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
header.pack(fill="x", pady=(25, 10), padx=20)

tk.Label(header, text="PAMICELL", bg=COLOR_SIDEBAR, fg=COLOR_ACCENT,
         font=(FONT, 24, "bold")).pack(anchor="w")

tk.Label(header, text="Sistema de ventas", bg=COLOR_SIDEBAR,
         fg="#94a3b8", font=(FONT, 11)).pack(anchor="w", pady=(5, 0))

tk.Frame(sidebar, height=1, bg="#1e293b").pack(fill="x", padx=20, pady=15)

# ---------------- BOTONES ---------------- #

botones = []
indicadores = []

def activar(btn, indicador):
    for b in botones:
        b.config(bg=COLOR_SIDEBAR, fg=COLOR_TEXT)
    for i in indicadores:
        i.config(bg=COLOR_SIDEBAR)

    btn.config(bg=COLOR_SIDEBAR_ACTIVE, fg="white")
    indicador.config(bg=COLOR_ACCENT)

def crear_boton(texto, comando):
    cont = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
    cont.pack(fill="x")

    indicador = tk.Frame(cont, width=5, bg=COLOR_SIDEBAR)
    indicador.pack(side="left", fill="y")

    btn = tk.Label(
        cont,
        text="   " + texto,
        bg=COLOR_SIDEBAR,
        fg=COLOR_TEXT,
        font=(FONT, 13, "bold"),
        anchor="w",
        padx=25,
        pady=16,
        cursor="hand2"
    )
    btn.pack(side="left", fill="both", expand=True)

    def enter(e):
        if btn["bg"] != COLOR_SIDEBAR_ACTIVE:
            btn.config(bg=COLOR_SIDEBAR_HOVER)

    def leave(e):
        if btn["bg"] != COLOR_SIDEBAR_ACTIVE:
            btn.config(bg=COLOR_SIDEBAR)

    def click(e):
        activar(btn, indicador)
        comando()

    btn.bind("<Enter>", enter)
    btn.bind("<Leave>", leave)
    btn.bind("<Button-1>", click)

    botones.append(btn)
    indicadores.append(indicador)

    return btn, indicador

def cerrar_sesion():
    mostrar_bloqueo()
    # Resetear visual de botones
    activar(btn_inicio, ind1)
    mostrar(frame_menu)


btn_inicio, ind1 = crear_boton("Inicio", lambda: mostrar(frame_menu))
btn_inv, ind2 = crear_boton("Inventario", lambda: mostrar(frame_inv))
btn_ventas, ind3 = crear_boton("Ventas", lambda: mostrar(frame_ventas))
btn_seguridad, ind4 = crear_boton("Configuracion", lambda: mostrar(frame_seguridad))

# --- ESPACIADOR ---
spacer = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
spacer.pack(fill="both", expand=True)

# --- BOTÓN CERRAR SESIÓN (Resaltado) ---
def cerrar_sesion():
    # Preguntar antes de salir
    respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas cerrar la sesión?")
    if respuesta: # Si dice que SÍ
        mostrar_bloqueo()
        activar(btn_inicio, ind1)
        mostrar(frame_menu)

cont_cerrar = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
cont_cerrar.pack(fill="x", side="bottom", pady=20) # 'side=bottom' asegura que esté abajo

btn_cerrar = tk.Label(
    cont_cerrar,
    text="   Cerrar Sesión",
    bg="#dc2626", # Un rojo elegante (Tailwind Red 600)
    fg="white",
    font=(FONT, 12, "bold"),
    anchor="w",
    padx=25,
    pady=12,
    cursor="hand2"
)
btn_cerrar.pack(fill="x", padx=20, pady=10)

# Eventos de hover para el botón resaltado
btn_cerrar.bind("<Enter>", lambda e: btn_cerrar.config(bg="#b91c1c")) # Rojo más oscuro
btn_cerrar.bind("<Leave>", lambda e: btn_cerrar.config(bg="#dc2626"))
btn_cerrar.bind("<Button-1>", lambda e: cerrar_sesion())

# ---------------- INICIO ---------------- #

mostrar(frame_menu)
activar(btn_inicio, ind1)

# Iniciar el rastreo de inactividad
reset_inactividad()

# Lanzar el bloqueo inicial
mostrar_bloqueo()

ventana.mainloop()