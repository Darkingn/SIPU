import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))
    reload = os.getenv("ENV", "development") == "development" and os.getenv("DEBUG_RELOAD", "false").lower() == "true"
    
    print(f"🚀 Iniciando API en {host}:{port}")
    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
