import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import os
import json
import re
import datetime

FICHERO_COPERATIVAS = "coperativas.json"
FICHERO_GRAFO = "grafo_destinos.json"
FICHERO_BUSES = "buses.json"
FICHERO_ASIENTOS = "asientos_ocupados.json"
FICHERO_VENTAS = "ventas.json"

def cargar_coperativas():
    FICHERO_COPERATIVAS_ADMINS = "coperativas_admins.json"
    if not os.path.exists(FICHERO_COPERATIVAS_ADMINS):
        return []
    with open(FICHERO_COPERATIVAS_ADMINS, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [coop["cooperativa"] for coop in data]

def ventana_gestion_admin(admin_obj, nombre_coperativa):
    win = tk.Toplevel()
    win.title("Boletería")
    win.geometry("800x520")
    win.resizable(False, False)

    frame_lateral = tk.Frame(win, bg="#f0f0f0", width=200)
    frame_lateral.pack(side=tk.LEFT, fill=tk.Y)
    frame_lateral.pack_propagate(False)

    tk.Label(frame_lateral, text="Boleteria", font=("Arial", 13, "bold"), anchor="w", bg="#f0f0f0").pack(pady=(10, 5), padx=10, anchor="w")
    tk.Label(frame_lateral, text=admin_obj.get("usuario", ""), font=("Arial", 11, "bold"), anchor="w", bg="#f0f0f0").pack(pady=(0, 10), padx=10, anchor="w")
    tk.Label(frame_lateral, text=nombre_coperativa, font=("Arial", 11), anchor="w", bg="#f0f0f0").pack(pady=(0, 15), padx=10, anchor="w")

    frame_principal = tk.Frame(win, bg="white")
    frame_principal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    seleccion = {"destino": None, "bus": None}

    def limpiar_panel():
        for widget in frame_principal.winfo_children():
            widget.destroy()

    # ----------- DESTINOS -----------
    def mostrar_destinos():
        limpiar_panel()
        tk.Label(frame_principal, text="Destinos", font=("Arial", 12, "bold")).pack(pady=10)

        frame_form = tk.Frame(frame_principal, bg="white")
        frame_form.pack(pady=10)
        tk.Label(frame_form, text="Origen:").grid(row=0, column=0, padx=5, pady=2)
        entry_origen = tk.Entry(frame_form, width=12)
        entry_origen.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(frame_form, text="Destino:").grid(row=1, column=0, padx=5, pady=2)
        entry_destino = tk.Entry(frame_form, width=12)
        entry_destino.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(frame_form, text="Hora (hh:mm):").grid(row=2, column=0, padx=5, pady=2)
        entry_hora = tk.Entry(frame_form, width=8)
        entry_hora.grid(row=2, column=1, padx=5, pady=2)
        tk.Label(frame_form, text="Costo ($):").grid(row=3, column=0, padx=5, pady=2)
        entry_costo = tk.Entry(frame_form, width=8)
        entry_costo.grid(row=3, column=1, padx=5, pady=2)

        def agregar_destino():
            origen = entry_origen.get().strip()
            destino = entry_destino.get().strip()
            hora = entry_hora.get().strip()
            costo = entry_costo.get().strip()
            if not re.match(r"^\d{1,2}(:[0-5]\d)?$", hora):
                messagebox.showerror("Error", "La hora debe ser un número entero (ej: 1, 2, 13) o en formato hh:mm (ej: 2:10).")
                return
            try:
                costo = float(costo)
            except ValueError:
                messagebox.showerror("Error", "Costo debe ser un número.")
                return
            if not origen or not destino:
                messagebox.showerror("Error", "Ingrese origen y destino.")
                return
            grafo = []
            if os.path.exists(FICHERO_GRAFO):
                with open(FICHERO_GRAFO, "r", encoding="utf-8") as f:
                    grafo = json.load(f)
            # Guardar también el usuario admin
            grafo.append([nombre_coperativa, origen, destino, hora, costo, admin_obj.get("usuario", "")])
            with open(FICHERO_GRAFO, "w", encoding="utf-8") as f:
                json.dump(grafo, f, ensure_ascii=False, indent=2)
            entry_origen.delete(0, tk.END)
            entry_destino.delete(0, tk.END)
            entry_hora.delete(0, tk.END)
            entry_costo.delete(0, tk.END)
            actualizar_lista_destinos()

        tk.Button(frame_form, text="Añadir destino", command=agregar_destino, bg="#d0f0c0").grid(row=4, column=0, columnspan=2, pady=8)

        frame_lista = tk.Frame(frame_principal, bg="white")
        frame_lista.pack(pady=10, fill=tk.BOTH, expand=True)

        def eliminar_destino(origen, destino, hora, costo):
            if not os.path.exists(FICHERO_GRAFO):
                return
            with open(FICHERO_GRAFO, "r", encoding="utf-8") as f:
                grafo = json.load(f)
            grafo = [
                d for d in grafo
                if not (d[0] == nombre_coperativa and d[1] == origen and d[2] == destino and d[3] == hora and d[4] == costo and d[5] == admin_obj.get("usuario", ""))
            ]
            with open(FICHERO_GRAFO, "w", encoding="utf-8") as f:
                json.dump(grafo, f, ensure_ascii=False, indent=2)
            actualizar_lista_destinos()

        def actualizar_lista_destinos():
            for widget in frame_lista.winfo_children():
                widget.destroy()
            destinos = []
            if os.path.exists(FICHERO_GRAFO):
                with open(FICHERO_GRAFO, "r", encoding="utf-8") as f:
                    grafo = json.load(f)
                destinos = [
                    d for d in grafo
                    if len(d) >= 6 and d[0] == nombre_coperativa and d[5] == admin_obj.get("usuario", "")
                ]
            for d in destinos:
                origen, destino, hora, costo = d[1], d[2], d[3], d[4]
                fila = tk.Frame(frame_lista, bg="white")
                fila.pack(fill=tk.X, pady=2)
                btn_destino = tk.Button(
                    fila,
                    text=f"{origen} → {destino} | {hora}h | ${costo}",
                    font=("Arial", 11),
                    relief=tk.RIDGE,
                    width=30,
                    bg="#d0f0c0",
                    anchor="w",
                    command=lambda dest=destino: mostrar_buses(dest)
                )
                btn_destino.pack(side=tk.LEFT, padx=2)
                btn_x = tk.Button(
                    fila,
                    text="X",
                    bg="#f08080",
                    fg="white",
                    width=3,
                    font=("Arial", 9, "bold"),
                    command=lambda o=origen, d=destino, h=hora, c=costo: eliminar_destino(o, d, h, c)
                )
                btn_x.pack(side=tk.LEFT, padx=2)

        frame_titulo = tk.Frame(frame_principal, bg="white")
        frame_titulo.pack(pady=10)
        tk.Label(frame_titulo, text="Buscar ruta", font=("Arial", 12, "bold"), bg="white").pack(side=tk.LEFT, padx=(0, 20))
        entry_buscar = tk.Entry(frame_titulo, width=18)
        entry_buscar.pack(side=tk.LEFT)
        entry_buscar.insert(0, "")

        def filtrar_destinos(event=None):
            filtro = entry_buscar.get().strip().lower()
            for widget in frame_lista.winfo_children():
                widget.destroy()
            destinos = []
            if os.path.exists(FICHERO_GRAFO):
                with open(FICHERO_GRAFO, "r", encoding="utf-8") as f:
                    grafo = json.load(f)
                destinos = [
                    d for d in grafo
                    if len(d) >= 6 and d[0] == nombre_coperativa and d[5] == admin_obj.get("usuario", "")
                ]
            for d in destinos:
                origen, destino, hora, costo = d[1], d[2], d[3], d[4]
                texto = f"{origen} → {destino} | {hora}h | ${costo}"
                if filtro in origen.lower() or filtro in destino.lower():
                    fila = tk.Frame(frame_lista, bg="white")
                    fila.pack(fill=tk.X, pady=2)
                    btn_destino = tk.Button(
                        fila,
                        text=texto,
                        font=("Arial", 11),
                        relief=tk.RIDGE,
                        width=30,
                        bg="#d0f0c0",
                        anchor="w",
                        command=lambda dest=destino: mostrar_buses(dest)
                    )
                    btn_destino.pack(side=tk.LEFT, padx=2)
                    btn_x = tk.Button(
                        fila,
                        text="X",
                        bg="#f08080",
                        fg="white",
                        width=3,
                        font=("Arial", 9, "bold"),
                        command=lambda o=origen, d=destino, h=hora, c=costo: eliminar_destino(o, d, h, c)
                    )
                    btn_x.pack(side=tk.LEFT, padx=2)

        entry_buscar.bind("<KeyRelease>", filtrar_destinos)
        actualizar_lista_destinos()

    # ----------- BUSES -----------
    def mostrar_buses(destino_seleccionado=None):
        limpiar_panel()
        if destino_seleccionado:
            seleccion["destino"] = destino_seleccionado
        if not seleccion["destino"]:
            tk.Label(frame_principal, text="Seleccione un destino", font=("Arial", 12, "bold")).pack(pady=10)
            return
        tk.Label(frame_principal, text=f"Buses/salida para {seleccion['destino']}", font=("Arial", 12, "bold")).pack(pady=10)

        frame_form = tk.Frame(frame_principal, bg="white")
        frame_form.pack(pady=10)
        tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=2)
        entry_nombre = tk.Entry(frame_form, width=15)
        entry_nombre.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(frame_form, text="salida:").grid(row=0, column=2, padx=5, pady=2)
        entry_salida = tk.Entry(frame_form, width=15)
        entry_salida.grid(row=0, column=3, padx=5, pady=2)
        tk.Label(frame_form, text="asientos:").grid(row=0, column=4, padx=5, pady=2)
        entry_cantidad = tk.Entry(frame_form, width=5)
        entry_cantidad.grid(row=0, column=5, padx=5, pady=2)
        def agregar_bus():
            nombre_bus = entry_nombre.get().strip()
            salida = entry_salida.get().strip()
            try:
                cantidad = int(entry_cantidad.get().strip())
                if cantidad < 27:
                    messagebox.showerror("Error", "La cantidad de asientos no puede ser menor a 27.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Ingrese una cantidad de asientos válida.")
                return
            if not nombre_bus or not salida:
                messagebox.showerror("Error", "Ingrese el nombre y el horario de salida del bus.")
                return
            buses = []
            if os.path.exists(FICHERO_BUSES):
                with open(FICHERO_BUSES, "r", encoding="utf-8") as f:
                    buses = json.load(f)
            buses.append({
                "nombre_coperativa": nombre_coperativa,
                "destino": seleccion["destino"],
                "nombre_bus": nombre_bus,
                "salida": salida,
                "cantidad_asientos": cantidad,
                "usuario_admin": admin_obj.get("usuario", "")
            })
            with open(FICHERO_BUSES, "w", encoding="utf-8") as f:
                json.dump(buses, f, ensure_ascii=False, indent=2)
            entry_nombre.delete(0, tk.END)
            entry_salida.delete(0, tk.END)
            entry_cantidad.delete(0, tk.END)
            mostrar_buses(seleccion["destino"])
        tk.Button(frame_form, text="Añadir Bus", command=agregar_bus, bg="#d0f0c0").grid(row=0, column=6, padx=8)

        frame_lista = tk.Frame(frame_principal, bg="white")
        frame_lista.pack(pady=10, fill=tk.BOTH, expand=True)
        buses = []
        if os.path.exists(FICHERO_BUSES):
            with open(FICHERO_BUSES, "r", encoding="utf-8") as f:
                buses = json.load(f)
        buses = [
            bus for bus in buses
            if bus.get("nombre_coperativa") == nombre_coperativa and
               bus.get("destino") == seleccion["destino"] and
               bus.get("usuario_admin", "") == admin_obj.get("usuario", "")
        ]
        for bus in buses:
            fila = tk.Frame(frame_lista, bg="white")
            fila.pack(fill=tk.X, pady=2)
            btn_bus = tk.Button(
                fila,
                text=f"{bus['nombre_bus']} | {bus.get('salida', '')}",
                font=("Arial", 11),
                bg="#d0f0c0",
                width=35,
                anchor="w",
                command=lambda nb=bus["nombre_bus"]: mostrar_asientos(nb)
            )
            btn_bus.pack(side=tk.LEFT, padx=5)
            def eliminar_bus(nb=bus["nombre_bus"], sal=bus.get("salida", "")):
                buses_data = []
                if os.path.exists(FICHERO_BUSES):
                    with open(FICHERO_BUSES, "r", encoding="utf-8") as f:
                        buses_data = json.load(f)
                buses_data = [
                    b for b in buses_data
                    if not (
                        b.get("nombre_coperativa") == nombre_coperativa and
                        b.get("destino") == seleccion["destino"] and
                        b.get("nombre_bus") == nb and
                        b.get("salida", "") == sal and
                        b.get("usuario_admin", "") == admin_obj.get("usuario", "")
                    )
                ]
                with open(FICHERO_BUSES, "w", encoding="utf-8") as f:
                    json.dump(buses_data, f, ensure_ascii=False, indent=2)
                mostrar_buses(seleccion["destino"])
            tk.Button(
                fila,
                text="X",
                bg="#f08080",
                command=eliminar_bus
            ).pack(side=tk.LEFT, padx=5, anchor="center")

    # ----------- ASIENTOS -----------
    def mostrar_asientos(bus_seleccionado=None):
        limpiar_panel()
        seleccion["bus"] = bus_seleccionado
        tk.Label(frame_principal, text=f"Asientos para {seleccion['bus']}", font=("Arial", 12, "bold")).pack(pady=10)

        cantidad_asientos = 24
        if os.path.exists(FICHERO_BUSES):
            with open(FICHERO_BUSES, "r", encoding="utf-8") as f:
                buses = json.load(f)
            for bus in buses:
                if (bus.get("nombre_coperativa") == nombre_coperativa and
                    bus.get("destino") == seleccion["destino"] and
                    bus.get("nombre_bus") == seleccion["bus"] and
                    bus.get("usuario_admin", "") == admin_obj.get("usuario", "")):
                    cantidad_asientos = int(bus.get("cantidad_asientos", 24))
                    break

        frame_central = tk.Frame(frame_principal, bg="white")
        frame_central.pack(pady=10, padx=10, fill="both", expand=True)

        frame_asientos = tk.Frame(frame_central, bg="white", bd=2, relief="groove")
        frame_asientos.pack(side="left", padx=30, pady=10)

        frame_controles = tk.Frame(frame_central, bg="white")
        frame_controles.pack(side="left", padx=40, pady=10, anchor="n")

        asientos = {}
        seleccionados = set()

        def seleccionar_asiento(n):
            if n in seleccionados:
                seleccionados.remove(n)
                asientos[n].configure(bg="lightgreen")
            else:
                seleccionados.add(n)
                asientos[n].configure(bg="green")

        columnas = 5
        filas = (cantidad_asientos + 3) // 4
        asiento_num = 1
        ocupados = cargar_asientos_ocupados(nombre_coperativa, seleccion["destino"], seleccion["bus"], admin_obj.get("usuario", ""))
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

        def generar_factura():
            if not seleccionados:
                messagebox.showwarning("Sin selección", "Debe seleccionar al menos un asiento.")
                return
            costo_unitario = 0
            hora = ""
            if os.path.exists(FICHERO_GRAFO):
                with open(FICHERO_GRAFO, "r", encoding="utf-8") as f:
                    grafo = json.load(f)
                for d in grafo:
                    if (d[0] == nombre_coperativa and d[2] == seleccion["destino"] and d[5] == admin_obj.get("usuario", "")):
                        hora = d[3]
                        costo_unitario = d[4]
                        break
            total = costo_unitario * len(seleccionados)
            factura = (
                f"----- FACTURA -----\n"
                f"Cooperativa: {nombre_coperativa}\n"
                f"Destino: {seleccion['destino']}\n"
                f"Bus: {seleccion['bus']}\n"
                f"Hora: {hora} h\n"
                f"Asientos: {', '.join(str(n) for n in sorted(seleccionados))}\n"
                f"Cantidad: {len(seleccionados)}\n"
                f"Precio unitario: ${costo_unitario:.2f}\n"
                f"Total a pagar: ${total:.2f}\n"
                f"-------------------"
            )
            messagebox.showinfo("Factura", factura)

        def factura_todos_los_asientos():
            ocupados = cargar_asientos_ocupados(nombre_coperativa, seleccion["destino"], seleccion["bus"], admin_obj.get("usuario", ""))
            if not ocupados:
                messagebox.showinfo("Factura", "No hay asientos vendidos para este bus.")
                return
            costo_unitario = 0
            hora = ""
            if os.path.exists(FICHERO_GRAFO):
                with open(FICHERO_GRAFO, "r", encoding="utf-8") as f:
                    grafo = json.load(f)
                for d in grafo:
                    if (d[0] == nombre_coperativa and d[2] == seleccion["destino"] and d[5] == admin_obj.get("usuario", "")):
                        hora = d[3]
                        costo_unitario = d[4]
                        break
            total = costo_unitario * len(ocupados)
            factura = (
                f"----- FACTURA TOTAL -----\n"
                f"Cooperativa: {nombre_coperativa}\n"
                f"Destino: {seleccion['destino']}\n"
                f"Bus: {seleccion['bus']}\n"
                f"Hora: {hora} h\n"
                f"Asientos vendidos: {', '.join(str(n) for n in sorted(ocupados))}\n"
                f"Cantidad: {len(ocupados)}\n"
                f"Precio unitario: ${costo_unitario:.2f}\n"
                f"Total recaudado: ${total:.2f}\n"
                f"-------------------------"
            )
            messagebox.showinfo("Factura total", factura)

        tk.Button(frame_controles, text="Factura asientos vendidos", width=22, bg="#c0e0ff", command=factura_todos_los_asientos).pack(pady=5)

        def limpiar_asientos():
            clave = f"{nombre_coperativa}|{seleccion['destino']}|{seleccion['bus']}|{admin_obj.get('usuario', '')}"
            if os.path.exists(FICHERO_ASIENTOS):
                with open(FICHERO_ASIENTOS, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if clave in data:
                    del data[clave]
                    with open(FICHERO_ASIENTOS, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
            mostrar_asientos(seleccion["bus"])
            messagebox.showinfo("Limpieza", "Todos los asientos han sido liberados para este bus.")

        tk.Button(frame_controles, text="Limpiar asientos", width=22, bg="#ffcccc", command=limpiar_asientos).pack(pady=5)

    tk.Button(frame_lateral, text="Destinos", width=18, height=2, command=mostrar_destinos).pack(pady=5)
    tk.Button(frame_lateral, text="Buses/salida", width=18, height=2, command=mostrar_buses).pack(pady=5)
    tk.Button(frame_lateral, text="Asientos", width=18, height=2, command=lambda: mostrar_asientos(seleccion["bus"])).pack(pady=5)
    tk.Button(frame_lateral, text="Reporte de ventas", width=18, height=2, command=lambda: abrir_reporte_ventas(admin_obj, nombre_coperativa)).pack(pady=5)

    def cerrar_sesion():
        win.destroy()
        import main
        main.ventana.deiconify()

    tk.Button(
        frame_lateral,
        text="Cerrar sesión",
        width=18,
        height=2,
        bg="#f08080",
        command=cerrar_sesion
    ).pack(pady=30)

    mostrar_destinos()

def cargar_asientos_ocupados(cooperativa, destino, bus, usuario_admin):
    clave = f"{cooperativa}|{destino}|{bus}|{usuario_admin}"
    if os.path.exists(FICHERO_ASIENTOS):
        with open(FICHERO_ASIENTOS, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get(clave, []))
    return set()

def registrar_venta(cooperativa, destino, bus, usuario_admin, asientos, monto):
    venta = {
        "cooperativa": cooperativa,
        "destino": destino,
        "bus": bus,
        "usuario_admin": usuario_admin,
        "asientos": list(asientos),
        "cantidad": len(asientos),
        "monto": monto,
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    ventas = []
    if os.path.exists(FICHERO_VENTAS):
        with open(FICHERO_VENTAS, "r", encoding="utf-8") as f:
            ventas = json.load(f)
    ventas.append(venta)
    with open(FICHERO_VENTAS, "w", encoding="utf-8") as f:
        json.dump(ventas, f, ensure_ascii=False, indent=2)

def abrir_reporte_ventas(admin_obj, nombre_coperativa):
    win_report = tk.Toplevel()
    win_report.title("Reporte de Ventas")
    win_report.geometry("600x500")

    tk.Label(win_report, text="Reporte de ventas", font=("Arial", 14, "bold")).pack(pady=10)

    frame_filtros = tk.Frame(win_report)
    frame_filtros.pack(pady=10)

    tk.Label(frame_filtros, text="Filtrar por:").grid(row=0, column=0, padx=5)
    filtro_var = tk.StringVar(value="dia")
    opciones = ["dia", "semana", "mes", "año", "rango"]
    menu = tk.OptionMenu(frame_filtros, filtro_var, *opciones)
    menu.grid(row=0, column=1, padx=5)

    tk.Label(frame_filtros, text="Fecha inicio:").grid(row=1, column=0, padx=5)
    fecha_inicio = DateEntry(frame_filtros, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    fecha_inicio.grid(row=1, column=1, padx=5)
    tk.Label(frame_filtros, text="Fecha fin:").grid(row=1, column=2, padx=5)
    fecha_fin = DateEntry(frame_filtros, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    fecha_fin.grid(row=1, column=3, padx=5)

    frame_resultado = tk.Frame(win_report)
    frame_resultado.pack(pady=15, fill=tk.BOTH, expand=True)

    def filtrar_ventas():
        for widget in frame_resultado.winfo_children():
            widget.destroy()
        ventas = []
        if os.path.exists(FICHERO_VENTAS):
            with open(FICHERO_VENTAS, "r", encoding="utf-8") as f:
                ventas = json.load(f)
        # Solo ventas de este admin y cooperativa
        ventas = [v for v in ventas if v["cooperativa"] == nombre_coperativa and v["usuario_admin"] == admin_obj.get("usuario", "")]
        filtro = filtro_var.get()
        hoy = datetime.datetime.now().date()
        ventas_filtradas = []
        if filtro == "dia":
            ventas_filtradas = [v for v in ventas if v["fecha"] == hoy.strftime("%Y-%m-%d")]
        elif filtro == "semana":
            semana = hoy.isocalendar()[1]
            ventas_filtradas = [v for v in ventas if datetime.datetime.strptime(v["fecha"], "%Y-%m-%d").isocalendar()[1] == semana and
                                datetime.datetime.strptime(v["fecha"], "%Y-%m-%d").year == hoy.year]
        elif filtro == "mes":
            ventas_filtradas = [v for v in ventas if v["fecha"][:7] == hoy.strftime("%Y-%m")]
        elif filtro == "año":
            ventas_filtradas = [v for v in ventas if v["fecha"][:4] == hoy.strftime("%Y")]
        elif filtro == "rango":
            fi = datetime.datetime.strptime(fecha_inicio.get(), "%Y-%m-%d").date()
            ff = datetime.datetime.strptime(fecha_fin.get(), "%Y-%m-%d").date()
            ventas_filtradas = [v for v in ventas if fi <= datetime.datetime.strptime(v["fecha"], "%Y-%m-%d").date() <= ff]

        total_boletos = sum(v["cantidad"] for v in ventas_filtradas)
        total_monto = sum(v["monto"] for v in ventas_filtradas)

        tk.Label(frame_resultado, text=f"Total boletos vendidos: {total_boletos}", font=("Arial", 12)).pack(pady=5)
        tk.Label(frame_resultado, text=f"Total recaudado: ${total_monto:.2f}", font=("Arial", 12)).pack(pady=5)

        for v in ventas_filtradas:
            tk.Label(frame_resultado, text=f"{v['fecha']} | {v['destino']} | {v['bus']} | {v['cantidad']} boletos | ${v['monto']:.2f}", anchor="w").pack(fill="x")

    tk.Button(win_report, text="Filtrar", command=filtrar_ventas, bg="#d0f0c0").pack(pady=10)
    filtrar_ventas()