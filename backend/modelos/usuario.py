from proceso_admision import ProcesoAdmision  # Importamos la clase base de procesos de admisión

class Usuario(ProcesoAdmision):  # Clase Usuario que hereda de ProcesoAdmision
    _total_usuarios = 0  # Contador de usuarios creados

    def __init__(self, codigo, nombre, fecha_inicio, cedula, correo, rol):
        super().__init__(codigo, nombre, fecha_inicio, "Sistema")  # Inicializamos atributos heredados
        self._cedula = cedula  # Guardamos la cédula del usuario
        self._correo = correo  # Guardamos el correo electrónico
        self._rol = rol  # Rol del usuario (Estudiante, Administrador, etc.)
        Usuario._total_usuarios += 1  # Incrementamos el contador de usuarios

    @property
    def cedula(self): return self._cedula  # Getter para obtener la cédula

    @cedula.setter
    def cedula(self, value):  # Setter que valida y asigna la cédula
        if not value.strip(): raise ValueError("La cédula no puede estar vacía")  # Validamos que no esté vacía
        self._cedula = value  # Asignamos el valor

    @property
    def correo(self): return self._correo  # Getter para obtener el correo

    @correo.setter
    def correo(self, value):  # Setter que valida y asigna el correo
        if not value.strip(): raise ValueError("El correo no puede estar vacío")  # Evita que quede vacío
        self._correo = value  # Asignamos el correo

    @property
    def rol(self): return self._rol  # Getter para obtener el rol del usuario

    @rol.setter
    def rol(self, value):  # Setter que valida y asigna el rol
        if value not in ["Estudiante", "Administrador"]: raise ValueError("Rol no válido")  # Solo permite valores válidos
        self._rol = value  # Guardamos el rol

    def obtener_info(self):  # Método que devuelve toda la información del usuario
        return f"Usuario {self._nombre} (Código: {self._codigo}, Cédula: {self._cedula}) - Correo: {self._correo}, Rol: {self._rol} - Estado: {self._estado}"  # Info completa

    @classmethod
    def total_usuarios(cls): return cls._total_usuarios  # Devuelve el total de usuarios creados
