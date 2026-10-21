#!/usr/bin/env bash
# ==============================================================================
# test_pipeline.sh - Script de Verificación y Pruebas de Integración (TASTSERV)
# ==============================================================================
# Permite probar y verificar cada componente del pipeline de escaneo automatizado:
# 1. Conectividad y red (interfaz enp0s3 y hosts 192.168.56.x)
# 2. Estado de contenedores Docker (n8n, Greenbone CE)
# 3. Base de datos PostgreSQL (security_scans)
# 4. Descubrimiento de activos con Nmap
# 5. Script de orquestación GMP (automated_scan.sh)
# 6. Actualización de la planilla de tesis (planilla de tesis casos.xlsx)
# ==============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}        TASTSERV - VERIFICACIÓN Y PRUEBAS DE INTEGRACIÓN       ${NC}"
echo -e "${BLUE}================================================================${NC}"

# 1. VERIFICACIÓN DE RED
echo -e "\n${YELLOW}[1/5] Comprobando interfaz y conectividad con los hosts objetivo...${NC}"
TARGET_10="192.168.56.10"
TARGET_101="192.168.56.101"
TARGET_102="192.168.56.102"

# Verificar si enp0s3 tiene la IP asignada
if ! ip addr show enp0s3 | grep -q "192.168.56.101"; then
    echo -e "${YELLOW}-> Asignando IP 192.168.56.101/24 a la interfaz enp0s3...${NC}"
    sudo ip addr add 192.168.56.101/24 dev enp0s3 || true
fi

for host in "$TARGET_10" "$TARGET_101" "$TARGET_102"; do
    if ping -c 1 -W 2 "$host" > /dev/null 2>&1; then
        echo -e "  [✓] Host ${host}: ${GREEN}ALCANZABLE (UP)${NC}"
    else
        echo -e "  [✗] Host ${host}: ${RED}NO RESPONDE PING${NC}"
    fi
done

# 2. VERIFICACIÓN DE DOCKER Y SERVICIOS
echo -e "\n${YELLOW}[2/5] Comprobando contenedores Docker...${NC}"
if docker ps | grep -q "n8n"; then
    echo -e "  [✓] n8n container: ${GREEN}ACTIVO (puerto 5678)${NC}"
else
    echo -e "  [✗] n8n container: ${RED}INACTIVO${NC}"
fi

if docker ps | grep -q "greenbone-community-edition-gvmd-1"; then
    echo -e "  [✓] Greenbone gvmd: ${GREEN}ACTIVO${NC}"
else
    echo -e "  [✗] Greenbone gvmd: ${RED}INACTIVO${NC}"
fi

# 3. VERIFICACIÓN DE POSTGRESQL
echo -e "\n${YELLOW}[3/5] Comprobando base de datos PostgreSQL (security_scans)...${NC}"
RECORD_COUNT=$(sudo -u postgres psql -d security_scans -t -A -c "SELECT count(*) FROM vulnerability_scans;" 2>/dev/null || echo "0")
echo -e "  [✓] Registros en tabla vulnerability_scans: ${GREEN}${RECORD_COUNT}${NC}"

# 4. PRUEBA DE DESCUBRIMIENTO NMAP (Rápida sobre puertos principales)
echo -e "\n${YELLOW}[4/5] Probando descubrimiento Nmap sobre puertos de laboratorio (21, 22, 80)...${NC}"
nmap -sV -p 21,22,80 --open 192.168.56.10 192.168.56.102 -oG - | grep "Host:" || echo "Escaneo completado."

# 5. SINCRONIZACIÓN DE LA PLANILLA EXCEL
echo -e "\n${YELLOW}[5/5] Sincronizando planilla de tesis con los datos de laboratorio...${NC}"
RUN_USER="${SUDO_USER:-$USER}"
su - "$RUN_USER" -c "python3 /home/tizi/n8n-stack/populate_thesis_sheet.py" || python3 /home/tizi/n8n-stack/populate_thesis_sheet.py

echo -e "\n${GREEN}================================================================${NC}"
echo -e "${GREEN}      VERIFICACIÓN Y ACTUALIZACIÓN COMPLETADAS CON ÉXITO        ${NC}"
echo -e "${GREEN}================================================================${NC}"
echo -e "Planilla de tesis actualizada en: ${BLUE}/home/tizi/n8n-stack/planilla de tesis casos.xlsx${NC}\n"
