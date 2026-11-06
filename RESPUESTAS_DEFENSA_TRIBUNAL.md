# Respuestas Técnicas y Evidencia para la Defensa — TASTSERV

Documento compilado a partir del código real del sistema, la base de datos PostgreSQL, los manifiestos de Docker y la memoria técnica del proyecto (*Proyecto Final TastServ.md*).

---

## 1. Alcance de las 5 corridas automatizadas (Nmap y OpenVAS)
* **¿Qué comando de Nmap corrió en las pruebas experimentales?**  
  Se utilizó el comando con IPs fijas:
  ```bash
  nmap -sV -sC -oX /tmp/nmap_scan_${TS}.xml 172.18.0.200 172.18.0.201 172.18.0.202
  ```
* **¿Qué hosts y puertos recibió OpenVAS?**  
  Nmap escaneó los 3 hosts completos (`.200`, `.201`, `.202`) y sus puertos por defecto (top-1000).  
  El nodo `Parse Nmap XML` filtró solo los hosts `up` y extrajo los puertos detectados como `open`. OpenVAS recibió como argumento la lista de IPs y sus puertos abiertos (`hostsArg` y `portsArg`).
* **En la tesis / diseño experimental (§3.5.2 y Tabla 5.2.3):**  
  Cada corrida experimental se enfocó en evaluar la efectividad sobre un grupo de servicio específico:
  - Corrida 1: FTP (hosts .200 y .202) — 6 hallazgos
  - Corrida 2: SSH (hosts .200, .201, .202) — 9 hallazgos
  - Corrida 3: HTTP (hosts .201 y .202) — 8 hallazgos
  - Corrida 4: ICMP/TCP Timestamps (.200, .201, .202) — 5 hallazgos
  - Corrida 5: Evaluación multiprotocolo (.202) — ítem 29 retirado (solo tiempo). Total = 28 vulnerabilidades.
* **Versión actual de producción:**  
  El comando actual usa autodescubrimiento o variable de entorno `$SCAN_TARGET`:
  ```bash
  nmap -sV -T4 -n --open --top-ports 1000 --host-timeout 5m -oX - $TARGET
  ```

---

## 2. Conjunto de las 28 vulnerabilidades de referencia
* **¿Cómo se construyó?**  
  Se armó **leyendo los Dockerfiles y archivos de configuración**, NO a partir de un escaneo de OpenVAS.
* **Justificación técnica:**  
  Para que sea un experimento científico válido con métrica de efectividad (Ground Truth), las debilidades debían conocerse de antemano de forma determinista:
  1. `srv1` (Debian Buster): vsftpd con login anónimo y sin TLS (`ssl_enable=NO`), SSH con ciphers CBC obsoletos y MACs débiles.
  2. `srv2` (Apache 2.4.49): CVE-2021-41773 (Path Traversal en `<Directory "/">`), `TraceEnable On`, `ServerTokens Full`, SSH débil.
  3. `srv3` (Ubuntu 20.04): vsftpd anónimo, Apache con `Options Indexes` (Directory Listing), SSH débil.
* **Diferencia entre 29 y 28:**  
  La tabla original tenía 29 filas. El ítem 29 ("Evaluación multiprotocolo concurrente") se retiró del cálculo estadístico porque era una combinación de servicios y no una vulnerabilidad individual, quedando exactamente **28 vulnerabilidades evaluadas**.

---

## 3. Versión del workflow de septiembre
* **Tag en Git:** `experimento-2026-09` (commit `945a79e` / `9179ca5`).
* **versionId de n8n:** `6c2dd8e7-2cf4-452c-91cd-97834774432b` (visible en `Anexo_II_Workflow/workflow_tastserv.json`).
* **Fecha `updatedAt`:** `2026-09-17T19:38:00.455Z`.
* **¿Qué cambió desde septiembre hasta hoy?**
  1. Se agregó autodescubrimiento dinámico por CIDR en el nodo Nmap (con soporte de override vía `$SCAN_TARGET` en `/home/tizi/scan.env`).
  2. Se agregó nodo Webhook y disparador manual para permitir integraciones externas.
  3. Se corrigió el parser XML de host/asset en OpenVAS.
  4. Se corrigió el DDL de PostgreSQL para persistir todas las columnas sin truncamiento.

---

## 4. Rango de Nmap y puertos: septiembre vs. hoy
* **Septiembre (corridas de tesis):**
  - Targets: `172.18.0.200 172.18.0.201 172.18.0.202`
  - Banderas: `-sV -sC` (top 1000 puertos por defecto de Nmap).
* **Hoy por defecto:**
  - Si no hay `scan.env`: detecta la interfaz por defecto y escanea la subred `/24` (por eso en pruebas caseras detectaba `192.168.100.x`).
  - Para pruebas de laboratorio: se configuró `/home/tizi/scan.env` con `SCAN_TARGET="172.18.0.200 172.18.0.201 172.18.0.202"`.
  - Banderas: `-sV -T4 -n --open --top-ports 1000 --host-timeout 5m`.

---

## 5. Scripts reales y vsftpd
* **Nombres reales:**
  1. `automated_scan.sh`: Es el wrapper Bash llamado por SSH desde n8n. Valida parámetros, genera un archivo temporal de configuración seguro (`chmod 600`) y ejecuta el contenedor `gvm-tools`.
  2. `automated_scan.gmp.py`: Es el script en Python que ejecuta el protocolo GMP contra `/run/gvmd/gvmd.sock`. Crea target, crea task, hace polling cada 15s y devuelve el reporte XML.
  - **Ubicación:** `/home/tizi/gvm-scripts/` y respaldados en `entrega_13-10/PUNTO_5_SCRIPTS_GVM/`.
* **vsftpd.conf:**
  - Ubicación: `vulnsrv/srv1/vsftpd.conf` y `vulnsrv/srv3/vsftpd.conf`.
* **¿Cómo se instaló vsftpd 3.0.5?**
  - **Dato clave para la defensa:** En Debian Buster y Ubuntu 20.04, el paquete de repositorio oficial instala **vsftpd 3.0.3**.
  - En `vulnsrv/srv3/vsftpd.conf`, se configuró explícitamente la directiva `ftpd_banner=vsftpd 3.0.5`. Por eso OpenVAS reporta el banner 3.0.5 (ítem 20 de la tabla de la tesis), tal como se aclara en la página de la tesis (§3.5.2, ítem 20).

---

## 6. Columnas reales de PostgreSQL y expresión `${v.host}:${v.port}`
* **Columnas reales en `security_scans.public.vulnerability_scans`:**
  - `id`: integer (PK, autoincrement)
  - `scan_date`: timestamp with time zone
  - `host`: text
  - `vulnerability_name`: text
  - `severity`: numeric(3,1)
  - `port`: text
  - `cve`: text
  - `description`: text
  - `solution`: text
  - `scan_source`: character varying(50) (default 'automated')
  - `scan_id`: text
  - `created_at`: timestamp with time zone (default now())
* **Expresión `${v.host}:${v.port}` en el Anexo IV:**
  - En el archivo JSON original del repositorio (`Anexo_II_Workflow/workflow_tastserv.json`) la sintaxis está en **ASCII puro** con template literals de JavaScript:
    ```javascript
    `\n**Host**: ${v.host}:${v.port}\n**Severidad**: ${v.severity}/10.0`
    ```
  - La conversión a símbolos matemáticos ocurrió al exportar o pegar el texto en Microsoft Word/LibreOffice, que interpretó las llaves y signos como notación de fórmulas KaTeX/LaTeX. El archivo original está disponible limpio en `entrega_13-10/PUNTO_2_WORKFLOW_EXPORTADO/workflow_tastserv.json`.

---

## 7. Congelamiento con Git Tag y exportación
* **Tag creado:** `pre-defensa-20261105`.
* **Workflow exportado:** guardado en `entrega_13-10/PUNTO_2_WORKFLOW_EXPORTADO/workflow_predefensa_20261105.json`.

---

## 8. Pruebas nuevas y debilidades deliberadas no incluidas
* **Fecha y versión:** Ejecución actual (05/11/2026) sobre los 3 contenedores `vuln-srv1/2/3` (`172.18.0.200/201/202`).
* **¿Aparecen en el reporte root por SSH, ServerSignature o /secretos?**
  - **No aparecen en el informe:** En la tesis (§3.5.2, pág. 586) se aclara explícitamente:
    > *"Debilidades deliberadas no incluidas: Los Dockerfiles del Anexo III introducen además configuraciones inseguras que no forman parte del conjunto de referencia evaluado: el acceso root por SSH con autenticación por contraseña y credenciales débiles (en los tres hosts), ServerSignature habilitado y el directorio /secretos en vuln-srv3..."*
  - Motivo: OpenVAS no realiza fuerza bruta de credenciales SSH ni auditoría de archivos locales sin credenciales de escaneo autenticado.
  - Para consistencia, hoy se creó el directorio `/secretos` con `config.txt` tanto en `vuln-srv2` como en `vuln-srv3`.

---

## 9. Saneamiento del repositorio y credenciales
* **Contraseña de Postgres:** Rotada hoy a clave criptográfica de 24 caracteres (`cPU3MX00cQED7Vc4rlo6Df9B`).
* **Historial Git:** Se ejecutó `git-filter-repo` reemplazando todas las apariciones de `hola123` y `Ajedrez2011` en todos los commits pasados por `REDACTADO`.
* **Typo docker-compose:** La clave del archivo es `environment:` (sintaxis correcta).
* **GMP admin y Mailtrap:** Documentados en el Anexo de auditoría como sandbox de laboratorio pendientes de rotar en pase a producción corporativo.

![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)


Informe mail 

# Informe de Escaneo de Vulnerabilidades

**ID de Escaneo**: scan_20261105_223632
**Fecha del Escaneo**: 5/11/2026, 22:36:56
**Hosts Escaneados**: 3 (172.18.0.200, 172.18.0.201, 172.18.0.202)
**Total de Vulnerabilidades**: 146

---

## Resumen Ejecutivo

| Severidad | Cantidad | Porcentaje |
|-----------|----------|------------|
| Critica (9.0-10.0) | 0 | 0.0% |
| Alta (7.0-8.9) | 23 | 15.8% |
| Media (4.0-6.9) | 49 | 33.6% |
| Baja e Informativa (0.0-3.9) | 74 | 50.7% |

---

## Vulnerabilidades Criticas
*No se encontraron vulnerabilidades criticas.*


## Vulnerabilidades Altas

### 1. Apache HTTP Server 2.4.17 < 2.4.49 'mod_proxy' HTTP/2 Request Smuggling Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 7.5/10.0
**CVE**: CVE-2021-33193

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.49
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.49 or later.

---


### 2. Apache HTTP Server 2.4.30 - 2.4.55 HTTP Request Smuggling Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 7.5/10.0
**CVE**: CVE-2023-27522

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.56
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.56 or later.

---


### 3. Apache HTTP Server 2.4.30 - 2.4.55 HTTP Request Smuggling Vulnerability - Linux

**Host**: 172.18.0.201:80/tcp
**Severidad**: 7.5/10.0
**CVE**: CVE-2023-27522

**Descripcion**:
Installed version: 2.4.49
Fixed version:     2.4.56
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.56 or later.

---


### 4. Apache HTTP Server 2.4.30 < 2.4.49 DoS Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 7.5/10.0
**CVE**: CVE-2021-36160

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.49
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.49 or later.

---


### 5. Apache HTTP Server 2.4.41 - 2.4.46 NULL Pointer Dereference Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 7.5/10.0
**CVE**: CVE-2020-13950

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.48
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.48 or later.

---


### 6. Apache HTTP Server 2.4.7 - 2.4.51 Multiple Vulnerabilities - Linux

**Host**: 172.18.0.201:80/tcp
**Severidad**: 8.2/10.0
**CVE**: CVE-2021-44224

**Descripcion**:
Installed version: 2.4.49
Fixed version:     2.4.52
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.52 or later.

---


### 7. Apache HTTP Server 2.4.7 - 2.4.51 Multiple Vulnerabilities - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 8.2/10.0
**CVE**: CVE-2021-44224

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.52
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.52 or later.

---


### 8. Apache HTTP Server < 2.4.58 'mod_macro' Out-of-bounds Read Vulnerability - Linux

**Host**: 172.18.0.201:80/tcp
**Severidad**: 7.5/10.0
**CVE**: CVE-2023-31122

**Descripcion**:
Installed version: 2.4.49
Fixed version:     2.4.58
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.58 or later.

---


### 9. Apache HTTP Server < 2.4.58 'mod_macro' Out-of-bounds Read Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 7.5/10.0
**CVE**: CVE-2023-31122

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.58
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.58 or later.

---


### 10. Apache HTTP Server < 2.4.59 Multiple Vulnerabilities - Linux

**Host**: 172.18.0.201:80/tcp
**Severidad**: 7.5/10.0
**CVE**: CVE-2023-38709, CVE-2024-24795, CVE-2024-27316

**Descripcion**:
Installed version: 2.4.49
Fixed version:     2.4.59
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.59 or later.

---
*...y 13 vulnerabilidades altas adicionales.*


## Vulnerabilidades Medias

### 1. Anonymous FTP Login Reporting

**Host**: 172.18.0.200:21/tcp
**Severidad**: 6.4/10.0
**CVE**: CVE-1999-0497

**Descripcion**:
It was possible to login to the remote FTP service with the following anonymous account(s):

anonymous:anonymous@example.com
ftp:anonymous@example.com

**Solucion Recomendada**:
If you do not want to share files, you should disable anonymous
  logins.

---


### 2. Anonymous FTP Login Reporting

**Host**: 172.18.0.202:21/tcp
**Severidad**: 6.4/10.0
**CVE**: CVE-1999-0497

**Descripcion**:
It was possible to login to the remote FTP service with the following anonymous account(s):

anonymous:anonymous@example.com
ftp:anonymous@example.com

**Solucion Recomendada**:
If you do not want to share files, you should disable anonymous
  logins.

---


### 3. Apache HTTP Server 2.4.0 < 2.4.42 Multiple Vulnerabilities - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 6.1/10.0
**CVE**: CVE-2020-1927, CVE-2020-1934

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.42
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.42 or later.

---


### 4. Apache HTTP Server 2.4.17 - 2.4.57 DoS Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 5.9/10.0
**CVE**: CVE-2023-45802

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.58
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.58 or later.

---


### 5. Apache HTTP Server 2.4.17 - 2.4.57 DoS Vulnerability - Linux

**Host**: 172.18.0.201:80/tcp
**Severidad**: 5.9/10.0
**CVE**: CVE-2023-45802

**Descripcion**:
Installed version: 2.4.49
Fixed version:     2.4.58
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.58 or later.

---


### 6. Apache HTTP Server 2.4.17 < 2.4.64 DoS Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 5/10.0
**CVE**: CVE-2025-53020

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.64
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.64 or later.

---


### 7. Apache HTTP Server 2.4.17 < 2.4.64 DoS Vulnerability - Linux

**Host**: 172.18.0.201:80/tcp
**Severidad**: 5/10.0
**CVE**: CVE-2025-53020

**Descripcion**:
Installed version: 2.4.49
Fixed version:     2.4.64
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.64 or later.

---


### 8. Apache HTTP Server 2.4.26 < 2.4.64 DoS Vulnerability - Linux

**Host**: 172.18.0.201:80/tcp
**Severidad**: 5/10.0
**CVE**: CVE-2025-49630

**Descripcion**:
Installed version: 2.4.49
Fixed version:     2.4.64
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.64 or later.

---


### 9. Apache HTTP Server 2.4.26 < 2.4.64 DoS Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 5/10.0
**CVE**: CVE-2025-49630

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.64
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.64 or later.

---


### 10. Apache HTTP Server 2.4.35 < 2.4.64 Access Control Bypass Vulnerability - Linux

**Host**: 172.18.0.201:80/tcp
**Severidad**: 5/10.0
**CVE**: CVE-2025-23048

**Descripcion**:
Installed version: 2.4.49
Fixed version:     2.4.64
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.64 or later.

---


### 11. Apache HTTP Server 2.4.35 < 2.4.64 Access Control Bypass Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 5/10.0
**CVE**: CVE-2025-23048

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.64
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.64 or later.

---


### 12. Apache HTTP Server 2.4.39 - 2.4.46 Unexpected URL Matching Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 5.3/10.0
**CVE**: CVE-2021-30641

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.48
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.48 or later.

---


### 13. Apache HTTP Server 2.4.6 - 2.4.46 Tunneling Misconfiguration Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 5.3/10.0
**CVE**: CVE-2019-17567

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.48
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.48 or later.

---


### 14. Apache HTTP Server 2.4.7 - 2.4.65 Authentication Bypass Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 5.8/10.0
**CVE**: CVE-2025-66200

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.66
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.66 or later.

---


### 15. Apache HTTP Server 2.4.7 - 2.4.65 Authentication Bypass Vulnerability - Linux

**Host**: 172.18.0.201:80/tcp
**Severidad**: 5.8/10.0
**CVE**: CVE-2025-66200

**Descripcion**:
Installed version: 2.4.49
Fixed version:     2.4.66
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.66 or later.

---
*...y 34 vulnerabilidades medias adicionales.*


## Vulnerabilidades Bajas e Informativas

### 1. Allowed HTTP Methods Enumeration

**Host**: 172.18.0.202:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
The following list contains the URLs and corresponding supported HTTP methods.

URL                                                   | HTTP Methods
----------------------------------------------------------------------------------------------------------------
http://vuln-srv3.greenbone-community-e...

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 2. Allowed HTTP Methods Enumeration

**Host**: 172.18.0.201:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
The following list contains the URLs and corresponding supported HTTP methods.

URL                                                   | HTTP Methods
----------------------------------------------------------------------------------------------------------------------
http://vuln-srv2.greenbone-commu...

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 3. Apache HTTP Server 2.4.30 - 2.4.65 Integer Overflow Vulnerability - Linux

**Host**: 172.18.0.201:80/tcp
**Severidad**: 2.6/10.0
**CVE**: CVE-2025-55753

**Descripcion**:
Installed version: 2.4.49
Fixed version:     2.4.66
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.66 or later.

---


### 4. Apache HTTP Server 2.4.30 - 2.4.65 Integer Overflow Vulnerability - Linux

**Host**: 172.18.0.202:80/tcp
**Severidad**: 2.6/10.0
**CVE**: CVE-2025-55753

**Descripcion**:
Installed version: 2.4.41
Fixed version:     2.4.66
Installation
path / port:       80/tcp

**Solucion Recomendada**:
Update to version 2.4.66 or later.

---


### 5. Apache HTTP Server Detection Consolidation

**Host**: 172.18.0.201
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Detected Apache HTTP Server

Version:       2.4.49
Location:      80/tcp
CPE:           cpe:/a:apache:http_server:2.4.49

Concluded from version/product identification result:
Server: Apache/2.4.49 (Unix)

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 6. Apache HTTP Server Detection Consolidation

**Host**: 172.18.0.202
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Detected Apache HTTP Server

Version:       2.4.41
Location:      80/tcp
CPE:           cpe:/a:apache:http_server:2.4.41

Concluded from version/product identification result:
Server: Apache/2.4.41 (Ubuntu)

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 7. CPE Inventory

**Host**: 172.18.0.201
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
172.18.0.201|cpe:/a:apache:http_server:2.4.49
172.18.0.201|cpe:/a:ietf:secure_shell_protocol:2.0
172.18.0.201|cpe:/a:openbsd:openssh:7.9p1
172.18.0.201|cpe:/o:debian:debian_linux:10

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 8. CPE Inventory

**Host**: 172.18.0.202
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
172.18.0.202|cpe:/a:apache:http_server:2.4.41
172.18.0.202|cpe:/a:ietf:secure_shell_protocol:2.0
172.18.0.202|cpe:/a:openbsd:openssh:8.2p1
172.18.0.202|cpe:/a:vsftpd_project:vsftpd:3.0.5
172.18.0.202|cpe:/o:canonical:ubuntu_linux:20.04

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 9. CPE Inventory

**Host**: 172.18.0.200
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
172.18.0.200|cpe:/a:ietf:secure_shell_protocol:2.0
172.18.0.200|cpe:/a:openbsd:openssh:7.9p1
172.18.0.200|cpe:/a:vsftpd_project:vsftpd:3.0.3
172.18.0.200|cpe:/o:debian:debian_linux:10

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 10. FTP Banner Detection

**Host**: 172.18.0.200:21/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Remote FTP server banner:

220 vsftpd 3.0.3

This is probably (a):

- vsftpd

Server operating system information collected via "SYST" command:

215 UNIX Type: L8

Server status information collected via "STAT" command:

211-FTP server status:
     Connected to 172.18.0.5
     Logged in as ftp
     ...

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 11. FTP Banner Detection

**Host**: 172.18.0.202:21/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Remote FTP server banner:

220 vsftpd 3.0.5

This is probably (a):

- vsftpd

Server operating system information collected via "SYST" command:

215 UNIX Type: L8

Server status information collected via "STAT" command:

211-FTP server status:
     Connected to 172.18.0.5
     Logged in as ftp
     ...

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 12. Hostname Determination Reporting

**Host**: 172.18.0.200
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Hostname determination for IP 172.18.0.200:

Hostname|Source
vuln-srv1.greenbone-community-edition_default|Reverse-DNS

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 13. Hostname Determination Reporting

**Host**: 172.18.0.202
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Hostname determination for IP 172.18.0.202:

Hostname|Source
vuln-srv3.greenbone-community-edition_default|Reverse-DNS

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 14. Hostname Determination Reporting

**Host**: 172.18.0.201
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Hostname determination for IP 172.18.0.201:

Hostname|Source
vuln-srv2.greenbone-community-edition_default|Reverse-DNS

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 15. HTTP Security Headers Detection

**Host**: 172.18.0.202:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Missing Headers                   | More Information
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Content-Security-Policy           | http...

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 16. HTTP Security Headers Detection

**Host**: 172.18.0.201:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Missing Headers                   | More Information
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Content-Security-Policy           | http...

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 17. HTTP Server Banner Enumeration

**Host**: 172.18.0.202:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
It was possible to enumerate the following HTTP server banner(s):

Server banner                  | Enumeration technique
-------------------------------------------------------------------------------------------------
Server: Apache/2.4.41 (Ubuntu) | Invalid HTTP 00.5 GET request (non-existent HTT...

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 18. HTTP Server Banner Enumeration

**Host**: 172.18.0.201:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
It was possible to enumerate the following HTTP server banner(s):

Server banner                | Enumeration technique
-----------------------------------------------------------------------------------------------
Server: Apache/2.4.49 (Unix) | Invalid HTTP 00.5 GET request (non-existent HTTP vers...

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 19. HTTP Server type and version

**Host**: 172.18.0.201:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
The remote HTTP Server banner is:

Server: Apache/2.4.49 (Unix)

**Solucion Recomendada**:
*Sin solucion especificada.*

---


### 20. HTTP Server type and version

**Host**: 172.18.0.202:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
The remote HTTP Server banner is:

Server: Apache/2.4.41 (Ubuntu)

**Solucion Recomendada**:
*Sin solucion especificada.*

---
*...y 54 vulnerabilidades bajas e informativas adicionales.*


---

## Resumen por Host

### 172.18.0.200
- Total: 35 | Criticas: 0 | Altas: 4 | Medias: 10 | Bajas/Info: 21

### 172.18.0.201
- Total: 49 | Criticas: 0 | Altas: 8 | Medias: 17 | Bajas/Info: 24

### 172.18.0.202
- Total: 62 | Criticas: 0 | Altas: 11 | Medias: 22 | Bajas/Info: 29

---

## Recomendaciones Generales

1. Priorizar la remediacion de vulnerabilidades criticas y altas de forma inmediata.
2. Aplicar parches y actualizaciones de seguridad para todos los servicios con hallazgos medios o superiores.
3. Revisar banners expuestos, metodos HTTP innecesarios y configuraciones debiles para reducir la superficie de ataque.
4. Implementar politicas de actualizacion regular de software y firmware.
5. Realizar escaneos de seguimiento tras aplicar correcciones para verificar la remediacion.

---

*Informe generado automaticamente por el sistema de escaneo de vulnerabilidades TASTSERV*


---
This email was sent automatically with n8n
https://n8n.io