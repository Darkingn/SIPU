from pydantic import BaseModel
from typing import Literal


PRESENCIAL = "Presencial"
VIRTUAL = "Virtual"
HIBRIDA = "Híbrida"

class CarreraBase(BaseModel):
    codigo: str
    nombre: str
    duracion: int
    modalidad: Literal[
        ModalidadSchema.PRESENCIAL,
        ModalidadSchema.VIRTUAL,
        ModalidadSchema.HIBRIDA,
    ]

class CarreraCreate(CarreraBase):
    pass


class CarreraResponse(CarreraBase):
    pass


class CarreraInfoResponse(BaseModel):
    info: str
