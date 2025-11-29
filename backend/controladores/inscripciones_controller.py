from modelos.postulante import Postulante
from servicios.supabase_service import SupabaseService

class InscripcionesController:
    def registrar_estudiante(self, estudiante: Postulante):
        data = {
            "id": estudiante.id,
            "nombre": estudiante.nombre,
            "correo": estudiante.correo,
            "carrera": estudiante.carrera
        }
        supabase = SupabaseService()
        res = supabase.client.table("estudiantes").insert(data).execute()
        return res
