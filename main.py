import argparse
from app.flows import get_flows, export_flows, import_flows, sync_flows
from app.variables import get_variables, post_variables
from app.utils import get_target_workspace_id, change_workspaceid

flows = get_flows()

def main():
    parser = argparse.ArgumentParser(description="Herramienta para importar/exportar flows de agentes")
    parser.add_argument('--export', type=str, help='Exportar flows a archivo JSON (ej: --export flows.json)')
    parser.add_argument('--import', dest='import_file', type=str, help='Importar flows desde archivo JSON (ej: --import flows.json)')
    parser.add_argument('--sync', action='store_true', help='Sincronizar: exportar de SOURCE_URL e importar a TARGET_URL')

    args = parser.parse_args()

    if args.export:
        export_flows(args.export)
    elif args.import_file:
        import_flows(args.import_file)
    elif args.sync:
        sync_flows()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
