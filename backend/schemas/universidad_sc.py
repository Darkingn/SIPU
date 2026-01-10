from pydantic import BaseModel
from enum import Enum
from typing import List, Dict

class TipoUniversidadSchema(str, Enum):
    PUBLICA = "Pública"
    PRIVADA = "Privada"
    COFINANCIADA = "Cofinanciada"

class SedeSchema(BaseModel):
    nombre: str
    inscripciones_abiertas: bool

class UniversidadBase(BaseModel):
    codigo: str
    nombre: str
    tipo: TipoUniversidadSchema
    ubicacion: str

class UniversidadCreate(UniversidadBase):
    sedes: List[str]

class UniversidadResponse(UniversidadBase):
    sedes: Dict[str, SedeSchema]

class GestionInscripcionSede(BaseModel):
    nombre_sede: str
    abrir: bool

class UniversidadInfoResponse(BaseModel):
    info: str