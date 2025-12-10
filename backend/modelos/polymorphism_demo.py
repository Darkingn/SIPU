from modelos.interfaces import IProcesoAdmision
from modelos.postulante import Postulante
from modelos.facultad import Facultad


def iniciar_si_no_iniciado(proceso: IProcesoAdmision, fecha_inicio: str | None = None):
    """Función que demuestra polimorfismo: acepta cualquier IProcesoAdmision
    y llama a iniciar_proceso sin importar la implementación concreta.
    """
    return proceso.iniciar_proceso(fecha_inicio)


def demo():
    # Crear instancias concretas que implementan IProcesoAdmision
    p = Postulante("P1", "Juan", "2025-01-01", "123", "j@x.com", "099", "estudiante", 0)
    f = Facultad("F1", "Facultad A", "2025-01-01", "Decano X")

    print(iniciar_si_no_iniciado(p))
    print(iniciar_si_no_iniciado(f, "2025-02-01"))


if __name__ == "__main__":
    demo()
