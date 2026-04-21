import tkinter as tk
from tkinter import ttk, messagebox
from services.seguridad_service import validar_password, actualizar_password

FONT = "Ubuntu"

def crear_frame_seguridad(parent, callback_bloqueo):
    # El frame principal debe expandirse para llenar todo el 'contenido' de app.py
    frame = tk.Frame(parent, bg="#f8fafc")
    
    # --- HEADER ---
    header = tk.Frame(frame, bg="#1f2022", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Configuracion",
        bg="#1f2022",
        fg="white",
        font=("Ubuntu", 18, "bold")
    ).pack(expand=True)

    # --- CONTENEDOR CENTRAL (MAESTRO) ---
    contenedor_maestro = tk.Frame(frame, bg="white", bd=1, relief="solid")
    contenedor_maestro.pack(expand=True, fill="both", padx=100, pady=50)

    # 1. Sidebar Interno
    nav_interna = tk.Frame(contenedor_maestro, bg="#f1f5f9", width=250)
    nav_interna.pack(side="left", fill="y")
    nav_interna.pack_propagate(False)

    # 2. Área de Formulario
    area_contenido = tk.Frame(contenedor_maestro, bg="white")
    area_contenido.pack(side="right", fill="both", expand=True)

    # Botón de Seguridad en el menú interno
    btn_seguridad = tk.Button(nav_interna, text="Seguridad", font=(FONT, 12, "bold"), 
                             bg="#e2e8f0", fg="#1e293b", relief="flat", anchor="w", padx=25)
    btn_seguridad.pack(fill="x", pady=20)

    # --- DISEÑO DEL FORMULARIO DE SEGURIDAD ---
    intentos_fallidos = 0
    
    form_container = tk.Frame(area_contenido, bg="white")
    form_container.pack(expand=True) # Esto centra el formulario vertical y horizontalmente

    tk.Label(form_container, text="Cambiar Contraseña del Sistema", bg="white", 
             fg="#0f172a", font=(FONT, 16, "bold")).pack(pady=(0, 30))

    def crear_campo(label_text):
        f = tk.Frame(form_container, bg="white")
        f.pack(fill="x", pady=10)
        
        tk.Label(f, text=label_text, bg="white", fg="#475569", font=(FONT, 10, "bold")).pack(anchor="w")
        
        e_frame = tk.Frame(f, bg="white")
        e_frame.pack(fill="x", pady=5)
        
        entry = ttk.Entry(e_frame, show="*", font=(FONT, 12), width=40)
        entry.pack(side="left", ipady=5)
        
        def toggle():
            entry.config(show="" if entry.cget("show") == "*" else "*")
            
        tk.Button(e_frame, text="🕶️", relief="flat", bg="white", command=toggle, 
                  cursor="hand2").pack(side="left", padx=5)
        return entry

    entry_actual = crear_campo("Contraseña Actual:")
    entry_nueva = crear_campo("Nueva Contraseña:")
    
    # Barra de fortaleza
    strength_frame = tk.Frame(form_container, bg="#e2e8f0", height=5)
    strength_frame.pack(fill="x", pady=5)
    strength_bar = tk.Frame(strength_frame, bg="#e2e8f0", width=0, height=5)
    strength_bar.pack(side="left")

    def checar_fortaleza(event):
        p = entry_nueva.get()
        color = "#ef4444" if len(p) < 5 else "#f59e0b" if len(p) < 8 else "#22c55e"
        ancho = min(len(p) * 35, 350)
        strength_bar.config(bg=color, width=ancho)

    entry_nueva.bind("<KeyRelease>", checar_fortaleza)
    entry_confirmar = crear_campo("Confirmar Nueva Contraseña:")
    
    lbl_feedback = tk.Label(form_container, text="", bg="white", fg="#ef4444", font=(FONT, 10))
    lbl_feedback.pack(pady=10)

    def guardar():
        nonlocal intentos_fallidos
        lbl_feedback.config(text="")
        
        if not entry_actual.get() or not entry_nueva.get():
            lbl_feedback.config(text="Completa todos los campos")
            return

        if validar_password(entry_actual.get()):
            if entry_nueva.get() == entry_confirmar.get():
                if actualizar_password(entry_nueva.get()):
                    messagebox.showinfo("Seguridad", "Contraseña actualizada. Por seguridad, el sistema se bloqueará para que ingreses con tu nueva clave.")
                    entry_actual.delete(0, tk.END)
                    entry_nueva.delete(0, tk.END)
                    entry_confirmar.delete(0, tk.END)

                    callback_bloqueo()
                else:
                    lbl_feedback.config(text="Error al conectar con la base de datos")
            else:
                lbl_feedback.config(text="Las nuevas contraseñas no coinciden")
        else:
            intentos_fallidos += 1
            if intentos_fallidos >= 3:
                messagebox.showerror("Seguridad", "Exceso de intentos. Bloqueando sistema.")
                callback_bloqueo()
            else:
                lbl_feedback.config(text=f"Contraseña incorrecta ({intentos_fallidos}/3)")

    tk.Button(form_container, text="Actualizar Contraseña", bg="#2563eb", fg="white", 
              font=(FONT, 11, "bold"), relief="flat", padx=30, pady=12, 
              command=guardar, cursor="hand2").pack(pady=20)

    return frame