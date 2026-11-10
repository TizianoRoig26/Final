#!/bin/sh
set -eu

# ==============================================================================
# automated_scan.sh - Wrapper de ejecucion segura para OpenVAS/GMP en gvm-tools
# Firma: automated_scan.sh <hosts> <puertos> [scan_id]
# ==============================================================================

TARGET_HOSTS="${1:-}"
TARGET_PORTS="${2:-}"
SCAN_ID="${3:-}"

# Normalizar literales vacios o undefined
[ "${TARGET_HOSTS}" = "undefined" ] || [ "${TARGET_HOSTS}" = "null" ] && TARGET_HOSTS=""
[ "${TARGET_PORTS}" = "undefined" ] || [ "${TARGET_PORTS}" = "null" ] && TARGET_PORTS=""
[ "${SCAN_ID}" = "undefined" ] || [ "${SCAN_ID}" = "null" ] && SCAN_ID=""

if [ -z "${TARGET_HOSTS}" ] || [ -z "${TARGET_PORTS}" ]; then
    echo "ERROR: Uso: $0 <hosts> <puertos> [scan_id]" >&2
    exit 1
fi

[ -n "${SCAN_ID}" ] || SCAN_ID="scan_$(date +%s)"

# 1. Resolver credenciales sin exponerlas en comandos ni logs
USER="${GVM_USER:-admin}"
PASS="${GVM_PASSWORD:-}"

if [ -z "${PASS}" ]; then
    if [ -f "/home/tizi/.gvm.env" ]; then
        . "/home/tizi/.gvm.env"
        USER="${GVM_USER:-admin}"
        PASS="${GVM_PASSWORD:-}"
    fi
fi

if [ -z "${PASS}" ]; then
    echo "ERROR: GVM_PASSWORD no esta configurada en el entorno ni en .gvm.env" >&2
    exit 1
fi

# 2. Generar archivo temporal de configuracion gvm-tools.conf protegido (chmod 600)
CONF_FILE=$(mktemp /tmp/gvm-tools-XXXXXX.conf)
chmod 600 "${CONF_FILE}"

cleanup() {
    rm -f "${CONF_FILE}"
}
trap cleanup EXIT INT TERM

# Escapar caracteres '%' para configparser en Python (BasicInterpolation requiere '%%')
PASS_ESCAPED=$(printf '%s\n' "${PASS}" | sed 's/%/%%/g')

cat <<EOF > "${CONF_FILE}"
[main]
timeout = 5400

[gmp]
username=${USER}
password=${PASS_ESCAPED}
EOF

# 3. Validar existencia del socket Unix de gvmd
SOCKET_PATH="/run/gvmd/gvmd.sock"
if [ ! -S "${SOCKET_PATH}" ]; then
    echo "ERROR: Socket GMP no encontrado en ${SOCKET_PATH}" >&2
    exit 2
fi

# 4. Ejecutar el script GMP asegurando que STDOUT sea puro XML y STDERR reciba los logs
echo "[automated_scan.sh] Ejecutando escaneo para hosts: ${TARGET_HOSTS} en puertos: ${TARGET_PORTS} (ID: ${SCAN_ID})" >&2

gvm-script -c "${CONF_FILE}" socket --socketpath "${SOCKET_PATH}" /scripts/automated_scan.gmp.py -- "${TARGET_HOSTS}" "${TARGET_PORTS}" "${SCAN_ID}"
EXIT_CODE=$?

exit ${EXIT_CODE}
