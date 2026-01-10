from pydantic import BaseModel
from enum import Enum

class RolUsuarioSchema(str, Enum):
    ESTUDIANTE = "Estudiante"
    ADMINISTRADOR = "Administrador"
    DOCENTE = "Docente"

class PersonaBase(BaseModel):
    cedula: str
    nombre: str
    correo: str

class UsuarioBase(PersonaBase):
    codigo: str
    rol: RolUsuarioSchema

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    pass

class UsuarioInfoResponse(BaseModel):
    info: str