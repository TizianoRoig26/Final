#!/usr/bin/env python3
"""
export_openvas_report.py
Script host para exportar reportes de OpenVAS en XML y CSV (perfiles primario y defecto).
Invoca gvm-script dentro del contenedor gvm-tools y guarda los artefactos en --salida.
"""
import argparse
import os
import subprocess
import sys
import json

def main():
    parser = argparse.ArgumentParser(description="Exportar reporte OpenVAS dual (primario y defecto)")
    parser.add_argument("--salida", required=True, help="Directorio destino en el host")
    parser.add_argument("--report-id", default="latest", help="UUID del reporte en gvmd (default: latest)")
    parser.add_argument("--perfil", default="ambos", choices=["primario", "defecto", "ambos"], help="Perfil de filtro a exportar")
    parser.add_argument("--secrets-file", default=os.path.expanduser("~/camino_b_secrets.env"), help="Ruta al archivo de secretos")
    args = parser.parse_args()

    abs_salida = os.path.abspath(args.salida)
    os.makedirs(abs_salida, exist_ok=True)

    # 1. Cargar credenciales GMP
    gvm_user = "admin"
    gvm_pass = ""
    if os.path.exists(args.secrets_file):
        with open(args.secrets_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("export GVM_USER="):
                    gvm_user = line.split("=", 1)[1].strip('"\'')
                elif line.startswith("export GVM_PASS="):
                    gvm_pass = line.split("=", 1)[1].strip('"\'')

    if not gvm_pass and os.path.exists("/home/tizi/.gvm.env"):
        with open("/home/tizi/.gvm.env", "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GVM_USER="):
                    gvm_user = line.split("=", 1)[1].strip('"\'')
                elif line.startswith("GVM_PASSWORD="):
                    gvm_pass = line.split("=", 1)[1].strip('"\'')

    if not gvm_pass:
        sys.stderr.write("ERROR: No se encontró GVM_PASS en ~/camino_b_secrets.env ni en ~/.gvm.env\n")
        sys.exit(1)

    repo_dir = "/home/tizi/n8n-stack"
    compose_file = "/home/tizi/docker-compose.yml"

    # 2. Comando docker compose para ejecutar gvm-script dentro de gvm-tools
    cmd = [
        "docker", "compose", "-f", compose_file, "run", "-T", "--rm", "--no-deps",
        "-v", f"{repo_dir}/scripts:/scripts",
        "-v", f"{abs_salida}:/salida",
        "gvm-tools", "sh", "-c",
        f"""
CONF=$(mktemp /tmp/gvm-XXXX.conf)
cat << 'CONF_EOF' > "$CONF"
[main]
timeout = 300

[gmp]
username = {gvm_user}
password = {gvm_pass}
CONF_EOF

gvm-script -c "$CONF" socket --socketpath /run/gvmd/gvmd.sock \
  /scripts/export_openvas_report.gmp.py -- "{args.report_id}" "/salida" "{args.perfil}"
STATUS=$?
rm -f "$CONF"
exit $STATUS
"""
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        sys.stderr.write(f"ERROR: Fallo al exportar reporte: {res.stderr}\n")
        sys.exit(res.returncode)

    sys.stdout.write(res.stdout)
    sys.stderr.write(f"[export_openvas_report] Reportes exportados exitosamente en: {abs_salida}\n")

if __name__ == "__main__":
    main()
