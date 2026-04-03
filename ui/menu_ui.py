import tkinter as tk

FONT = "Ubuntu"

def crear_frame_menu(parent):
    frame = tk.Frame(parent, bg="#f8fafc")

    contenedor = tk.Frame(frame, bg="#f8fafc")
    contenedor.pack(fill="both", expand=True)

    # ---------------- HEADER PRINCIPAL ---------------- #

    contenido = tk.Frame(contenedor, bg="#f8fafc")
    contenido.place(relx=0.5, rely=0.35, anchor="center")

    # TITULO GRANDE
    tk.Label(
        contenido,
        text="CREDICELL & PAMICELL",
        font=(FONT, 48, "bold"),
        bg="#f8fafc",
        fg="#0f172a"
    ).pack()

    # SUBTITULO
    tk.Label(
        contenido,
        text="Sistema Integral de Ventas e Inventario",
        font=(FONT, 15),
        bg="#f8fafc",
        fg="#64748b"
    ).pack(pady=(10, 5))

    # DESCRIPCION
    tk.Label(
        contenido,
        text="Administra equipos, controla inventario y gestiona ventas de manera eficiente.",
        font=(FONT, 11),
        bg="#f8fafc",
        fg="#94a3b8"
    ).pack()

    # LINEA DECORATIVA
    tk.Frame(
        contenedor,
        bg="#1f2022",
        height=3,
        width=250
    ).place(relx=0.5, rely=0.50, anchor="center")

    # ---------------- SECCION ACCESOS ---------------- #

    seccion = tk.Frame(contenedor, bg="#f8fafc")
    seccion.place(relx=0.5, rely=0.68, anchor="center")

    tk.Label(
        seccion,
        text="Módulos del sistema",
        font=(FONT, 16, "bold"),
        bg="#f8fafc",
        fg="#0f172a"
    ).pack(pady=(0, 20))

    # ---------------- CARDS ---------------- #

    cont_cards = tk.Frame(seccion, bg="#f8fafc")
    cont_cards.pack()

    def card(parent, titulo, desc, color):
        c = tk.Frame(
            parent,
            bg="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#e5e7eb"
        )
        c.pack(side="left", padx=20, ipadx=25, ipady=20)

        # BARRA DE COLOR SUPERIOR
        barra = tk.Frame(c, bg=color, height=4)
        barra.pack(fill="x", side="top")

        cont = tk.Frame(c, bg="white")
        cont.pack(pady=15)

        tk.Label(
            cont,
            text=titulo,
            font=(FONT, 14, "bold"),
            bg="white",
            fg="#0f172a"
        ).pack(pady=(5, 5))

        tk.Label(
            cont,
            text=desc,
            font=(FONT, 10),
            bg="white",
            fg="#64748b",
            wraplength=200,
            justify="center"
        ).pack()

        # HOVER
        def enter(e):
            c.config(bg="#f1f5f9")

        def leave(e):
            c.config(bg="white")

        c.bind("<Enter>", enter)
        c.bind("<Leave>", leave)

        return c

    # CARDS CON COLOR
    card(
        cont_cards,
        "Inventario",
        "Gestiona equipos, controla stock y registra dispositivos.",
        "#2563eb"
    )

    card(
        cont_cards,
        "Ventas",
        "Administra ventas, créditos y movimientos.",
        "#16a34a"
    )

    card(
        cont_cards,
        "Control",
        "Supervisa disponibilidad y estado del sistema.",
        "#f59e0b"
    )

    return frame