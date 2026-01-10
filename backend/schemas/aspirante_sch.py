from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Union
from enum import Enum

class GrupoPrioridadSchema(str, Enum):
    GENERAL = "Bachilleres General"
    GAR = "Grupo de Alto Rendimiento"
    VULNERABILIDAD = "Situación de Vulnerabilidad"
    PUEBLOS = "Pueblos y Nacionalidades"
    FRONTERA = "Zona de Frontera"

class AspiranteBase(BaseModel):
    cedula: str = Field(..., min_length=10, max_length=10)
    nombre: str
    correo: EmailStr
    p_examen: float
    p_bachiller: float

class AspiranteGARCreate(AspiranteBase):
    tipo: Literal["GAR"]
    grupo: GrupoPrioridadSchema = GrupoPrioridadSchema.GAR

class AspiranteVulnerableCreate(AspiranteBase):
    tipo: Literal["VULNERABLE"]
    grupo: GrupoPrioridadSchema = GrupoPrioridadSchema.VULNERABILIDAD
    puntos_bono: int = Field(..., ge=15, le=45)

class AspiranteEscolarCreate(AspiranteBase):
    tipo: Literal["ESCOLAR"]
    grupo: GrupoPrioridadSchema = GrupoPrioridadSchema.GENERAL

class AspiranteEtniaCreate(AspiranteBase):
    tipo: Literal["ETNIA"]
    grupo: GrupoPrioridadSchema = GrupoPrioridadSchema.PUEBLOS

AspiranteCreate = Union[
    AspiranteGARCreate,
    AspiranteVulnerableCreate,
    AspiranteEscolarCreate,
    AspiranteEtniaCreate
]

class AspiranteResponse(BaseModel):
    cedula: str
    nombre: str
    correo: EmailStr
    tipo_aspirante: str
    puntaje_examen: float
    puntaje_bachiller: float
    puntaje_final: float
