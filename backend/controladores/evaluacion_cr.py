from fastapi import FastAPI, HTTPException
from enum import Enum
from typing import List

# =====================================================
# MODELOS
# =====================================================

class EstadoEvaluacion(Enum):
    PROGRAMADA = "Programada"
    EN_CURSO = "En curso"
    FINALIZADA = "Finalizada"


class Evaluacion:
    def __init__(self, codigo, nombre, fecha, hora, sala, duracion, tipo):
        self.codigo = codigo
        self.nombre = nombre
        self.fecha = fecha
        self.hora = hora
        self.sala = sala
        self.duracion = duracion
        self.tipo = tipo
        self.estado = EstadoEvaluacion.PROGRAMADA


# =====================================================
# REPOSITORY (EN MEMORIA)
# =====================================================

class EvaluacionRepository:
    def __init__(self):
        self._evaluaciones: List[Evaluacion] = []

    def guardar(self, evaluacion: Evaluacion):
        if any(e.codigo == evaluacion.codigo for e in self._evaluaciones):
            raise ValueError("La evaluación ya existe")
        self._evaluaciones.append(evaluacion)

    def listar(self):
        return self._evaluaciones

    def buscar(self, codigo):
        for e in self._evaluaciones:
            if e.codigo == codigo:
                return e
        return None


# =====================================================
# CONTROLLER
# =====================================================

app = FastAPI(title="API Evaluaciones")

repo = EvaluacionRepository()


@app.post("/evaluaciones")
def crear_evaluacion(
    codigo: str,
    nombre: str,
    fecha: str,
    hora: str,
    sala: str,
    duracion: int,
    tipo: str
):
    try:
        evaluacion = Evaluacion(codigo, nombre, fecha, hora, sala, duracion, tipo)
        repo.guardar(evaluacion)
        return {"mensaje": "Evaluación registrada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/evaluaciones")
def listar_evaluaciones():
    return [
        {
            "codigo": e.codigo,
            "nombre": e.nombre,
            "fecha": e.fecha,
            "hora": e.hora,
            "sala": e.sala,
            "duracion": e.duracion,
            "tipo": e.tipo,
            "estado": e.estado.value
        }
        for e in repo.listar()
    ]


@app.put("/evaluaciones/{codigo}/iniciar")
def iniciar_evaluacion(codigo: str):
    evaluacion = repo.buscar(codigo)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    if evaluacion.estado != EstadoEvaluacion.PROGRAMADA:
        raise HTTPException(status_code=400, detail="La evaluación no puede iniciarse")

    evaluacion.estado = EstadoEvaluacion.EN_CURSO
    return {"mensaje": "Evaluación iniciada"}


@app.put("/evaluaciones/{codigo}/finalizar")
def finalizar_evaluacion(codigo: str):
    evaluacion = repo.buscar(codigo)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    if evaluacion.estado != EstadoEvaluacion.EN_CURSO:
        raise HTTPException(status_code=400, detail="La evaluación no puede finalizarse")

    evaluacion.estado = EstadoEvaluacion.FINALIZADA
    return {"mensaje": "Evaluación finalizada"}
