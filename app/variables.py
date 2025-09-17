# variables.py
# Obtiene las variables del sistema source y las guarda en variables.json
# Luego, publica esas variables en el sistema target

import json
import requests
from app.config import TARGET_URL, HEADERS_TARGET, SOURCE_URL, HEADERS_SOURCE
from typing import Optional

def get_variables() -> None:
    """Obtiene las variables del sistema source y las guarda en variables.json."""
    url = f"{SOURCE_URL}/variables"
    try:
        resp = requests.get(url, headers=HEADERS_SOURCE, timeout=30)
        if resp.status_code == 200:
            variables = resp.json()
            print(f"Variables obtenidas del source: {variables}")
            # Guardar en variables.json
            with open('variables.json', 'w', encoding='utf-8') as f:
                json.dump(variables, f, indent=2, ensure_ascii=False)
            print("Variables guardadas en variables.json")
        else:
            print(f"Error obteniendo variables del source: {resp.status_code} {resp.text}")
    except requests.RequestException as e:
        print(f"Error de red al obtener variables del source: {e}")

def post_variables(variables: list) -> None:
    """Publica una lista de variables en el sistema target."""
    url = f"{TARGET_URL}/variables"
    try:
        resp = requests.post(url, headers=HEADERS_TARGET, json=variables, timeout=30)
        if resp.status_code == 200 or resp.status_code == 201:
            print(f"Variables publicadas exitosamente: {resp.json()}")
        else:
            print(f"Error publicando variables en el target: {resp.status_code} {resp.text}")
    except requests.RequestException as e:
        print(f"Error de red al publicar variables en el target: {e}")

# prueba
if __name__ == "__main__":
    get_variables()