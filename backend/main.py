from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Admisión",
    description="API para la comunicación entre frontend y backend",
    version="1.0.0"
)

# Configurar CORS
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar routers de controladores
from backend.controladores.carrera_cr import router as carrera_router

# Incluir routers
app.include_router(carrera_router)

# Health check
@app.get("/")
def health_check():
    return {"estado": "API activa", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}
