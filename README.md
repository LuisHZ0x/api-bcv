# API BCV - Tasas de Cambio

API construida con Flask que obtiene las tasas de cambio del Dólar y el Euro directamente del sitio web del [Banco Central de Venezuela (BCV)](https://www.bcv.org.ve/) mediante web scraping.

## Requisitos

- Python 3.x
- pip

## Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone <url-del-repositorio>
   cd api-bcv
   ```

2. **Crear y activar un entorno virtual**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate   # Windows
   ```

3. **Instalar las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:

   ```bash
   cp .env.example .env
   ```

   | Variable | Descripción | Default |
   |----------|-------------|---------|
   | `URL_BASE` | URL del sitio del BCV | `https://www.bcv.org.ve/` |
   | `CACHE_TTL_SECONDS` | Tiempo de vida del caché en segundos | `3600` (1 hora) |
   | `BCV_TIMEOUT` | Timeout del request HTTP en segundos | `10` |

## Uso

```bash
python3 app.py
```

La aplicación se inicia en `http://127.0.0.1:5000`.

### Endpoints

Todos los endpoints están bajo el prefijo `/v1`.

URL base: `https://api-bcv-nine.vercel.app`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/v1` | Fecha del BCV y lista de endpoints |
| `GET` | `/v1/dolar` | Tasa actual del dólar |
| `GET` | `/v1/euro` | Tasa actual del euro |
| `GET` | `/v1/bancos` | Listado de bancos con sus tasas |
| `GET` | `/v1/bancos/<nombre>` | Tasa de un banco específico |

#### Ejemplos de respuesta

**`GET /v1/dolar`**

```json
{
  "currency": "USD",
  "dolar": "93.58"
}
```

**`GET /v1/bancos/banesco`**

```json
{
  "banco": {
    "banco": "BANESCO",
    "tasa": "93,58000000"
  }
}
```

## Estructura del proyecto

```
api-bcv/
├── app.py                       # Configuración de Flask, CORS y blueprints
├── src/
│   ├── scraper/
│   │   ├── __init__.py
│   │   └── bcv_scraper.py       # Scraping y parseo del BCV (con caché)
│   └── routes/
│       ├── __init__.py
│       ├── dolar.py             # Endpoint /dolar
│       ├── euro.py              # Endpoint /euro
│       └── bancos.py            # Endpoints /bancos
├── .env.example
├── requirements.txt
└── vercel.json                  # Configuración para deploy en Vercel
```

### Arquitectura

La lógica de scraping está centralizada en `BCVScraper` (`src/scraper/bcv_scraper.py`). Es el **único módulo** que hace requests HTTP al BCV y parsea HTML. Las rutas solo consumen datos del scraper y arman respuestas JSON.

El scraper incluye un **caché en memoria con TTL** configurable. Una vez que se hace el primer request al BCV, las siguientes peticiones a cualquier endpoint devuelven datos cacheados hasta que expire el TTL.

## Modificación

- **Cambios en la web del BCV**: Si la estructura HTML del BCV cambia, solo hay que modificar `src/scraper/bcv_scraper.py`.
- **Nueva moneda**: Llamar `scraper.get_rate("nueva_moneda_id")` desde una nueva ruta — el scraper ya soporta cualquier divisa por ID de elemento HTML.
