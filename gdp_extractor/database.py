# con esto creo mi base de datos 

from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'sqlite:///bd_AR_BR_PY.sqlite' 
engine =create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Esta función puede ser utilizada como una dependencia
def get_db():
    db = SessionLocal() # Crea una nueva sesión de base de datos
    try:
        yield db # Devuelve la sesión para ser utilizada en la ruta de la API
    finally:
        db.close() # Cierra la sesión de base de datos al finalizar