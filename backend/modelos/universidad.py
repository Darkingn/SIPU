from proceso_admision import ProcesoAdmision  # Importamos la clase base de procesos de admisión

class Universidad(ProcesoAdmision):  # Clase Universidad que hereda de ProcesoAdmision
    _total_universidades = 0  # Contador de universidades creadas

    def __init__(self, codigo, nombre, fecha_inicio, tipo, ubicacion, sedes):
        super().__init__(codigo, nombre, fecha_inicio, "Sistema")  # Inicializamos atributos de la clase padre
        self._tipo = tipo  # Tipo de universidad (Pública o Privada)
        self._ubicacion = ubicacion  # Ubicación principal de la universidad
        self._sedes = sedes if isinstance(sedes, list) else [sedes]  # Lista de sedes; si viene una sola, la convertimos en lista
        self._inscripciones_abiertas = {sede: False for sede in self._sedes}  # Estado de inscripciones por sede, inicialmente cerradas
        Universidad._total_universidades += 1  # Incrementamos el contador total de universidades

    @property
    def tipo(self): return self._tipo  # Getter para obtener el tipo de universidad

    @tipo.setter
    def tipo(self, value):  # Setter que valida y asigna el tipo
        if value not in ["Pública", "Privada"]: raise ValueError("Tipo no válido")  # Solo permite Pública o Privada
        self._tipo = value  # Asigna el valor validado

    @property
    def ubicacion(self): return self._ubicacion  # Getter para obtener la ubicación

    @ubicacion.setter
    def ubicacion(self, value):  # Setter que valida y asigna la ubicación
        if not value.strip(): raise ValueError("La ubicación no puede estar vacía")  # Validamos que no esté vacía
        self._ubicacion = value  # Asignamos el valor

    @property
    def sedes(self): return self._sedes  # Getter para obtener la lista de sedes

    @sedes.setter
    def sedes(self, value):  # Setter que valida y asigna las sedes
        if not isinstance(value, list): raise ValueError("Las sedes deben ser una lista")  # Validamos que sea lista
        self._sedes = value  # Asignamos la lista de sedes
        self._inscripciones_abiertas = {sede: False for sede in self._sedes}  # Inicializamos inscripciones cerradas por cada sede

    def abrir_inscripciones(self, sede=None):  # Método para abrir inscripciones en una o todas las sedes
        if sede:  # Si se especifica una sede
            if sede in self._sedes:  # Verificamos que exista la sede
                if not self._inscripciones_abiertas[sede]:  # Solo si no están abiertas
                    self._inscripciones_abiertas[sede] = True  # Abrimos las inscripciones
                    return f"Inscripciones abiertas en {sede} ({self._nombre})"  # Mensaje de confirmación
                raise ValueError("Las inscripciones ya están abiertas en esta sede")  # Error si ya estaban abiertas
            raise ValueError("Sede no encontrada")  # Error si la sede no existe
        for s in self._sedes:  # Si no se especifica sede, abrimos todas
            self._inscripciones_abiertas[s] = True
        return f"Inscripciones abiertas en todas las sedes de {self._nombre}"  # Mensaje general

    def cerrar_inscripciones(self, sede=None):  # Método para cerrar inscripciones en una o todas las sedes
        if sede:  # Si se especifica una sede
            if sede in self._sedes:  # Verificamos que exista
                if self._inscripciones_abiertas[sede]:  # Solo si estaban abiertas
                    self._inscripciones_abiertas[sede] = False  # Cerramos las inscripciones
                    return f"Inscripciones cerradas en {sede} ({self._nombre})"  # Mensaje de confirmación
                raise ValueError("Las inscripciones ya están cerradas en esta sede")  # Error si ya estaban cerradas
            raise ValueError("Sede no encontrada")  # Error si la sede no existe
        for s in self._sedes:  # Si no se especifica sede, cerramos todas
            self._inscripciones_abiertas[s] = False
        return f"Inscripciones cerradas en todas las sedes de {self._nombre}"  # Mensaje general

    def obtener_info(self):  # Método para mostrar información completa de la universidad
        return f"Universidad {self._nombre} (Código: {self._codigo}) - Tipo: {self._tipo}, Ubicación: {self._ubicacion}, Sedes: {', '.join(self._sedes)} - Estado: {self._estado}"  # Devuelve info formateada

    @classmethod
    def total_universidades(cls): return cls._total_universidades  # Método de clase que devuelve total de universidades creada
