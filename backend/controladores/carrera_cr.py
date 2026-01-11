from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.servicios.supabase_service import SupabaseService


# =====================================================
# SCHEMAS
# =====================================================

class CarreraCreate(BaseModel):
    codigo: str
    nombre: str
    duracion: int
    modalidad: str


class CarreraResponse(BaseModel):
    id: Optional[int] = None
    codigo: str
    nombre: str
    duracion: int
    modalidad: str


class CarreraUpdate(BaseModel):
    nombre: Optional[str] = None
    duracion: Optional[int] = None
    modalidad: Optional[str] = None


# =====================================================
# ROUTER
# =====================================================

router = APIRouter(prefix="/carreras", tags=["carreras"])
service = SupabaseService()


@router.get("", response_model=List[CarreraResponse])
def listar_carreras():
    """Obtiene todas las carreras."""
    try:
        resultado = service.select("carreras")
        return resultado.data if hasattr(resultado, 'data') else resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{carrera_id}", response_model=CarreraResponse)
def obtener_carrera(carrera_id: int):
    """Obtiene una carrera por ID."""
    try:
        resultado = service.select("carreras", filters={"id": carrera_id})
        data = resultado.data if hasattr(resultado, 'data') else resultado
        if not data or len(data) == 0:
            raise HTTPException(status_code=404, detail="Carrera no encontrada")
        return data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=CarreraResponse, status_code=201)
def crear_carrera(carrera: CarreraCreate):
    """Crea una nueva carrera."""
    try:
        resultado = service.insert("carreras", [carrera.dict()])
        data = resultado.data if hasattr(resultado, 'data') else resultado
        return data[0] if data else carrera.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{carrera_id}", response_model=CarreraResponse)
def actualizar_carrera(carrera_id: int, carrera: CarreraUpdate):
    """Actualiza una carrera existente."""
    try:
        datos = {k: v for k, v in carrera.dict().items() if v is not None}
        if not datos:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        resultado = service.update("carreras", {"id": carrera_id}, datos)
        data = resultado.data if hasattr(resultado, 'data') else resultado
        return data[0] if data else None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{carrera_id}", status_code=204)
def eliminar_carrera(carrera_id: int):
    """Elimina una carrera."""
    try:
        service.delete("carreras", {"id": carrera_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
