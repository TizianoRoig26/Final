#!/bin/sh
# automated_scan.sh
# Reemplaza automated_scan.gmp.py usando gvm-cli con XML directo.
# Todo el output de debug va a stderr, solo el XML del reporte va a stdout.
# Uso: automated_scan.sh <host_o_rango> <gmp_username> <gmp_password>

set -e

TARGET_HOSTS="${1:-192.168.100.0/24}"
GMP_USER="${2:-admin}"
GMP_PASS="${3:-<REDACTADO>}"

PORT_LIST_ID="33d0cd82-57c6-11e1-8ed1-406186ea4fc5"
SCAN_CONFIG_ID="daba56c8-73ec-11df-a475-002264764cea"
SCANNER_ID="08b69003-5fc2-4037-a479-93b440211c73"

TIMESTAMP=$(date +%s)
TARGET_NAME="Auto-Target-${TIMESTAMP}"
TASK_NAME="Auto-Scan-${TIMESTAMP}"

CLI="gvm-cli --gmp-username ${GMP_USER} --gmp-password ${GMP_PASS} socket"

echo "DEBUG: Creando target para ${TARGET_HOSTS}" >&2
TARGET_RESPONSE=$(${CLI} --xml "<create_target><name>${TARGET_NAME}</name><hosts>${TARGET_HOSTS}</hosts><port_list id='${PORT_LIST_ID}'/></create_target>")
echo "DEBUG: target response: ${TARGET_RESPONSE}" >&2

TARGET_ID=$(echo "${TARGET_RESPONSE}" | grep -o 'id="[^"]*"' | head -1 | cut -d'"' -f2)
echo "DEBUG: target_id=${TARGET_ID}" >&2

if [ -z "${TARGET_ID}" ]; then
    echo "ERROR: No se pudo crear el target. Respuesta: ${TARGET_RESPONSE}" >&2
    exit 1
fi

echo "DEBUG: Creando task" >&2
TASK_RESPONSE=$(${CLI} --xml "<create_task><name>${TASK_NAME}</name><target id='${TARGET_ID}'/><config id='${SCAN_CONFIG_ID}'/><scanner id='${SCANNER_ID}'/></create_task>")
echo "DEBUG: task response: ${TASK_RESPONSE}" >&2

TASK_ID=$(echo "${TASK_RESPONSE}" | grep -o 'id="[^"]*"' | head -1 | cut -d'"' -f2)
echo "DEBUG: task_id=${TASK_ID}" >&2

if [ -z "${TASK_ID}" ]; then
    echo "ERROR: No se pudo crear la task. Respuesta: ${TASK_RESPONSE}" >&2
    exit 1
fi

echo "DEBUG: Iniciando task" >&2
START_RESPONSE=$(${CLI} --xml "<start_task task_id='${TASK_ID}'/>")
echo "DEBUG: start response: ${START_RESPONSE}" >&2

REPORT_ID=$(echo "${START_RESPONSE}" | grep -o '<report_id>[^<]*</report_id>' | sed 's/<[^>]*>//g')
echo "DEBUG: report_id=${REPORT_ID}" >&2

if [ -z "${REPORT_ID}" ]; then
    echo "ERROR: No se pudo iniciar la task. Respuesta: ${START_RESPONSE}" >&2
    exit 1
fi

# Polling hasta que termine (max 30 minutos)
MAX_WAIT=1800
POLL_INTERVAL=15
ELAPSED=0

echo "DEBUG: Esperando que el escaneo termine..." >&2

while [ ${ELAPSED} -lt ${MAX_WAIT} ]; do
    STATUS_RESPONSE=$(${CLI} --xml "<get_tasks task_id='${TASK_ID}'/>")
    STATUS=$(echo "${STATUS_RESPONSE}" | grep -o '<status>[^<]*</status>' | head -1 | sed 's/<[^>]*>//g')
    PROGRESS=$(echo "${STATUS_RESPONSE}" | grep -o '<progress>[^<]*</progress>' | head -1 | sed 's/<[^>]*>//g')
    echo "DEBUG: status=${STATUS} progress=${PROGRESS}% elapsed=${ELAPSED}s" >&2

    case "${STATUS}" in
        Done|Stopped|Interrupted)
            echo "DEBUG: Escaneo finalizado con status=${STATUS}" >&2
            break
            ;;
    esac

    sleep ${POLL_INTERVAL}
    ELAPSED=$((ELAPSED + POLL_INTERVAL))
done

if [ ${ELAPSED} -ge ${MAX_WAIT} ]; then
    echo "ADVERTENCIA: timeout de ${MAX_WAIT}s alcanzado" >&2
fi

echo "DEBUG: Obteniendo reporte..." >&2
${CLI} --xml "<get_reports report_id='${REPORT_ID}' details='1' ignore_pagination='1'/>"

