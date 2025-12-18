from proceso_admision import ProcesoAdmision  # Importamos la clase base que maneja el proceso de admisión

class OfertaAcademica(ProcesoAdmision):  # Definimos la clase OfertaAcademica que hereda de ProcesoAdmision
    _total_ofertas = 0  # Contador general para saber cuántas ofertas académicas se han creado

    def __init__(self, codigo, nombre, fecha_inicio, num_carreras, num_areas, cupos):
        super().__init__(codigo, nombre, fecha_inicio, "Sistema")  # Llamamos al constructor del padre para inicializar atributos comunes
        self._num_carreras = num_carreras  # Guardamos la cantidad de carreras disponibles en la oferta
        self._num_areas = num_areas  # Guardamos la cantidad de áreas académicas incluidas
        self._cupos = cupos  # Definimos el número de cupos totales disponibles
        OfertaAcademica._total_ofertas += 1  # Cada vez que se crea una oferta, aumentamos el contador general

    @property
    def num_carreras(self): 
        return self._num_carreras  # Devuelve el número de carreras disponibles

    @num_carreras.setter
    def num_carreras(self, value):
        if value < 0: raise ValueError("El número de carreras no puede ser negativo")  # Validamos que el número no sea negativo
        self._num_carreras = value  # Si es válido, lo asignamos

    @property
    def num_areas(self): 
        return self._num_areas  # Devuelve la cantidad de áreas académicas

    @num_areas.setter
    def num_areas(self, value):
        if value < 0: 
            raise ValueError("El número de áreas no puede ser negativo")  # No se permiten valores negativos
        self._num_areas = value  # Si es correcto, lo guardamos

    @property
    def cupos(self):
        return self._cupos  # Devuelve el número total de cupos disponibles

    @cupos.setter
    def cupos(self, value):
        if value < 0:
            raise ValueError("Los cupos no pueden ser negativos")  # Validamos que los cupos sean positivos
        self._cupos = value  # Si pasa la validación, lo guardamos

    def actualizar_cupos(self, nuevos_cupos):  # Método para actualizar el número de cupos disponibles
        if nuevos_cupos < 0: raise ValueError("Los cupos no pueden ser negativos")  # No se permiten valores negativos
        self._cupos = nuevos_cupos  # Asignamos el nuevo valor de cupos
        return f"Cupos actualizados a {self._cupos} para la oferta {self._nombre}"  # Retornamos un mensaje de confirmación

    def obtener_info(self):  # Método que muestra toda la información completa de la oferta académica
        return f"Oferta {self._nombre} (Código: {self._codigo}) - Carreras: {self._num_carreras}, Áreas: {self._num_areas}, Cupos: {self._cupos} - Estado: {self._estado}"  # Retornamos los datos clave de la oferta

    @classmethod
    def total_ofertas(cls): 
        return cls._total_ofertas  # Devuelve el número total de ofertas académicas creadas

    def to_public_dict(self) -> dict:
        return {
            "codigo": getattr(self, "_codigo", None),
            "nombre": getattr(self, "_nombre", None),
            "num_carreras": getattr(self, "_num_carreras", 0),
            "num_areas": getattr(self, "_num_areas", 0),
            "cupos": getattr(self, "_cupos", 0),
            "estado": getattr(self, "_estado", None),
        }
