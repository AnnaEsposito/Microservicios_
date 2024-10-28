from fastapi import FastAPI, HTTPException, Depends, Header
from gdp_variation.auth import generar_token
from gdp_variation.database import get_db, engine
from sqlalchemy.orm import Session
from gdp_variation.service_2 import consultar_pib, calcular_variacion, guardar_variacion
from gdp_variation.models import Base, PIBVariacion
from gdp_variation.schemas import PIBVariacionSchema
import jwt
from datetime import datetime, timedelta
app = FastAPI()

@app.on_event("startup")
def startup_event():
    # Eliminar tablas y recrearlas
    #Base.metadata.drop_all(bind=engine)  # Esto eliminará todas las tablas
    Base.metadata.create_all(bind=engine)  # Esto creará las tablas nuevamente
@app.get("/")
def read_root():
    return "{Mensaje: Servicio2 en línea}"

SECRET_KEY = "mi_clave_secreta"

@app.post("/generar-token/")
def generar_token(usuario_id: str):
    payload = {"usuario_id": usuario_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"token": token}

@app.post("/calcular-variacion/", response_model=None)
def calcular_y_guardar_variacion(pais: str, año1: int, año2: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.split(" ")[1]  # Extraer el token del encabezado
    
    # Consultar PIBs pasando el token
    pib_año1 = consultar_pib(pais, año1, token)
    pib_año2 = consultar_pib(pais, año2, token)
    
    # Continuar con el procesamiento...
    if pib_año1 is None or pib_año2 is None:
        raise HTTPException(status_code=404, detail="No se pudo obtener los datos de PIB para los años solicitados")

    # Calcular la variación
    variacion = calcular_variacion(pib_año1, pib_año2)

    # Guardar la variación en la base de datos
    guardar_variacion(db, pais, año1, año2, variacion)

    return {"message": "Variación del PIB guardada exitosamente"}



@app.get("/pib/{pais}/variacion", response_model=PIBVariacionSchema)
def obtener_variacion_pib(pais: str, db: Session = Depends(get_db)):
    variacion = db.query(PIBVariacion).filter(PIBVariacion.pais == pais).first()
    if variacion is None:
        raise HTTPException(status_code=404, detail="Variación del PIB no encontrada")
    return variacion  # Devuelve los datos como un objeto compatible con Pydantic


# Ejecutar la aplicación con Uvicorn
#if __name__ == "__main__":
 #   import uvicorn
  #  uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
  #if __name__ == "__main__":
    # Generar el token
    #token = generar_token("usuario123")
    
    # Consultar el PIB para un país y año específicos
    #valor_pib = consultar_pib("Argentina", 2020, token)
    #print(f"El PIB de Argentina en 2020 es: {valor_pib}")