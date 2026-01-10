from abc import ABC, abstractmethod
from enum import Enum

class GrupoPrioridad(Enum):
    GENERAL = "Bachilleres General"
    GAR = "Grupo de Alto Rendimiento"
    VULNERABILIDAD = "Situación de Vulnerabilidad"
    PUEBLOS = "Pueblos y Nacionalidades"
    FRONTERA = "Zona de Frontera"

class Aspirante(ABC):
    def __init__(self, cedula, nombre, correo, p_examen, p_bachiller, grupo: GrupoPrioridad):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.p_examen = p_examen
        self.p_bachiller = p_bachiller
        self.grupo = grupo
        self.puntos_adicionales = 0

    @abstractmethod
    def calcular_puntaje_final(self):
        """Cada tipo de aspirante define cómo se suman sus puntos extra."""
        pass

    def get_data_for_supabase(self):
        """Prepara el diccionario para insertar en la base de datos."""
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "correo": self.correo,
            "tipo_aspirante": self.grupo.value,
            "puntaje_examen": self.p_examen,
            "puntaje_bachiller": self.p_bachiller,
            "puntaje_final": self.calcular_puntaje_final()
        }

# --- Implementación de Tipos Específicos ---

class AspiranteGAR(Aspirante):
    """Grupo de Alto Rendimiento: Los mejores puntuados."""
    def calcular_puntaje_final(self):
        # El GAR suele postular con su nota pura, pero tiene prioridad de cupo
        return (self.p_examen * 0.5) + (self.p_bachiller * 0.5)

class AspiranteVulnerable(Aspirante):
    """Personas en condiciones socioeconómicas críticas (+15 a +45 puntos)."""
    def __init__(self, cedula, nombre, correo, p_examen, p_bachiller, puntos_bono):
        super().__init__(cedula, nombre, correo, p_examen, p_bachiller, GrupoPrioridad.VULNERABILIDAD)
        self.puntos_adicionales = puntos_bono

    def calcular_puntaje_final(self):
        base = (self.p_examen * 0.5) + (self.p_bachiller * 0.5)
        return base + self.puntos_adicionales

class AspiranteEscolar(Aspirante):
    """Estudiantes de último año (Régimen Costa/Sierra)."""
    def calcular_puntaje_final(self):
        return (self.p_examen * 0.5) + (self.p_bachiller * 0.5)

class AspiranteEtnia(Aspirante):
    """Acción afirmativa por Pueblos y Nacionalidades (+10 puntos)."""
    def calcular_puntaje_final(self):
        base = (self.p_examen * 0.5) + (self.p_bachiller * 0.5)
        return base + 10