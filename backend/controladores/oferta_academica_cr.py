from fastapi import FastAPI, HTTPException
from typing import List

# =====================================================
# MODELOS SIMPLES
# =====================================================

class Carrera:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre


class ProcesoAdmision:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre


# =====================================================
# MODELO OFERTA ACADÉMICA
# =====================================================

class OfertaAcademica:
    def __init__(self, codigo, carrera, sede, proceso):
        self.codigo = codigo
        self.carrera = carrera
        self.sede = sede
        self.proceso = proceso
        self.estado = "Activa"


# =====================================================
# REPOSITORY (MEMORIA)
# =====================================================

class OfertaAcademicaRepository:
    def __init__(self):
        self._ofertas: List[OfertaAcademica] = []

    def guardar(self, oferta: OfertaAcademica):
        if any(o.codigo == oferta.codigo for o in self._ofertas):
            raise ValueError("La oferta académica ya existe")
        self._ofertas.append(oferta)

    def listar(self):
        return self._ofertas

    def buscar(self, codigo):
        for o in self._ofertas:
            if o.codigo == codigo:
                return o
        return None


# =====================================================
# CONTROLLER
# =====================================================

app = FastAPI(title="API Oferta Académica")

repo = OfertaAcademicaRepository()


@app.post("/ofertas")
def crear_oferta(
    codigo: str,
    codigo_carrera: str,
    nombre_carrera: str,
    sede: str,
    codigo_proceso: str,
    nombre_proceso: str
):
    try:
        carrera = Carrera(codigo_carrera, nombre_carrera)
        proceso = ProcesoAdmision(codigo_proceso, nombre_proceso)

        oferta = OfertaAcademica(
            codigo,
            carrera,
            sede,
            proceso
        )

        repo.guardar(oferta)
        return {"mensaje": "Oferta académica creada correctamente"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/ofertas")
def listar_ofertas():
    return [
        {
            "codigo": o.codigo,
            "carrera": o.carrera.nombre,
            "sede": o.sede,
            "proceso": o.proceso.nombre,
            "estado": o.estado
        }
        for o in repo.listar()
    ]


@app.get("/ofertas/{codigo}")
def obtener_oferta(codigo: str):
    o = repo.buscar(codigo)
    if not o:
        raise HTTPException(status_code=404, detail="Oferta académica no encontrada")

    return {
        "codigo": o.codigo,
        "carrera": o.carrera.nombre,
        "sede": o.sede,
        "proceso": o.proceso.nombre,
        "estado": o.estado
    }
