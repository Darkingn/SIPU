from modelos.postulante import Postulante
from servicios.supabase_service import SupabaseService

class InscripcionesController:
    def registrar_estudiante(self, estudiante: Postulante):
        data = {
            "codigo": estudiante._codigo,
            "nombre": estudiante._nombre,
            "correo": estudiante._correo,
            "telefono": estudiante._telefono,
            "rol": estudiante._rol,
            "puntaje": estudiante._puntaje
        }
        supabase = SupabaseService()
        res = supabase.client.table("estudiantes").insert(data).execute()
        return res
