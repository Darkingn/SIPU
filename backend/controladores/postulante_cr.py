from fastapi import FastAPI, HTTPException
from enum import Enum
from dataclasses import dataclass
from typing import List

# =====================================================
# MODELOS
# =====================================================

class RolPostulante(Enum):
    ASPIRANTE = "Aspirante"
    ESTUDIANTE = "Estudiante"


@dataclass(frozen=True)
class Contacto:
    correo: str
    telefono: str

    def __post_init__(self):
        if "@" not in self.correo:
            raise ValueError("Correo inválido")


class Postulante:
    def __init__(self, codigo, nombre, cedula, contacto: Contacto, rol, puntaje):
        self.codigo = codigo
        self.nombre = nombre
        self.cedula = cedula
        self.contacto = contacto
        self.rol = rol
        self.puntaje = puntaje


# =====================================================
# REPOSITORY (EN MEMORIA)
# =====================================================

class PostulanteRepository:
    def __init__(self):
        self._postulantes: List[Postulante] = []

    def guardar(self, postulante: Postulante):
        if any(p.codigo == postulante.codigo for p in self._postulantes):
            raise ValueError("Postulante ya registrado")
        self._postulantes.append(postulante)

    def listar(self):
        return self._postulantes

    def buscar(self, codigo):
        for p in self._postulantes:
            if p.codigo == codigo:
                return p
        return None


# =====================================================
# CONTROLLER
# =====================================================

app = FastAPI(title="API Postulantes - Sistema de Admisión")
repo = PostulanteRepository()


@app.post("/postulantes")
def crear_postulante(
    codigo: str,
    nombre: str,
    cedula: str,
    correo: str,
    telefono: str,
    rol: RolPostulante,
    puntaje: int
):
    try:
        contacto = Contacto(correo, telefono)
        postulante = Postulante(codigo, nombre, cedula, contacto, rol, puntaje)
        repo.guardar(postulante)
        return {"mensaje": "Postulante registrado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/postulantes")
def listar_postulantes():
    return [
        {
            "codigo": p.codigo,
            "nombre": p.nombre,
            "cedula": p.cedula,
            "correo": p.contacto.correo,
            "telefono": p.contacto.telefono,
            "rol": p.rol.value,
            "puntaje": p.puntaje
        }
        for p in repo.listar()
    ]


@app.get("/postulantes/{codigo}")
def obtener_postulante(codigo: str):
    p = repo.buscar(codigo)
    if not p:
        raise HTTPException(status_code=404, detail="Postulante no encontrado")

    return {
        "codigo": p.codigo,
        "nombre": p.nombre,
        "cedula": p.cedula,
        "correo": p.contacto.correo,
        "telefono": p.contacto.telefono,
        "rol": p.rol.value,
        "puntaje": p.puntaje
    }
