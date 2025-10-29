from supabase import create_client, Client
from backend.config import SUPABASE_URL, SUPABASE_KEY
from backend.utils.error_handler import DatabaseError
import logging

class SupabaseService:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                # Log presence (not value) to help debug missing/invalid keys
                logging.info(f"SUPABASE_URL present: {bool(SUPABASE_URL)}")
                logging.info(f"SUPABASE_KEY present: {bool(SUPABASE_KEY)}")

                cls._client = create_client(SUPABASE_URL, SUPABASE_KEY)
                logging.info("Supabase client initialized successfully")
            except Exception as e:
                logging.error(f"Error initializing Supabase client: {str(e)}")
                raise DatabaseError("Could not connect to database")
        return cls._instance

    @property
    def client(self) -> Client:
        if not self._client:
            raise DatabaseError("Database client not initialized")
        return self._client

    def execute_query(self, query_func):
        """
        Ejecuta una consulta con manejo de errores
        """
        try:
            return query_func(self.client)
        except Exception as e:
            logging.error(f"Database error: {str(e)}")
            raise DatabaseError(str(e))

    def health_check(self):
        """
        Verifica la conexión a la base de datos
        """
        try:
            # Realiza una consulta simple para verificar la conexión usando la tabla real 'aspirantes'
            self.client.table('aspirantes').select("id").limit(1).execute()
            return True
        except Exception as e:
            logging.error(f"Database health check failed: {str(e)}")
            return False