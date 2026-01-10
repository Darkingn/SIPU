from datetime import datetime
from typing import List

# --- SRP: Clase para manejar la lógica de fechas ---
class RangoFechas:
    def __init__(self, inicio: str, fin: str):
        self.inicio = datetime.strptime(inicio, "%Y-%m-%d")
        self.fin = datetime.strptime(fin, "%Y-%m-%d")
        
        if self.inicio > self.fin:
            raise ValueError("La fecha de inicio no puede ser posterior a la de fin")

    def incluye(self, fecha: datetime) -> bool:
        return self.inicio <= fecha <= self.fin

# --- SRP: La clase Periodo es ahora una Entidad pura ---
class Periodo:
    def __init__(self, codigo: str, nombre: str, descripcion: str, rango: RangoFechas):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.rango = rango  # Composición

    def esta_activo_en(self, fecha: datetime) -> bool:
        return self.rango.incluye(fecha)

    def obtener_info(self) -> str:
        return (f"Periodo: {self.nombre} ({self.codigo})\n"
                f"Descripción: {self.descripcion}\n"
                f"Rango: {self.rango.inicio.date()} a {self.rango.fin.date()}")

# --- SRP & OCP: Gestor de Periodos ---
class PeriodoRepository:
    def __init__(self):
        self._periodos: List[Periodo] = []

    def registrar_periodo(self, periodo: Periodo):
        self._periodos.append(periodo)

    @property
    def total(self) -> int:
        return len(self._periodos)

# --- USO DEL SISTEMA ---

# 1. Definimos el rango de tiempo
try:
    rango_2025 = RangoFechas("2025-01-01", "2025-06-30")
    periodo_1 = Periodo("P1-2025", "Primer Semestre 2025", "Periodo ordinario", rango_2025)

    # 2. Registramos en el repositorio
    repo = PeriodoRepository()
    repo.registrar_periodo(periodo_1)

    # 3. Verificamos actividad con fechas reales
    hoy = datetime.now()
    estado = "ACTIVO" if periodo_1.esta_activo_en(hoy) else "INACTIVO"
    
    print(periodo_1.obtener_info())
    print(f"Estado al día de hoy ({hoy.date()}): {estado}")
    print(f"Total de periodos registrados: {repo.total}")

except ValueError as e:
    print(f"Error de validación: {e}")