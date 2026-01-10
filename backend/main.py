from fastapi import FastAPI


app = FastAPI(
    title="Sistema de Admisión",
    description="API para la comunicación entre frontend y backend",
    version="1.0.0"
)




@app.get("/")
def health_check():
    return {"estado": "API activa"}
