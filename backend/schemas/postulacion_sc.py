from pydantic import BaseModel

class PostulacionBase(BaseModel):
    codigo: str
    postulante: str
    carrera: str
    sede: str
    evaluacion: str
    fecha_registro: str

class PostulacionCreate(BaseModel):
    postulante: str
    carrera: str
    sede: str
    evaluacion: str

class PostulacionResponse(PostulacionBase):
    pass

class PostulacionResumenResponse(BaseModel):
    resumen: str

class PostulacionAccionResponse(BaseModel):
    mensaje: str