from proceso_admision import ProcesoAdmision  # Se importa la clase base del proceso de admisión
from evaluacion import Evaluacion  # Se importa la clase Evaluacion para componerla dentro de Postulacion
from typing import Optional


class Postulacion(ProcesoAdmision):  # La clase Postulacion hereda de ProcesoAdmision
    _total_postulaciones = 0  # Variable de clase que lleva el conteo total de postulaciones

    def __init__(
        self,
        codigo,
        nombre,
        fecha_inicio,
        postulante,
        carrera,
        sede,
        fecha_postulacion,
        hora,
        sala,
        duracion,
        tipo,
        evaluacion: Optional[Evaluacion] = None,
    ):
        """Ahora `Postulacion` admite inyección de la dependencia `Evaluacion`.

        Si no se provee, se crea una instancia por compatibilidad (fallback).
        Esto facilita pruebas y respeta DIP.
        """
        super().__init__(codigo, nombre, fecha_inicio, "Sistema")  # Se inicializan los atributos de la clase padre
        self._postulante = postulante  # Se guarda el postulante que realiza la postulación
        self._carrera = carrera  # Se asocia la carrera a la que postula
        self._sede = sede  # Se guarda la sede donde se realiza el proceso
        if evaluacion is None:
            # Fallback: crear evaluación si no fue inyectada (mantener compatibilidad)
            self._evaluacion = Evaluacion(
                codigo, nombre, fecha_postulacion, fecha_postulacion, hora, sala, duracion, tipo
            )
        else:
            self._evaluacion = evaluacion
        Postulacion._total_postulaciones += 1  # Cada vez que se crea una nueva postulación se incrementa el contador total

    @property
    def postulante(self):  # Getter para acceder al postulante
        return self._postulante  # Retorna el objeto postulante

    @postulante.setter
    def postulante(self, value):  # Setter que valida y asigna el postulante
        if not value:
            raise ValueError("El postulante no puede ser nulo")  # Si no hay postulante, lanza un error
        self._postulante = value  # Asigna el postulante validado

    @property
    def carrera(self):  # Getter para la carrera
        return self._carrera  # Devuelve la carrera asignada

    @carrera.setter
    def carrera(self, value):  # Setter para validar la carrera
        if not value:
            raise ValueError("La carrera no puede ser nula")  # Evita que la carrera sea vacía
        self._carrera = value  # Asigna la carrera al objeto

    @property
    def sede(self):  # Getter para la sede
        return self._sede  # Retorna la sede actual

    @sede.setter
    def sede(self, value):  # Setter que valida si la sede pertenece a la universidad del postulante
        if not value in self._postulante.universidad.sedes: 
            raise ValueError("Sede no válida")  # Comprueba que la sede exista dentro de las sedes registradas
        self._sede = value  # Asigna la sede si es válida

    @property
    def evaluacion(self):  # Getter para la evaluación asociada
        return self._evaluacion  # Devuelve el objeto Evaluacion

    @evaluacion.setter
    def evaluacion(self, value):  # Setter que valida el tipo de dato asignado
        if not isinstance(value, Evaluacion): 
            raise ValueError("Debe ser un objeto Evaluacion")  # Asegura que el valor sea de tipo Evaluacion
        self._evaluacion = value  # Asigna la evaluación al objeto

    def iniciar_evaluacion(self):  # Método para iniciar la evaluación
        return self._evaluacion.iniciar_evaluacion()  # Llama al método iniciar_evaluacion() de la clase Evaluacion

    def finalizar_evaluacion(self):  # Método para finalizar la evaluación
        return self._evaluacion.finalizar_evaluacion()  # Llama al método finalizar_evaluacion() de Evaluacion

    def obtener_info(self):  # Método para obtener un resumen de la postulación
        return f"Postulación {self._nombre} (Código: {self._codigo}) de {self._postulante.nombre} a {self._carrera.nombre} en {self._sede} - {self._evaluacion.obtener_info().split('-')[1].strip()} - Estado: {self._estado}"  # Devuelve una cadena con toda la información formateada

    @classmethod
    def total_postulaciones(cls):  # Método de clase que devuelve el total de postulaciones
        return cls._total_postulaciones  # Retorna el contador de postulaciones creadas

    def to_public_dict(self) -> dict:
        """Representación pública de la postulación; incluye información pública del postulante si está disponible."""
        postulante_public = None
        try:
            postulante_public = self._postulante.to_public_dict()
        except Exception:
            # Fallback: exponer sólo nombre si no tiene método
            postulante_public = getattr(self._postulante, "_nombre", str(self._postulante))

        return {
            "codigo": getattr(self, "_codigo", None),
            "nombre": getattr(self, "_nombre", None),
            "carrera": getattr(self, "_carrera", None),
            "sede": getattr(self, "_sede", None),
            "postulante": postulante_public,
            "estado": getattr(self, "_estado", None),
        }
