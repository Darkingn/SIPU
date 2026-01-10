from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict

# --- OCP: Definimos Tipos de Universidad como Enum ---
class TipoUniversidad(Enum):
    PUBLICA = "Pública"
    PRIVADA = "Privada"
    COFINANCIADA = "Cofinanciada"

# --- SRP: Clase dedicada a gestionar una Sede y su estado ---
class Sede:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.inscripciones_abiertas = False

    def abrir_inscripcion(self):
        self.inscripciones_abiertas = True

    def cerrar_inscripcion(self):
        self.inscripciones_abiertas = False

# --- SRP: La clase Universidad como Entidad Administrativa ---
class Universidad:
    def __init__(self, codigo: str, nombre: str, tipo: TipoUniversidad, ubicacion: str):
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.ubicacion = ubicacion
        self._sedes: Dict[str, Sede] = {}

    def agregar_sedes(self, nombres_sedes: List[str]):
        for nombre in nombres_sedes:
            self._sedes[nombre] = Sede(nombre)

    # Fachada para gestionar inscripciones (Delegación)
    def gestionar_inscripciones_sede(self, nombre_sede: str, abrir: bool):
        sede = self._sedes.get(nombre_sede)
        if not sede:
            raise ValueError(f"La sede '{nombre_sede}' no existe.")
        
        if abrir:
            sede.abrir_inscripcion()
        else:
            sede.cerrar_inscripcion()

    def obtener_info(self):
        sedes_str = ", ".join([s.nombre for s in self._sedes.values()])
        return (f"Universidad: {self.nombre} ({self.tipo.value})\n"
                f"Ubicación Principal: {self.ubicacion}\n"
                f"Sedes: {sedes_str}")

# --- SRP: Repositorio para contabilidad global ---
class UniversidadRepository:
    def __init__(self):
        self._universidades = []

    def registrar(self, universidad: Universidad):
        self._universidades.append(universidad)

    @property
    def total(self):
        return len(self._universidades)

# --- USO DEL SISTEMA ---

repo = UniversidadRepository()

# Creamos la universidad
uce = Universidad("UCE-001", "Univ. Central", TipoUniversidad.PUBLICA, "Quito")
uce.agregar_sedes(["Quito", "Santo Domingo"])

# Operamos sobre una sede específica
uce.gestionar_inscripciones_sede("Quito", abrir=True)

repo.registrar(uce)

print(uce.obtener_info())
print(f"Estado inscripción Quito: {uce._sedes['Quito'].inscripciones_abiertas}")