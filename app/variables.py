def import_variables(input_file: str) -> None:
    """Importa variables desde un archivo JSON al TARGET_URL. PUT si existe, POST si no existe."""
    print(f"Importando variables desde {input_file} a {TARGET_URL}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            variables = json.load(f)
    except FileNotFoundError:
        print(f"Archivo {input_file} no encontrado.")
        return
    if not isinstance(variables, list):
        print("El archivo no contiene una lista de variables.")
        return

    # Obtener variables existentes en el target
    try:
        url = f"{TARGET_URL}/variables"
        resp = requests.get(url, headers=HEADERS_TARGET, timeout=30)
        if resp.status_code == 200:
            existing = resp.json()
            existing_ids = {v.get("id") for v in existing if "id" in v}
        else:
            print(f"No se pudo obtener las variables existentes del target, se hará POST por defecto. Código: {resp.status_code}")
            existing_ids = set()
    except Exception as e:
        print(f"Error obteniendo ids existentes: {e}")
        existing_ids = set()

    for i, variable in enumerate(variables, 1):
        var_id = variable.get("id")
        if var_id and var_id in existing_ids:
            put_variables(var_id, variable)
        else:
            post_variables([variable])
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


def put_variables(id: str, variable: dict) -> None:
    """Actualiza una variable existente en el sistema target."""
    url = f"{TARGET_URL}/variables/{id}"
    #crear payload solo con con: name, type y value
    payload_variable = {
        "name": variable.get("name"),
        "type": variable.get("type"),
        "value": variable.get("value")
    }
    try:
        resp = requests.put(url, headers=HEADERS_TARGET, json=payload_variable, timeout=30)
        if resp.status_code == 200:
            print(f"Variable {id} actualizada exitosamente: {resp.json()}")
        else:
            print(f"Error actualizando variable {id} en el target: {resp.status_code} {resp.text}")
    except requests.RequestException as e:
        print(f"Error de red al actualizar variable {id} en el target: {e}")
# prueba
if __name__ == "__main__":
    get_variables()