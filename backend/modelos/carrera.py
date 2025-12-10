from proceso_admision import ProcesoAdmision  # Importamos la clase base que maneja el proceso de admisión

class Carrera(ProcesoAdmision):  # Definimos la clase Carrera que hereda de ProcesoAdmision
    _total_carreras = 0  # Contador general para saber cuántas carreras se han creado

    def __init__(self, codigo, nombre, fecha_inicio, duracion, modalidad):
        super().__init__(codigo, nombre, fecha_inicio, "Sistema")  # Llamamos al constructor del padre para inicializar los datos comunes
        self._duracion = duracion  # Guardamos la duración de la carrera (por ejemplo, en semestres)
        self._modalidad = modalidad  # Definimos la modalidad: presencial, virtual o híbrida
        Carrera._total_carreras += 1  # Cada vez que se crea una carrera, aumentamos el contador total

    @property
    def duracion(self): 
        return self._duracion  # Devuelve la duración actual de la carrera

    @duracion.setter
    def duracion(self, value):
        if value <= 0: raise ValueError("La duración debe ser mayor a 0")  # Validamos que la duración no sea cero ni negativa
        self._duracion = value  # Si es válida, la actualizamos

    @property
    def modalidad(self): 
        return self._modalidad  # Retorna la modalidad actual de la carrera

    @modalidad.setter
    def modalidad(self, value):
        if value not in ["Presencial", "Virtual", "Híbrida"]: raise ValueError("Modalidad no válida")  # Solo se permiten estas tres modalidades
        self._modalidad = value  # Si pasa la validación, la asignamos

    def obtener_info(self):  # Método que muestra toda la información de la carrera
        return f"Carrera {self._nombre} (Código: {self._codigo}) - Duración: {self._duracion} semestres, Modalidad: {self._modalidad} - Estado: {self._estado}"  # Retornamos un texto con los datos completos

    @classmethod
    def total_carreras(cls): 
        return cls._total_carreras  # Devuelve cuántas carreras se han creado en total

    def to_public_dict(self) -> dict:
        return {
            "codigo": getattr(self, "_codigo", None),
            "nombre": getattr(self, "_nombre", None),
            "duracion": getattr(self, "_duracion", None),
            "modalidad": getattr(self, "_modalidad", None),
            "estado": getattr(self, "_estado", None),
        }
