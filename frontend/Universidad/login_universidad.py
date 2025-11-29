# frontend_universidad/login_universidad.py

import tkinter as tk
from tkinter import messagebox
from menu_admin import MenuAdmin

class LoginUniversidad:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Universidad")
        self.root.geometry("350x220")

        tk.Label(self.root, text="Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack()

        tk.Label(self.root, text="Contraseña:").pack(pady=5)
        self.entry_pass = tk.Entry(self.root, show="*")
        self.entry_pass.pack()

        tk.Button(self.root, text="Ingresar", command=self.validar_login).pack(pady=15)

        self.root.mainloop()

    def validar_login(self):
        usuario = self.entry_user.get()
        clave = self.entry_pass.get()

        # 🔵 Temporal mientras conectas Supabase
        if usuario == "admin" and clave == "1234":
            messagebox.showinfo("Éxito", "Bienvenido")
            self.root.destroy()
            MenuAdmin()  # Abre el menú principal
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")


if __name__ == "__main__":
    LoginUniversidad()
