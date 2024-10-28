from sqlalchemy.orm import Session
from .models import pibData
import requests
from lxml import etree
import pika

def enviar_mensaje(mensaje):
    """Función para enviar mensajes a RabbitMQ"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue="notificaciones")
    channel.basic_publish(exchange='', routing_key='notificaciones', body=mensaje)
    print("Mensaje enviado:", mensaje)
    connection.close()

def buscar_y_almacenar_pib(db: Session):
    # URLs de interés
    urls = {
        "AR": "https://api.worldbank.org/v2/country/AR/indicator/NY.GDP.MKTP.CD",
        "BR": "https://api.worldbank.org/v2/country/BR/indicator/NY.GDP.MKTP.CD",
        "PY": "https://api.worldbank.org/v2/country/PY/indicator/NY.GDP.MKTP.CD"
    }

    for pais, url in urls.items():
        # Realizar la consulta a la API
        response = requests.get(url)

        if response.status_code == 200:
            arbol = etree.fromstring(response.content)

            # Obtener los PIBs para 2022 y 2023
            for año in [2022, 2023]:
                pib_value = arbol.xpath(f"//wb:data[wb:date='{año}']/wb:value/text()", namespaces={'wb': 'http://www.worldbank.org'})
                
                if pib_value:
                    # Verificar si ya existe en la base de datos
                    registro_existente = db.query(pibData).filter_by(pais=pais, año=año).first()
                    
                    if not registro_existente:
                        # Crear una nueva instancia de pibData
                        new_record = pibData(pais=pais, año=año, pib_valor=float(pib_value[0]))

                        # Agregar a la sesión y confirmar cambios
                        db.add(new_record)
                        db.commit()

                        # Enviar mensaje de notificación a RabbitMQ
                        mensaje = f"Nueva información disponible: PIB de {pais} para {año} registrado con valor {pib_value[0]}"
                        enviar_mensaje(mensaje)
                    else:
                        print(f"El PIB de {pais} para el año {año} ya está registrado.")
        else:
            print(f'Error al acceder a la API para {pais}, estado: {response.status_code}')
