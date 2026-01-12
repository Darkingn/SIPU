import tkinter as tk
from tkinter import messagebox
import random
import string


def ventana_super_admin(parent):
    parent.withdraw()
    ventana = tk.Toplevel(parent)
    ventana.title("Super Admin - Crear Cuentas de Docentes")
    ventana.geometry("700x550")

    # --- UI ---
    tk.Label(ventana, text="Crear nueva cuenta de docente", font=("Arial", 14, "bold")).pack(pady=10)
    frame_form = tk.Frame(ventana)
    frame_form.pack(pady=5)

    # Campos: nombres, cedula, correo personal, carrera, titulo academico, rol
    tk.Label(frame_form, text="Nombres: ").grid(row=0, column=0, sticky="e", padx=5, pady=4)
    entry_nombres = tk.Entry(frame_form, width=40)
    entry_nombres.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(frame_form, text="Cédula: ").grid(row=1, column=0, sticky="e", padx=5, pady=4)
    entry_cedula = tk.Entry(frame_form, width=25)
    entry_cedula.grid(row=1, column=1, padx=5, pady=4, sticky="w")

    tk.Label(frame_form, text="Correo personal: ").grid(row=2, column=0, sticky="e", padx=5, pady=4)
    entry_correo = tk.Entry(frame_form, width=40)
    entry_correo.grid(row=2, column=1, padx=5, pady=4)

    tk.Label(frame_form, text="Carrera: ").grid(row=3, column=0, sticky="e", padx=5, pady=4)
    entry_carrera = tk.Entry(frame_form, width=30)
    entry_carrera.grid(row=3, column=1, padx=5, pady=4, sticky="w")

    tk.Label(frame_form, text="Título académico: ").grid(row=4, column=0, sticky="e", padx=5, pady=4)
    entry_titulo = tk.Entry(frame_form, width=40)
    entry_titulo.grid(row=4, column=1, padx=5, pady=4)

    tk.Label(frame_form, text="Rol: ").grid(row=5, column=0, sticky="e", padx=5, pady=4)
    entry_rol = tk.Entry(frame_form, width=30)
    entry_rol.grid(row=5, column=1, padx=5, pady=4, sticky="w")

    tk.Label(frame_form, text="").grid(row=6, column=0)  # espacio

    def generar_clave_temp(length=8):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def crear_docente():
        nombres = entry_nombres.get().strip()
        cedula = entry_cedula.get().strip()
        correo_personal = entry_correo.get().strip()
        carrera = entry_carrera.get().strip()
        titulo = entry_titulo.get().strip()
        rol = entry_rol.get().strip()

        if not (nombres and cedula and carrera and rol):
            messagebox.showerror("Error", "Complete al menos: nombres, cédula, carrera y rol.", parent=ventana)
            return
        if not cedula.isdigit():
            messagebox.showerror("Error", "La cédula debe contener solo dígitos.", parent=ventana)
            return

        correo_institucional = f"e{cedula}@universidad.edu.ec"
        contraseña_temp = generar_clave_temp()

        # Mostrar credenciales al usuario
        messagebox.showinfo(
            "Cuenta creada",
            f"Docente: {nombres}\nCorreo institucional: {correo_institucional}\nContraseña temporal: {contraseña_temp}",
            parent=ventana,
        )

        # Limpiar campos
        entry_nombres.delete(0, tk.END)
        entry_cedula.delete(0, tk.END)
        entry_correo.delete(0, tk.END)
        entry_carrera.delete(0, tk.END)
        entry_titulo.delete(0, tk.END)
        entry_rol.delete(0, tk.END)

    tk.Button(frame_form, text="Crear cuenta docente", command=crear_docente, bg="#d0f0c0").grid(row=7, column=0, columnspan=2, pady=12)

    # Botón para cerrar sesión y volver al login
    def cerrar_sesion():
        ventana.destroy()
        parent.deiconify()

    tk.Button(
        ventana,
        text="Cerrar sesión",
        bg="#f08080",
        font=("Arial", 11, "bold"),
        command=cerrar_sesion
    ).pack(pady=15, side="bottom")

