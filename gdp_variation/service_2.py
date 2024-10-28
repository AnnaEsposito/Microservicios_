import requests
import pybreaker
from sqlalchemy.orm import Session
from .models import PIBVariacion

# Crear un circuito breaker
breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=30)

# Modificar la función de consultar_pib
@breaker
def consultar_pib(pais: str, año: int, token: str):
    BASE_URL = f"http://localhost:8000/extractor/pib/?pais={pais}&año={año}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Realizar la solicitud al microservicio 1
        response = requests.get(BASE_URL, headers=headers)
        response.raise_for_status()  # Levantar error si la respuesta no es exitosa (4xx, 5xx)

        # Parsear la respuesta
        pib_data = response.json()
        return pib_data["pib_valor"]
    
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar PIB de {pais} en {año}: {e}")
        return None
    except pybreaker.CircuitBreakerError:
        print("Circuit breaker activo, solicitud bloqueada temporalmente.")
        return None

def calcular_variacion(pib_año1: float, pib_año2: float):
    return pib_año1 - pib_año2

def guardar_variacion(db: Session, pais: str, año_inicial: int, año_final: int, variacion: float):
    nuevo_registro = PIBVariacion(
        pais=pais,
        año_inicial=año_inicial,
        año_final=año_final,
        variacion=variacion
    )
    db.add(nuevo_registro)
    db.commit()
