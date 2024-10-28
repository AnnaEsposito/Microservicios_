import jwt
from datetime import datetime, timedelta

SECRET_KEY = "mi_clave_secreta"

def generar_token(usuario_id: str):
    payload = {"usuario_id": usuario_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


