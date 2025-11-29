# frontend_universidad/menu_admin.py

import tkinter as tk
from vista_carreras import VistaCarreras
from vista_facultades import VistaFacultades
from vista_periodos import VistaPeriodos
from vista_oferta_academica import VistaOferta

class MenuAdmin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Menú de Universidad")
        self.root.geometry("400x350")

        tk.Label(self.root, text="Panel de Administración", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="Gestionar Carreras", width=25,
                  command=VistaCarreras).pack(pady=10)

        tk.Button(self.root, text="Gestionar Facultades", width=25,
                  command=VistaFacultades).pack(pady=10)

        tk.Button(self.root, text="Gestionar Períodos", width=25,
                  command=VistaPeriodos).pack(pady=10)

        tk.Button(self.root, text="Oferta Académica", width=25,
                  command=VistaOferta).pack(pady=10)

        tk.Button(self.root, text="Salir", width=25,
                  command=self.root.destroy).pack(pady=10)

        self.root.mainloop()
