import tkinter as tk
from tkinter import ttk, messagebox
from services.seguridad_service import validar_password, actualizar_password

FONT = "Ubuntu"

def crear_frame_seguridad(parent, callback_bloqueo):
    frame = tk.Frame(parent, bg="#f8fafc")
    intentos_fallidos = 0 # Contador local para bloqueo por intentos

    # Header (Igual al que ya tienes)
    header = tk.Frame(frame, bg="#1f2022", height=70)
    header.pack(fill="x")
    tk.Label(header, text="Módulo de Seguridad", bg="#1f2022", fg="white", font=(FONT, 18, "bold")).pack(expand=True)

    cuerpo = tk.Frame(frame, bg="#f8fafc")
    cuerpo.pack(fill="both", expand=True, padx=24, pady=24)

    card = tk.Frame(cuerpo, bg="white", bd=1, relief="solid")
    card.place(relx=0.5, rely=0.4, anchor="center", width=550, height=520)

    tk.Label(card, text="Configuración de Acceso", bg="white", fg="#0f172a", font=(FONT, 14, "bold")).pack(pady=(20, 10))

    # --- Función para crear campos con "Ojo" e Iconos ---
    def crear_campo(label_text, icon):
        container = tk.Frame(card, bg="white")
        container.pack(fill="x", padx=50, pady=5)
        
        tk.Label(container, text=f"{icon} {label_text}", bg="white", fg="#334155", font=(FONT, 10, "bold")).pack(anchor="w")
        
        entry_frame = tk.Frame(container, bg="white")
        entry_frame.pack(fill="x")
        
        entry = ttk.Entry(entry_frame, show="*", font=(FONT, 12))
        entry.pack(side="left", fill="x", expand=True)
        
        def toggle_reveal():
            if entry.cget("show") == "*":
                entry.config(show="")
                btn_eye.config(text="👁️")
            else:
                entry.config(show="*")
                btn_eye.config(text="🕶️")

        btn_eye = tk.Button(entry_frame, text="🕶️", font=(FONT, 10), command=toggle_reveal, relief="flat", bg="white", cursor="hand2")
        btn_eye.pack(side="right", padx=5)
        
        return entry

    entry_actual = crear_campo("Contraseña Actual:", "")
    entry_nueva = crear_campo("Nueva Contraseña:", "")
    
    # --- Indicador de Fortaleza ---
    strength_frame = tk.Frame(card, bg="#e2e8f0", height=5)
    strength_frame.pack(fill="x", padx=50, pady=(0, 10))
    strength_bar = tk.Frame(strength_frame, bg="#e2e8f0", width=0, height=5)
    strength_bar.pack(side="left")

    def verificar_fortaleza(event):
        pwd = entry_nueva.get()
        if len(pwd) == 0: color, width = "#e2e8f0", 0
        elif len(pwd) < 5: color, width = "#ef4444", 130 # Rojo
        elif len(pwd) < 8: color, width = "#f59e0b", 260 # Naranja
        else: color, width = "#22c55e", 450 # Verde
        strength_bar.config(bg=color, width=width)

    entry_nueva.bind("<KeyRelease>", verificar_fortaleza)

    entry_confirmar = crear_campo("Confirmar Nueva:", "")
    
    # --- Feedback Visual (Label de error invisible) ---
    lbl_feedback = tk.Label(card, text="", bg="white", fg="#ef4444", font=(FONT, 9, "bold"))
    lbl_feedback.pack(pady=5)

    def ejecutar_cambio():
        nonlocal intentos_fallidos
        lbl_feedback.config(text="") # Limpiar error previo
        
        actual = entry_actual.get()
        nueva = entry_nueva.get()
        confirmar = entry_confirmar.get()

        if not actual or not nueva or not confirmar:
            lbl_feedback.config(text="Todos los campos son obligatorios")
            return

        if validar_password(actual):
            intentos_fallidos = 0 # Resetear si acierta
            if nueva == confirmar:
                if actualizar_password(nueva):
                    messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
                    for e in [entry_actual, entry_nueva, entry_confirmar]: e.delete(0, tk.END)
                else:
                    lbl_feedback.config(text="Error al guardar en base de datos")
            else:
                lbl_feedback.config(text="Las nuevas contraseñas no coinciden")
        else:
            intentos_fallidos += 1
            if intentos_fallidos >= 3:
                messagebox.showerror("Seguridad", "Demasiados intentos fallidos. Sesión cerrada.")
                callback_bloqueo() # Llamamos al cierre de sesión de app.py
            else:
                lbl_feedback.config(text=f"Contraseña actual incorrecta ({intentos_fallidos}/3)")

    tk.Button(card, text="Actualizar Contraseña", bg="#2563eb", fg="white", font=(FONT, 11, "bold"),
              relief="flat", padx=20, pady=12, cursor="hand2", command=ejecutar_cambio).pack(pady=20)

    return frame