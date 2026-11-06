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
