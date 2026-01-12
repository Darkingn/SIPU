import tkinter as tk
from tkinter import messagebox
import os
import json
import datetime
from profesores import cargar_coperativas

# Archivos de datos
FICHERO_GRAFO = "grafo_destinos.json"
FICHERO_BUSES = "buses.json"
FICHERO_ASIENTOS = "asientos_ocupados.json"
FICHERO_HISTORIAL = "compras_usuarios.json"

# Obtiene el usuario admin responsable de un bus
def obtener_usuario_admin(nombre_coperativa, destino, bus):
    if os.path.exists(FICHERO_BUSES):
        with open(FICHERO_BUSES, "r", encoding="utf-8") as f:
            buses = json.load(f)
        for b in buses:
            if (b.get("nombre_coperativa") == nombre_coperativa and
                b.get("destino") == destino and
                b.get("nombre_bus") == bus):
                return b.get("usuario_admin", "")
    return ""

# Guarda los asientos ocupados por un usuario para un bus específico
def guardar_asientos_ocupados(cooperativa, destino, bus, asientos):
    usuario_admin = obtener_usuario_admin(cooperativa, destino, bus)
    clave = f"{cooperativa}|{destino}|{bus}|{usuario_admin}"
    data = {}
    if os.path.exists(FICHERO_ASIENTOS):
        with open(FICHERO_ASIENTOS, "r", encoding="utf-8") as f:
            data = json.load(f)
    ocupados = set(data.get(clave, []))
    ocupados.update(asientos)
    data[clave] = list(ocupados)
    with open(FICHERO_ASIENTOS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Guarda el historial de compras por usuario
def guardar_historial_usuario(usuario, cooperativa, destino, bus, asientos, monto, fecha):
    compra = {
        "usuario": usuario,
        "cooperativa": cooperativa,
        "destino": destino,
        "bus": bus,
        "asientos": list(asientos),
        "monto": monto,
        "fecha": fecha
    }
    data = []
    if os.path.exists(FICHERO_HISTORIAL):
        with open(FICHERO_HISTORIAL, "r", encoding="utf-8") as f:
            data = json.load(f)
    data.append(compra)
    with open(FICHERO_HISTORIAL, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Carga los asientos ocupados para un bus específico
def cargar_asientos_ocupados(cooperativa, destino, bus):
    usuario_admin = obtener_usuario_admin(cooperativa, destino, bus)
    clave = f"{cooperativa}|{destino}|{bus}|{usuario_admin}"
    if os.path.exists(FICHERO_ASIENTOS):
        with open(FICHERO_ASIENTOS, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get(clave, []))
    return set()

# Ventana principal para el usuario
def ventana_principal_usuario(usuario_obj):
    win = tk.Toplevel()
    win.title("Boletería")
    win.geometry("800x520")
    win.resizable(False, False)

    # Diccionario para guardar la selección actual del usuario
    seleccion = {"cooperativa": None, "destino": None, "bus": None, "asientos": set()}

    # Panel lateral con navegación y datos del usuario
    frame_lateral = tk.Frame(win, bg="#f0f0f0", width=180)
    frame_lateral.pack(side=tk.LEFT, fill=tk.Y)
    frame_lateral.pack_propagate(False)

    tk.Label(frame_lateral, text="Boleteria", font=("Arial", 13, "bold"), anchor="w", bg="#f0f0f0").pack(pady=(10, 5), padx=10, anchor="w")
    tk.Label(frame_lateral, text=f"{usuario_obj.get('cedula', usuario_obj.get('correo', 'Usuario'))}", font=("Arial", 11), anchor="w", bg="#f0f0f0").pack(pady=(0, 15), padx=10, anchor="w")

    # Panel principal donde se muestran cooperativas, destinos, buses o asientos
    frame_principal = tk.Frame(win, bg="white")
    frame_principal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Limpia el panel principal
    def limpiar_panel():
        for widget in frame_principal.winfo_children():
            widget.destroy()

    # ----------- COOPERATIVAS -----------
    def mostrar_cooperativas():
        limpiar_panel()
        seleccion["cooperativa"] = None
        seleccion["destino"] = None
        seleccion["bus"] = None
        seleccion["asientos"] = set()
        tk.Label(frame_principal, text="Cooperativas disponibles", font=("Arial", 12, "bold")).pack(pady=10)

        # Cuadro de búsqueda para cooperativas
        entry_buscar = tk.Entry(frame_principal, width=25)
        entry_buscar.pack(pady=5)
        entry_buscar.insert(0, "")

        frame_lista = tk.Frame(frame_principal, bg="white")
        frame_lista.pack(pady=5, fill=tk.BOTH, expand=True)

        # Actualiza la lista de cooperativas según el filtro de búsqueda
        def actualizar_lista(*args):
            for widget in frame_lista.winfo_children():
                widget.destroy()
            filtro = entry_buscar.get().strip().lower()
            for nombre in cargar_coperativas():
                if filtro in nombre.lower():
                    tk.Button(
                        frame_lista,
                        text=nombre,
                        font=("Arial", 11),
                        relief=tk.RIDGE,
                        width=30,
                        bg="#d0f0c0",
                        command=lambda n=nombre: mostrar_destinos(n)
                    ).pack(pady=4)
        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        actualizar_lista()

    # ----------- DESTINOS -----------
    def mostrar_destinos(cooperativa):
        limpiar_panel()
        seleccion["cooperativa"] = cooperativa
        seleccion["destino"] = None
        seleccion["bus"] = None
        seleccion["asientos"] = set()
        tk.Label(frame_principal, text=f"Buscar destino en {cooperativa}", font=("Arial", 12, "bold")).pack(pady=10)

        frame_busqueda = tk.Frame(frame_principal, bg="white")
        frame_busqueda.pack(pady=5)

        tk.Label(frame_busqueda, text="Ciudad de origen:").grid(row=0, column=0, padx=5, pady=2)
        entry_origen = tk.Entry(frame_busqueda, width=15)
        entry_origen.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_busqueda, text="Ciudad de destino:").grid(row=0, column=2, padx=5, pady=2)
        entry_destino = tk.Entry(frame_busqueda, width=15)
        entry_destino.grid(row=0, column=3, padx=5, pady=2)

        frame_lista = tk.Frame(frame_principal, bg="white")
        frame_lista.pack(pady=10, fill=tk.BOTH, expand=True)

        def actualizar_lista(*args):
            for widget in frame_lista.winfo_children():
                widget.destroy()
            origen_filtro = entry_origen.get().strip().lower()
            destino_filtro = entry_destino.get().strip().lower()
            destinos = []
            if os.path.exists(FICHERO_GRAFO):
                with open(FICHERO_GRAFO, "r", encoding="utf-8") as f:
                    grafo = json.load(f)
                # Solo destinos válidos (con usuario admin)
                destinos = [d for d in grafo if len(d) >= 6 and d[0] == cooperativa]
            for d in destinos:
                origen, destino, hora, costo = d[1], d[2], d[3], d[4]
                if (origen_filtro in origen.lower() if origen_filtro else True) and \
                   (destino_filtro in destino.lower() if destino_filtro else True):
                    texto = f"{origen} → {destino} | {hora}h | ${costo}"
                    tk.Button(
                        frame_lista,
                        text=texto,
                        font=("Arial", 11),
                        relief=tk.RIDGE,
                        width=35,
                        bg="#d0f0c0",
                        command=lambda dest=destino: mostrar_buses(cooperativa, dest)
                    ).pack(pady=3)

        entry_origen.bind("<KeyRelease>", actualizar_lista)
        entry_destino.bind("<KeyRelease>", actualizar_lista)
        actualizar_lista()

    # ----------- BUSES -----------
    def mostrar_buses(cooperativa, destino):
        limpiar_panel()
        seleccion["destino"] = destino
        seleccion["bus"] = None
        seleccion["asientos"] = set()
        tk.Label(frame_principal, text=f"Buses para {destino}", font=("Arial", 12, "bold")).pack(pady=10)

        # Cuadro de búsqueda para buses
        entry_buscar = tk.Entry(frame_principal, width=25)
        entry_buscar.pack(pady=5)
        entry_buscar.insert(0, "")

        frame_lista = tk.Frame(frame_principal, bg="white")
        frame_lista.pack(pady=5, fill=tk.BOTH, expand=True)

        # Actualiza la lista de buses según el filtro de búsqueda
        def actualizar_lista(*args):
            for widget in frame_lista.winfo_children():
                widget.destroy()
            filtro = entry_buscar.get().strip().lower()
            buses = []
            if os.path.exists(FICHERO_BUSES):
                with open(FICHERO_BUSES, "r", encoding="utf-8") as f:
                    buses = json.load(f)
                buses = [
                    bus for bus in buses
                    if bus.get("nombre_coperativa") == cooperativa and bus.get("destino") == destino
                ]
            for bus in buses:
                texto = f"{bus['nombre_bus']} | {bus.get('salida', '')} | {bus.get('cantidad_asientos', '')} asientos"
                if filtro in bus['nombre_bus'].lower() or filtro in bus.get('salida', '').lower():
                    tk.Button(
                        frame_lista,
                        text=texto,
                        font=("Arial", 11),
                        relief=tk.RIDGE,
                        width=35,
                        bg="#d0f0c0",
                        command=lambda nb=bus["nombre_bus"]: mostrar_asientos(cooperativa, destino, nb)
                    ).pack(pady=3)
        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        actualizar_lista()

    # ----------- ASIENTOS -----------
    def mostrar_asientos(cooperativa, destino, bus_nombre):
        limpiar_panel()
        seleccion["bus"] = bus_nombre
        seleccion["asientos"] = set()
        tk.Label(frame_principal, text=f"Asientos para {bus_nombre}", font=("Arial", 12, "bold")).pack(pady=10)

        # Obtener cantidad de asientos del bus seleccionado
        cantidad_asientos = 24
        if os.path.exists(FICHERO_BUSES):
            with open(FICHERO_BUSES, "r", encoding="utf-8") as f:
                buses = json.load(f)
            for bus in buses:
                if (bus.get("nombre_coperativa") == cooperativa and
                    bus.get("destino") == destino and
                    bus.get("nombre_bus") == bus_nombre):
                    cantidad_asientos = int(bus.get("cantidad_asientos", 24))
                    break

        frame_central = tk.Frame(frame_principal, bg="white")
        frame_central.pack(pady=10, padx=10, fill="both", expand=True)

        frame_asientos = tk.Frame(frame_central, bg="white", bd=2, relief="groove")
        frame_asientos.pack(side="left", padx=30, pady=10)

        frame_controles = tk.Frame(frame_central, bg="white")
        frame_controles.pack(side="left", padx=40, pady=10, anchor="n")

        asientos = {}
        seleccionados = set()  # Solo los de esta compra
        columnas = 5  # 4 asientos + 1 pasillo
        filas = (cantidad_asientos + 3) // 4

        # Cargar asientos ocupados por todos los usuarios (usando usuario_admin correcto)
        ocupados = cargar_asientos_ocupados(cooperativa, destino, bus_nombre)

        # Dibuja los botones de asientos (rojo=ocupado, verde=libre)
        asiento_num = 1
        for i in range(filas):
            for j in range(columnas):
                if j == 2:
                    tk.Label(frame_asientos, text=" ", bg="white", width=2).grid(row=i, column=j, padx=8)
                    continue
                if asiento_num > cantidad_asientos:
                    continue
                if asiento_num in ocupados:
                    btn = tk.Button(
                        frame_asientos,
                        text=str(asiento_num),
                        width=4,
                        height=2,
                        bg="red",
                        font=("Arial", 10, "bold"),
                        state="disabled"
                    )
                else:
                    def seleccionar_asiento(n=asiento_num):
                        if n in seleccionados:
                            asientos[n].config(bg="lightgreen")
                            seleccionados.remove(n)
                        else:
                            asientos[n].config(bg="red")
                            seleccionados.add(n)
                    btn = tk.Button(
                        frame_asientos,
                        text=str(asiento_num),
                        width=4,
                        height=2,
                        bg="lightgreen",
                        font=("Arial", 10, "bold"),
                        command=lambda n=asiento_num: seleccionar_asiento(n)
                    )
                btn.grid(row=i, column=j, padx=5, pady=5)
                asientos[asiento_num] = btn
                asiento_num += 1
            if asiento_num > cantidad_asientos:
                break

        # Genera la factura solo con los asientos seleccionados por el usuario actual
        def generar_factura():
            if not seleccionados:
                messagebox.showwarning("Sin selección", "Debe seleccionar al menos un asiento.")
                return
            # Buscar datos del destino
            costo_unitario = 0
            hora = ""
            if os.path.exists(FICHERO_GRAFO):
                with open(FICHERO_GRAFO, "r", encoding="utf-8") as f:
                    grafo = json.load(f)
                for d in grafo:
                    if (len(d) >= 6 and d[0] == cooperativa and d[2] == destino):
                        hora = d[3]
                        costo_unitario = d[4]
                        break
            total = costo_unitario * len(seleccionados)
            factura = (
                f"----- FACTURA -----\n"
                f"Cooperativa: {cooperativa}\n"
                f"Destino: {destino}\n"
                f"Bus: {bus_nombre}\n"
                f"Hora: {hora} h\n"
                f"Asientos: {', '.join(str(n) for n in sorted(seleccionados))}\n"
                f"Cantidad: {len(seleccionados)}\n"
                f"Precio unitario: ${costo_unitario:.2f}\n"
                f"Total a pagar: ${total:.2f}\n"
                f"-------------------"
            )
            guardar_asientos_ocupados(cooperativa, destino, bus_nombre, seleccionados)
            guardar_historial_usuario(
                usuario_obj.get("usuario", usuario_obj.get("correo", "")),
                cooperativa, destino, bus_nombre, seleccionados, total,
                datetime.datetime.now().strftime("%Y-%m-%d")
            )
            messagebox.showinfo("Factura", factura)
            mostrar_asientos(cooperativa, destino, bus_nombre)  # Refresca la vista

        # Botón para generar factura
        tk.Button(frame_controles, text="Generar factura", width=18, bg="#e0e0e0", command=generar_factura).pack(pady=10)
        frame_cantidad = tk.Frame(frame_controles, bg="white")
        frame_cantidad.pack(pady=10)
        tk.Label(frame_cantidad, text="Cantidad de asientos:", font=("Arial", 10), bg="white").pack(side="left")
        tk.Label(frame_cantidad, text=str(cantidad_asientos), font=("Arial", 10, "bold"), bg="white").pack(side="left", padx=8)

    # ----------- HISTORIAL DE COMPRAS -----------
    def mostrar_historial_usuario():
        limpiar_panel()
        tk.Label(frame_principal, text="Mis compras", font=("Arial", 12, "bold")).pack(pady=10)
        usuario = usuario_obj.get("usuario", usuario_obj.get("correo", ""))
        historial = []
        if os.path.exists(FICHERO_HISTORIAL):
            with open(FICHERO_HISTORIAL, "r", encoding="utf-8") as f:
                historial = json.load(f)
        # Filtrar solo las compras del usuario actual
        historial_usuario = [h for h in historial if h.get("usuario") == usuario]

        if not historial_usuario:
            tk.Label(frame_principal, text="No se encontraron compras anteriores.", font=("Arial", 10)).pack(pady=20)
            return

        for compra in historial_usuario:
            texto = f"{compra.get('fecha')} - {compra.get('cooperativa')} - {compra.get('destino')} - ${compra.get('monto'):.2f}"
            tk.Label(frame_principal, text=texto, font=("Arial", 10)).pack(anchor="w", padx=20, pady=5)

    # Botones de navegación lateral
    tk.Button(frame_lateral, text="Cooperativas", width=18, height=2, command=mostrar_cooperativas).pack(pady=5)
    tk.Button(frame_lateral, text="Destinos", width=18, height=2, command=lambda: mostrar_destinos(seleccion["cooperativa"]) if seleccion["cooperativa"] else None).pack(pady=5)
    tk.Button(frame_lateral, text="Buses/salida", width=18, height=2, command=lambda: mostrar_buses(seleccion["cooperativa"], seleccion["destino"]) if seleccion["cooperativa"] and seleccion["destino"] else None).pack(pady=5)
    tk.Button(frame_lateral, text="Asientos", width=18, height=2, command=lambda: mostrar_asientos(seleccion["cooperativa"], seleccion["destino"], seleccion["bus"]) if seleccion["cooperativa"] and seleccion["destino"] and seleccion["bus"] else None).pack(pady=5)
    tk.Button(frame_lateral, text="Historial", width=18, height=2, command=mostrar_historial_usuario).pack(pady=5)

    # Botón para cerrar sesión y volver al login
    def cerrar_sesion():
        win.destroy()
        import main
        main.ventana.deiconify()

    tk.Button(frame_lateral, text="Cerrar sesión", width=18, height=2, command=cerrar_sesion, bg="#ff6666").pack(pady=20)

    # Mostrar cooperativas al inicio
    mostrar_cooperativas()

    return win