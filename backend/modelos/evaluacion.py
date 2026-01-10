from enum import Enum

# --- SRP: Definimos los estados de forma clara ---
class EstadoEvaluacion(Enum):
    PROGRAMADA = "Programada"
    EN_CURSO = "En curso"
    FINALIZADA = "Finalizada"

# --- SRP: La clase Evaluacion es ahora una Entidad pura ---
class Evaluacion:
    def __init__(self, codigo, nombre, fecha, hora, sala, duracion, tipo):
        self.codigo = codigo
        self.nombre = nombre
        self.fecha = fecha
        self.hora = hora
        self.sala = sala
        self.duracion = duracion
        self.tipo = tipo
        self.estado = EstadoEvaluacion.PROGRAMADA

    def obtener_info(self):
        return (f"[{self.tipo}] {self.nombre} (Cod: {self.codigo}) - "
                f"Lugar: {self.sala} a las {self.hora} - Estado: {self.estado.value}")

# --- SRP & DIP: El Gestor se encarga de la lógica de negocio ---
class EvaluacionManager:
    """Clase responsable de controlar el flujo y el conteo de evaluaciones."""
    def __init__(self):
        self._evaluaciones = []

    def registrar_evaluacion(self, evaluacion: Evaluacion):
        self._evaluaciones.append(evaluacion)

    def iniciar(self, evaluacion: Evaluacion):
        if evaluacion.estado == EstadoEvaluacion.PROGRAMADA:
            evaluacion.estado = EstadoEvaluacion.EN_CURSO
            return f"Evaluación {evaluacion.nombre} iniciada en sala {evaluacion.sala}."
        raise ValueError("La evaluación no se puede iniciar (debe estar Programada).")

    def finalizar(self, evaluacion: Evaluacion):
        if evaluacion.estado == EstadoEvaluacion.EN_CURSO:
            evaluacion.estado = EstadoEvaluacion.FINALIZADA
            return f"Evaluación {evaluacion.nombre} finalizada."
        raise ValueError("No se puede finalizar una evaluación que no esté en curso.")

    @property
    def total_evaluaciones(self):
        return len(self._evaluaciones)

# --- USO DEL SISTEMA ---

manager = EvaluacionManager()

# Creamos la evaluación (ya no hereda de ProcesoAdmision)
examen_mate = Evaluacion(
    "MAT01", "Examen de Matemáticas", "2024-05-20", 
    "09:00", "Sala A-12", 2, "Escrito"
)

manager.registrar_evaluacion(examen_mate)

# Control de flujo a través del Manager
print(examen_mate.obtener_info())
print(manager.iniciar(examen_mate))
print(examen_mate.obtener_info())
print(manager.finalizar(examen_mate))

print(f"Total evaluaciones registradas: {manager.total_evaluaciones}")