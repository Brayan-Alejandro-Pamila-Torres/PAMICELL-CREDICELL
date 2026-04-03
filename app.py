import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from database import inicializar_db
from ui.menu_ui import crear_frame_menu
from ui.inventario_ui import crear_frame_inventario
from ui.ventas_ui import crear_frame_ventas

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

FONT = "Ubuntu"  # Puedes cambiar a "Inter" si la tienes

# ---------------- COLORES ---------------- #

COLOR_SIDEBAR = "#1f2022"
COLOR_SIDEBAR_HOVER = "#1f2022"
COLOR_SIDEBAR_ACTIVE = "#1f2022"
COLOR_ACCENT = "#ffffff"
COLOR_TEXT = "#e5e7eb"
COLOR_BG = "#f8fafc"

# ---------------- ESTILOS TTK ---------------- #

style = ttk.Style()
style.theme_use("clam")

# TREEVIEW
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

# ENTRY
style.configure(
    "TEntry",
    fieldbackground="white",
    foreground="#111827"
)

# COMBOBOX
style.configure(
    "TCombobox",
    fieldbackground="white",
    background="white",
    foreground="#111827"
)

# ---------------- LAYOUT ---------------- #

contenedor = tk.Frame(ventana, bg=COLOR_BG)
contenedor.pack(fill="both", expand=True)

contenedor.grid_rowconfigure(0, weight=1)
contenedor.grid_columnconfigure(1, weight=1)

# SIDEBAR MÁS ANCHO
sidebar = tk.Frame(contenedor, bg=COLOR_SIDEBAR, width=380)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)

contenido = tk.Frame(contenedor, bg=COLOR_BG)
contenido.grid(row=0, column=1, sticky="nsew")
contenido.grid_rowconfigure(0, weight=1)
contenido.grid_columnconfigure(0, weight=1)

# ---------------- FRAMES ---------------- #

frame_menu = crear_frame_menu(contenido)
frame_inv = crear_frame_inventario(contenido)
frame_ventas = crear_frame_ventas(contenido)

for f in (frame_menu, frame_inv, frame_ventas):
    f.grid(row=0, column=0, sticky="nsew")

def mostrar(frame):
    frame.tkraise()

    if hasattr(frame, "refrescar"):
        frame.refrescar()

# ---------------- SIDEBAR UI ---------------- #

header = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
header.pack(fill="x", pady=(25, 10), padx=20)

tk.Label(
    header,
    text="PAMICELL",
    bg=COLOR_SIDEBAR,
    fg=COLOR_ACCENT,
    font=(FONT, 24, "bold")
).pack(anchor="w")

tk.Label(
    header,
    text="Sistema de ventas",
    bg=COLOR_SIDEBAR,
    fg="#94a3b8",
    font=(FONT, 11)
).pack(anchor="w", pady=(5, 0))

tk.Frame(sidebar, height=1, bg="#1e293b").pack(fill="x", padx=20, pady=15)

# ---------------- BOTONES SIDEBAR ---------------- #

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
    cont.pack(fill="x")  # <- sin padding

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
    btn.pack(side="left", fill="both", expand=True)  # <- CLAVE

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

btn_inicio, ind1 = crear_boton("Inicio", lambda: mostrar(frame_menu))
btn_inv, ind2 = crear_boton("Inventario", lambda: mostrar(frame_inv))
btn_ventas, ind3 = crear_boton("Ventas", lambda: mostrar(frame_ventas))

# ---------------- INICIO ---------------- #

mostrar(frame_menu)
activar(btn_inicio, ind1)

ventana.mainloop()