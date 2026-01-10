from typing import List

# --- SRP: La clase OfertaAcademica ahora es un contenedor de datos reales ---
class OfertaAcademica:
    def __init__(self, codigo: str, nombre: str, cupos_totales: int):
        self.codigo = codigo
        self.nombre = nombre
        self._cupos_totales = cupos_totales
        # DIP: En lugar de un número, usamos una lista de objetos Carrera
        self._carreras: List = [] 
        self._areas = set() # Usamos un set para contar áreas únicas automáticamente

    @property
    def cupos(self):
        return self._cupos_totales

    @cupos.setter
    def cupos(self, value):
        if value < 0:
            raise ValueError("Los cupos no pueden ser negativos")
        self._cupos_totales = value

    # --- OCP: Podemos añadir carreras sin modificar la estructura interna ---
    def agregar_carrera(self, carrera, area_nombre: str):
        self._carreras.append(carrera)
        self._areas.add(area_nombre)

    @property
    def num_carreras(self):
        return len(self._carreras)

    @property
    def num_areas(self):
        return len(self._areas)

    def obtener_info(self):
        return (f"Oferta: {self.nombre} [{self.codigo}]\n"
                f"Carreras ofertadas: {self.num_carreras}\n"
                f"Áreas cubiertas: {self.num_areas}\n"
                f"Cupos disponibles: {self._cupos_totales}")

# --- SRP: Separamos el conteo global a un Gestor de Ofertas ---
class OfertaManager:
    def __init__(self):
        self._ofertas = []

    def registrar_oferta(self, oferta: OfertaAcademica):
        self._ofertas.append(oferta)

    @property
    def total_ofertas(self):
        return len(self._ofertas)

# --- USO DEL SISTEMA (Conectando con lo anterior) ---

# 1. Creamos las carreras (del ejercicio anterior)
carrera_1 = "Ingeniería de Software" # Simulando el objeto
carrera_2 = "Ciberseguridad"

# 2. Creamos la oferta
oferta_2024 = OfertaAcademica("OFER-2024", "Admisiones Segundo Semestre", 500)

# 3. Inyectamos las carreras
oferta_2024.agregar_carrera(carrera_1, "Tecnología")
oferta_2024.agregar_carrera(carrera_2, "Tecnología")

# 4. Resultados
print(oferta_2024.obtener_info())
print(f"Total de áreas únicas: {oferta_2024.num_areas}")