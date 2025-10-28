from proceso_admision import ProcesoAdmision  # Importamos la clase base que gestiona el proceso de admisión

class Evaluacion(ProcesoAdmision):  # Creamos la clase Evaluacion que hereda de ProcesoAdmision
    _total_evaluaciones = 0  # Contador para saber cuántas evaluaciones se han creado en total

    def __init__(self, codigo, nombre, fecha_inicio, fecha, hora, sala, duracion, tipo):
        super().__init__(codigo, nombre, fecha_inicio, "Sistema")  # Llamamos al constructor del padre para inicializar datos comunes
        self._fecha = fecha  # Guardamos la fecha en la que se realizará la evaluación
        self._hora = hora  # Guardamos la hora de inicio de la evaluación
        self._sala = sala  # Asignamos la sala o aula donde se llevará a cabo
        self._duracion = duracion  # Indicamos cuántas horas durará la evaluación
        self._tipo = tipo  # Definimos el tipo de evaluación (por ejemplo, examen, entrevista, etc.)
        Evaluacion._total_evaluaciones += 1  # Cada vez que se crea una evaluación, aumentamos el contador total

    @property
    def fecha(self): return self._fecha  # Retorna la fecha de la evaluación

    @fecha.setter
    def fecha(self, value):
        if not value.strip(): raise ValueError("La fecha no puede estar vacía")  # Validamos que la fecha no venga vacía
        self._fecha = value  # Si es válida, la guardamos

    @property
    def hora(self): return self._hora  # Devuelve la hora de inicio de la evaluación

    @hora.setter
    def hora(self, value):
        if not value.strip(): raise ValueError("La hora no puede estar vacía")  # Validamos que la hora esté definida
        self._hora = value  # Si es válida, la asignamos

    @property
    def sala(self): return self._sala  # Devuelve la sala asignada para la evaluación

    @sala.setter
    def sala(self, value):
        if not value.strip(): raise ValueError("La sala no puede estar vacía")  # Validamos que no esté vacía
        self._sala = value  # Guardamos la sala si pasa la validación

    @property
    def duracion(self): return self._duracion  # Devuelve la duración de la evaluación

    @duracion.setter
    def duracion(self, value):
        if value <= 0: raise ValueError("La duración debe ser mayor a 0")  # Validamos que la duración sea positiva
        self._duracion = value  # Si es válida, la guardamos

    @property
    def tipo(self): return self._tipo  # Retorna el tipo de evaluación

    @tipo.setter
    def tipo(self, value):
        if not value.strip(): raise ValueError("El tipo no puede estar vacío")  # Validamos que el tipo esté definido
        self._tipo = value  # Si es válido, lo guardamos

    def iniciar_evaluacion(self):  # Método para cambiar el estado a "En curso"
        if self._estado == "Iniciado":  # Solo puede iniciarse si el estado actual es "Iniciado"
            self._estado = "En curso"  # Cambiamos el estado
            return f"Evaluación {self._nombre} en {self._sala} iniciada"  # Retornamos un mensaje informativo
        raise ValueError("La evaluación no está en estado 'Iniciado'")  # Si no cumple, lanzamos un error

    def finalizar_evaluacion(self):  # Método para finalizar la evaluación
        if self._estado == "En curso":  # Solo puede finalizar si está en curso
            self._estado = "Finalizada"  # Cambiamos el estado a finalizada
            return f"Evaluación {self._nombre} en {self._sala} finalizada"  # Mensaje confirmando la finalización
        raise ValueError("La evaluación no está en estado 'En curso'")  # Si no está en curso, lanzamos un error

    def obtener_info(self):  # Método para mostrar toda la información de la evaluación
        return f"Evaluación {self._nombre} (Código: {self._codigo}) - {self._tipo} - Fecha: {self._fecha}, Hora: {self._hora}, Sala: {self._sala}, Duración: {self._duracion}h - Estado: {self._estado}"  # Devolvemos los datos completos

    @classmethod
    def total_evaluaciones(cls): return cls._total_evaluaciones  # Devuelve cuántas evaluaciones se han creado en total
