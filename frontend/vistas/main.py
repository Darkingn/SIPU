import tkinter as tk
from inicio_sesion import iniciar_sesion, abrir_ventana_registro, buscar_admin_cooperativa
from tkinter import messagebox

# Crear la ventana principal de inicio de sesión
ventana = tk.Tk()
ventana.title("Inicio de Sesión")
ventana.geometry("600x400")

# Etiqueta y campo para el usuario
tk.Label(ventana, text="Usuario:").pack(pady=5)
entry_usuario = tk.Entry(ventana)  
entry_usuario.pack()

# Etiqueta y campo para la contraseña
tk.Label(ventana, text="Contraseña:").pack(pady=5)
entry_contraseña = tk.Entry(ventana, show="*")
entry_contraseña.pack()

# Botón para iniciar sesión
tk.Button(
    ventana,
    text="Iniciar Sesión",
    command=lambda: iniciar_sesion(entry_usuario, entry_contraseña, ventana)
).pack(pady=10)

# Botón para abrir la ventana de registro de cuenta
tk.Button(ventana, text="Registrar Cuenta", command=abrir_ventana_registro).pack(pady=5)

# Inicia el bucle principal de la interfaz gráfica
ventana.mainloop()

def iniciar_sesion(entry_usuario, entry_contraseña, ventana):
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    if usuario == "admin" and contraseña == "admin":
        from super_admin import ventana_super_admin
        ventana_super_admin(ventana)
        entry_usuario.delete(0, tk.END)
        entry_contraseña.delete(0, tk.END)
        return

    # Buscar admin de cooperativa
    admin_obj, nombre_coop = buscar_admin_cooperativa(usuario, contraseña)
    if admin_obj and nombre_coop:
        from profesores import ventana_gestion_admin
        messagebox.showinfo("Bienvenido", f"Bienvenido administrador de {nombre_coop}")
        ventana.withdraw()
        ventana_gestion_admin(admin_obj, nombre_coop)
        entry_usuario.delete(0, tk.END)
        entry_contraseña.delete(0, tk.END)
        return

    # ...el resto de tu código para usuarios normales y otros admins...
