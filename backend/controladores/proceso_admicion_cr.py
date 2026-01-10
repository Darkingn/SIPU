from fastapi import FastAPI, HTTPException
from abc import ABC, abstractmethod
from typing import List

# =====================================================
# MODELOS DE ESTADO (STATE PATTERN)
# =====================================================

class EstadoProceso(ABC):
    @abstractmethod
    def manejar(self) -> str:
        pass


class EstadoNoIniciado(EstadoProceso):
    def manejar(self) -> str:
        return "No iniciado"


class EstadoIniciado(EstadoProceso):
    def manejar(self) -> str:
        return "Iniciado"


class EstadoFinalizado(EstadoProceso):
    def manejar(self) -> str:
        return "Finalizado"


# =====================================================
# MODELO PRINCIPAL
# =====================================================

class ProcesoAdmision:
    def __init__(self, codigo: str, nombre: str, responsable: str):
        self.codigo = codigo
        self.nombre = nombre
        self.responsable = responsable
        self._estado: EstadoProceso = EstadoNoIniciado()

    @property
    def estado_actual(self):
        return self._estado.manejar()

    def cambiar_estado(self, nuevo_estado: EstadoProceso):
        self._estado = nuevo_estado


# =====================================================
# REPOSITORY (EN MEMORIA)
# =====================================================

class ProcesoAdmisionRepository:
    def __init__(self):
        self._procesos: List[ProcesoAdmision] = []

    def guardar(self, proceso: ProcesoAdmision):
        if any(p.codigo == proceso.codigo for p in self._procesos):
            raise ValueError("El proceso ya existe")
        self._procesos.append(proceso)

    def listar(self):
        return self._procesos

    def buscar(self, codigo: str):
        for p in self._procesos:
            if p.codigo == codigo:
                return p
        return None


# =====================================================
# CONTROLLER
# =====================================================

app = FastAPI(title="API Proceso de Admisión")

repo = ProcesoAdmisionRepository()


@app.post("/procesos")
def crear_proceso(codigo: str, nombre: str, responsable: str):
    try:
        proceso = ProcesoAdmision(codigo, nombre, responsable)
        repo.guardar(proceso)
        return {"mensaje": "Proceso de admisión creado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/procesos")
def listar_procesos():
    return [
        {
            "codigo": p.codigo,
            "nombre": p.nombre,
            "responsable": p.responsable,
            "estado": p.estado_actual
        }
        for p in repo.listar()
    ]


@app.put("/procesos/{codigo}/iniciar")
def iniciar_proceso(codigo: str):
    proceso = repo.buscar(codigo)
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")

    proceso.cambiar_estado(EstadoIniciado())
    return {"mensaje": "Proceso iniciado"}


@app.put("/procesos/{codigo}/finalizar")
def finalizar_proceso(codigo: str):
    proceso = repo.buscar(codigo)
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")

    proceso.cambiar_estado(EstadoFinalizado())
    return {"mensaje": "Proceso finalizado"}
