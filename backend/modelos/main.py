from periodo import Periodo             # Importamos la clase para manejar los períodos académicos.
from oferta_academica import OfertaAcademica # Importamos la clase que gestiona las ofertas de carreras.
from postulante import Postulante         # Importamos la clase para manejar la información de los aspirantes.
from backend.modelos.universidad import Universidad  # Importamos la clase que representa las instituciones de educación superior.
from facultad import Facultad             # Importamos la clase para organizar las facultades dentro de la universidad.
from postulacion import Postulacion       # Importamos la clase para registrar las solicitudes de postulación.
from proceso_admision import ProcesoAdmision # Importamos la clase para controlar las etapas de admisión.
from evaluacion import Evaluacion         # Importamos la clase para gestionar los exámenes y pruebas.
from carrera import Carrera               # Importamos la clase para definir las carreras disponibles.
from usuario import Usuario               # Importamos la clase para gestionar a los usuarios del sistema (admins, etc.).

datos = {                                 # Este es el diccionario central que guarda todos nuestros datos.
    "periodos": {},                       # Aquí irán los períodos académicos.
    "ofertas": {},                        # Aquí se almacenan todas las ofertas de carreras.
    "postulantes": {},                    # Aquí guardaremos a los aspirantes a ingresar.
    "universidades": {},                  # Aquí estarán las universidades registradas.
    "facultades": {},                     # Aquí se guardan las facultades.
    "postulaciones": {},                  # Aquí se registran las postulaciones realizadas.
    "procesos": {},                       # Aquí se controlan los procesos de admisión.
    "evaluaciones": {},                   # Aquí se registran las evaluaciones y exámenes.
    "carreras": {},                       # Aquí se definen las carreras.
    "usuarios": {}                        # Aquí se guardan los usuarios administradores.
}

def menu_principal():                   
    while True:                         
        print("SISTEMA DE INSCRIPCIÓN Y POSTULACIÓN UNIVERSITARIA")
        print("\n1. Gestión de Períodos Académicos")        
        print("2. Gestión de Ofertas Académicas")            
        print("3. Gestión de Aspirantes")                      
        print("4. Gestión de Universidades")                
        print("5. Gestión de Facultades")                      
        print("6. Gestión de Postulaciones")             
        print("7. Gestión de Proceso de Admisión")            
        print("8. Gestión de Evaluaciones")                   
        print("9. Gestión de Carreras")                     
        print("10. Gestión de Usuarios")                      
        print("11. Ver Resumen del Sistema")                 
        print("12. Salir")                                        
        
        opcion = input("\nSelecciona una opción: ").strip()     
        
        if opcion == "1": menu_periodos()                 
        elif opcion == "2": menu_ofertas()            
        elif opcion == "3": menu_aspirantes()              
        elif opcion == "4": menu_universidades()              
        elif opcion == "5": menu_facultades()                 
        elif opcion == "6": menu_postulaciones()          
        elif opcion == "7": menu_proceso_admision()          
        elif opcion == "8": menu_evaluaciones()              
        elif opcion == "9": menu_carreras()                    
        elif opcion == "10": menu_usuarios()                   
        elif opcion == "11": ver_resumen()                    
        elif opcion == "12":                                   
            print("\nGracias por usar el sistema. Hasta pronto.") 
            break                                            
        else: print("Opción no válida")                    

def menu_periodos():
    while True:
        print("GESTIÓN DE PERÍODOS ACADÉMICOS")  
        print("\n1. Crear período")             
        print("2. Verificar período activo")    
        print("3. Cerrar período")              
        print("4. Ver períodos")               
        print("5. Volver al menú principal")    
        
        opcion = input("\nSelecciona una opción  ").strip() 
        
        if opcion == "1":                                         
            codigo = input("\nCódigo del período (ej: 2025-2): ").strip() # Pedimos el código único.
            nombre = input("Nombre del período (ej: Semestre 2 2025): ").strip() # Pedimos un nombre descriptivo.
            fecha_inicio = input("Fecha de inicio (DD/MM/YYYY): ").strip() # Cuándo empieza el período.
            fecha_fin = input("Fecha de fin (DD/MM/YYYY): ").strip() # Cuándo termina el período.
            descripcion = input("Descripción: ").strip()  # Detalles adicionales.
            try:
                periodo = Periodo(codigo, nombre, fecha_inicio, fecha_fin, descripcion) # Intentamos crear el objeto Periodo.
                datos["periodos"][codigo] = periodo # ¡Guardamos el nuevo período en el diccionario!
                print(f"\nPeríodo creado: {periodo.obtener_info()}") # Confirmamos la creación con éxito.
            except ValueError as e: print(f"\nError: {str(e)}")  # Si faltan datos, mostramos el error.
        
        elif opcion == "2":                                       
            codigo = input("\nCódigo del período: ").strip()  # Preguntamos qué período quiere verificar.
            fecha_actual = input("Fecha actual (DD/MM/YYYY): ").strip() # Solicitamos la fecha para la verificación.
            if codigo in datos["periodos"]:  # Verificamos que el período exista.
                print(f"\n{datos['periodos'][codigo].verificar_activo(fecha_actual)}") # Mostramos si está activo o no.
            else: print("\nPeríodo no encontrado")  # Si el código no está, avisamos.
        
        elif opcion == "3":                                       #
            codigo = input("\nCódigo del período a cerrar: ").strip() # Preguntamos cuál cerrar.
            if codigo in datos["periodos"]:  # Verificamos si existe antes de intentar.
                try:
                    datos["periodos"][codigo].estado = "Finalizado" # Cambiamos su estado a 'Finalizado'.
                    print(f"\nEl período {codigo} ha sido cerrado") # Confirmación.
                except ValueError as e: print(f"\nError: {str(e)}") # Manejo de errores (aunque aquí es simple).
            else: print("\nPeríodo no encontrado") # Avisamos si no se encuentra.
        
        elif opcion == "4":
            if datos["periodos"]:
                print("\nPERÍODOS REGISTRADOS:")                 
                for cod, periodo in datos["periodos"].items():# Recorremos cada período en el sistema.
                    print(f"  - {periodo.obtener_info()}") # Imprimimos la información clave.
            else: print("\nNo hay períodos registrados")# Si el diccionario está vacío.
        
        elif opcion == "5":
            break                                 # Properly indented to exit the while loop
        else: print("Opción no válida")

def menu_ofertas():   # Función para gestionar las ofertas académicas (carreras, cupos...).
    while True:
        print("GESTIÓN DE OFERTAS ACADÉMICAS")
        print("\n1. Crear oferta académica")
        print("2. Actualizar cupos")                  
        print("3. Ver ofertas")                       
        print("4. Volver al menú principal")          
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1":                                  # Crear una nueva oferta.
            codigo = input("\nCódigo de la oferta : ").strip() # Identificador único.
            nombre = input("Nombre de la oferta: ").strip()  # Nombre (авис

        elif opcion == "2":                               
            nombre = input("\nNombre de la oferta: ").strip() # ¿A qué oferta queremos cambiarle los cupos?
            try:
                nuevos_cupos = int(input("Nuevos cupos: ").strip()) # Pedimos el nuevo número de cupos.
                if nombre in datos["ofertas"]:  # Verificamos que la oferta exista.
                    print(f"\n{datos['ofertas'][nombre].actualizar_cupos(nuevos_cupos)}") # Aplicamos el cambio.
                else: print("\nOferta no encontrada")                
            except ValueError as e: print(f"\nError: {str(e)}")    
        
        elif opcion == "3":                                
            if datos["ofertas"]:                          
                print("\nOFERTAS ACADÉMICAS:")           
                for nombre, oferta in datos["ofertas"].items(): # Recorremos y mostramos.
                    print(f"  - {oferta.obtener_info()}")
            else: print("\nNo hay ofertas registradas") #Se envia este mensaje si no hay ninguna oferta.
        
        elif opcion == "4": break
        else: print("Opción no válida")                    

def menu_aspirantes():                             
    while True:                                    # Added missing while loop
        print("GESTIÓN DE ASPIRANTES")               
        print("\n1. Registrar aspirante")          
        print("2. Inscribir aspirante")            
        print("3. Actualizar correo")              
        print("4. Ver aspirantes")
        print("5. Volver al menú principal")      
        
        opcion = input("\nSelecciona una opción : ").strip() 
        
        if opcion == "1":                                  
            print("\n Registrar Aspirante ")
            codigo = input("Código del postulante : ").strip() # Código interno del aspirante.
            nombre = input("Nombre del postulante: ").strip()  # Nombre completo.
            fecha_inicio = input("Fecha de registro (DD/MM/YYYY): ").strip() # Fecha de registro en el sistema.
            cedula = input("Cédula: ").strip()  # Su número de identificación (clave principal).
            correo = input("Correo electrónico: ").strip() # Correo para contacto.
            telefono = input("Teléfono: ").strip()  # Número de teléfono.
            rol = input("Rol (Estudiante/Graduado): ").strip()  # Tipo de aspirante.
            try:
                puntaje = float(input("Puntaje inicial: ").strip()) # Pedimos el puntaje base (de examen, etc.).
                postulante = Postulante(codigo, nombre, fecha_inicio, cedula, correo, telefono, rol, puntaje) # Creamos el aspirante.
                datos["postulantes"][cedula] = postulante  # Lo guardamos con la cédula como clave.
                print(f"\nPostulante registrado: {postulante.obtener_informacion()}") # Confirmamos.
            except ValueError as e: print(f"\nError: {str(e)}") # Si el puntaje no es un número válido.
        
        elif opcion == "2":                                
            cedula = input("\nCédula del postulante: ").strip() # ¿Quién se va a inscribir?
            comentario = input("Comentario (opcional): ").strip() or None # Pedimos un comentario (puede ser vacío).
            if cedula in datos["postulantes"]:  # Verificamos que exista.
                try:
                    print(f"\n{datos['postulantes'][cedula].inscribirse(comentario)}") # Llamamos al método de inscripción.
                except ValueError as e: print(f"\nError: {str(e)}") # Manejo de errores.
            else: print("\nPostulante no encontrado")  # Avisamos si la cédula es incorrecta.
        
        elif opcion == "3":                                 
            cedula = input("\nCédula del postulante: ").strip() # ¿De quién es el correo a cambiar?
            nuevo_correo = input("Nuevo correo electrónico: ").strip() # Pedimos el nuevo correo.
            if cedula in datos["postulantes"]:# Verificamos que exista.
                try:
                    datos["postulantes"][cedula].correo = nuevo_correo # Actualizamos directamente el atributo.
                    print(f"\nCorreo actualizado para {cedula}")   # Confirmamos el cambio.
                except ValueError as e: print(f"\nError: {str(e)}") 
            else: print("\nPostulante no encontrado")           
        
        elif opcion == "4":                                 
            if datos["postulantes"]:                        
                print("\nASPIRANTES REGISTRADOS:")
                for cedula, postulante in datos["postulantes"].items(): # Recorremos.
                    print(f"  - {postulante.obtener_informacion()}") # Imprimimos sus datos.
            else: print("\nNo hay postulantes registrados")  # Se envia este mensaje si no hay nadie registrado.
        
        elif opcion == "5": break                         
        else: print("Opción no válida")                  

def menu_universidades():                              
    while True:                                       
        print("GESTIÓN DE UNIVERSIDADES")             
        print("\n1. Registrar universidad")            
        print("2. Abrir inscripciones")              
        print("3. Cerrar inscripciones")               
        print("4. Ver universidades")                   
        print("5. Volver al menú principal")             
    
        opcion = input("\nSelecciona una opción : ").strip()
        
        if opcion == "1":                                 
            codigo = input("\nCódigo de la universidad : ").strip() # Código único.
            nombre = input("Nombre de la universidad: ").strip() # Nombre oficial.
            fecha_inicio = input("Fecha de registro (DD/MM/YYYY): ").strip() # Fecha de registro.
            tipo = input("Tipo (Pública/Privada): ").strip()  # Tipo de institución.
            ubicacion = input("Ubicación principal: ").strip()  # Ciudad o ubicación principal.
            sedes_input = input("Sedes (separadas por coma, ej: Matriz, Sede Norte, Sede Sur): ").strip().split(",") # Sedes, separadas por coma.
            sedes = [s.strip() for s in sedes_input if s.strip()] # Limpiamos y guardamos la lista de sedes.
            try:
                universidad = Universidad(codigo, nombre, fecha_inicio, tipo, ubicacion, sedes) # Creamos la universidad.
                datos["universidades"][codigo] = universidad # Guardamos con el código como clave.
                print(f"\nUniversidad registrada: {universidad.obtener_info()}") # Confirmamos.
            except ValueError as e: print(f"\nError: {str(e)}")               
        
        elif opcion == "2":                                  
            codigo = input("\nCódigo de la universidad: ").strip() # ¿A qué universidad le abrimos?
            sede = input("Sede (dejar vacío para todas): ").strip() or None # Si es para una sede específica.
            if codigo in datos["universidades"]: # Verificamos que exista.
                try:
                    print(f"\n{datos['universidades'][codigo].abrir_inscripciones(sede)}") # Llamamos a la función de apertura.
                except ValueError as e: print(f"\nError: {str(e)}")
            else: print("\nUniversidad no encontrada")        
        
        elif opcion == "3":                                  
            codigo = input("\nCódigo de la universidad: ").strip() # ¿A qué universidad le cerramos?
            sede = input("Sede (dejar vacío para todas): ").strip() or None # Si es para una sede específica.
            if codigo in datos["universidades"]: # Verificamos existencia.
                try:
                    print(f"\n{datos['universidades'][codigo].cerrar_inscripciones(sede)}") # Llamamos a la función de cierre.
                except ValueError as e: print(f"\nError: {str(e)}")
            else: print("\nUniversidad no encontrada")        
        
        elif opcion == "4":
            if datos["universidades"]:                         
                print("\nUNIVERSIDADES REGISTRADAS:")
                for codigo, universidad in datos["universidades"].items(): # Recorremos.
                    print(f"  - {universidad.obtener_info()}")
            else: print("\nNo hay universidades registradas")   
        
        elif opcion == "5": break                            
        else: print("Opción no válida")                     

def menu_facultades():                          
    while True:                                   
        print("GESTIÓN DE FACULTADES")             
        print("\n1. Registrar facultad")          
        print("2. Agregar laboratorio")           
        print("3. Agregar computadoras")
        print("4. Ver facultades")                 
        print("5. Volver al menú principal")       
        
        opcion = input("\nSelecciona una opción : ").strip() 
        
        if opcion == "1":                                    
            codigo = input("\nCódigo de la facultad : ").strip() # Código único.
            nombre = input("Nombre de la facultad: ").strip()# Nombre de la facultad
            fecha_inicio = input("Fecha de registro (DD/MM/YYYY): ").strip() # Fecha del registri
            decano = input("Nombre del decano: ").strip()# Nombre del decano/a.
            try:
                facultad = Facultad(codigo, nombre, fecha_inicio, decano) # Creamos lafacultad.
                datos["facultades"][codigo] = facultad                   # Lo guardamos.
                print(f"\nFacultad registrada: {facultad.obtener_info()}") # Confirmamos.
            except ValueError as e: print(f"\nError: {str(e)}")          
        
        elif opcion == "2":                                 
            codigo = input("\nCódigo de la facultad: ").strip() # ¿A qué facultad le agregamos?
            if codigo in datos["facultades"]:   # Verificamos que exista.
                print(f"\n{datos['facultades'][codigo].agregar_laboratorio()}") # Aplicamos la suma de laboratorio.
            else: print("\nFacultad no encontrada")            # Aviso.
        
        elif opcion == "3":                                
            codigo = input("\nCódigo de la facultad: ").strip() # ¿A qué facultad le agregamos PCs?
            try:
                cantidad = int(input("Cantidad de computadoras: ").strip()) # ¿Cuántas computadoras?
                if codigo in datos["facultades"]: # Verificamos existencia.
                    print(f"\n{datos['facultades'][codigo].agregar_computadoras(cantidad)}") # Aplicamos la suma de PCs.
                else: print("\nFacultad no encontrada")           
            except ValueError as e: print(f"\nError: {str(e)}") 
        
        elif opcion == "4":
            if datos["facultades"]:                            
                print("\nFACULTADES REGISTRADAS:")
                for codigo, facultad in datos["facultades"].items():# Recorremos.
                    print(f"  - {facultad.obtener_info()}")
            else: print("\nNo hay facultades registradas")
        
        elif opcion == "5": break
        else: print("Opción no válida")                       

def menu_postulaciones():
    while True:                                         
        print("GESTIÓN DE POSTULACIONES")              
        print("\n1. Registrar postulación")             
        print("2. Ver postulaciones")
        print("3. Volver al menú principal")            
        
        opcion = input("\nSelecciona una opción : ").strip() 
        
        if opcion == "1":                                
            codigo = input("\nCódigo de la postulación (ej: POST001): ").strip() # Código único de la postulación.
            nombre = input("Nombre de la postulación: ").strip()# Nombre.
            fecha_inicio = input("Fecha de inicio (DD/MM/YYYY): ").strip() # Fecha de registro.
            cedula = input("Cédula del postulante: ").strip()  # Cédula del aspirante.
            codigo_carrera = input("Código de la carrera: ").strip()  # Código de la carrera deseada.
            sede = input("Sede de postulación: ").strip()  # Sede a la que aplica.
            fecha_postulacion = input("Fecha de postulación (DD/MM/YYYY): ").strip() # Fecha en que postula.
            hora = input("Hora de evaluación (HH:MM): ").strip()  # Hora de la posible evaluación.
            sala = input("Sala de evaluación: ").strip()  # Sala asignada.
            try:
                duracion = float(input("Duración de evaluación (horas): ").strip()) # Duración del examen.
                tipo = input("Tipo de evaluación: ").strip() # Tipo de prueba.
                if cedula in datos["postulantes"] and codigo_carrera in datos["carreras"]: # Verificamos que el aspirante y la carrera existan.
                    postulante = datos["postulantes"][cedula]  # Obtenemos el objeto postulante.
                    carrera = datos["carreras"][codigo_carrera]  # Obtenemos el objeto carrera.
                    # Aquí el código verifica si la sede es válida (POSIBLE PUNTO DE ERROR si Postulante no tiene Universidad/Sedes)
                    try:
                        if any(s in postulante.universidad.sedes for s in [sede]): # Verificamos que la sede exista en la universidad del postulante.
                            postulacion = Postulacion(codigo, nombre, fecha_inicio, postulante, carrera, sede, fecha_postulacion, hora, sala, duracion, tipo) # Creamos la postulacion.
                            datos["postulaciones"][codigo] = postulacion   # ¡Guardamos la postulación!
                            print(f"\nPostulación registrada: {postulacion.obtener_info()}") # Confirmamos.
                        else: print("\nSede no válida para esta universidad")   # Si la sede no está en la lista de la universidad.
                    except AttributeError:
                         print("\nError: Asegúrate de que el postulante esté asociado a una universidad con sedes válidas.") # Mensaje de error si la clase no tiene los atributos necesarios.
                else: print("\nPostulante o carrera no encontrados") # siel aspirante o la carrera no existen.
            except ValueError as e: print(f"\nError: {str(e)}")            
        
        elif opcion == "2":                                   
            if datos["postulaciones"]:                            
                print("\nPOSTULACIONES REGISTRADAS:")
                for codigo, postulacion in datos["postulaciones"].items(): # Recorremos.
                    print(f"  - {postulacion.obtener_info()}")
            else: print("\nNo hay postulaciones registradas")     
        
        elif opcion == "3": break                               
        else: print("Opción no válida")                           

def menu_proceso_admision():                            
    while True:                                       
        print("GESTIÓN DE PROCESO DE ADMISIÓN")        
        print("\n1. Crear proceso de admisión")        
        print("2. Iniciar proceso")                    
        print("3. Finalizar proceso")                   
        print("4. Ver procesos")                        
        print("5. Volver al menú principal")            
        
        opcion = input("\nSelecciona una opción ").strip() 
        
        if opcion == "1":                                 
            codigo = input("\nCódigo del proceso (ej: ADM2025): ").strip() # Código único.
            nombre = input("Nombre del proceso: ").strip() # Nombre.
            fecha_inicio = input("Fecha de inicio (DD/MM/YYYY): ").strip() # Cuándo empieza el proceso.
            responsable = input("Responsable: ").strip()   
            try:
                proceso = ProcesoAdmision(codigo, nombre, fecha_inicio, responsable) # Creamos el proceso.
                datos["procesos"][codigo] = proceso   # Lo guardamos.
                print(f"\nProceso creado: {proceso.obtener_info()}")  # Confirmamos.
            except ValueError as e: print(f"\nError: {str(e)}")  # Manejo de errores.
        
        elif opcion == "2":                                 
            codigo = input("\nCódigo del proceso: ").strip()  
            fecha_inicio = input("Fecha de inicio (opcional, DD/MM/YYYY): ").strip() or None # Fecha de inicio real.
            comentario = input("Comentario (opcional): ").strip() or None # Notas adicionales.
            if codigo in datos["procesos"]: # Verificamos que exista.
                try:
                    print(f"\n{datos['procesos'][codigo].iniciar_proceso(fecha_inicio, comentario)}") # Ponemos el proceso en 'En Curso'.
                except ValueError as e: print(f"\nError: {str(e)}")
            else: print("\nProceso no encontrado")            
        
        elif opcion == "3":                                 
            codigo = input("\nCódigo del proceso: ").strip()    
            if codigo in datos["procesos"]: # Verificamos existencia.
                try:
                    print(f"\n{datos['procesos'][codigo].finalizar_proceso()}") # Cambiamos su estado a 'Finalizado'.
                except ValueError as e: print(f"\nError: {str(e)}")
            else: print("\nProceso no encontrado")            
        
        elif opcion == "4":                                
            if datos["procesos"]:                             
                print("\nPROCESOS DE ADMISIÓN:")
                for codigo, proceso in datos["procesos"].items(): # Recorremos.
                    print(f"  - {proceso.obtener_info()}")
            else: print("\nNo hay procesos registrados")        
        
        elif opcion == "5": break
        else: print("Opción no válida")                        

def menu_evaluaciones():                           
    while True:
        print("GESTIÓN DE EVALUACIONES")            
        print("\n1. Registrar evaluación")           
        print("2. Iniciar evaluación")             
        print("3. Finalizar evaluación")            
        print("4. Ver evaluaciones")                
        print("5. Volver al menú principal")         
        
        opcion = input("\nSelecciona una opción : ").strip() 
        
        if opcion == "1":                                   
            codigo = input("\nCódigo de la evaluación : ").strip() # Código único del examen.
            nombre = input("Nombre de la evaluación: ").strip()     # Nombre del examen (ej: Prueba de Aptitud).
            fecha_inicio = input("Fecha de inicio (DD/MM/YYYY): ").strip() # Fecha de registro en el sistema.
            fecha = input("Fecha de evaluación (DD/MM/YYYY): ").strip()  # Fecha programada del examen.
            hora = input("Hora (HH:MM): ").strip()  # Hora de inicio.
            sala = input("Sala: ").strip()  # Sala o lugar.
            try:
                duracion = float(input("Duración (horas): ").strip())  # Duración en horas.
                tipo = input("Tipo de evaluación: ").strip()  # Tipo de evaluación (escrita, oral, etc.).
                evaluacion = Evaluacion(codigo, nombre, fecha_inicio, fecha, hora, sala, duracion, tipo) # Creamos ls evaluacion.
                datos["evaluaciones"][codigo] = evaluacion   # Lo guardamos.
                print(f"\nEvaluación registrada: {evaluacion.obtener_info()}") # Confirmamos.
            except ValueError as e: print(f"\nError: {str(e)}")           
        
        elif opcion == "2":                               
            codigo = input("\nCódigo de la evaluación: ").strip() 
            if codigo in datos["evaluaciones"]:                 
                try:
                    print(f"\n{datos['evaluaciones'][codigo].iniciar_evaluacion()}") # Cambiamos su estado a 'En Curso'.
                except ValueError as e: print(f"\nError: {str(e)}")
            else: print("\nEvaluación no encontrada")      
        
        elif opcion == "3":                  
            codigo = input("\nCódigo de la evaluación: ").strip() 
            if codigo in datos["evaluaciones"]:                 
                try:
                    print(f"\n{datos['evaluaciones'][codigo].finalizar_evaluacion()}") # Cambiamos su estado a 'Finalizada'.
                except ValueError as e: print(f"\nError: {str(e)}")
            else: print("\nEvaluación no encontrada")         
        elif opcion == "4":                                  
            if datos["evaluaciones"]:                          
                print("\nEVALUACIONES REGISTRADAS:")
                for codigo, evaluacion in datos["evaluaciones"].items(): # Recorremos.
                    print(f"  - {evaluacion.obtener_info()}")
            else: print("\nNo hay evaluaciones registradas")   
        
        elif opcion == "5": break                               
        else: print("Opción no válida")                          

def menu_carreras():                              
    while True:                                   
        print("GESTIÓN DE CARRERAS")             
        print("\n1. Registrar carrera")           
        print("2. Ver carreras")                   
        print("3. Volver al menú principal")     
        
        opcion = input("\nSelecciona una opción : ").strip() 
        
        if opcion == "1":       
            codigo = input("\nCódigo de la carrera : ").strip() # Código único de la carrera.
            nombre = input("Nombre de la carrera: ").strip()     # Nombre oficial de la carrera.
            fecha_inicio = input("Fecha de registro (DD/MM/YYYY): ").strip() # Fecha de registro.
            try:
                duracion = int(input("Duración (semestres): ").strip()) # Duración total en semestres.
                modalidad = input("Modalidad (Presencial/Virtual/Híbrida): ").strip() # Cómo se estudiara la carrera.
                carrera = Carrera(codigo, nombre, fecha_inicio, duracion, modalidad) # Creamos el usuario.
                datos["carreras"][codigo] = carrera  # Lo guardamos.
                print(f"\nCarrera registrada: {carrera.obtener_info()}") # Confirmamos.
            except ValueError as e: print(f"\nError: {str(e)}")  # Si la duración no es un número.
        
        elif opcion == "2":                                
            if datos["carreras"]:                          
                print("\nCARRERAS REGISTRADAS:")
                for codigo, carrera in datos["carreras"].items(): # Recorremos.
                    print(f"  - {carrera.obtener_info()}")
            else: print("\nNo hay carreras registradas")     
        
        elif opcion == "3": break                          
        else: print("Opción no válida")                      

def menu_usuarios():                              
    while True:                                  
        print("GESTIÓN DE USUARIOS")              
        print("\n1. Registrar usuario")            
        print("2. Ver usuarios")                   
        print("3. Volver al menú principal")      
        
        opcion = input("\nSelecciona una opción : ").strip() 
        
        if opcion == "1":                          
            codigo = input("\nCódigo del usuario : ").strip() # Código de usuario.
            nombre = input("Nombre del usuario: ").strip()  # Nombre del usuario
            fecha_inicio = input("Fecha de registro (DD/MM/YYYY): ").strip() # Fecha de registro.
            cedula = input("Cédula: ").strip() # Cédula (clave principal).
            correo = input("Correo electrónico: ").strip() # Correo del usuario.
            rol = input("Rol (Estudiante/Administrador): ").strip() # Nivel de acceso.
            try:
                usuario = Usuario(codigo, nombre, fecha_inicio, cedula, correo, rol) # Creamos el objeto.
                datos["usuarios"][cedula] = usuario                  
                print(f"\nUsuario registrado: {usuario.obtener_info()}") 
            except ValueError as e: print(f"\nError: {str(e)}")        
    
        elif opcion == "2":                                
            if datos["usuarios"]:                            
                print("\nUSUARIOS REGISTRADOS:")
                for cedula, usuario in datos["usuarios"].items(): # Recorremos.
                    print(f"  - {usuario.obtener_info()}")
            else: print("\nNo hay usuarios registrados")   
        
        elif opcion == "3": break                        
        else: print("Opción no válida")                      

def ver_resumen(): # Función para mostrar un resumen de todos los datos.
    print("RESUMEN DEL SISTEMA")                   
    print(f"Períodos: {Periodo.periodos_activos()}") # Mostramos el total de períodos activos.
    print(f"Ofertas: {OfertaAcademica.total_ofertas()}") # Mostramos el total de ofertas.
    print(f"Postulantes: {Postulante.total_postulantes()}") # Mostramos el total de aspirantes.
    print(f"Universidades: {Universidad.total_universidades()}") # Mostramos el total de universidades.
    print(f"Facultades: {Facultad.total_facultades()}") # Mostramos el total de facultades.
    print(f"Postulaciones: {Postulacion.total_postulaciones()}") # Mostramos el total de postulaciones.
    print(f"Procesos: {ProcesoAdmision.total_procesos()}") # Mostramos el total de procesos de admisión.
    print(f"Evaluaciones: {Evaluacion.total_evaluaciones()}") # Mostramos el total de evaluaciones programadas.
    print(f"Carreras: {Carrera.total_carreras()}") # Mostramos el total de carreras disponibles.
    print(f"Usuarios: {Usuario.total_usuarios()}") # Mostramos el total de usuarios del sistema.

if __name__ == "__main__":                       
    menu_principal()                             