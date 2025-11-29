# main.py
import tkinter as tk
from Universidad.vista_facultades import FacultadView

if __name__ == "__main__":
    root = tk.Tk()
    app = FacultadView(root)
    root.mainloop()
