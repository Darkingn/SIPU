from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date

# =====================================================
# MODELO DE DOMINIO
# =====================================================

class Periodo:
    def __init__(self, codigo: str, nombre: str, fecha_inicio: date, fecha_fin: date):
        if fecha_inicio > fecha_fin:
            raise ValueError("La fecha de inicio no puede ser mayor a la fecha fin")

        self.codigo = codigo
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def esta_activo(self, fecha_actual: date) -> bool:
        return self.fecha_inicio <= fecha_actual <= self.fecha_fin

    def obtener_info(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin
        }


# =====================================================
# SCHEMAS
# =====================================================

class PeriodoCreateSchema(BaseModel):
    codigo: str
    nombre: str
    fecha_inicio: date
    fecha_fin: date


class PeriodoResponseSchema(BaseModel):
    codigo: str
    nombre: str
    fecha_inicio: date
    fecha_fin: date


# =====================================================
# REPOSITORIO SIMPLE
# =====================================================

class PeriodoRepository:
    def __init__(self):
        self._periodos = {}

    def guardar(self, periodo: Periodo):
        if periodo.codigo in self._periodos:
            raise ValueError("El periodo ya existe")
        self._periodos[periodo.codigo] = periodo

    def listar(self):
        return list(self._periodos.values())

    def obtener(self, codigo: str):
        return self._periodos.get(codigo)


# =====================================================
# CONTROLLER
# =====================================================

app = FastAPI(title="Periodo Controller")

repo = PeriodoRepository()


@app.post("/periodos", response_model=PeriodoResponseSchema)
def crear_periodo(data: PeriodoCreateSchema):
    try:
        periodo = Periodo(
            codigo=data.codigo,
            nombre=data.nombre,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin
        )
        repo.guardar(periodo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return periodo.obtener_info()


@app.get("/periodos", response_model=List[PeriodoResponseSchema])
def listar_periodos():
    return [p.obtener_info() for p in repo.listar()]


@app.get("/periodos/{codigo}", response_model=PeriodoResponseSchema)
def obtener_periodo(codigo: str):
    periodo = repo.obtener(codigo)
    if not periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    return periodo.obtener_info()


@app.get("/periodos/{codigo}/activo")
def estado_periodo(codigo: str):
    periodo = repo.obtener(codigo)
    if not periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")

    return {
        "codigo": codigo,
        "activo": periodo.esta_activo(date.today())
    }
