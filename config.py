import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Variables de configuración
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
SOURCE_URL = os.getenv("SOURCE_URL")  # URL de donde extraer los agentes (flows)
TARGET_URL = os.getenv("TARGET_URL")  # URL donde importar los agentes (flows)

# Cabeceras comunes (con Authorization)
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
