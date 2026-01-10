# --- SRP: Clase separada para gestionar Recursos Físicos ---
class InventarioRecursos:
    def __init__(self, laboratorios=0, computadoras=0):
        self.laboratorios = laboratorios
        self.computadoras = computadoras

    def agregar_laboratorio(self):
        self.laboratorios += 1

    def agregar_computadoras(self, cantidad):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self.computadoras += cantidad

# --- SRP: La clase Facultad solo representa la entidad administrativa ---
class Facultad:
    def __init__(self, codigo, nombre, decano, recursos: InventarioRecursos = None):
        self.codigo = codigo
        self.nombre = nombre
        self.decano = decano
        # DIP: Dependemos de una abstracción de recursos (Composición)
        self.recursos = recursos if recursos else InventarioRecursos()

    @property
    def decano(self):
        return self._decano

    @decano.setter
    def decano(self, value):
        if not value or not value.strip():
            raise ValueError("El decano no puede estar vacío")
        self._decano = value

    def obtener_info(self):
        return (f"Facultad: {self.nombre} (ID: {self.codigo})\n"
                f"Decano: {self.decano}\n"
                f"Infraestructura: {self.recursos.laboratorios} Labs, "
                f"{self.recursos.computadoras} Computadoras")

# --- SRP: Gestión global de facultades (Repositorio) ---
class FacultadRepository:
    def __init__(self):
        self._facultades = []

    def registrar(self, facultad: Facultad):
        self._facultades.append(facultad)
        print(f"Facultad '{facultad.nombre}' registrada.")

    @property
    def total(self):
        return len(self._facultades)

# --- USO DEL SISTEMA ---

# 1. Creamos el gestor y los recursos
repo = FacultadRepository()
recursos_sistemas = InventarioRecursos(laboratorios=5, computadoras=150)

# 2. Creamos la facultad inyectando sus dependencias
facultad_sistemas = Facultad("FISE", "Ingeniería en Sistemas", "Ing. Juan Pérez", recursos_sistemas)

# 3. Operamos de forma limpia
facultad_sistemas.recursos.agregar_computadoras(20)
repo.registrar(facultad_sistemas)

print("-" * 30)
print(facultad_sistemas.obtener_info())
print(f"Total facultades en el sistema: {repo.total}")