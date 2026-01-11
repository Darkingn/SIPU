"""Servicio ligero para interactuar con Supabase.

Este módulo expone `SupabaseService`, una utilidad singleton que inicializa
un cliente Supabase (a través de `supabase_client.get_supabase_client`) y
proporciona funciones CRUD genéricas con manejo básico de errores.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, Optional

from .supabase_client import get_supabase_client
from utils.error_handler import DatabaseError


class SupabaseService:
    _instance: Optional["SupabaseService"] = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._client = get_supabase_client()
                logging.info("Cliente de Supabase inicializado correctamente")
            except RuntimeError as e:
                logging.error("Error al inicializar el cliente de Supabase: %s", e)
                raise DatabaseError("No se pudo conectar a la base de datos") from e
        return cls._instance

    @property
    def client(self):
        if not self._client:
            raise DatabaseError("Database client not initialized")
        return self._client

    def execute_query(self, query_func):
        """Ejecuta una función pasando el cliente con manejo de errores."""
        try:
            return query_func(self.client)
        except Exception as exc:
            logging.error("Error de la base de datos: %s", exc)
            raise DatabaseError(str(exc)) from exc

    def health_check(self) -> bool:
        """Realiza una consulta sencilla para verificar la conexión."""
        try:
            # Intenta seleccionar una fila de cualquier tabla conocida; si no existe
            # la tabla, la llamada fallará y se reportará como no saludable.
            self.client.table("aspirantes").select("id").limit(1).execute()
            return True
        except Exception as exc:  # pylint: disable=broad-except
            logging.error("La comprobación de salud de la base de datos falló: %s", exc)
            return False

    # --- Operaciones CRUD genéricas ---
    def select(
        self,
        table: str,
        columns: str = "*",
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order: Optional[str] = None,
    ) -> Any:
        """Selecciona datos de `table` aplicando filtros simples (dict de eq)."""
        try:
            q = self.client.table(table).select(columns)
            if filters:
                for col, val in filters.items():
                    q = q.eq(col, val)
            if order:
                q = q.order(order)
            if limit:
                q = q.limit(limit)
            if offset:
                q = q.range(offset, (offset or 0) + (limit or 100) - 1) if limit else q
            return q.execute()
        except Exception as exc:
            logging.error("Error al seleccionar en %s: %s", table, exc)
            raise DatabaseError(str(exc)) from exc

    def insert(self, table: str, records: Iterable[Dict[str, Any]]) -> Any:
        """Inserta uno o varios registros en `table`."""
        try:
            return self.client.table(table).insert(list(records)).execute()
        except Exception as exc:
            logging.error("Error al insertar en %s: %s", table, exc)
            raise DatabaseError(str(exc)) from exc

    def update(self, table: str, filters: Dict[str, Any], data: Dict[str, Any]) -> Any:
        """Actualiza filas en `table` que cumplan `filters` (dict de eq)."""
        try:
            q = self.client.table(table).update(data)
            for col, val in filters.items():
                q = q.eq(col, val)
            return q.execute()
        except Exception as exc:
            logging.error("Error al actualizar en %s: %s", table, exc)
            raise DatabaseError(str(exc)) from exc

    def delete(self, table: str, filters: Dict[str, Any]) -> Any:
        """Elimina filas en `table` que cumplan `filters` (dict de eq)."""
        try:
            q = self.client.table(table).delete()
            for col, val in filters.items():
                q = q.eq(col, val)
            return q.execute()
        except Exception as exc:
            logging.error("Error al eliminar en %s: %s", table, exc)
            raise DatabaseError(str(exc)) from exc


__all__ = ["SupabaseService"]