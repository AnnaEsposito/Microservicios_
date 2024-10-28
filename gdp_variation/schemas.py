from pydantic import BaseModel  # Importación absoluta
from .models import PIBVariacion 

class PIBVariacionSchema(BaseModel):
    id:int
    pais: str
    año_inicial: int
    año_final: int
    variacion: float

    class Config:
        orm_mode = True  # Permite a Pydantic trabajar con objetos ORM de SQLAlchemy

