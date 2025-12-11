# API BCV - Tasa de Cambio

Esta es una API sencilla construida con Flask que obtiene las tasas de cambio del Dólar y el Euro directamente del sitio web del Banco Central de Venezuela (BCV).

## Funcionalidad

La API realiza *web scraping* al sitio oficial del BCV para extraer los valores actuales de las divisas y los sirve en formato JSON.

## Requisitos

*   Python 3.x
*   pip (gestor de paquetes de Python)

## Instalación

1.  **Clonar el repositorio** (o descargar los archivos):
    ```bash
    git clone <url-del-repositorio>
    cd api-bcv
    ```

2.  **Crear un entorno virtual** (recomendado):
    ```bash
    python3 -m venv .venv
    user@machine:~/file/routes$. .venv/bin/activate  # En Linux/Mac
    # .venv\Scripts\activate   # En Windows
    ```

3.  **Instalar las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1.  **Iniciar la aplicación**:
    ```bash
    python3 app.py
    ```
    La aplicación se iniciará en `http://127.0.0.1:5000` (por defecto).

2.  **Endpoints disponibles**:

    *   **Inicio (`GET /`)**:
        Muestra un mensaje de bienvenida, la fecha actual del BCV y la lista de endpoints.
        ```json
        {
          "date": "Fecha del BCV",
          "endpoints": [
            {
              "tasa del dolar": "/dolar",
              "tasa del euro": "/euro",
              "bancos": "/bancos",
              "bancos/:banco_nombre": "/bancos/:banco_nombre"
            }
          ]
        }
        ```

    *   **Tasa del Dólar (`GET /dolar`)**:
        Devuelve el valor actual del dólar.
        ```json
        {
          "currency": " USD",
          "dolar": " 35,00000000 "
        }
        ```

    *   **Tasa del Euro (`GET /euro`)**:
        Devuelve el valor actual del euro.
        ```json
        {
          "currency": " EUR",
          "euro": " 38,00000000 "
        }
        ```

## Modificación

El código principal se encuentra en `app.py`.

*   **Extracción de datos**: Se utiliza `BeautifulSoup` para analizar el HTML del BCV. Si la estructura de la página del BCV cambia, deberás actualizar los selectores en las funciones `dolar()`, `euro()` y `bancos()`.
    *   Actualmente busca `div` con id `dolar` y `euro`.
    *   Actualmente busca `table` con class `views-table cols-3 table table-0 table-0 table-0 table-0`.
*   **Nuevas monedas**: Para agregar otra moneda (ej. Yuan), puedes duplicar la función `dolar()` o `euro()`, cambiar la ruta (`@app.route('/yuan')`) y ajustar el ID del elemento HTML que buscas (`soup.find_all("div", id="yuan")`).
*   **Puerto**: Puedes cambiar el puerto por defecto en la línea `app.run(debug=True, port=5001)`.

## Notas

*   Esta API desactiva las advertencias de SSL (`urllib3.disable_warnings`) para evitar errores con el certificado del sitio del BCV.
*   El `User-Agent` está configurado para simular un navegador real y evitar bloqueos.
