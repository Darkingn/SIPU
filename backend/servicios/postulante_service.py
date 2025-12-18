from modelos.postulante import Postulante
from servicios.event_bus import emit

# Observability / Event emission rationale:
# Aplicamos aquí el patrón Observer (publicador/suscriptor) en el Service
# porque la inscripción es una operación del caso de uso que debe
# desencadenar efectos secundarios (notificaciones, audit, realtime)
# sin que la entidad `Postulante` conozca quién los maneja. Emitir el
# evento desde el service permite:
#  - mantener a las entidades enfocadas en su responsabilidad (SRP),
#  - centralizar el punto donde se orquesta la operación (fácil de testear),
#  - añadir o quitar listeners (observadores) sin tocar la lógica del dominio.
# El payload enviado debe ser seguro (no exponer PII); usamos `to_public_dict()`.


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
