from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# =====================================================
# MODELOS DE DOMINIO
# =====================================================

class InventarioRecursos:
    def __init__(self, laboratorios: int = 0, computadoras: int = 0):
        self.laboratorios = laboratorios
        self.computadoras = computadoras

    def agregar_laboratorio(self):
        self.laboratorios += 1

    def agregar_computadoras(self, cantidad: int):
        if cantidad < 0:
            raise ValueError("Cantidad inválida")
        self.computadoras += cantidad


class Facultad:
    def __init__(self, codigo: str, nombre: str, decano: str):
        self.codigo = codigo
        self.nombre = nombre
        self.decano = decano
        self.recursos = InventarioRecursos()

    def obtener_info(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "decano": self.decano,
            "laboratorios": self.recursos.laboratorios,
            "computadoras": self.recursos.computadoras
        }


# =====================================================
# SCHEMAS
# =====================================================

class FacultadCreateSchema(BaseModel):
    codigo: str
    nombre: str
    decano: str


class ComputadorasSchema(BaseModel):
    cantidad: int


# =====================================================
# REPOSITORIO SIMPLE
# =====================================================

class FacultadRepository:
    def __init__(self):
        self._facultades: Dict[str, Facultad] = {}

    def guardar(self, facultad: Facultad):
        if facultad.codigo in self._facultades:
            raise ValueError("La facultad ya existe")
        self._facultades[facultad.codigo] = facultad

    def obtener(self, codigo: str):
        return self._facultades.get(codigo)

    def listar(self):
        return list(self._facultades.values())


# =====================================================
# CONTROLLER
# =====================================================

app = FastAPI(title="Facultad Controller")

repo = FacultadRepository()


@app.post("/facultades")
def crear_facultad(data: FacultadCreateSchema):
    try:
        facultad = Facultad(
            codigo=data.codigo,
            nombre=data.nombre,
            decano=data.decano
        )
        repo.guardar(facultad)
        return facultad.obtener_info()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/facultades")
def listar_facultades():
    return [f.obtener_info() for f in repo.listar()]


@app.post("/facultades/{codigo}/laboratorios")
def agregar_laboratorio(codigo: str):
    facultad = repo.obtener(codigo)
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    facultad.recursos.agregar_laboratorio()
    return {"mensaje": "Laboratorio agregado correctamente"}


@app.post("/facultades/{codigo}/computadoras")
def agregar_computadoras(codigo: str, data: ComputadorasSchema):
    facultad = repo.obtener(codigo)
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    try:
        facultad.recursos.agregar_computadoras(data.cantidad)
        return {"mensaje": f"{data.cantidad} computadoras agregadas"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
