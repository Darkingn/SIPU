from modelos.proceso_admision import ProcesoAdmision
from modelos.base_model import BaseModel
from utils.validators import validate_email, validate_cedula, validate_phone, validate_required
from utils.error_handler import ValidationError
from servicios.event_bus import emit

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

    def to_public_dict(self):
        """Devuelve un diccionario con datos públicos del postulante (sin PII sensible)."""
        return {
            "codigo": self._codigo,
            "nombre": self._nombre,
            "estado": self._estado,
            "rol": self._rol,
            "puntaje": self._puntaje
        }

    def to_dict(self):
        """Devuelve un diccionario completo del postulante (incluyendo datos sensibles)."""
        return {
            "codigo": self._codigo,
            "nombre": self._nombre,
            "fecha_inicio": self._fecha_inicio,
            "cedula": self._cedula,
            "correo": self._correo,
            "telefono": self._telefono,
            "rol": self._rol,
            "puntaje": self._puntaje,
            "estado": self._estado
        }

    def inscribirse(self, comentario=None):  # Método que permite inscribirse con un comentario opcional
        if self._estado == "No iniciado":  # Solo permite inscribirse si el estado está "No iniciado"
            self._estado = "Inscrito"  # Cambia el estado del postulante a inscrito
            # Emitir evento para notificaciones (patrón Observer)
            try:
                payload = {
                    "type": "postulante_inscrito",
                    "postulante": self.to_public_dict()
                }
                emit("postulante_inscrito", payload)
            except Exception:
                # No fallar la inscripción si el bus falla
                pass
            if comentario:  # Si el usuario agregó un comentario, lo incluye en el mensaje
                return f"{self._nombre} se ha inscrito correctamente - Comentario: {comentario}"  # Retorna mensaje con comentario
            return f"{self._nombre} se ha inscrito correctamente"  # Si no hay comentario, muestra mensaje simple
        raise ValueError("El postulante no está en estado 'No iniciado'")  # Si no cumple la condición, lanza un error

    def obtener_informacion(self):  # Método que muestra toda la información relevante del postulante
        return f"Postulante {self._nombre} (Código: {self._codigo}, Cédula: {self._cedula}) - Correo: {self._correo}, Rol: {self._rol}, Estado: {self._estado}, Puntaje: {self._puntaje}"  # Devuelve un resumen formateado

    @classmethod
    def total_postulantes(cls):  # Método de clase que devuelve el total de postulantes creados
        return cls._total_postulantes  # Retorna el contador global de postulantes
