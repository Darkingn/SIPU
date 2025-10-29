from servicios.supabase_service import SupabaseService

def list_tables():
    try:
        supabase = SupabaseService().client
        
        print("\nConexión exitosa con Supabase!")
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