from servicios.supabase_service import SupabaseService

def init_database():
    try:
        supabase = SupabaseService().client

        # Nota: la creación de tablas se hace desde el dashboard de Supabase.
        # Aquí mostramos la estructura esperada y hacemos una verificación simple.
        print("Por favor, asegúrate de que la tabla 'aspirantes' exista en el dashboard de Supabase (o actualiza este script para usar tu tabla real). Aquí un ejemplo de columnas esperadas:")
        print("""
        Tabla: aspirantes
        Columnas (ejemplo):
        - id: uuid (primary key)
        - user_id: uuid (FK -> auth.users)
        - cedula: text (UNIQUE)
        - nombre: text
        - correo: text (UNIQUE)
        - telefono: text
        - direccion: text
        - created_at: timestamp with time zone
        """)

        # Verificar si la tabla existe intentando hacer una consulta en 'aspirantes'
        result = supabase.table('aspirantes').select("id").limit(1).execute()
        print("\n✅ La tabla 'aspirantes' existe y es accesible.")
        # result.data puede ser vacio, no todos los drivers devuelven count de la misma forma
        print(f"Registros consultados (muestra): {result.data}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPor favor, sigue estos pasos:")
        print("1. Ve al dashboard de Supabase: https://app.supabase.com")
        print("2. Selecciona tu proyecto")
        print("3. Ve a 'Database' -> 'Tables'")
        print("4. Crea o ajusta la tabla 'aspirantes' según la estructura mostrada arriba")

if __name__ == "__main__":
    init_database()