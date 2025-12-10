from modelos.proceso_admision import ProcesoAdmision
from modelos.base_model import BaseModel
from utils.validators import validate_email, validate_cedula, validate_phone, validate_required
from utils.error_handler import ValidationError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Evitar import circular en tiempo de ejecución: import en tiempo de ejecución dentro del método
    from servicios.postulante_service import PostulanteService
from utils.privacy import mask_id, mask_email, mask_phone, hash_value

class Postulante(ProcesoAdmision, BaseModel):  # Hereda de ProcesoAdmision y BaseModel
    _total_postulantes = 0  # Atributo de clase para contar cuántos postulantes se han creado

    def __init__(self, codigo, nombre, fecha_inicio, cedula, correo, telefono, rol, puntaje):
        super().__init__(codigo, nombre, fecha_inicio, "Sistema")  # Se inicializan los atributos heredados de la clase padre
        self._cedula = cedula  # Se almacena la cédula del postulante
        self._correo = correo  # Se guarda el correo electrónico del postulante
        self._telefono = telefono  # Se asigna el número telefónico
        self._rol = rol  # Se guarda el rol del postulante (por ejemplo: aspirante, estudiante, etc.)
        self._puntaje = puntaje  # Se guarda el puntaje del postulante
        Postulante._total_postulantes += 1  # Cada vez que se crea un postulante, se incrementa el contador total

    @property
    def cedula(self):  # Getter para obtener la cédula
        return self._cedula  # Devuelve la cédula actual del postulante

    @cedula.setter
    def cedula(self, value):  # Setter que valida y asigna la cédula
        validate_cedula(value)  # Usa el validador de cédula
        self._cedula = value

    @property
    def correo(self):  # Getter para obtener el correo
        return self._correo  # Retorna el correo del postulante

    @correo.setter
    def correo(self, value):  # Setter que valida el formato del correo electrónico
        validate_email(value)  # Usa el validador de email
        self._correo = value

    @property
    def telefono(self):  # Getter para obtener el número de teléfono
        return self._telefono  # Devuelve el número actual

    @telefono.setter
    def telefono(self, value):  # Setter para validar el teléfono
        validate_phone(value)  # Usa el validador de teléfono
        self._telefono = value

    @property
    def rol(self):  # Getter para acceder al rol del postulante
        return self._rol  # Devuelve el rol (por ejemplo, postulante o estudiante)

    @rol.setter
    def rol(self, value):  # Setter que valida el rol ingresado
        validate_required(value, "Rol")  # Usa el validador de campos requeridos
        self._rol = value  # Asigna el rol al postulante

    @property
    def puntaje(self):  # Getter para el puntaje del postulante
        return self._puntaje  # Devuelve el puntaje actual

    @puntaje.setter
    def puntaje(self, value):  # Setter que valida el puntaje
        if value < 0: 
            raise ValueError("El puntaje no puede ser negativo")  # Se asegura de que el puntaje sea positivo
        self._puntaje = value  # Asigna el valor validado al atributo

    def inscribirse(self, comentario=None):  # Método que permite inscribirse con un comentario opcional
        # Delegamos la lógica de negocio a PostulanteService (SRP).
        # Importar en tiempo de ejecución para evitar ciclos de importación.
        try:
            from servicios.postulante_service import PostulanteService
        except Exception:
            # Si no está disponible, mantenemos comportamiento local como fallback.
            if self._estado == "No iniciado":
                self._estado = "Inscrito"
                if comentario:
                    return f"{self._nombre} se ha inscrito correctamente - Comentario: {comentario}"
                return f"{self._nombre} se ha inscrito correctamente"
            raise ValueError("El postulante no está en estado 'No iniciado'")

        # Usar el servicio para ejecutar la inscripción
        return PostulanteService.inscribir(self, comentario)

    def obtener_informacion(self):  # Método que muestra toda la información relevante del postulante
        return f"Postulante {self._nombre} (Código: {self._codigo}, Cédula: {self._cedula}) - Correo: {self._correo}, Rol: {self._rol}, Estado: {self._estado}, Puntaje: {self._puntaje}"  # Devuelve un resumen formateado

    @classmethod
    def total_postulantes(cls):  # Método de clase que devuelve el total de postulantes creados
        return cls._total_postulantes  # Retorna el contador global de postulantes

    def to_public_dict(self) -> dict:
        """Devuelve una representación pública del postulante con PII enmascarada."""
        data = {
            "codigo": getattr(self, "_codigo", None),
            "nombres": getattr(self, "_nombre", None),
            "rol": getattr(self, "_rol", None),
            "estado": getattr(self, "_estado", None),
            "puntaje": getattr(self, "_puntaje", None),
            # Masked PII
            "cedula_masked": mask_id(getattr(self, "_cedula", None)),
            "correo_masked": mask_email(getattr(self, "_correo", None)),
            "telefono_masked": mask_phone(getattr(self, "_telefono", None)),
            # Hash for internal matching without exposing raw id
            "ident_hash": hash_value(getattr(self, "_cedula", None)),
        }
        return data
