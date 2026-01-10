from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# =====================================================
# MODELO DE DOMINIO
# =====================================================

class Carrera:
    def __init__(self, codigo: str, nombre: str, area: str, cupos: int):
        self.codigo = codigo
        self.nombre = nombre
        self.area = area
        self.cupos = cupos

    def obtener_info(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "area": self.area,
            "cupos": self.cupos
        }


# =====================================================
# SCHEMAS
# =====================================================

class CarreraCreateSchema(BaseModel):
    codigo: str
    nombre: str
    area: str
    cupos: int


class CarreraResponseSchema(BaseModel):
    codigo: str
    nombre: str
    area: str
    cupos: int


# =====================================================
# REPOSITORIO SIMPLE
# =====================================================

class CarreraRepository:
    def __init__(self):
        self._carreras = {}

    def guardar(self, carrera: Carrera):
        if carrera.codigo in self._carreras:
            raise ValueError("La carrera ya existe")
        self._carreras[carrera.codigo] = carrera

    def listar(self):
        return list(self._carreras.values())

    def obtener(self, codigo: str):
        return self._carreras.get(codigo)


# =====================================================
# CONTROLLER
# =====================================================

app = FastAPI(title="Carrera Controller")

repo = CarreraRepository()


@app.post("/carreras", response_model=CarreraResponseSchema)
def crear_carrera(data: CarreraCreateSchema):
    carrera = Carrera(
        codigo=data.codigo,
        nombre=data.nombre,
        area=data.area,
        cupos=data.cupos
    )

    try:
        repo.guardar(carrera)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return carrera.obtener_info()


@app.get("/carreras", response_model=List[CarreraResponseSchema])
def listar_carreras():
    return [c.obtener_info() for c in repo.listar()]


@app.get("/carreras/{codigo}", response_model=CarreraResponseSchema)
def obtener_carrera(codigo: str):
    carrera = repo.obtener(codigo)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera.obtener_info()
