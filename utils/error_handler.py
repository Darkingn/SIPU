"""Manejadores de errores comunes del proyecto.

Contiene excepciones ligeras usadas por los servicios de base de datos.
"""

class DatabaseError(Exception):
    """Excepción que representa errores relacionados con la base de datos.

    Esta excepción se puede importar como `from utils.error_handler import DatabaseError`.
    """

    def __init__(self, message: str = "Database error"):
        super().__init__(message)


__all__ = ["DatabaseError"]
