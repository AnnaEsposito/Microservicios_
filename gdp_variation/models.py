from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float
from .database import Base, engine
from sqlalchemy.orm import sessionmaker

# Definición del modelo
class PIBVariacion(Base):
    __tablename__ = 'pib_variaciones'
    id = Column(Integer, primary_key=True)
    pais = Column(String, nullable=False)
    año_inicial = Column(Integer, nullable=False)
    año_final = Column(Integer, nullable=False)
    variacion = Column(Float, nullable=False)

