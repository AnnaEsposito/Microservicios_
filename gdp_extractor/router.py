from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .models import pibData
from .database import get_db
import jwt

extractor_pib = APIRouter()
SECRET_KEY = "mi_clave_secreta"

# Función para validar el token
def validar_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  # Eliminar el prefijo 'Bearer '
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token inválido")

# Endpoint que expone los datos del PIB a otros servicios
@extractor_pib.get("/pib/")
def retornar_pib(pais: str, año: int, db: Session = Depends(get_db),token_payload: dict = Depends(validar_token)):#autenthification: str = depend(token)
    #token=autenthification
    #if token == "mi_token":
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



