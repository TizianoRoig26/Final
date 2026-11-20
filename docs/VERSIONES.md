# Historial y Registro de Versiones — TASTSERV

Este documento detalla exhaustivamente las diferencias arquitectónicas, de configuración y de código entre la versión basal de los experimentos de la tesis (septiembre de 2026) y la versión consolidada actual (noviembre de 2026).

---

## 1. Tabla Comparativa Resumen

| Dimensión / Componente | Versión Septiembre 2026 (`experimento-2026-09`) | Versión Actual (`entrega-defensa-20261118`) | Impacto / Justificación Técnica |
|---|---|---|---|
| **Workflow n8n: ID de Versión** | `6c2dd8e7-2cf4-452c-91cd-97834774432b` | `ab9345e2-b451-481a-9101-ee1624da8691` | Exportación en vivo desde la base de datos SQLite de n8n. |
| **Workflow n8n: Nodos de Disparo** | Solo `Schedule Trigger` (cron diario a las 02:00). | `Schedule Trigger` + `Webhook - Trigger Scan` (`/webhook/trigger-scan`) + `When clicking 'Test workflow'` (manual trigger). | Permite disparar escaneos bajo demanda desde APIs/Webhooks o desde la interfaz gráfica sin esperar la ejecución del cron. |
| **Workflow n8n: Descubrimiento Nmap** | IPs fijas del laboratorio hardcodeadas en nodo SSH (`172.18.0.200 172.18.0.201 172.18.0.202`). | Detección dinámica de subred activa en host vía interfaz de red (`ip -o -4 addr show...`). | Mayor portabilidad del flujo ante cambios de direccionamiento IP o interfaces virtuales de Docker. |
| **Control de Concurrencia** | Sin mecanismo de exclusión mutua. | Wrapper bash con `flock -n /tmp/gvm_scan.lock`. | Previene que ejecuciones concurrentes colisionen o corrompan tareas activas en OpenVAS. |
| **Filtro GMP (OpenVAS)** | `filter_string="rows=-1 levels=hmlg min_qod=0"` | `filter_string="levels=chmlg rows=-1 min_qod=0"` | En septiembre se omitía el nivel `c` (Críticas), reportando **146 hallazgos**. La versión actual incluye `c`, capturando los **169 hallazgos totales** (incluyendo las 23 críticas y CVE-2021-41773). |
| **Manejo de Credenciales GMP** | Credenciales pasadas por variables inline o argumentos bash. | Archivo protegido `/home/tizi/.gvm.env` (`chmod 600`) y variables de entorno sin salida en consola. | Protege las credenciales administrativas de Greenbone contra inspección de procesos (`ps aux`) y logs de n8n. |
| **Persistencia PostgreSQL** | Expresión `${v.host}:${v.port}` susceptible a concatenación ambigua. | Normalización estricta de host y puerto, DDL con índices y clave primaria `SERIAL`. | Integridad referencial y deduplicación de hallazgos en la tabla `vulnerability_scans`. |
| **Seguridad de Repositorio** | Contraseñas de desarrollo presentes en commits históricos. | Historial saneado con `git-filter-repo` (`<REDACTADO>`), contraseña de PostgreSQL rotada a 24 caracteres aleatorios. | Mitigación total de fuga de secretos y saneamiento formal del repositorio Git. |

---

## 2. Evolución Detallada del Workflow n8n

### Septiembre 2026 (`workflows/experimento-2026-09.json`)
- **Version ID**: `6c2dd8e7-2cf4-452c-91cd-97834774432b`
- **Total de Nodos**: 10 nodos secuenciales.
- **Topología**: Disparo exclusivo por temporizador programado (`Schedule Trigger`).
- **Comportamiento**:
  1. Ejecuta Nmap directamente contra los 3 objetivos del laboratorio (`172.18.0.200`, `172.18.0.201`, `172.18.0.202`).
  2. Parsea el XML de salida para extraer tuplas `(host, port)`.
  3. Lanza el escaneo en Greenbone llamando a `automated_scan.sh`.
  4. Extrae y convierte el reporte XML a formato JSON.
  5. Inserta los registros en PostgreSQL (`security_scans`).
  6. Compone y despacha el correo electrónico de notificación.

### Actual (`workflows/actual-20261105.json`)
- **Version ID**: `ab9345e2-b451-481a-9101-ee1624da8691`
- **Total de Nodos**: 12 nodos (incorporación de disparadores alternativos).
- **Mejoras Incorporadas**:
  - **Disparador Manual (`When clicking 'Test workflow'`)**: Permite realizar pruebas operativas y corridas ad-hoc desde el editor visual de n8n.
  - **Disparador Webhook (`Webhook - Trigger Scan`)**: Expone un endpoint HTTP POST (`/webhook/trigger-scan`) para integrar el pipeline con plataformas externas o sistemas CI/CD.
  - **Detección Dinámica de Subred**: Nmap autodescubre el segmento de red activo o recurre a la subred de fallback sin requerir direcciones IP fijas en el nodo.
  - **Persistencia Robusta**: Corrección en la extracción de campos para asegurar que host y puerto se registren correctamente en las columnas de la base de datos PostgreSQL.

---

## 3. Evolución de los Scripts de Escaneo (`scripts/`)

### 1. Parámetro de Severidad GMP (`automated_scan.gmp.py`)
En la ejecución experimental de septiembre de 2026, la consulta al protocolo GMP utilizaba:
```python
# Versión de Septiembre (146 hallazgos capturados)
filter_string = "rows=-1 levels=hmlg min_qod=0"
```
Los niveles de severidad en OpenVAS/GMP se codifican como:
- `c`: Critical (9.0 - 10.0)
- `h`: High (7.0 - 8.9)
- `m`: Medium (4.0 - 6.9)
- `l`: Low (0.1 - 3.9)
- `g`: Log / Informational (0.0)

Al utilizar `levels=hmlg`, el filtro excluía deliberadamente el nivel `c`. En el laboratorio de pruebas, el total de hallazgos descubiertos es de **169**, de los cuales exactamente **23 son de severidad Crítica**. Por esta razón, el script de septiembre persistía $169 - 23 = 146$ vulnerabilidades.

En la versión actual, el script configura:
```python
# Versión Actual (169 hallazgos totales, captura íntegra)
filter_string = "levels=chmlg rows=-1 min_qod=0"
```
Con la adición de `c`, el pipeline captura la totalidad de las 169 vulnerabilidades, incluyendo el hallazgo activo de **CVE-2021-41773** (severidad 9.8 Crítica) en `172.18.0.201:80/tcp`.

### 2. Wrapper de Ejecución (`automated_scan.sh`)
- **Control de Bloqueo (`flock`)**: Se incorporó el uso de `flock -n /tmp/gvm_scan.lock` para garantizar que una ejecución no solape ni interrumpa a otra en el motor Greenbone.
- **Gestión Segura de Secretos**: El script consulta `/home/tizi/.gvm.env` (con permisos de lectura restringida `chmod 600`) para autenticarse ante `gvm-tools`, asegurando que ninguna contraseña se transmita en texto plano ni se registre en el buffer de salida de n8n.
- **Normalización de Argumentos**: Valida literales `"undefined"` o `"null"` para prevenir errores cuando n8n evalúa expresiones vacías.

---

## 4. Evolución de la Infraestructura y Servidores Vulnerables (`infra/`)

### Aclaración Definitiva de Servicios
Durante las iteraciones de la documentación preliminar existió una errata sobre la ubicación de Apache 2.4.49. La configuración real y definitiva desplegada en los contenedores es:

1. **`vuln-srv1` (`172.18.0.200`)**:
   - Sistema base: Debian Buster.
   - Servicios: `vsftpd` 3.0.3 (con login anónimo permitido) y `OpenSSH` configurado con cifrados y MACs obsoletas (3DES-CBC, HMAC-MD5).
2. **`vuln-srv2` (`172.18.0.201`)**:
   - Imagen base: `httpd:2.4.49` oficial.
   - Servicios: **Apache HTTP Server 2.4.49** en puerto 80/tcp y OpenSSH en puerto 22/tcp.
   - Vulnerabilidad intencional: **CVE-2021-41773** (Path Traversal y RCE) habilitada mediante directiva `<Directory /> Require all granted` en `httpd.conf`.
   - Directorio `/secretos/config.txt` para pruebas de auditoría local.
3. **`vuln-srv3` (`172.18.0.202`)**:
   - Sistema base: Ubuntu 20.04.
   - Servicios: **Apache HTTP Server 2.4.41** en puerto 80/tcp, `vsftpd` en puerto 21/tcp y `OpenSSH` en puerto 22/tcp.
   - Configuraciones: `ServerTokens Full`, `ServerSignature On` e indexación de directorios activada.
   - Directorio `/secretos/config.txt`.

---

## 5. Esquema de Base de Datos y Persistencia (`db/`)

El archivo [ddl_vulnerability_scans.sql](../db/ddl_vulnerability_scans.sql) define el esquema normalizado en PostgreSQL:
- Clave primaria subrogada (`SERIAL PRIMARY KEY`).
- Campo `scan_date` con marca temporal y zona horaria (`TIMESTAMP WITH TIME ZONE`).
- Índices B-tree en `host`, `scan_date` y `severity` para acelerar las consultas agregadas y reportes ejecutivos.
- Asignación de privilegios de lectura, inserción y secuencias para el usuario de servicio `n8n_user`.

---

## 6. Saneamiento de Seguridad y Buenas Prácticas

1. **Rotación Criptográfica de Contraseñas**:
   - PostgreSQL: Rotada el 17/11/2026; valor no publicado.
   - Greenbone/GMP: Contraseña de usuario `admin` rotada y aislada en `.gvm.env`.
   - Mailtrap: Credenciales sandbox revocadas y documentadas como variables de plantilla.
2. **Reescritura de Historial Git**:
   - Se aplicó `git-filter-repo` para purgar todas las apariciones de credenciales de desarrollo (`hola123`, `Ajedrez2011`) en la totalidad de los commits anteriores, reemplazándolas por el token `<REDACTADO>`.
3. **Plantillas de Configuración**:
   - Creación de `.env.example` para evitar la inclusión accidental de variables confidenciales en el control de versiones.

---

## 7. Mapeo de Git Tags y Hashes

| Tag | Tipo | Commit Hash Apuntado | Propósito / Hito |
|---|---|---|---|
| **`experimento-2026-09`** | Annotated | `945a79eb0b1c067a6645ccab38b77fc4fa8d0729` | Congelamiento de la base experimental de la tesis (septiembre de 2026). |
| **`pre-defensa-20261105`** | Annotated | `ea31cf69d47ced34df6ac883a4fcaf688ec86214` | Hito de saneamiento de credenciales, rotación de PostgreSQL y respuestas preliminares. |
| **`entrega-defensa-20261110`** | Annotated | `0cb131258c585ea3232a1cf51bfd81c6e23ae754` | Versión final para defensa: workflow vivo exportado (`ab9345e2`), filtro GMP `chmlg` y scripts sincronizados. |
| **`entrega-defensa-20261118`** | Annotated | `2c23ed22a58c3f0955ab77a7d5be63306be35753` | Consolidación para defensa: réplica pareada Camino B, fe de erratas, digests fijados (C6), endurecimiento de n8n (C9) y protección de hashes. |

