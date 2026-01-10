import tkinter as tk
from tkinter import messagebox
import os
import json

# Archivos de estudiantes y profesores
FICHERO_ESTUDIANTES = "estudiantes.json"
FICHERO_PROFESORES = "profesores.json"

# Carga la lista de usuarios desde un archivo JSON
def cargar_usuarios(fichero):
    if not os.path.exists(fichero):
        return []
    with open(fichero, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []

# Valida si las credenciales corresponden a un usuario o admin registrado
def validar_credenciales(usuario, contraseña):
    for fichero in [FICHERO_ESTUDIANTES, FICHERO_PROFESORES]:
        usuarios = cargar_usuarios(fichero)
        for u in usuarios:
            cedula = u.get("cedula", "")
            correo = u.get("correo", "")
            passw = u.get("contraseña", "")
            if (usuario == cedula or usuario == correo) and contraseña == passw:
                return True
    return False

# Verifica si el usuario es profesor (de profesores.json)
def es_profesor(usuario):
    usuarios = cargar_usuarios(FICHERO_PROFESORES)
    for u in usuarios:
        if usuario == u.get("cedula", "") or usuario == u.get("correo", ""):
            return True
    return False

# Obtiene el objeto estudiante (dict) a partir del usuario (cédula o correo)
def obtener_estudiante(usuario):
    usuarios = cargar_usuarios(FICHERO_ESTUDIANTES)
    for u in usuarios:
        if usuario == u.get("cedula", "") or usuario == u.get("correo", ""):
            return u
    return None


# Obtiene el objeto profesor (dict) a partir del usuario (cédula o correo)
def obtener_profesor(usuario):
    usuarios = cargar_usuarios(FICHERO_PROFESORES)
    for u in usuarios:
        if usuario == u.get("cedula", "") or usuario == u.get("correo", ""):
            return u
    return None


# Abre la ventana para registrar un nuevo usuario
def abrir_ventana_registro():
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Crear Cuenta")
    ventana_registro.geometry("400x500")

    tk.Label(ventana_registro, text="Cédula o Correo:").pack(pady=5)
    entry_usuario_reg = tk.Entry(ventana_registro)
    entry_usuario_reg.pack()

    tk.Label(ventana_registro, text="Contraseña:").pack(pady=5)
    entry_pass = tk.Entry(ventana_registro, show="*")
    entry_pass.pack()

    # Lógica para registrar un nuevo estudiante
    def registrar():
        usuario = entry_usuario_reg.get().strip()
        contraseña = entry_pass.get().strip()

        if not usuario or not contraseña:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validar si es cédula (10 dígitos) o correo electrónico
        if usuario.isdigit() and len(usuario) == 10:
            cedula = usuario
            correo = f"{usuario}@user.com"
        elif "@" in usuario and "." in usuario:
            cedula = ""
            correo = usuario
        else:
            messagebox.showerror("Error", "Ingrese una cédula válida (10 dígitos) o un correo electrónico válido.")
            return

        usuarios = cargar_usuarios(FICHERO_ESTUDIANTES)
        for u in usuarios:
            if usuario == u.get("cedula", "") or usuario == u.get("correo", ""):
                messagebox.showerror("Error", "Ya existe una cuenta con ese usuario o correo.")
                return

        # Guarda el nuevo estudiante en el archivo JSON
        usuarios.append({"cedula": cedula, "correo": correo, "contraseña": contraseña})
        with open(FICHERO_ESTUDIANTES, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Éxito", "Cuenta creada correctamente.")
        ventana_registro.destroy()

    tk.Button(ventana_registro, text="Registrar", command=registrar).pack(pady=10)
    tk.Button(ventana_registro, text="Volver", command=ventana_registro.destroy, bg="#f08080").pack(pady=10)


