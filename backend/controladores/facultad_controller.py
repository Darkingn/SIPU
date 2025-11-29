# controladores/facultad_controller.py
from controladores.supabase_client import supabase

class FacultadController:

    @staticmethod
    def obtener_facultades():
        res = supabase.table("facultades").select("*").execute()
        return res.data

    @staticmethod
    def crear_facultad(nombre, descripcion=""):
        data = {
            "nombre": nombre,
            "descripcion": descripcion
        }
        return supabase.table("facultades").insert(data).execute()

    @staticmethod
    def eliminar_facultad(id_facultad):
        return supabase.table("facultades").delete().eq("id", id_facultad).execute()
