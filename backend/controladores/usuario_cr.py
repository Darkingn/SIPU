from fastapi import FastAPI, HTTPException
from enum import Enum
import supabase

# =====================================================
# MODELO
# =====================================================

class RolUsuario(Enum):
    ESTUDIANTE = "Estudiante"
    ADMINISTRADOR = "Administrador"
    DOCENTE = "Docente"


class Usuario:
    def __init__(self, codigo: str, nombre: str, cedula: str, correo: str, rol: RolUsuario):
        self.codigo = codigo
        self.nombre = nombre
        self.cedula = cedula
        self.correo = correo
        self.rol = rol


# =====================================================
# REPOSITORY (SQLite simple)
# =====================================================

class UsuarioRepository:
    def __init__(self):
        self.conn = supabase.connect("admisiones.db", check_same_thread=False)
        self._crear_tabla()

    def _crear_tabla(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                codigo TEXT PRIMARY KEY,
                nombre TEXT,
                cedula TEXT,
                correo TEXT,
                rol TEXT
            )
        """)
        self.conn.commit()

    def guardar(self, usuario: Usuario):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (codigo, nombre, cedula, correo, rol)
            VALUES (?, ?, ?, ?, ?)
        """, (
            usuario.codigo,
            usuario.nombre,
            usuario.cedula,
            usuario.correo,
            usuario.rol.value
        ))
        self.conn.commit()

    def listar(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        return cursor.fetchall()

    def buscar_por_codigo(self, codigo: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE codigo = ?", (codigo,))
        return cursor.fetchone()


# =====================================================
# CONTROLLER (FastAPI)
# =====================================================

app = FastAPI(title="API Usuarios - Sistema de Admisión")

repo = UsuarioRepository()


@app.post("/usuarios")
def crear_usuario(
    codigo: str,
    nombre: str,
    cedula: str,
    correo: str,
    rol: RolUsuario
):
    # Validación simple
    if "@" not in correo:
        raise HTTPException(status_code=400, detail="Correo inválido")

    usuario = Usuario(codigo, nombre, cedula, correo, rol)

    try:
        repo.guardar(usuario)
        return {"mensaje": "Usuario registrado correctamente"}
    except supabase.IntegrityError:
        raise HTTPException(status_code=400, detail="El usuario ya existe")


@app.get("/usuarios")
def listar_usuarios():
    datos = repo.listar()
    return [
        {
            "codigo": u[0],
            "nombre": u[1],
            "cedula": u[2],
            "correo": u[3],
            "rol": u[4]
        }
        for u in datos
    ]


@app.get("/usuarios/{codigo}")
def obtener_usuario(codigo: str):
    usuario = repo.buscar_por_codigo(codigo)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "codigo": usuario[0],
        "nombre": usuario[1],
        "cedula": usuario[2],
        "correo": usuario[3],
        "rol": usuario[4]
    }
