# vistas/facultad_view.py

import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
from backend.controladores.facultad_controller import FacultadController

class FacultadView:

    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Facultades")

        # ------- CAMPOS -------
        tk.Label(root, text="Nombre:").grid(row=0, column=0)
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.grid(row=0, column=1)

        tk.Label(root, text="Descripción:").grid(row=1, column=0)
        self.entry_desc = tk.Entry(root)
        self.entry_desc.grid(row=1, column=1)

        # ------- BOTONES -------
        tk.Button(root, text="Crear Facultad", command=self.crear_facultad).grid(row=2, column=0, columnspan=2, pady=5)

        # ------- LISTADO -------
        self.lista = tk.Listbox(root, width=60)
        self.lista.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(root, text="Eliminar Seleccionada", command=self.eliminar_facultad).grid(row=4, column=0, columnspan=2)

        self.cargar_facultades()

    def cargar_facultades(self):
        self.lista.delete(0, tk.END)
        facultades = FacultadController.obtener_facultades()

        for f in facultades:
            self.lista.insert(tk.END, f"{f['id']} - {f['nombre']}")

    def crear_facultad(self):
        nombre = self.entry_nombre.get().strip()
        desc = self.entry_desc.get().strip()

        if not nombre:
            messagebox.showerror("Error", "Debe ingresar un nombre")
            return

        FacultadController.crear_facultad(nombre, desc)
        self.cargar_facultades()
        messagebox.showinfo("Éxito", "Facultad creada")

    def eliminar_facultad(self):
        seleccion = self.lista.get(tk.ACTIVE)

        if not seleccion:
            messagebox.showwarning("Error", "Seleccione una facultad")
            return

        id_fac = seleccion.split(" - ")[0]

        FacultadController.eliminar_facultad(id_fac)
        self.cargar_facultades()
        messagebox.showinfo("Eliminado", "Facultad eliminada")
