# API Contract - Microservicio de PIB

## Descripción del Servicio
Este microservicio proporciona datos del PIB de un país específico en un año determinado. La autenticación es requerida para acceder a este endpoint, validando un token previamente.

## Base URL
`/pib/`

---

## Endpoint: Obtener Datos del PIB
- **Descripción:** Recupera el valor del PIB para un país y un año específicos.
- **Método HTTP:** `GET`
- **URL del Endpoint:** `/pib/`

### Parámetros de Consulta (Query Parameters)
- **pais** (requerido): `string`  
  Descripción: Nombre del país para el que se requiere el dato del PIB.

- **año** (requerido): `integer`  
  Descripción: Año para el cual se requiere el valor del PIB.

### Encabezados (Headers)
- **Authorization** (requerido): `string`  
  Descripción: Token de autenticación en formato Bearer (`Bearer <token>`).

### Dependencias y Autenticación
- **Token de Autenticación:** Se espera que el token sea validado mediante la dependencia `validar_token`, que debe retornar un `token_payload` válido para que el acceso sea permitido.
- **Base de Datos:** La conexión a la base de datos es gestionada a través de la dependencia `get_db`, que proporciona acceso a la sesión de base de datos para realizar consultas.

### Respuesta
- **Código 200 - OK**
  - **Descripción:** Retorna el valor del PIB encontrado.
  - **Cuerpo de la Respuesta (Response Body):**  
    ```json
    {
        "pais": "string",
        "año": "integer",
        "pib_valor": "decimal"
    }
    ```

- **Código 404 - Not Found**
  - **Descripción:** Indica que no se encontraron datos para el país y año solicitados.
  - **Cuerpo de la Respuesta:**
    ```json
    {
        "detail": "Los datos no se encuentran disponibles"
    }
    ```

- **Código 401 - Unauthorized**
  - **Descripción:** Se presenta cuando el token de autorización no es válido o no se ha proporcionado.

### Errores y Manejo de Excepciones
- **404 Not Found:** Lanzada si los datos del PIB no están disponibles para el país y año solicitados.
- **401 Unauthorized:** Se maneja en la dependencia `validar_token` para validar la autenticidad del token antes de procesar la solicitud.
