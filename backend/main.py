from backend.modelos.postulante import Estudiante
from backend.controladores.inscripciones_controller import InscripcionesController

if __name__ == "__main__":
    controlador = InscripcionesController()

    nuevo = Estudiante(1, "Joseph Zambrano", "joseph@example.com", "Ingeniería de Software")
    resultado = controlador.registrar_estudiante(nuevo)

    print("✅ Estudiante registrado:", resultado)
