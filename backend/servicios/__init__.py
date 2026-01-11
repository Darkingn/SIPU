"""Helpers para el paquete `servicios` relacionados con Supabase.

Exporta `get_supabase_client` y `SupabaseService` para uso desde el resto
del backend. Coloca tus credenciales en variables de entorno o en el
archivo `.env` (usa `example.env` como plantilla):

	SUPABASE_URL=
	SUPABASE_SERVICE_ROLE_KEY=   # clave para operaciones de servidor
	SUPABASE_ANON_KEY=           # clave pública/anónima
	SUPABASE_API_URL=            # (opcional) URL base para Functions / REST proxy

Nota: por seguridad, NO comites las claves en el repositorio.
"""

from .supabase_client import get_supabase_client, get_supabase_keys
from .supabase_service import SupabaseService

__all__ = ["get_supabase_client", "get_supabase_keys", "SupabaseService"]

