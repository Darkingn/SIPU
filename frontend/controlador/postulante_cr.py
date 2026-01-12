from servicios.api_servicio import ApiService

class PostulanteController:

    def crear_postulante(self, data: dict):
        if not data.get("nombre") or not data.get("cedula"):
            raise ValueError("Nombre y cédula son obligatorios")

        return ApiService.post("/postulantes", data)

    def listar_postulantes(self):
        return ApiService.get("/postulantes")
