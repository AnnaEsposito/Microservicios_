from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DATABASE_URI = 'sqlite:///pib_variaciones.db'  
engine = create_engine(DATABASE_URI)
Base = declarative_base()

#crear una session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Esta función puede ser utilizada como una dependencia
def get_db():
    db = SessionLocal() # Crea una nueva sesión de base de datos
    try:
        yield db # Devuelve la sesión para ser utilizada en la ruta de la API
    finally:
        db.close() # Cierra la sesión de base de datos al finalizar