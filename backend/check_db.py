import sys
sys.path.append("c:/Users/mayo_/Desktop/SIPU/SIPU")

from backend.servicios.supabase_service import SupabaseService

def check_connection():
    try:
        service = SupabaseService()
        if service.health_check():
            print("✓ Conexión a Supabase exitosa.")
        else:
            print("✗ Fallo la verificación de salud de Supabase.")
    except Exception as e:
        print(f"✗ Error al conectar con Supabase: {e}")

if __name__ == "__main__":
    check_connection()
