from backend.servicios.supabase_service import SupabaseService
from backend.modelos.postulante import Postulante
from backend.utils.error_handler import DatabaseError

def test_connection():
    try:
        # Inicializar el servicio de Supabase
        supabase_service = SupabaseService()
        
        # Probar la conexión
        print("Probando conexión con Supabase...")
        is_healthy = supabase_service.health_check()
        print(f"Conexión exitosa: {is_healthy}")

        # Crear un postulante de prueba
        postulante = Postulante(
            codigo="001",
            nombre="Usuario de Prueba",
            fecha_inicio="2025-10-29",
            cedula="1234567890",  # Asegúrate de usar una cédula válida
            correo="test@ejemplo.com",
            telefono="+593987654321",
            rol="estudiante",
            puntaje=85
        )

        # Preparar un diccionario que coincida con la tabla 'aspirantes' en Supabase
        aspirante_dict = {
            "cedula": postulante.cedula,
            "nombre": getattr(postulante, "_nombre", "Usuario Prueba"),
            "correo": postulante.correo,
            "telefono": postulante.telefono,
            "direccion": "",  # campo opcional en este ejemplo
        }

        # Insertar en Supabase (tabla 'aspirantes')
        print("\nIntentando insertar aspirante de prueba en la tabla 'aspirantes'...")
        result = supabase_service.client.table('aspirantes').insert(aspirante_dict).execute()
        
        print("Postulante insertado exitosamente!")
        print("\nDatos insertados:", result.data)

    except DatabaseError as e:
        print(f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    test_connection()