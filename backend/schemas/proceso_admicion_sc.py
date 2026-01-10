from pydantic import BaseModel
from enum import Enum

class EstadoProcesoSchema(str, Enum):
    NO_INICIADO = "No iniciado"
    INICIADO = "Iniciado"
    FINALIZADO = "Finalizado"

class ProcesoAdmisionBase(BaseModel):
    codigo: str
    nombre: str
    fecha_inicio: str
    responsable: str

class ProcesoAdmisionCreate(ProcesoAdmisionBase):
    pass

class ProcesoAdmisionResponse(ProcesoAdmisionBase):
    estado_actual: EstadoProcesoSchema

class ProcesoCambioEstado(BaseModel):
    nuevo_estado: EstadoProcesoSchema

class ProcesoAdmisionInfoResponse(BaseModel):
    info: str