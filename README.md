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

Ejecuta el script con:

```bash
python main.py
```

El script extraerá los flujos desde `SOURCE_URL` y los importará a `TARGET_URL`.

## Funciones

- `get_flows()`: Obtiene la lista de flujos desde la URL local.
- `put_flow(flow, idx, total)`: Envía un flujo individual al endpoint de Azure.

## Notas

- Asegúrate de que las URLs y tokens sean correctos antes de ejecutar.
- El script maneja errores de red y respuestas HTTP.
