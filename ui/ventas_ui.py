import tkinter as tk

def crear_frame_ventas(parent):
    frame = tk.Frame(parent, bg="#f8fafc")

    header = tk.Frame(frame, bg="#1f2022", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Módulo de Ventas",
        bg="#1f2022",
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(expand=True)

    cuerpo = tk.Frame(frame, bg="#f8fafc")
    cuerpo.pack(fill="both", expand=True, padx=30, pady=30)

    tarjeta = tk.Frame(cuerpo, bg="white", bd=1, relief="solid")
    tarjeta.pack(fill="both", expand=True)

    tk.Label(
        tarjeta,
        text="Aquí se integrará la gestión de ventas y créditos.",
        bg="white",
        fg="#475569",
        font=("Segoe UI", 13)
    ).pack(pady=40)

    return frame