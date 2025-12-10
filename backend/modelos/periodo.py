from proceso_admision import ProcesoAdmision  # Importamos la clase base que gestiona los procesos de admisión
from typing import Optional
from modelos.interfaces import ICalendarService


class Periodo(ProcesoAdmision):  # Definimos la clase Periodo que hereda de ProcesoAdmision
    _total_periodos = 0  # Contador general para saber cuántos períodos se han creado

    def __init__(self, codigo, nombre, fecha_inicio, fecha_fin, descripcion, calendar_service: Optional[ICalendarService] = None):
        super().__init__(codigo, nombre, fecha_inicio, "Sistema")  # Llamamos al constructor del padre para inicializar los datos comunes
        self._fecha_fin = fecha_fin  # Guardamos la fecha en la que finaliza el período académico
        self._descripcion = descripcion  # Guardamos una breve descripción del período (por ejemplo, "Periodo 2025-2")
        # Inyección opcional de un servicio de calendario (mejora testabilidad y aplica DIP)
        self._calendar_service = calendar_service
        Periodo._total_periodos += 1  # Cada vez que se crea un período, aumentamos el contador total

    @property
    def fecha_fin(self):
        return self._fecha_fin  # Devuelve la fecha de finalización del período

    @fecha_fin.setter
    def fecha_fin(self, value):
        if not value.strip():
            raise ValueError("La fecha de fin no puede estar vacía")  # Validamos que la fecha no esté vacía
        self._fecha_fin = value  # Si es válida, la guardamos

    @property
    def descripcion(self):
        return self._descripcion  # Devuelve la descripción del período académico

    @descripcion.setter
    def descripcion(self, value):
        if not value.strip():
            raise ValueError("La descripción no puede estar vacía")  # Validamos que la descripción no esté vacía
        self._descripcion = value  # Si pasa la validación, la guardamos

    def verificar_activo(self, fecha_actual):  # Método que permite verificar si el período está activo o no
        # Si se inyectó un calendar_service, delegamos la verificación a la abstracción (DIP).
        if self._calendar_service:
            activo = self._calendar_service.is_active(self._codigo, fecha_actual)
            return f"Período {self._codigo} está {'activo' if activo else 'inactivo'} en {fecha_actual}"
        # Comportamiento por defecto basado en el estado interno
        return f"Período {self._codigo} está {'activo' if self.estado == 'Iniciado' else 'inactivo'} en {fecha_actual}"  # Devuelve un texto indicando si está activo o inactivo en una fecha específica

    def obtener_info(self):  # Método que muestra toda la información del período académico
        return f"Período {self._nombre} (Código: {self._codigo}) - {self._descripcion} ({self._fecha_inicio} al {self._fecha_fin}) - Estado: {self._estado}"  # Retornamos los datos completos y organizados del período

    @classmethod
    def periodos_activos(cls):
        return cls._total_periodos  # Devuelve el número total de períodos creados hasta el momento

    def to_public_dict(self) -> dict:
        """Representación pública de Periodo; delega a calendar_service si existe."""
        return {
            "codigo": getattr(self, "_codigo", None),
            "nombre": getattr(self, "_nombre", None),
            "fecha_inicio": getattr(self, "_fecha_inicio", None),
            "fecha_fin": getattr(self, "_fecha_fin", None),
            "descripcion": getattr(self, "_descripcion", None),
            "estado": getattr(self, "_estado", None),
        }
