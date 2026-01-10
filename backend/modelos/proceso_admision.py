from abc import ABC, abstractmethod

# --- OCP: Interfaz para los diferentes estados ---
class EstadoProceso(ABC):
    @abstractmethod
    def manejar(self):
        pass

class EstadoNoIniciado(EstadoProceso):
    def manejar(self): return "No iniciado"

class EstadoIniciado(EstadoProceso):
    def manejar(self): return "Iniciado"

class EstadoFinalizado(EstadoProceso):
    def manejar(self): return "Finalizado"

# --- SRP: Clase Base para Entidades con Identidad ---
# Resolvemos el problema de "herencia por conveniencia"
class Identificable(ABC):
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

# --- SRP & DIP: La clase Proceso ahora es una Orquestadora ---
class ProcesoAdmision(Identificable):
    def __init__(self, codigo, nombre, fecha_inicio, responsable):
        super().__init__(codigo, nombre)
        self.fecha_inicio = fecha_inicio
        self.responsable = responsable
        self._estado: EstadoProceso = EstadoNoIniciado()

    @property
    def estado_actual(self):
        return self._estado.manejar()

    # DIP: Inversión de Dependencia al cambiar estados
    def cambiar_estado(self, nuevo_estado: EstadoProceso):
        self._estado = nuevo_estado

    def obtener_info(self):
        return (f"PROCESO: {self.nombre} [{self.codigo}]\n"
                f"Responsable: {self.responsable}\n"
                f"Estado: {self.estado_actual}")

# --- Ejemplo de aplicación real ---
class AdmisionPregrado(ProcesoAdmision):
    """Ahora esta clase SÍ es un proceso de admisión real."""
    def ejecutar_logica(self):
        print(f"Ejecutando validaciones para {self.nombre}...")

# USO
proceso = AdmisionPregrado("ADM-2026", "Admisión General", "2026-02-01", "Dr. Ramos")
print(proceso.obtener_info())

# Cambiamos estado de forma flexible
proceso.cambiar_estado(EstadoIniciado())
print(f"Nuevo estado: {proceso.estado_actual}")