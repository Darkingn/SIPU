from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactoSchema(BaseModel):
    correo: EmailStr
    telefono: str

class PostulanteBase(BaseModel):
    id_postulante: str
    nombre: str
    cedula: str
    contacto: ContactoSchema
    rol: str
    puntaje: int

class PostulanteCreate(PostulanteBase):
    pass

class PostulanteResponse(PostulanteBase):
    pass


class PostulanteResumenResponse(BaseModel):
    resumen: str

class InscripcionCreate(BaseModel):
    id_postulante: str
    comentario: Optional[str] = None

class InscripcionResponse(BaseModel):
    mensaje: str