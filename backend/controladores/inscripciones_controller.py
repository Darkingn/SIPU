from backend.modelos.estudiante import Estudiante
from backend.servicios.supabase_service import supabase

class InscripcionesController:
    def registrar_estudiante(self, estudiante: Estudiante):
        data = {
            "id": estudiante.id,
            "nombre": estudiante.nombre,
            "correo": estudiante.correo,
            "carrera": estudiante.carrera
        }
        res = supabase.table("estudiantes").insert(data).execute()
        return res
