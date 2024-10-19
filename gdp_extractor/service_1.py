from sqlalchemy.orm import Session
from models import pibData
import requests
from lxml import etree

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
                    # Crear una nueva instancia de pibData
                    new_record = pibData(pais=pais, año=año, pib_valor=float(pib_value[0]))

                    # Agregar a la sesión
                    db.add(new_record)

            # Confirmar los cambios en la base de datos
            db.commit()
        else:
            print(f'Error al acceder a la API para {pais}, estado: {response.status_code}')
