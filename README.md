# TASTSERV — Automatización de Escaneo de Vulnerabilidades con n8n y OpenVAS

Repositorio oficial y reproducible del proyecto de grado **TASTSERV** (*Total Automated Security Testing Service*). El sistema orquesta de forma autónoma el descubrimiento de red con Nmap, el análisis profundo de vulnerabilidades con OpenVAS / Greenbone Community Edition, la persistencia estructurada en PostgreSQL y la notificación ejecutiva y técnica vía correo electrónico.

---

## Estructura del Repositorio

```text
/
├── README.md                    ← Qué es, cómo reproducir y tabla de versiones
├── workflows/
│   ├── experimento-2026-09.json ← Workflow de septiembre (versionId 6c2dd8e7…)
│   └── actual-20261105.json     ← Workflow en vivo (versionId ab9345e2…)
├── scripts/                     ← Scripts automated_scan.sh y automated_scan.gmp.py actuales
│   ├── automated_scan.sh
│   └── automated_scan.gmp.py
├── infra/
│   ├── greenbone/               ← Docker-compose de Greenbone Community Edition
│   ├── n8n/                     ← Compose de n8n y PostgreSQL con .env.example
│   └── vulnerables/             ← Dockerfiles, vsftpd.conf y configuraciones de Apache
├── db/
│   └── ddl_vulnerability_scans.sql ← DDL formal de la tabla en PostgreSQL
├── datos/
│   ├── tiempos_corridas.xlsx    ← Excel original de tiempos y métricas de tesis
│   ├── hallazgos_20261105.csv   ← CSV con los 146 hallazgos de la corrida 05/11
│   └── SHA256SUMS.txt          ← Sumas de verificación SHA-256 de los datos
├── evidencia/
│   └── 2026-11-05/              ← Capturas de pantalla y correo de reporte de escaneo
└── docs/
    └── VERSIONES.md             ← Registro detallado de cambios entre septiembre y hoy
```

---

## ¿Qué es TASTSERV?

TASTSERV es un pipeline integral para la automatización de escaneos de ciberseguridad, diseñado para reducir la sobrecarga operativa manual y eliminar errores de transcripción en la gestión continua de vulnerabilidades.

### Arquitectura del Pipeline

```
  ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
  │  Schedule Cron  │  o    │ Webhook Trigger │  o    │  Manual Button  │
  └────────┬────────┘       └────────┬────────┘       └────────┬────────┘
           │                         │                         │
           └─────────────────────────┼─────────────────────────┘
                                     ▼
                    ┌─────────────────────────────────┐
                    │ 1. Descubrimiento de Activos    │
                    │    Nmap (-sV -sC) sobre subred  │
                    └────────────────┬────────────────┘
                                     ▼
                    ┌─────────────────────────────────┐
                    │ 2. Extracción y Normalización   │
                    │    Parser XML (IPs y Puertos)   │
                    └────────────────┬────────────────┘
                                     ▼
                    ┌─────────────────────────────────┐
                    │ 3. Escaneo de Vulnerabilidades  │
                    │    OpenVAS / GMP Socket         │
                    │    (automated_scan.sh + .gmp.py)│
                    └────────────────┬────────────────┘
                                     ▼
                    ┌─────────────────────────────────┐
                    │ 4. Procesamiento de Hallazgos   │
                    │    Parser XML a JSON            │
                    └────────┬────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌──────────────────────────────┐  ┌──────────────────────────────┐
│ 5. Persistencia Relacional   │  │ 6. Notificación Ejecutiva    │
│    PostgreSQL 15             │  │    SMTP / Mailtrap (HTML+MD) │
│    (vulnerability_scans)     │  │    Resumen por severidad     │
└──────────────────────────────┘  └──────────────────────────────┘
```

---

## Tabla de Versiones

Para un desglose exhaustivo de cada cambio técnico, consultar [docs/VERSIONES.md](file:///home/tizi/n8n-stack/docs/VERSIONES.md).

| Parámetro | Versión Septiembre 2026 (`experimento-2026-09`) | Versión Actual (`actual-20261105`) |
|---|---|---|
| **Archivo Workflow** | `workflows/experimento-2026-09.json` | `workflows/actual-20261105.json` |
| **versionId n8n** | `6c2dd8e7-2cf4-452c-91cd-97834774432b` | `ab9345e2-b451-481a-9101-ee1624da8691` |
| **Git Tag** | `experimento-2026-09` | `entrega-defensa-20261110` (previa: `pre-defensa-20261105`) |
| **Commit Base** | `945a79eb0b1c067a6645ccab38b77fc4fa8d0729` | `0cb131258c585ea3232a1cf51bfd81c6e23ae754` |
| **Filtro GMP** | `rows=-1 levels=hmlg min_qod=0` (omite críticas) | `levels=chmlg rows=-1 min_qod=0` (captura total) |
| **Hallazgos Capturados** | 146 vulnerabilidades | 169 vulnerabilidades (incluye 23 críticas + CVE-2021-41773) |
| **Triggers de Inicio** | Solo `Schedule Trigger` (02:00 AM) | `Schedule` + `Webhook POST` + `Manual Trigger` |
| **Concurrencia** | Sin exclusión mutua | Control de proceso mediante `flock` en `/tmp/gvm_scan.lock` |
| **Manejo de Credenciales** | Contraseñas directas en entorno experimental | Rotadas criptográficamente y redactadas en Git (`<REDACTADO>`) |

---

## Guía de Reproducción Paso a Paso

### Prerrequisitos
* **Sistema Operativo**: Linux (Ubuntu 22.04 / 24.04 LTS o Debian 11/12).
* **Docker Engine**: Versión $\ge 24.0$.
* **Docker Compose**: Plugin V2 (`docker compose`).
* **Python**: 3.9 o superior.

---

### Paso 1: Configurar la Red Docker Común
Todos los contenedores de escaneo y objetivos conviven en la red tipo bridge `greenbone-community-edition_default`:
```bash
docker network create --subnet=172.18.0.0/16 greenbone-community-edition_default 2>/dev/null || true
```

---

### Paso 2: Desplegar el Motor Greenbone Community Edition
1. Posicionarse en el directorio de infraestructura de Greenbone:
   ```bash
   cd infra/greenbone
   docker compose up -d
   ```
2. Esperar a la sincronización de feeds de firmas (VT, SCAP, CERT). El estado puede verificarse con:
   ```bash
   docker compose logs -f gvmd
   ```
3. Una vez operativo, el servicio web de Greenbone Security Assistant estará disponible en `http://localhost:9392`.

---

### Paso 3: Desplegar los Servidores Vulnerables de Prueba
1. Iniciar los 3 contenedores del laboratorio experimental:
   ```bash
   cd infra/vulnerables
   docker compose up -d --build
   ```
2. Verificar la conectividad en la subred `172.18.0.0/16`:
   ```bash
   ping -c 1 172.18.0.200 # vuln-srv1 (FTP vsftpd, SSH débil)
   ping -c 1 172.18.0.201 # vuln-srv2 (Apache 2.4.49 CVE-2021-41773, SSH)
   ping -c 1 172.18.0.202 # vuln-srv3 (Apache 2.4.41, vsftpd, SSH)
   ```

---

### Paso 4: Desplegar PostgreSQL y n8n
1. Copiar la plantilla de variables de entorno y ajustar contraseñas:
   ```bash
   cd infra/n8n
   cp .env.example .env
   ```
2. Iniciar la base de datos PostgreSQL y el contenedor de n8n:
   ```bash
   docker compose up -d
   ```
3. El esquema se carga automáticamente al inicio desde [db/ddl_vulnerability_scans.sql](file:///home/tizi/n8n-stack/db/ddl_vulnerability_scans.sql). En caso de configurarlo manualmente:
   ```bash
   docker exec -i security_db psql -U n8n_user -d security_scans < ../../db/ddl_vulnerability_scans.sql
   ```

---

### Paso 5: Configurar los Scripts de Escaneo
1. Copiar los scripts de ejecución al directorio del sistema correspondiente o verificar que el contenedor n8n tenga el bind mount sobre `scripts/`:
   ```bash
   chmod +x scripts/automated_scan.sh scripts/automated_scan.gmp.py
   ```
2. Configurar las credenciales administrativas de Greenbone en `/home/tizi/.gvm.env` con permisos restringidos:
   ```bash
   cat << 'EOF' > ~/.gvm.env
   export GMP_USER="admin"
   export GMP_PASSWORD="tu_password_greenbone"
   EOF
   chmod 600 ~/.gvm.env
   ```

---

### Paso 6: Importar y Ejecutar el Workflow en n8n
1. Abrir la interfaz web de n8n en `http://localhost:5678`.
2. Crear un nuevo flujo y seleccionar **Import from File**.
3. Cargar el archivo [workflows/actual-20261105.json](file:///home/tizi/n8n-stack/workflows/actual-20261105.json).
4. Configurar las 3 credenciales en el gestor de n8n:
   - **SSH Password**: Credencial local o de host para lanzar Nmap y gvm-tools.
   - **PostgreSQL**: Host `security_db` (puerto interno `5432` o `host.docker.internal:5433`), base de datos `security_scans`, usuario `n8n_user`.
   - **SMTP**: Servidor Mailtrap o SMTP corporativo.
5. Hacer clic en **Test workflow** o disparar mediante Webhook:
   ```bash
   curl -X POST http://localhost:5678/webhook/trigger-scan
   ```
6. Verificar que los resultados se persistan en la tabla `vulnerability_scans` y se reciba el correo de resumen.

---

## Verificación de Integridad de Datos

Los archivos de datos originales y los reportes experimentales cuentan con sumas criptográficas generadas con SHA-256 en [datos/SHA256SUMS.txt](file:///home/tizi/n8n-stack/datos/SHA256SUMS.txt):

```bash
cd datos
sha256sum -c SHA256SUMS.txt
```
Salida esperada:
```
tiempos_corridas.xlsx: CORRECTO (OK)
hallazgos_20261105.csv: CORRECTO (OK)
```
