import tkinter as tk
from tkinter import messagebox
import os
import json

# Archivos de usuarios y administradores
FICHERO_USUARIOS = "usuarios.json"
FICHERO_ADMINISTRADORES = "administradores.json"
FICHERO_COPERATIVAS_ADMINS = "coperativas_admins.json"

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
    for fichero in [FICHERO_USUARIOS, FICHERO_ADMINISTRADORES]:
        usuarios = cargar_usuarios(fichero)
        for u in usuarios:
            cedula = u.get("cedula", "")
            correo = u.get("correo", "")
            passw = u.get("contraseña", "")
            if (usuario == cedula or usuario == correo) and contraseña == passw:
                return True
    return False

# Verifica si el usuario es administrador (de administradores.json)
def es_admin(usuario):
    usuarios = cargar_usuarios(FICHERO_ADMINISTRADORES)
    for u in usuarios:
        if usuario == u.get("cedula", "") or usuario == u.get("correo", ""):
            return True
    return False

# Obtiene el objeto usuario (dict) a partir del usuario (cédula o correo)
def obtener_usuario(usuario):
    usuarios = cargar_usuarios(FICHERO_USUARIOS)
    for u in usuarios:
        if usuario == u.get("cedula", "") or usuario == u.get("correo", ""):
            return u
    return None

# Busca si el usuario y contraseña corresponden a un admin de cooperativa
def buscar_admin_cooperativa(usuario, contraseña):
    if not os.path.exists(FICHERO_COPERATIVAS_ADMINS):
        return None, None
    with open(FICHERO_COPERATIVAS_ADMINS, "r", encoding="utf-8") as f:
        data = json.load(f)
    for coop in data:
        for admin in coop.get("admins", []):
            if admin["usuario"] == usuario and admin["contraseña"] == contraseña:
                return admin, coop["cooperativa"]
    return None, None

# Lógica de inicio de sesión: verifica credenciales y abre la ventana correspondiente
def iniciar_sesion(entry_usuario, entry_contraseña, ventana):
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    # Super admin
    if usuario == "admin" and contraseña == "admin":
        from super_admin import ventana_super_admin
        ventana_super_admin(ventana)
        entry_usuario.delete(0, tk.END)
        entry_contraseña.delete(0, tk.END)
        return

    # Admin de cooperativa (creado por super admin)
    admin_obj, nombre_coop = buscar_admin_cooperativa(usuario, contraseña)
    if admin_obj and nombre_coop:
        from profesores import ventana_gestion_admin
        messagebox.showinfo("Bienvenido", f"Bienvenido administrador de {nombre_coop}")
        ventana.withdraw()
        ventana_gestion_admin(admin_obj, nombre_coop)
        entry_usuario.delete(0, tk.END)
        entry_contraseña.delete(0, tk.END)
        return

    # Admin o usuario normal (de los archivos tradicionales)
    if validar_credenciales(usuario, contraseña):
        if es_admin(usuario):
            from profesores import ventana_gestion_admin
            admin_obj = obtener_usuario(usuario)
            messagebox.showinfo("Bienvenido", "Bienvenido administrador")
            ventana.withdraw()
            ventana_gestion_admin(admin_obj, nombre_coop)
        else:
            from usuarios import ventana_principal_usuario
            usuario_obj = obtener_usuario(usuario)
            messagebox.showinfo("Éxito", f"Bienvenido usuario: {usuario_obj.get('cedula', usuario_obj.get('correo', ''))}")
            ventana.withdraw()
            ventana_principal_usuario(usuario_obj)
        entry_usuario.delete(0, tk.END)
        entry_contraseña.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

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

    # Lógica para registrar un nuevo usuario
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

        usuarios = cargar_usuarios(FICHERO_USUARIOS)
        for u in usuarios:
            if usuario == u.get("cedula", "") or usuario == u.get("correo", ""):
                messagebox.showerror("Error", "Ya existe una cuenta con ese usuario o correo.")
                return

        # Guarda el nuevo usuario en el archivo JSON
        usuarios.append({"cedula": cedula, "correo": correo, "contraseña": contraseña})
        with open(FICHERO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Éxito", "Cuenta creada correctamente.")
        ventana_registro.destroy()

    tk.Button(ventana_registro, text="Registrar", command=registrar).pack(pady=10)
    tk.Button(ventana_registro, text="Volver", command=ventana_registro.destroy, bg="#f08080").pack(pady=10)


