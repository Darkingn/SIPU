from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List, Dict

# =====================================================
# MODELO DE DOMINIO
# =====================================================

class TipoUniversidad(str, Enum):
    PUBLICA = "Publica"
    PRIVADA = "Privada"
    COFINANCIADA = "Cofinanciada"


class Sede:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.inscripciones_abiertas = False

    def abrir_inscripciones(self):
        self.inscripciones_abiertas = True

    def cerrar_inscripciones(self):
        self.inscripciones_abiertas = False


class Universidad:
    def __init__(self, codigo: str, nombre: str, tipo: TipoUniversidad, ubicacion: str):
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.ubicacion = ubicacion
        self.sedes: Dict[str, Sede] = {}

    def agregar_sede(self, nombre_sede: str):
        if nombre_sede in self.sedes:
            raise ValueError("La sede ya existe")
        self.sedes[nombre_sede] = Sede(nombre_sede)

    def gestionar_inscripcion(self, nombre_sede: str, abrir: bool):
        sede = self.sedes.get(nombre_sede)
        if not sede:
            raise ValueError("La sede no existe")

        if abrir:
            sede.abrir_inscripciones()
        else:
            sede.cerrar_inscripciones()

    def obtener_info(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "ubicacion": self.ubicacion,
            "sedes": [
                {
                    "nombre": s.nombre,
                    "inscripciones_abiertas": s.inscripciones_abiertas
                }
                for s in self.sedes.values()
            ]
        }


# =====================================================
# SCHEMAS
# =====================================================

class UniversidadCreateSchema(BaseModel):
    codigo: str
    nombre: str
    tipo: TipoUniversidad
    ubicacion: str


class SedeCreateSchema(BaseModel):
    nombre: str


class GestionInscripcionSchema(BaseModel):
    abrir: bool


# =====================================================
# REPOSITORIO SIMPLE
# =====================================================

class UniversidadRepository:
    def __init__(self):
        self._universidades: Dict[str, Universidad] = {}

    def guardar(self, universidad: Universidad):
        if universidad.codigo in self._universidades:
            raise ValueError("La universidad ya existe")
        self._universidades[universidad.codigo] = universidad

    def obtener(self, codigo: str):
        return self._universidades.get(codigo)

    def listar(self):
        return list(self._universidades.values())


# =====================================================
# CONTROLLER
# =====================================================

app = FastAPI(title="Universidad Controller")

repo = UniversidadRepository()


@app.post("/universidades")
def crear_universidad(data: UniversidadCreateSchema):
    try:
        universidad = Universidad(
            codigo=data.codigo,
            nombre=data.nombre,
            tipo=data.tipo,
            ubicacion=data.ubicacion
        )
        repo.guardar(universidad)
        return universidad.obtener_info()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/universidades")
def listar_universidades():
    return [u.obtener_info() for u in repo.listar()]


@app.post("/universidades/{codigo}/sedes")
def agregar_sede(codigo: str, data: SedeCreateSchema):
    universidad = repo.obtener(codigo)
    if not universidad:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")

    try:
        universidad.agregar_sede(data.nombre)
        return {"mensaje": "Sede agregada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/universidades/{codigo}/sedes/{nombre_sede}/inscripciones")
def gestionar_inscripciones(codigo: str, nombre_sede: str, data: GestionInscripcionSchema):
    universidad = repo.obtener(codigo)
    if not universidad:
        raise HTTPException(status_code=404, detail="Universidad no encontrada")

    try:
        universidad.gestionar_inscripcion(nombre_sede, data.abrir)
        estado = "abiertas" if data.abrir else "cerradas"
        return {"mensaje": f"Inscripciones {estado} en la sede {nombre_sede}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
