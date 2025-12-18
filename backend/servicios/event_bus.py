from collections import defaultdict
from typing import Callable, Any
import logging

# Event Bus simple (síncrono) — explicación:
# Este módulo implementa un dispatcher en memoria muy ligero para publicar
# eventos dentro de la misma ejecución del proceso. Es útil para desacoplar
# emisores de consumidores sin introducir un broker externo. Para producción
# con múltiples procesos/servicios, conviene usar una cola/broker (Redis, RabbitMQ)
# o un patrón transactional outbox para garantizar entrega.

_listeners: dict = defaultdict(list)


def register(event_name: str, fn: Callable[[Any], None]):
    """Registrar un listener para un evento específico."""
    _listeners[event_name].append(fn)


def unregister(event_name: str, fn: Callable[[Any], None]):
    """Quitar un listener previamente registrado."""
    if fn in _listeners[event_name]:
        _listeners[event_name].remove(fn)


def emit(event_name: str, payload: dict):
    """Emitir un evento a todos los listeners registrados.

    Nota: los listeners se ejecutan síncronamente y cualquier excepción se
    captura para no bloquear la emisión a otros listeners.
    """
    listeners = list(_listeners.get(event_name, []))
    for fn in listeners:
        try:
            fn(payload)
        except Exception as e:
            logging.exception("Error en listener para evento %s: %s", event_name, e)
