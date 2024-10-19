from fastapi import FastAPI
from sqlalchemy.orm import Session
from router import extractor_pib
from service_1 import buscar_y_almacenar_pib
from database import get_db, engine, Base
from models import pibData  # Importa tu modelo

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

    
    