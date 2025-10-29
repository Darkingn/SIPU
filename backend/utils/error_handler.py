class APIError(Exception):
    def __init__(self, message, status_code=500, details=None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

class ValidationError(APIError):
    def __init__(self, message="Validation error", details=None):
        super().__init__(message, status_code=400, details=details)

class DatabaseError(APIError):
    def __init__(self, message="Database error", details=None):
        super().__init__(message, status_code=500, details=details)

class AuthenticationError(APIError):
    def __init__(self, message="Authentication failed", details=None):
        super().__init__(message, status_code=401, details=details)

def handle_error(error):
    """
    Manejador global de errores para la aplicación
    """
    if isinstance(error, APIError):
        response = {
            "error": error.message,
            "status": error.status_code
        }
        if error.details:
            response["details"] = error.details
        return response, error.status_code
    
    # Para errores no manejados
    return {
        "error": "Internal server error",
        "status": 500
    }, 500