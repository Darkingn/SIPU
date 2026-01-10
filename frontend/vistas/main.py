import tkinter as tk
from inicio_sesion import iniciar_sesion, abrir_ventana_registro
from tkinter import messagebox

# Crear la ventana principal de inicio de sesión
ventana = tk.Tk()
ventana.title("Sistema de admisión - Inicio de Sesión")
ventana.geometry("400x500")

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

# La lógica de inicio de sesión se maneja en `inicio_sesion.py`
