#!/bin/sh
# automated_scan.sh
# Wrapper ultra-robusto para n8n -> OpenVAS (Greenbone)
# Tolera llamadas con 4 argumentos, 3 argumentos, argumentos vacios o desplazados.

DEFAULT_HOSTS=""
DEFAULT_PORTS="22,80,443,5678,8080"
DEFAULT_USER="admin"
DEFAULT_PASS="<REDACTADO>"
SOCKET_PATH="/run/gvmd/gvmd.sock"

ARG1="${1}"
ARG2="${2}"
ARG3="${3}"
ARG4="${4}"

# Normalizar cadenas literales 'undefined' o 'null'
[ "${ARG1}" = "undefined" ] || [ "${ARG1}" = "null" ] && ARG1=""
[ "${ARG2}" = "undefined" ] || [ "${ARG2}" = "null" ] && ARG2=""
[ "${ARG3}" = "undefined" ] || [ "${ARG3}" = "null" ] && ARG3=""
[ "${ARG4}" = "undefined" ] || [ "${ARG4}" = "null" ] && ARG4=""

# =========================================================================
# Resolucion inteligente de argumentos
# =========================================================================

# Caso 1: Argumentos desplazados (hosts y puertos vinieron vacios)
# ej: sh automated_scan.sh admin <password>
if [ "${ARG1}" = "admin" ] || [ "${ARG2}" = "${DEFAULT_PASS}" ] && [ -z "${ARG3}" ]; then
    echo "WARN: [automated_scan.sh] Argumentos desplazados detectados sin hosts especificados." >&2
    TARGET_HOSTS=""
    TARGET_PORTS="${DEFAULT_PORTS}"
    GMP_USER="${ARG1:-${DEFAULT_USER}}"
    GMP_PASS="${ARG2:-${DEFAULT_PASS}}"

# Caso 2: Formato clasico de 3 argumentos: <hosts> <user> <pass> (sin puertos)
# ej: sh automated_scan.sh 192.168.100.10 admin <password>
elif [ -n "${ARG1}" ] && [ "${ARG2}" = "admin" ]; then
    echo "INFO: [automated_scan.sh] Formato de 3 argumentos detectado (<hosts> <user> <pass>). Asignando puertos por defecto." >&2
    TARGET_HOSTS="${ARG1}"
    TARGET_PORTS="${DEFAULT_PORTS}"
    GMP_USER="${ARG2}"
    GMP_PASS="${ARG3:-${DEFAULT_PASS}}"

# Caso 3: Formato estandar de 4 argumentos: <hosts> <ports> [user] [pass]
else
    TARGET_HOSTS="${ARG1}"
    TARGET_PORTS="${ARG2:-${DEFAULT_PORTS}}"
    GMP_USER="${ARG3:-${DEFAULT_USER}}"
    GMP_PASS="${ARG4:-${DEFAULT_PASS}}"
fi

# Validar que existan hosts objetivos
if [ -z "${TARGET_HOSTS}" ]; then
    echo "ERROR: [automated_scan.sh] No se recibieron hosts objetivos para escanear (TARGET_HOSTS vacio)." >&2
    exit 1
fi

# Sanity check: si TARGET_PORTS no contiene digitos, forzar DEFAULT_PORTS
if ! echo "${TARGET_PORTS}" | grep -qE '[0-9]'; then
    echo "WARN: [automated_scan.sh] TARGET_PORTS ('${TARGET_PORTS}') no contiene numeros. Usando ${DEFAULT_PORTS}" >&2
    TARGET_PORTS="${DEFAULT_PORTS}"
fi

echo "DEBUG: TARGET_HOSTS=${TARGET_HOSTS}" >&2
echo "DEBUG: TARGET_PORTS=${TARGET_PORTS}" >&2
echo "DEBUG: GMP_USER=${GMP_USER}" >&2
echo "DEBUG: SOCKET_PATH=${SOCKET_PATH}" >&2

# --- Verificacion del socket GVM ---
if [ ! -S "${SOCKET_PATH}" ]; then
    echo "ERROR: Socket GVM no encontrado en ${SOCKET_PATH}" >&2
    exit 1
fi
echo "DEBUG: Socket GVM OK: ${SOCKET_PATH}" >&2

# --- Verificacion de gvm-script ---
if ! command -v gvm-script > /dev/null 2>&1; then
    echo "ERROR: gvm-script no encontrado en PATH" >&2
    exit 1
fi

# --- Archivo de configuracion temporal ---
CONF_FILE="/tmp/gvm-tools-$$.conf"
cat > "${CONF_FILE}" << CONF
[main]
timeout = 600

[gmp]
username=${GMP_USER}
password=${GMP_PASS}
CONF

echo "DEBUG: Configuracion temporal creada en ${CONF_FILE}" >&2

# Limpiar el archivo de config al salir
trap 'rm -f "${CONF_FILE}"; echo "DEBUG: Conf temporal eliminada." >&2' EXIT

echo "DEBUG: Lanzando gvm-script..." >&2

# Lanzar gvm-script con '--' para delimitar argumentos
gvm-script \
    -c "${CONF_FILE}" \
    socket --socketpath "${SOCKET_PATH}" \
    /scripts/automated_scan.gmp.py \
    -- \
    "${TARGET_HOSTS}" \
    "${TARGET_PORTS}"

GVM_EXIT=$?
echo "DEBUG: gvm-script finalizo con codigo de salida: ${GVM_EXIT}" >&2
exit "${GVM_EXIT}"