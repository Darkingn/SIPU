from servicios.event_bus import register
import logging

try:
    from servicios.supabase_service import SupabaseService
except Exception:
    SupabaseService = None


def _push_to_realtime(payload: dict):
    """
    Observador encargado de reenviar eventos al canal Realtime o almacenarlos
    según la implementación disponible. Mantener este comportamiento en un
    observador separado evita acoplar la lógica de negocio a la infraestructura
    de notificación.

    Nota de seguridad: el payload proviene de `postulante.to_public_dict()` y
    por tanto no debe incluir PII. Si se necesita información sensible, usar
    identificadores y resolverlos en una capa autorizada.
    """
    try:
        if SupabaseService is None:
            logging.info("[realtime_pusher] Supabase not available — payload: %s", payload)
            return
        svc = SupabaseService()
        # Insert into an events table or use realtime publish mechanism depending on setup
        svc.client.table('events').insert({
            'type': payload.get('type', 'unknown'),
            'data': payload
        }).execute()
    except Exception as e:
        logging.exception("Error pushing event to realtime: %s", e)


def register_realtime():
    # Registramos este observador para el evento 'postulante_inscrito'.
    # Si en el futuro quieres añadir más observadores (email, audit),
    # regístralos también aquí o en otro módulo de observers.
    register('postulante_inscrito', _push_to_realtime)
