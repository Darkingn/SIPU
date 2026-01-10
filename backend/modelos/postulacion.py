# --- SRP: La clase Postulacion es ahora un mediador limpio ---
class Postulacion:
    def __init__(self, codigo, postulante, carrera, sede, evaluacion):
        # DIP: Recibimos los objetos ya instanciados (Inyección)
        self.codigo = codigo
        self.postulante = postulante
        self.carrera = carrera
        self.sede = sede
        self.evaluacion = evaluacion
        self.fecha_registro = "2026-01-10" # Ejemplo de dato propio

    @property
    def postulante(self): return self._postulante

    @postulante.setter
    def postulante(self, value):
        if not value: raise ValueError("El postulante es obligatorio")
        self._postulante = value

    # Delegación de comportamiento (Law of Demeter respetada)
    def iniciar_proceso(self):
        return self.evaluacion.iniciar()

    def obtener_resumen(self):
        return (f"POSTULACIÓN [{self.codigo}]\n"
                f"Aspirante: {self.postulante.nombre}\n"
                f"Carrera: {self.carrera.nombre}\n"
                f"Sede: {self.sede}\n"
                f"Estado Evaluación: {self.evaluacion.estado.value}")

# --- SRP: Un Servicio o Gestor para orquestar la creación ---
class PostulacionService:
    """
    Esta clase es la única que sabe CÓMO se construye una postulación completa.
    """
    def __init__(self):
        self._historial = []

    def crear_postulacion(self, aspirante, carrera, sede, evaluacion):
        # Aquí irían las validaciones de negocio cruzadas
        nueva_postulacion = Postulacion(
            codigo=f"POST-{len(self._historial) + 1}",
            postulante=aspirante,
            carrera=carrera,
            sede=sede,
            evaluacion=evaluacion
        )
        self._historial.append(nueva_postulacion)
        return nueva_postulacion

# --- USO DEL SISTEMA SOLID COMPLETO ---

# 1. Tenemos los objetos listos (vienen de sus propias fábricas/repositorios)
# Estos objetos ya fueron validados individualmente
aspirante_leo = "Objeto AspiranteNuevo" 
carrera_soft = "Objeto Carrera Software"
examen_ingreso = "Objeto Evaluacion Programada"

# 2. El servicio orquesta la unión sin acoplamiento
servicio = PostulacionService()
postulacion_final = servicio.crear_postulacion(
    aspirante_leo, 
    carrera_soft, 
    "Sede Central", 
    examen_ingreso
)

print(postulacion_final.obtener_resumen())