from fastapi import FastAPI, HTTPException, Header
from sqlalchemy.orm import Session
from gdp_extractor.router import extractor_pib
from gdp_extractor.service_1 import buscar_y_almacenar_pib
from gdp_extractor.database import get_db, engine, Base
from gdp_extractor.models import pibData  # Importa tu modelo
import jwt

app = FastAPI()

# Registrar la ruta
app.include_router(extractor_pib, prefix="/extractor")

@app.get("/")
def read_root():
    return "HOLA"
    
@app.on_event("startup")
def startup_event():
    
    # Crear las tablas en la base de datos si no existen
    Base.metadata.create_all(bind=engine)
    
    # Obtener la sesión de la base de datos
    db: Session = next(get_db())
    buscar_y_almacenar_pib(db)  # Ejecutar la función para buscar y almacenar PIB

SECRET_KEY = "mi_clave_secreta"
@app.post("/validar-token/")
def validar_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  # Obtener el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"mensaje": "Token válido", "payload": payload}
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(status_code=403, detail="Token inválido o ha expirado") 
    