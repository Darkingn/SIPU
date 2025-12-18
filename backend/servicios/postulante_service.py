from modelos.postulante import Postulante
from servicios.event_bus import emit

class PostulanteService:
    """Servicio que centraliza la lógica de inscripción para Postulante.

    Aplicación: SRP (delegar la responsabilidad de flujo/negocio fuera de la entidad).
    """

    @staticmethod
    def inscribir(postulante: Postulante, comentario: str | None = None) -> str:
        # Comportamiento mínimo replicado desde la entidad original,
        # pero centralizado aquí para separar responsabilidad.
        if postulante._estado == "No iniciado":
            postulante._estado = "Inscrito"
            # Emitir evento seguro con datos públicos
            try:
                payload = {
                    "type": "postulante_inscrito",
                    "postulante": postulante.to_public_dict()
                }
                emit("postulante_inscrito", payload)
            except Exception:
                # No fallar la inscripción si el bus falla
                pass
            if comentario:
                return f"{postulante._nombre} se ha inscrito correctamente - Comentario: {comentario}"
            return f"{postulante._nombre} se ha inscrito correctamente"
        raise ValueError("El postulante no está en estado 'No iniciado'")
