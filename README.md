# Hybo Agent Flow Import/Export Utility

Esta utilidad permite importar y exportar flujos (flows) de agentes desde una instancia local de Flowise a una aplicación desplegada en Azure.

## Descripción

El script `main.py` extrae flujos (flows) de agentes desde `SOURCE_URL` y los importa a `TARGET_URL` usando autenticación Bearer Token.

## Requisitos

- Python 3.x
- Librería `requests`: Instala con `pip install requests`

## Configuración

1. Edita `.env` (basado en `.env.example`) y configura:
   - `BEARER_TOKEN`: Tu token de autenticación Bearer.
   - `SOURCE_URL`: La URL de donde extraer los agentes (flows).
   - `TARGET_URL`: La URL donde importar los agentes (flows).

2. Instala dependencias: `pip install -r requirements.txt`.

## Uso

La herramienta soporta varios modos de operación:

- **Exportar flows a un archivo**:
  ```bash
  python main.py --export flows.json
  ```
  Esto extrae los flows desde `SOURCE_URL` y los guarda en `flows.json`.

- **Importar flows desde un archivo**:
  ```bash
  python main.py --import flows.json
  ```
  Esto lee los flows desde `flows.json` y los importa a `TARGET_URL`.

- **Sincronizar directamente**:
  ```bash
  python main.py --sync
  ```
  Esto extrae los flows desde `SOURCE_URL` y los importa directamente a `TARGET_URL`.

Si no se proporciona ningún argumento, se muestra la ayuda.

## Funciones

- `get_flows()`: Obtiene la lista de flujos desde `SOURCE_URL`.
- `put_flow(flow, idx, total)`: Envía un flujo individual a `TARGET_URL`.
- `export_flows(output_file)`: Exporta flujos a un archivo JSON.
- `import_flows(input_file)`: Importa flujos desde un archivo JSON.
- `sync_flows()`: Sincroniza flujos directamente entre URLs.
- `get_target_workspace_id()`: Obtiene el ID del workspace del destino desde `TARGET_URL`.
- `change_workspaceid(filename)`: Cambia el `workspaceId` en todos los elementos de un archivo JSON al ID del workspace del destino.

## Notas

- Asegúrate de que las URLs y tokens sean correctos antes de ejecutar.
- El script maneja errores de red y respuestas HTTP.
