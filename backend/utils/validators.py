import re
from ..utils.error_handler import ValidationError

def validate_email(email: str) -> bool:
    """
    Valida que el email tenga un formato correcto
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")
    return True

def validate_cedula(cedula: str) -> bool:
    """
    Valida que la cédula ecuatoriana sea válida
    """
    if not cedula.isdigit() or len(cedula) != 10:
        raise ValidationError("Cédula debe tener 10 dígitos numéricos")
    
    # Algoritmo de validación de cédula ecuatoriana
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    
    for i in range(9):
        valor = int(cedula[i]) * coeficientes[i]
        if valor > 9:
            valor -= 9
        total += valor
    
    verificador = 10 - (total % 10)
    if verificador == 10:
        verificador = 0
        
    if verificador != int(cedula[-1]):
        raise ValidationError("Número de cédula no válido")
    
    return True

def validate_phone(phone: str) -> bool:
    """
    Valida que el número de teléfono tenga un formato válido
    """
    pattern = r'^\+?593?\d{9}$'  # Formato: +593xxxxxxxxx o 0xxxxxxxxx
    if not re.match(pattern, phone):
        raise ValidationError("Invalid phone number format")
    return True

def validate_required(value: str, field_name: str) -> bool:
    """
    Valida que un campo requerido no esté vacío
    """
    if not value or not str(value).strip():
        raise ValidationError(f"{field_name} is required")
    return True