try:
    from servicios.supabase_service import SupabaseService
except Exception:
    SupabaseService = None


class _MockClient:
    def rpc(self, name: str):
        class _Res:
            def execute(self):
                # Simulated data
                return type("R", (), {"data": ["estudiantes", "facultades", "carreras"]})()
        return _Res()


class _MockSupabaseService:
    def __init__(self):
        self._client = _MockClient()

    @property
    def client(self):
        return self._client


def list_tables():
    try:
        if SupabaseService is None:
            # Fallback: usar servicio simulado para desarrollo sin dependencias
            supabase = _MockSupabaseService().client
            print("\nAdvertencia: paquete 'supabase' no disponible — usando modo simulado.")
        else:
            supabase = SupabaseService().client

        print("\nIntentando listar las tablas existentes...")

        # Consulta para obtener las tablas
        result = supabase.rpc('get_tables').execute()

        print("\nTablas encontradas:")
        for table in result.data:
            print(f"- {table}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    list_tables()