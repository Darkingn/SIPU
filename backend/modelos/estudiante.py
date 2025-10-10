class Estudiante:
    def __init__(self, id, nombre, correo, carrera):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.carrera = carrera

    def __str__(self):
        return f"{self.nombre} ({self.carrera})"
