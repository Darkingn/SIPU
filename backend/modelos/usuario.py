from proceso_admision import ProcesoAdmision  # Importamos la clase base de procesos de admisión
from typing import Optional
from modelos.interfaces import IAuthProvider

class Usuario(ProcesoAdmision):  # Clase Usuario que hereda de ProcesoAdmision
    _total_usuarios = 0  # Contador de usuarios creados

    def __init__(self, codigo, nombre, fecha_inicio, cedula, correo, rol, auth_provider: Optional[IAuthProvider] = None):
        super().__init__(codigo, nombre, fecha_inicio, "Sistema")  # Inicializamos atributos heredados
        self._cedula = cedula  # Guardamos la cédula del usuario
        self._correo = correo  # Guardamos el correo electrónico
        self._rol = rol  # Rol del usuario (Estudiante, Administrador, etc.)
        # Inyectamos una abstracción para autenticación/validación externa (DIP)
        self._auth_provider = auth_provider
        Usuario._total_usuarios += 1  # Incrementamos el contador de usuarios

    @property
    def cedula(self):
        return self._cedula  # Getter para obtener la cédula

    @cedula.setter
    def cedula(self, value):  # Setter que valida y asigna la cédula
        if not value.strip():
            raise ValueError("La cédula no puede estar vacía")  # Validamos que no esté vacía
        self._cedula = value  # Asignamos el valor

    @property
    def correo(self):
        return self._correo  # Getter para obtener el correo

    @correo.setter
    def correo(self, value):  # Setter que valida y asigna el correo
        if not value.strip():
            raise ValueError("El correo no puede estar vacío")  # Evita que quede vacío
        self._correo = value  # Asignamos el correo

    @property
    def rol(self): 
        return self._rol  # Getter para obtener el rol del usuario

    @rol.setter
    def rol(self, value):  # Setter que valida y asigna el rol
        if value not in ["Estudiante", "Administrador"]: 
            raise ValueError("Rol no válido")  # Solo permite valores válidos
        self._rol = value  # Guardamos el rol

    def obtener_info(self):  # Método que devuelve toda la información del usuario
        return f"Usuario {self._nombre} (Código: {self._codigo}, Cédula: {self._cedula}) - Correo: {self._correo}, Rol: {self._rol} - Estado: {self._estado}"  # Info completa

    @classmethod
    def total_usuarios(cls):
        return cls._total_usuarios  # Devuelve el total de usuarios creados

    def authenticate(self, credentials: dict) -> bool:
        """Intenta autenticar al usuario usando un proveedor inyectado.

        Esta pequeña adaptación introduce DIP: la lógica de autenticar depende de una
        abstracción (IAuthProvider) en vez de una implementación concreta.
        """
        if not self._auth_provider:
            # Sin proveedor, comportamiento por defecto: fallar la autenticación
            return False
        return self._auth_provider.authenticate(self._codigo, credentials)

    def to_public_dict(self) -> dict:
        """Representación pública de Usuario con PII enmascarada."""
        from utils.privacy import mask_id, mask_email

        return {
            "codigo": getattr(self, "_codigo", None),
            "nombre": getattr(self, "_nombre", None),
            "rol": getattr(self, "_rol", None),
            "estado": getattr(self, "_estado", None),
            "cedula_masked": mask_id(getattr(self, "_cedula", None)),
            "correo_masked": mask_email(getattr(self, "_correo", None)),
        }
