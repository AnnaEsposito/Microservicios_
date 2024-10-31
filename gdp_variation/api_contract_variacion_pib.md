# API Contract - Microservicio de Variación del PIB

## Descripción
Este microservicio proporciona endpoints para generar tokens, calcular y guardar la variación del PIB entre dos años y consultar las variaciones almacenadas para un país específico.

## Endpoints

---

### 1. Generar Token

- **URL:** `/generar-token/`
- **Método:** `POST`
- **Descripción:** Genera un token de autenticación para un usuario especificado.
- **Parámetros del Cuerpo (JSON):**
  - `usuario_id` (string, requerido): Identificador único del usuario para el cual se generará el token.
- **Respuesta:**
  - **Código 200 - OK:**
    ```json
    {
      "token": "string"  // Token JWT para autenticación.
    }
    ```

---

### 2. Calcular y Guardar Variación del PIB

- **URL:** `/calcular-variacion/`
- **Método:** `POST`
- **Descripción:** Calcula la variación del PIB entre dos años para un país y guarda el resultado en la base de datos.
- **Parámetros de la Consulta:**
  - `pais` (string, requerido): Nombre del país.
  - `año1` (integer, requerido): Año inicial para la comparación del PIB.
  - `año2` (integer, requerido): Año final para la comparación del PIB.
- **Encabezado de Autorización:**
  - `Authorization` (string, requerido): Token JWT con formato `Bearer <token>`.
- **Respuesta:**
  - **Código 200 - OK:**
    ```json
    {
      "message": "Variación del PIB guardada exitosamente"
    }
    ```
  - **Código 404 - Not Found:**
    ```json
    {
      "detail": "No se pudo obtener los datos de PIB para los años solicitados"
    }
    ```

---

### 3. Obtener Variación del PIB

- **URL:** `/pib/{pais}/variacion`
- **Método:** `GET`
- **Descripción:** Obtiene la variación del PIB almacenada para un país.
- **Parámetros de Ruta:**
  - `pais` (string, requerido): Nombre del país.
- **Respuesta:**
  - **Código 200 - OK:** Devuelve la variación del PIB.
    ```json
    {
      "id": 1,
      "pais": "string",
      "año_inicial": 2020,
      "año_final": 2021,
      "variacion": 5.5
    }
    ```
  - **Código 404 - Not Found:**
    ```json
    {
      "detail": "Variación del PIB no encontrada"
    }
    ```

---

## Modelos de Respuesta

### PIBVariacionSchema

```json
{
  "id": "integer",
  "pais": "string",
  "año_inicial": "integer",
  "año_final": "integer",
  "variacion": "number"
}
