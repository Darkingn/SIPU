from pydantic import BaseModel


class InventarioRecursosSchema(BaseModel):
    laboratorios: int = 0
    computadoras: int = 0

class FacultadBase(BaseModel):
    codigo: str
    nombre: str
    decano: str
    recursos: InventarioRecursosSchema | None = None

class FacultadCreate(FacultadBase):
    pass

class FacultadResponse(FacultadBase):
    pass

class FacultadInfoResponse(BaseModel):
    info: str