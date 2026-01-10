from abc import ABC, abstractmethod

#clase abstracta para los aspirantes

class Aspirante(ABC):
    def __init__(self, nombre, cedula, carrera):
        self.nombre = nombre
        self.cedula = cedula
        self.carrera = carrera

    @abstractmethod
    def validar_requisitos(self):
        pass

#clases concretas de aspirantes

class AspiranteNuevo(Aspirante):
    def validar_requisitos(self):
        return bool(self.cedula and self.carrera)

class AspiranteTraslado(Aspirante):
    def __init__(self, nombre, cedula, carrera, universidad_origen):
        super().__init__(nombre, cedula, carrera)
        self.universidad_origen = universidad_origen

    def validar_requisitos(self):
        return bool(self.cedula and self.carrera and self.universidad_origen)

#fabrica para crear aspirantes

class AspiranteFactory:
    @staticmethod
    def crear_aspirante(tipo, **datos):
        if tipo == "nuevo":
            return AspiranteNuevo(
                datos["nombre"], datos["cedula"], datos["carrera"]
            )
        elif tipo == "traslado":
            return AspiranteTraslado(
                datos["nombre"], datos["cedula"],
                datos["carrera"], datos["universidad_origen"]
            )
        else:
            raise ValueError("Tipo de admisión no válido")

#uso del patron factory method

aspirante = AspiranteFactory.crear_aspirante(
    "traslado",
    nombre="Ana",
    cedula="0102030405",
    carrera="Ingeniería",
    universidad_origen="UCE"
)

aspirante1 = AspiranteFactory.crear_aspirante(
    "nuevo",
    nombre="leo",
    cedula="0102030405",
    carrera=""
)

if aspirante.validar_requisitos():
    print("Aspirante aceptado para evaluación")
else:
    print("Requisitos incompletos")

if aspirante1.validar_requisitos():
    print("Aspirante aceptado para evaluación")
else:
    print("Requisitos incompletos")
