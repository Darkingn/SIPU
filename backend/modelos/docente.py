from .estudiante import Estudiante
class Docente(Estudiante):
    def __init__(self, nombre, cedula, carrera, semestre, materia, años_experiencia):
        # Llamamos al constructor de la clase padre (Estudiante)
        super().__init__(nombre, cedula, carrera, semestre)
        self.materia = materia
        self.años_experiencia = años_experiencia

    def mostrar_informacion(self):
        # Reutilizamos la función del padre y agregamos más información
        super().mostrar_informacion()
        print(f"Materia: {self.materia}")
        print(f"Años de experiencia: {self.años_experiencia}")
