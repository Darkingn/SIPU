from datetime import datetime

class BaseModel:
    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Convierte el modelo a un diccionario, eliminando los guiones bajos de los nombres de atributos
        """
        return {
            key.lstrip('_'): value 
            for key, value in self.__dict__.items()
            if not key.startswith('__')
        }

    def from_dict(self, data: dict):
        """
        Actualiza el modelo con datos de un diccionario
        """
        for key, value in data.items():
            setattr(self, f"_{key}", value)
        self.updated_at = datetime.now()
        return self

    def validate(self):
        """
        Método para ser sobreescrito por las clases hijas
        para implementar validaciones específicas
        """
        return True