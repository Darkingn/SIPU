from modelos.postulante import Postulante


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
            if comentario:
                return f"{postulante._nombre} se ha inscrito correctamente - Comentario: {comentario}"
            return f"{postulante._nombre} se ha inscrito correctamente"
        raise ValueError("El postulante no está en estado 'No iniciado'")
