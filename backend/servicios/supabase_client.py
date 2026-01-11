"""Ayudantes para el cliente de Supabase.

Este módulo expone utilidades para crear y reutilizar un cliente de
Supabase configurado desde variables de entorno. Lee `SUPABASE_URL` y
ya sea `SUPABASE_SERVICE_ROLE_KEY` (preferida para operaciones del servidor)
o `SUPABASE_ANON_KEY`.

Coloca las claves en tu entorno o en un archivo `.env` (ver `example.env`).
"""
from __future__ import annotations


import logging
import os
from typing import Optional, Tuple, TYPE_CHECKING


# `python-dotenv` es opcional para despliegues; manejar su ausencia
try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    def load_dotenv(*_args, **_kwargs):
        return None


# Importa el cliente de Supabase de forma perezosa para evitar errores de
# importación en entornos donde el paquete no esté instalado (el análisis
# de tipos aún lo reconocerá).
if TYPE_CHECKING:  # pragma: no cover - only for static analysis
    from supabase import create_client, Client  # type: ignore


# Carga automáticamente `.env` cuando esté presente
load_dotenv()


def _get_env_value(name: str) -> Optional[str]:
    """Leer de las variables de entorno y devolver el valor si existe."""
    val = os.environ.get(name)
    if val:
        return val
    return None


def get_supabase_keys() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Devuelve (url, clave_de_servicio, clave_anonima) leídas del entorno.

    Variables comprobadas: `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY`;
    como alternativa se consulta `SUPABASE_KEY`.
    """
    url = _get_env_value("SUPABASE_URL")
    service_key = _get_env_value("SUPABASE_SERVICE_ROLE_KEY")
    anon_key = _get_env_value("SUPABASE_ANON_KEY") or _get_env_value("SUPABASE_KEY")

    logging.info(f"DEBUG: SUPABASE_URL={url}")
    logging.info(f"DEBUG: SUPABASE_SERVICE_ROLE_KEY={'*' * len(service_key) if service_key else 'None'}")
    logging.info(f"DEBUG: SUPABASE_ANON_KEY={'*' * len(anon_key) if anon_key else 'None'}")

    return url, service_key, anon_key


def get_supabase_client(use_service_role: bool = False):
    """Devuelve un `Client` de Supabase inicializado.

    - Si `use_service_role=True` intentará usar `SUPABASE_SERVICE_ROLE_KEY`.
    - En caso contrario usará la clave anónima/pública.

    Lanza `RuntimeError` cuando faltan la URL o la clave.
    """
    url, service_key, anon_key = get_supabase_keys()

    # Seleccionar la clave según la intención del llamador
    key = service_key if use_service_role else (anon_key or service_key)

    if not url or not key:
        logging.error("Falta la configuración de Supabase: SUPABASE_URL o la clave no está establecida")
        raise RuntimeError(
            "SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY/SUPABASE_ANON_KEY deben estar definidas en el entorno"
        )

    # Importar perezosamente para evitar errores si el paquete no está instalado
    try:
        from supabase import create_client  # type: ignore
    except ImportError as exc:  # pragma: no cover - se informa claramente
        raise RuntimeError("El paquete 'supabase' es necesario para crear un cliente") from exc

    client = create_client(url, key)
    return client


def get_supabase_api_url() -> Optional[str]:
    """Return an optional API base URL for Supabase functions or REST endpoints.

    This lets you configure an alternate endpoint (for example when using
    a proxy or functions URL). Environment variables checked (in order):
    `SUPABASE_API_URL`, `SUPABASE_FUNCTIONS_URL`, `SUPABASE_REST_URL`.
    """
    return (
        _get_env_value("SUPABASE_API_URL")
        or _get_env_value("SUPABASE_FUNCTIONS_URL")
        or _get_env_value("SUPABASE_REST_URL")
    )


__all__ = [
    "get_supabase_client",
    "get_supabase_keys",
    "get_supabase_api_url",
]

