class ProcesoAdmision:  # Clase base que representa un proceso de admisión genérico
    _total_procesos = 0  # Contador de procesos creados

    def __init__(self, codigo, nombre, fecha_inicio, responsable):
        self._codigo = codigo  # Código único del proceso
        self._nombre = nombre  # Nombre descriptivo del proceso
        self._fecha_inicio = fecha_inicio  # Fecha de inicio del proceso
        self._responsable = responsable  # Persona a cargo del proceso
        self._estado = "No iniciado"  # Estado inicial del proceso
        ProcesoAdmision._total_procesos += 1  # Incrementamos el contador de procesos creados

    @property
    def codigo(self): return self._codigo  # Getter para obtener el código del proceso

    @codigo.setter
    def codigo(self, value):  # Setter que valida y asigna el código
        if not value.strip(): raise ValueError("El código no puede estar vacío")  # Validación para que no quede vacío
        self._codigo = value  # Asigna el código al atributo

    @property
    def nombre(self): return self._nombre  # Getter para obtener el nombre del proceso

    @nombre.setter
    def nombre(self, value):  # Setter que valida y asigna el nombre
        if not value.strip(): raise ValueError("El nombre no puede estar vacío")  # Validación básica
        self._nombre = value  # Guarda el nombre

    @property
    def fecha_inicio(self): return self._fecha_inicio  # Getter para obtener la fecha de inicio

    @fecha_inicio.setter
    def fecha_inicio(self, value):  # Setter que valida y asigna la fecha de inicio
        if not value.strip(): raise ValueError("La fecha no puede estar vacía")  # Validamos que no esté vacía
        self._fecha_inicio = value  # Asigna la fecha al atributo

    @property
    def responsable(self): return self._responsable  # Getter para obtener el responsable del proceso

    @responsable.setter
    def responsable(self, value):  # Setter que valida y asigna responsable
        if not value.strip(): raise ValueError("El responsable no puede estar vacío")  # Evita que quede sin responsable
        self._responsable = value  # Asigna el valor validado

    @property
    def estado(self): return self._estado  # Getter para conocer el estado actual del proceso

    @estado.setter
    def estado(self, value):  # Setter que valida y asigna el estado
        if value not in ["No iniciado", "Iniciado", "Finalizado"]: raise ValueError("Estado no válido")  # Solo permite estados válidos
        self._estado = value  # Guarda el estado validado

    def iniciar_proceso(self, fecha_inicio=None, comentario=None):  # Método para iniciar el proceso con parámetros opcionales
        if self._estado == "No iniciado":  # Solo se puede iniciar si no estaba iniciado
            self._estado = "Iniciado"  # Cambiamos el estado a iniciado
            if fecha_inicio:  # Si se proporciona una fecha de inicio, la actualizamos
                self._fecha_inicio = fecha_inicio  # Asignamos la nueva fecha
                return f"Proceso {self._codigo} iniciado en {fecha_inicio} - Comentario: {comentario if comentario else 'Sin comentario'}"  # Mensaje con comentario opcional
            return f"Proceso {self._codigo} iniciado"  # Mensaje simple si no hay fecha
        raise ValueError("El proceso no está en estado 'No iniciado'")  # Error si ya estaba iniciado o finalizado

    def finalizar_proceso(self):  # Método para finalizar el proceso
        if self._estado == "Iniciado":  # Solo se puede finalizar si está iniciado
            self._estado = "Finalizado"  # Cambiamos el estado
            return f"Proceso {self._codigo} finalizado"  # Mensaje confirmando finalización
        raise ValueError("El proceso no está en estado 'Iniciado'")  # Error si no estaba iniciado

    def obtener_info(self):  # Método que devuelve toda la información del proceso
        return f"Proceso {self._nombre} (Código: {self._codigo}) - Fecha: {self._fecha_inicio} - Responsable: {self._responsable} - Estado: {self._estado}"  # Información completa y organizada

    @classmethod
    def total_procesos(cls): return cls._total_procesos  # Devuelve el número total de procesos creados
