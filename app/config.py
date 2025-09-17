import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Variables de configuración
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
SOURCE_URL = os.getenv("SOURCE_URL")  # URL de donde extraer los agentes (flows)
TARGET_URL = os.getenv("TARGET_URL")  # URL donde importar los agentes (flows)
TOKEN_SOURCE = os.getenv("TOKEN_SOURCE")
TOKEN_TARGET = os.getenv("TOKEN_TARGET")
# Cabeceras comunes (con Authorization)
HEADERS_SOURCE = {
    "Authorization": f"Bearer {TOKEN_SOURCE}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

HEADERS_TARGET = {
    "Authorization": f"Bearer {TOKEN_TARGET}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
