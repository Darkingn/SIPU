from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from controladores.inscripciones_controller import InscripcionesController
from modelos.postulante import Postulante
from servicios.observers.realtime_pusher import register_realtime

class PostulanteCreate(BaseModel):
    codigo: int
    nombre: str
    fecha_inicio: str
    cedula: str
    correo: str
    telefono: str
    rol: str
    puntaje: float

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origins en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

controlador = InscripcionesController()
controlador = InscripcionesController()

@app.get("/")
async def read_root():
    return {"message": "Bienvenido al sistema SIPU"}

@app.post("/estudiantes")
async def crear_estudiante(estudiante_data: PostulanteCreate):
    estudiante = Postulante(
        estudiante_data.codigo,
        estudiante_data.nombre,
        estudiante_data.fecha_inicio,
        estudiante_data.cedula,
        estudiante_data.correo,
        estudiante_data.telefono,
        estudiante_data.rol,
        estudiante_data.puntaje
    )
    resultado = controlador.registrar_estudiante(estudiante)
    return {"mensaje": "Estudiante registrado exitosamente", "estudiante": estudiante.to_dict()}

# Registrar observadores al iniciar la aplicación
register_realtime()
