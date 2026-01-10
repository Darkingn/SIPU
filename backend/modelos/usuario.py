from enum import Enum
from abc import ABC

# --- OCP: Definición de Roles Extensible ---
class RolUsuario(Enum):
    ESTUDIANTE = "Estudiante"
    ADMINISTRADOR = "Administrador"
    DOCENTE = "Docente"  # Fácil de añadir sin tocar lógica compleja

# --- SRP: Clase Base para Entidades Físicas ---
class Persona(ABC):
    def __init__(self, cedula: str, nombre: str, correo: str):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo

# --- SRP: Entidad Usuario enfocada en Identidad ---
class Usuario(Persona):
    def __init__(self, codigo: str, nombre: str, cedula: str, correo: str, rol: RolUsuario):
        super().__init__(cedula, nombre, correo)
        self.codigo = codigo
        self.rol = rol

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, value):
        if "@" not in value: # Validación básica (podría ser un validador externo)
            raise ValueError("Formato de correo inválido")
        self._correo = value

    def obtener_info(self):
        return (f"Usuario: {self.nombre} (ID: {self.codigo})\n"
                f"Cédula: {self.cedula} | Rol: {self.rol.value}")

# --- SRP: Gestor de Usuarios (Repository Pattern) ---
class UsuarioRepository:
    def __init__(self):
        self._usuarios = []

    def registrar_usuario(self, usuario: Usuario):
        self._usuarios.append(usuario)
        print(f"Sistema: Usuario '{usuario.nombre}' registrado con éxito.")

    @property
    def total(self):
        return len(self._usuarios)

# --- USO DEL SISTEMA ---

repo = UsuarioRepository()

# Creación de usuario usando el Enum de Roles
nuevo_usuario = Usuario(
    codigo="USR-100",
    nombre="Ana Martínez",
    cedula="0987654321",
    correo="ana.mtz@universidad.edu",
    rol=RolUsuario.ADMINISTRADOR
)

repo.registrar_usuario(nuevo_usuario)

print("-" * 30)
print(nuevo_usuario.obtener_info())
print(f"Total de usuarios en base de datos: {repo.total}")