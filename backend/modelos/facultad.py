from proceso_admision import ProcesoAdmision  # Importamos la clase base que maneja los procesos de admisión

class Facultad(ProcesoAdmision):  # Creamos la clase Facultad que hereda de ProcesoAdmision
    _total_facultades = 0  # Contador general para saber cuántas facultades se han creado

    def __init__(self, codigo, nombre, fecha_inicio, decano):
        super().__init__(codigo, nombre, fecha_inicio, "Sistema")  # Llamamos al constructor del padre para inicializar los atributos comunes
        self._decano = decano  # Asignamos el nombre del decano a cargo de la facultad
        self._laboratorios = 0  # Inicializamos el número de laboratorios en 0
        self._computadoras = 0  # Inicializamos el número de computadoras en 0
        Facultad._total_facultades += 1  # Cada vez que se crea una facultad, aumentamos el contador total

    @property
    def decano(self): return self._decano  # Devuelve el nombre del decano actual de la facultad

    @decano.setter
    def decano(self, value):
        if not value.strip(): raise ValueError("El decano no puede estar vacío")  # Validamos que el nombre del decano no esté vacío
        self._decano = value  # Si es válido, lo guardamos

    @property
    def laboratorios(self): return self._laboratorios  # Devuelve la cantidad actual de laboratorios

    @laboratorios.setter
    def laboratorios(self, value):
        if value < 0: raise ValueError("El número de laboratorios no puede ser negativo")  # No se permiten valores negativos
        self._laboratorios = value  # Si es válido, lo asignamos

    @property
    def computadoras(self): return self._computadoras  # Devuelve la cantidad actual de computadoras

    @computadoras.setter
    def computadoras(self, value):
        if value < 0: raise ValueError("El número de computadoras no puede ser negativo")  # Validamos que no sea negativo
        self._computadoras = value  # Si pasa la validación, lo guardamos

    def agregar_laboratorio(self):  # Método para añadir un nuevo laboratorio a la facultad
        self._laboratorios += 1  # Sumamos uno al número actual de laboratorios
        return f"Laboratorio añadido a la facultad {self._nombre}"  # Retornamos un mensaje confirmando la acción

    def agregar_computadoras(self, cantidad):  # Método para añadir una cantidad específica de computadoras
        if cantidad < 0: raise ValueError("La cantidad no puede ser negativa")  # Validamos que la cantidad sea positiva
        self._computadoras += cantidad  # Sumamos la cantidad de computadoras al total existente
        return f"{cantidad} computadoras añadidas a la facultad {self._nombre}"  # Retornamos un mensaje de confirmación

    def obtener_info(self):  # Método que devuelve un resumen completo de la facultad
        return f"Facultad {self._nombre} (Código: {self._codigo}) - Decano: {self._decano}, Laboratorios: {self._laboratorios}, Computadoras: {self._computadoras} - Estado: {self._estado}"  # Mostramos toda la información clave de la facultad

    @classmethod
    def total_facultades(cls): return cls._total_facultades  # Devuelve cuántas facultades se han creado en total
