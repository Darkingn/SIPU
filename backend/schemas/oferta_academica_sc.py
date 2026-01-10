from pydantic import BaseModel
from typing import List

class OfertaAcademicaBase(BaseModel):
    codigo: str
    nombre: str
    cupos_totales: int

class OfertaAcademicaCreate(OfertaAcademicaBase):
    pass

class OfertaAcademicaResponse(OfertaAcademicaBase):
    num_carreras: int
    num_areas: int

class OfertaAgregarCarrera(BaseModel):
    carrera: str
    area_nombre: str
    
class OfertaInfoResponse(BaseModel):
    info: str