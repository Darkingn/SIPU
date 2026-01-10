from pydantic import BaseModel
from enum import Enum
from typing import Literal


class EstadoEvaluacionSchema(str, Enum):
    PROGRAMADA = "Programada"
    EN_CURSO = "En curso"
    FINALIZADA = "Finalizada"


class EvaluacionBase(BaseModel):
    codigo: str
    nombre: str
    fecha: str
    hora: str
    sala: str
    duracion: int
    tipo: str

class EvaluacionCreate(EvaluacionBase):
    pass

class EvaluacionResponse(EvaluacionBase):
    estado: EstadoEvaluacionSchema


class EvaluacionAccionResponse(BaseModel):
    mensaje: str
