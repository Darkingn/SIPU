from abc import ABC, abstractmethod

# --- OCP: Definimos las modalidades de forma extensible ---
class Modalidad:
    PRESENCIAL = "Presencial"
    VIRTUAL = "Virtual"
    HIBRIDA = "Híbrida"
    # Ahora es fácil añadir: DUAL = "Dual"

# --- SRP: La clase Carrera solo representa los DATOS de una carrera ---
class Carrera:
    def __init__(self, codigo, nombre, duracion, modalidad: str):
        self.codigo = codigo
        self.nombre = nombre
        self.duracion = duracion
        self.modalidad = modalidad

    @property
    def duracion(self):
        return self._duracion

    @duracion.setter
    def duracion(self, value):
        if value <= 0: 
            raise ValueError("La duración debe ser mayor a 0")
        self._duracion = value

    def obtener_info(self):
        return (f"Carrera {self.nombre} (ID: {self.codigo}) - "
                f"Duración: {self.duracion} semestres, Modalidad: {self.modalidad}")

# --- SRP: Separamos la gestión (contador) en un Repositorio o Manager ---
class CarreraRepository:
    def __init__(self):
        self._carreras = []

    def registrar_carrera(self, carrera: Carrera):
        # Aquí podrías añadir lógica para no repetir códigos
        self._carreras.append(carrera)
        print(f"Carrera '{carrera.nombre}' registrada exitosamente.")

    @property
    def total_carreras(self):
        return len(self._carreras)

# --- USO DEL SISTEMA ---

# 1. Creamos el gestor
repo = CarreraRepository()

# 2. Creamos instancias de carrera (Sin heredar de ProcesoAdmision)
software = Carrera("SOFT01", "Ingeniería de Software", 10, Modalidad.PRESENCIAL)
derecho = Carrera("DER02", "Derecho", 9, Modalidad.VIRTUAL)

# 3. Las registramos
repo.registrar_carrera(software)
repo.registrar_carrera(derecho)

print(f"Total de carreras en el sistema: {repo.total_carreras}")
print(software.obtener_info())