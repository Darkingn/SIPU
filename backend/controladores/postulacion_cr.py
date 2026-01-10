from fastapi import FastAPI, HTTPException
from typing import List

# =====================================================
# MODELOS SIMPLES (referencias mínimas)
# =====================================================

class Postulante:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre


class Carrera:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre


class Evaluacion:
    def __init__(self, codigo, estado):
        self.codigo = codigo
        self.estado = estado


# =====================================================
# MODELO POSTULACIÓN
# =====================================================

class Postulacion:
    def __init__(self, codigo, postulante, carrera, sede, evaluacion):
        self.codigo = codigo
        self.postulante = postulante
        self.carrera = carrera
        self.sede = sede
        self.evaluacion = evaluacion
        self.estado = "Registrada"


# =====================================================
# REPOSITORY (EN MEMORIA)
# =====================================================

class PostulacionRepository:
    def __init__(self):
        self._postulaciones: List[Postulacion] = []

    def guardar(self, postulacion: Postulacion):
        if any(p.codigo == postulacion.codigo for p in self._postulaciones):
            raise ValueError("La postulación ya existe")
        self._postulaciones.append(postulacion)

    def listar(self):
        return self._postulaciones

    def buscar(self, codigo):
        for p in self._postulaciones:
            if p.codigo == codigo:
                return p
        return None


# =====================================================
# CONTROLLER
# =====================================================

app = FastAPI(title="API Postulaciones")

repo = PostulacionRepository()


@app.post("/postulaciones")
def crear_postulacion(
    codigo: str,
    codigo_postulante: str,
    nombre_postulante: str,
    codigo_carrera: str,
    nombre_carrera: str,
    sede: str,
    codigo_evaluacion: str
):
    try:
        postulante = Postulante(codigo_postulante, nombre_postulante)
        carrera = Carrera(codigo_carrera, nombre_carrera)
        evaluacion = Evaluacion(codigo_evaluacion, "Programada")

        postulacion = Postulacion(
            codigo,
            postulante,
            carrera,
            sede,
            evaluacion
        )

        repo.guardar(postulacion)
        return {"mensaje": "Postulación creada correctamente"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/postulaciones")
def listar_postulaciones():
    return [
        {
            "codigo": p.codigo,
            "postulante": p.postulante.nombre,
            "carrera": p.carrera.nombre,
            "sede": p.sede,
            "evaluacion": p.evaluacion.codigo,
            "estado": p.estado
        }
        for p in repo.listar()
    ]


@app.get("/postulaciones/{codigo}")
def obtener_postulacion(codigo: str):
    p = repo.buscar(codigo)
    if not p:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")

    return {
        "codigo": p.codigo,
        "postulante": p.postulante.nombre,
        "carrera": p.carrera.nombre,
        "sede": p.sede,
        "evaluacion": p.evaluacion.codigo,
        "estado": p.estado
    }
