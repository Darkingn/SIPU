from proceso_admision import ProcesoAdmision  # Se importa la clase base del proceso de admisión
import re  # Se importa el módulo 're' para validar correos con expresiones regulares

class Postulante(ProcesoAdmision):  # La clase Postulante hereda de ProcesoAdmision
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
        if not value.strip(): raise ValueError("La cédula no puede estar vacía")  # Evita que se ingrese una cédula vacía
        self._cedula = value  # Asigna el valor validado

    @property
    def correo(self):  # Getter para obtener el correo
        return self._correo  # Retorna el correo del postulante

    @correo.setter
    def correo(self, value):  # Setter que valida el formato del correo electrónico
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value): raise ValueError("Correo no válido")  # Usa una expresión regular para validar el formato
        self._correo = value  # Asigna el correo validado

    @property
    def telefono(self):  # Getter para obtener el número de teléfono
        return self._telefono  # Devuelve el número actual

    @telefono.setter
    def telefono(self, value):  # Setter para validar el teléfono
        if not value.strip(): raise ValueError("El teléfono no puede estar vacío")  # Se asegura de que no esté vacío
        self._telefono = value  # Asigna el número telefónico al atributo

    @property
    def rol(self):  # Getter para acceder al rol del postulante
        return self._rol  # Devuelve el rol (por ejemplo, postulante o estudiante)

    @rol.setter
    def rol(self, value):  # Setter que valida el rol ingresado
        if not value.strip():
            raise ValueError("El rol no puede estar vacío")  # Evita que quede sin rol asignado
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
        if self._estado == "No iniciado":  # Solo permite inscribirse si el estado está "No iniciado"
            self._estado = "Inscrito"  # Cambia el estado del postulante a inscrito
            if comentario:  # Si el usuario agregó un comentario, lo incluye en el mensaje
                return f"{self._nombre} se ha inscrito correctamente - Comentario: {comentario}"  # Retorna mensaje con comentario
            return f"{self._nombre} se ha inscrito correctamente"  # Si no hay comentario, muestra mensaje simple
        raise ValueError("El postulante no está en estado 'No iniciado'")  # Si no cumple la condición, lanza un error

    def obtener_informacion(self):  # Método que muestra toda la información relevante del postulante
        return f"Postulante {self._nombre} (Código: {self._codigo}, Cédula: {self._cedula}) - Correo: {self._correo}, Rol: {self._rol}, Estado: {self._estado}, Puntaje: {self._puntaje}"  # Devuelve un resumen formateado

    @classmethod
    def total_postulantes(cls):  # Método de clase que devuelve el total de postulantes creados
        return cls._total_postulantes  # Retorna el contador global de postulantes
