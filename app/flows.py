#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Requiere: pip install requests python-dotenv

import json
import requests

from app.config import BEARER_TOKEN, SOURCE_URL, TARGET_URL, HEADERS_SOURCE, HEADERS_TARGET

from .utils import get_target_workspace_id, change_workspaceid
from .variables import get_variables, post_variables, put_variables
# === 3) Obtener los flows desde SOURCE_URL ===

def get_flows() -> list:
    try:
        url = f"{SOURCE_URL}/chatflows"
        resp = requests.get(url, headers=HEADERS_SOURCE, timeout=45)
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

    url = f"{TARGET_URL}/chatflows/{flow_id}"
    # print(f"[{idx}/{total}] URL: {url}")
    # print(f"[{idx}/{total}] Headers: {HEADERS}")
    # print(f"[{idx}/{total}] Payload: {json.dumps(flow, indent=2)}")
    try:
        resp = requests.put(url, headers=HEADERS_TARGET, json=flow, timeout=45)
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

def post_flow(flow: dict, idx: int, total: int) -> None:
    url = f"{TARGET_URL}/chatflows"
    try:
        resp = requests.post(url, headers=HEADERS_TARGET, json=flow, timeout=45)
        ok = 200 <= resp.status_code < 300
        status = "✅ OK" if ok else "❌ FAIL"
        print(f"[{idx}/{total}] POST {flow.get('id')} -> {resp.status_code} {status}")
        if not ok:
            body = resp.text
            if len(body) > 500:
                body = body[:500] + "…"
            print("   Respuesta:", body)
    except requests.RequestException as e:
        print(f"[{idx}/{total}] ❌ Error de red para {flow.get('id')}: {e}")

def export_variables(output_file: str) -> None:
    """Exporta las variables desde SOURCE_URL a un archivo JSON."""
    print(f"Exportando variables desde {SOURCE_URL}...")
    variables = get_variables()
    if not variables:
        print("No se encontraron variables para exportar.")
        return
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variables, f, indent=2, ensure_ascii=False)
    print(f"Variables exportadas a {output_file}")

def import_variables(input_file: str) -> None:
    """Importa las variables desde un archivo JSON a TARGET_URL."""
    print(f"Importando variables desde {input_file} a {TARGET_URL}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            variables = json.load(f)
    except FileNotFoundError:
        print(f"Archivo {input_file} no encontrado.")
        return
    total = len(variables)
    if total == 0:
        print("No hay variables en el archivo.")
        return

    # Publicar las variables en el sistema target
    for i, variable in enumerate(variables, 1):
        post_variables(variable)

def export_flows(output_file: str) -> None:
    """Exporta los flows desde SOURCE_URL a un archivo JSON."""
    print(f"Exportando flows desde {SOURCE_URL}...")
    flows = get_flows()
    variables = get_variables()
    if not flows:
        print("No se encontraron flows para exportar.")
        return
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(flows, f, indent=2, ensure_ascii=False)
    print(f"Flows exportados a {output_file}")


def import_flows(input_file: str) -> None:
    """Importa los flows desde un archivo JSON a TARGET_URL."""
    print(f"Importando flows desde {input_file} a {TARGET_URL}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            flows = json.load(f)
    except FileNotFoundError:
        print(f"Archivo {input_file} no encontrado.")
        return
    total = len(flows)
    if total == 0:
        print("No hay flows en el archivo.")
        return

    # Obtener los ids existentes en el target
    try:
        url = f"{TARGET_URL}/chatflows"
        resp = requests.get(url, headers=HEADERS_TARGET, timeout=45)
        if resp.status_code == 200:
            existing = resp.json()
            existing_ids = {f.get("id") for f in existing if "id" in f}
        else:
            print(f"No se pudo obtener los flows existentes del target, se hará POST por defecto. Código: {resp.status_code}")
            existing_ids = set()
    except Exception as e:
        print(f"Error obteniendo ids existentes: {e}")
        existing_ids = set()

    for i, flow in enumerate(flows, 1):
        if flow.get("id") in existing_ids:
            put_flow(flow, i, total)
        else:
            post_flow(flow, i, total)

def sync_flows() -> None:
    """Sincroniza: exporta de SOURCE_URL e importa a TARGET_URL."""
    print(f"Sincronizando flows de {SOURCE_URL} a {TARGET_URL}...")
    flows = get_flows()
    total = len(flows)
    workspace_id = get_target_workspace_id()
    flows = change_workspaceid(flows, workspace_id)
    if total == 0:
        print("No hay flows para sincronizar.")
        return
    for i, flow in enumerate(flows, 1):
        put_flow(flow, i, total)

