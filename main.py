#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Requiere: pip install requests python-dotenv

import json
import requests
from config import BEARER_TOKEN, SOURCE_URL, TARGET_URL, HEADERS

# === 3) Obtener los flows desde SOURCE_URL ===

def get_flows() -> list:
    try:
        resp = requests.get(SOURCE_URL, headers=HEADERS, timeout=45)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"Error obteniendo flows: {resp.status_code} {resp.text}")
            return []
    except requests.RequestException as e:
        print(f"Error de red al obtener flows: {e}")
        return []


def put_flow(flow: dict, idx: int, total: int) -> None:
    flow_id = flow.get("id")
    if not flow_id:
        print(f"[{idx}/{total}] ❌ Objeto sin 'id'. Saltando.")
        return

    url = f"{TARGET_URL}/{flow_id}"
    # print(f"[{idx}/{total}] URL: {url}")
    # print(f"[{idx}/{total}] Headers: {HEADERS}")
    # print(f"[{idx}/{total}] Payload: {json.dumps(flow, indent=2)}")
    try:
        resp = requests.put(url, headers=HEADERS, json=flow, timeout=45)
        ok = 200 <= resp.status_code < 300
        status = "✅ OK" if ok else "❌ FAIL"
        print(f"[{idx}/{total}] PUT {flow_id} -> {resp.status_code} {status}")
        if not ok:
            body = resp.text
            if len(body) > 500:
                body = body[:500] + "…"
            print("   Respuesta:", body)
    except requests.RequestException as e:
        print(f"[{idx}/{total}] ❌ Error de red para {flow_id}: {e}")

flows = get_flows()

def main():
    total = len(flows)
    if total == 0:
        print("No hay elementos en 'flows'. Pega tu array en la variable 'flows'.")
        return

    for i, flow in enumerate(flows, 1):
        put_flow(flow, i, total)

if __name__ == "__main__":
    main()
