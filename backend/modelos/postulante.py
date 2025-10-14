class Postulante:
    def __init__(self, nombre, cedula, carrera, semestre):
        self.nombre = nombre
        self.cedula = cedula
        self.carrera = carrera
        self.semestre = semestre

    def mostrar_informacion(self):
        print(f"Nombre: {self.nombre}")
        print(f"Cédula: {self.cedula}")
        print(f"Carrera: {self.carrera}")
        print(f"Semestre: {self.semestre}")

