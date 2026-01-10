from dataclasses import dataclass
from datetime import datetime

# --- SRP: Objeto de Valor para Datos de Contacto ---
# Esto permite reutilizar la lógica de contacto en Profesores o Empleados.
@dataclass(frozen=True)
class Contacto:
    correo: str
    telefono: str
    
    def __post_init__(self):
        # Aquí se llamarían a los validadores externos
        if "@" not in self.correo:
            raise ValueError("Email inválido")

# --- SRP: La Entidad Postulante (Limpia de procesos) ---
class Postulante:
    def __init__(self, id_postulante, nombre, cedula, contacto: Contacto, rol, puntaje):
        self.id = id_postulante
        self.nombre = nombre
        self.cedula = cedula
        self.contacto = contacto
        self.rol = rol
        self.puntaje = puntaje

    def obtener_resumen(self):
        return f"{self.nombre} (ID: {self.id}) - Puntaje: {self.puntaje}"

# --- SRP & DIP: Servicio de Admisiones ---
# Esta clase maneja la lógica de estado que antes estaba "atrapada" en el postulante.
class InscripcionService:
    def __init__(self):
        self._inscritos = {} # Diccionario para persistencia temporal

    def inscribir_postulante(self, postulante: Postulante, comentario=None):
        # Lógica de negocio fuera de la entidad
        if postulante.id in self._inscritos:
            raise ValueError("El postulante ya está inscrito")
        
        self._inscritos[postulante.id] = {
            "fecha": datetime.now(),
            "comentario": comentario,
            "estado": "Inscrito"
        }
        return f"Éxito: {postulante.nombre} ha sido procesado."

# --- USO DEL SISTEMA ---

# 1. Creamos los datos de contacto
contacto_leo = Contacto(correo="leo@example.com", telefono="099999999")

# 2. Creamos al postulante (Entidad pura)
postulante_1 = Postulante(
    id_postulante="POST-001",
    nombre="Leo",
    cedula="1712345678",
    contacto=contacto_leo,
    rol="Aspirante",
    puntaje=850
)

# 3. Usamos el servicio para la lógica de proceso
servicio = InscripcionService()
print(servicio.inscribir_postulante(postulante_1, "Aplica a beca"))