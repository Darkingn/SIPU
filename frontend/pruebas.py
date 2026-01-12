from frontend.controlador.usuario_cr import PostulanteController

controller = PostulanteController()

postulante = {
    "codigo": "POST-100",
    "nombre": "Carlos",
    "cedula": "0987654321",
    "correo": "carlos@uni.edu",
    "rol": "ADMINISTRADOR"
}

print(controller.crear_postulante(postulante))
print(controller.listar_postulantes())