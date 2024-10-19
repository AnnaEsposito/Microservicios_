from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import pibData
from database import get_db


extractor_pib = APIRouter()

# Endpoint que expone los datos del PIB a otros servicios
@extractor_pib.get("/pib/")

def retornar_pib(pais: str, año: int, db: Session = Depends(get_db)):
    # Consultar la base de datos para el país y año dados
    datos_pib = db.query(pibData).filter(pibData.pais == pais, pibData.año == año).first()

    # Verificar si se encontraron datos
    if datos_pib is None:
        raise HTTPException(status_code=404, detail="Los datos no se encuentran disponibles")

    # Retornar los datos
    return {
        "pais": datos_pib.pais,
        "año": datos_pib.año,
        "pib_valor": datos_pib.pib_valor
    }



