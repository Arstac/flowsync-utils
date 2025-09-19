# utils.py

# Funcion get target workspace id
# Descripcion: hace una llamada a <target_url>/api/v1/variables, y, de cualquier elemento de la lista, si hay un elemento con "name" == "WORKSPACE_ID", devuelve su "value"
# Si no hay ningun elemento con "name" == "WORKSPACE_ID", devuelve None
import json
import requests
from app.config import TARGET_URL, HEADERS_TARGET
from typing import Optional

def get_target_workspace_id() -> Optional[str]:
    """
    Obtiene el identificador del workspace del sistema target.
    Realiza una solicitud GET al endpoint de variables del sistema target y extrae el valor de "workspaceId"
    de la primera variable encontrada, si existe. Si no se encuentra la variable o ocurre un error en la solicitud,
    retorna None.
    Returns:
        Optional[str]: El identificador del workspace si se encuentra, de lo contrario None.
    """
    url = f"{TARGET_URL}/variables"
    try:
        resp = requests.get(url, headers=HEADERS_TARGET, timeout=30)
        if resp.status_code == 200:
            variables = resp.json()
            print(f"Variables obtenidas del target: {variables}")
            
            if isinstance(variables, list) and len(variables) > 0:
                return variables[0].get("workspaceId")
            print("No se encontró la variable workspaceId en el target.")
            return None
        else:
            print(f"Error obteniendo variables del target: {resp.status_code} {resp.text}")
            return None
    except requests.RequestException as e:
        print(f"Error de red al obtener variables del target: {e}")
        return None


def change_workspaceid(filename: str, new_workspace_id: str) -> None:
    """Cambia el workspaceId de todos los elementos en el archivo JSON al workspaceId del destino."""
    if not new_workspace_id:
        print("No se pudo obtener el workspace ID del destino. Abortando.")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("El archivo JSON no es una lista. Abortando.")
            return

        changed_count = 0
        for item in data:
            if "workspaceId" in item:
                item["workspaceId"] = new_workspace_id
                changed_count += 1

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Se cambió el workspaceId en {changed_count} elementos del archivo {filename}.")

    except FileNotFoundError:
        print(f"Archivo {filename} no encontrado.")
    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON: {e}")
    except Exception as e:
        print(f"Error procesando el archivo: {e}")


# prueba
if __name__ == "__main__":
    workspace_id = get_target_workspace_id()
    if workspace_id:
        print(f"Cambiando workspaceId a {workspace_id}")
        change_workspaceid("flow.json", workspace_id)
    else:
        print("No se pudo obtener el WORKSPACE_ID del target.")