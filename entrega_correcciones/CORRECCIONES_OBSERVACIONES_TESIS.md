# CORRECCIONES A OBSERVACIONES DE LA TESIS — TASTSERV

> Documento preparado con texto listo para insertar/reemplazar en la tesis.
> Cada sección corresponde a una observación identificada por Luca.

---

## N3 — Anexos faltantes (§3.5.3 promete Anexos I y II, §5.1 cita registro de observaciones, §3.7 cita repositorio sin URL)

### Problema

- §3.5.3 promete Anexos I y II pero no existen en el documento.
- No hay docker-compose, JSON del workflow, DDL ni capturas.
- §3.7 menciona un repositorio público sin URL.
- La implementación es creíble pero no verificable por el tribunal.

### Solución

#### 3a. Agregar la URL del repositorio en §3.7

**Buscar en §3.7 (línea ~633):**
```
se encuentra disponible en un repositorio público con fines de documentación académica
```

**Reemplazar por:**
```
se encuentra disponible en un repositorio público
(https://github.com/TizianoRoig26/Final.git) con fines de documentación
académica y de reproducibilidad del experimento
```

---

#### 3b. Crear Anexo I — Infraestructura como Código (docker-compose)

> Insertar al final del documento, antes de las referencias o después de ellas, según el formato que use la tesis.

##### A.I.1. Manifiesto de orquestación principal (Greenbone Community Edition)

El despliegue de la suite Greenbone Community Edition se realiza mediante el
siguiente manifiesto Docker Compose, que declara el conjunto completo de
microservicios necesarios para el funcionamiento del motor de análisis de
vulnerabilidades:

```yaml
# Archivo: docker-compose-openvas.yml
name: greenbone-community-edition

services:
  vulnerability-tests:
    image: registry.community.greenbone.net/community/vulnerability-tests
    environment:
      FEED_RELEASE: "24.10"
      KEEP_ALIVE: 1
    volumes:
      - vt_data_vol:/mnt

  notus-data:
    image: registry.community.greenbone.net/community/notus-data
    environment:
      KEEP_ALIVE: 1
    volumes:
      - notus_data_vol:/mnt

  scap-data:
    image: registry.community.greenbone.net/community/scap-data
    environment:
      KEEP_ALIVE: 1
    volumes:
      - scap_data_vol:/mnt

  cert-bund-data:
    image: registry.community.greenbone.net/community/cert-bund-data
    environment:
      KEEP_ALIVE: 1
    volumes:
      - cert_data_vol:/mnt

  dfn-cert-data:
    image: registry.community.greenbone.net/community/dfn-cert-data
    environment:
      KEEP_ALIVE: 1
    volumes:
      - cert_data_vol:/mnt
    depends_on:
      cert-bund-data:
        condition: service_healthy

  data-objects:
    image: registry.community.greenbone.net/community/data-objects
    environment:
      FEED_RELEASE: "24.10"
      KEEP_ALIVE: 1
    volumes:
      - data_objects_vol:/mnt

  report-formats:
    image: registry.community.greenbone.net/community/report-formats
    environment:
      FEED_RELEASE: "24.10"
      KEEP_ALIVE: 1
    volumes:
      - data_objects_vol:/mnt
    depends_on:
      data-objects:
        condition: service_healthy

  gpg-data:
    image: registry.community.greenbone.net/community/gpg-data
    volumes:
      - gpg_data_vol:/mnt

  redis-server:
    image: registry.community.greenbone.net/community/redis-server
    restart: on-failure
    volumes:
      - redis_socket_vol:/run/redis/

  pg-gvm:
    image: registry.community.greenbone.net/community/pg-gvm:stable
    restart: on-failure:10
    volumes:
      - psql_data_vol:/var/lib/postgresql
      - psql_socket_vol:/var/run/postgresql
    depends_on:
      pg-gvm-migrator:
        condition: service_completed_successfully

  pg-gvm-migrator:
    image: registry.community.greenbone.net/community/pg-gvm-migrator:stable
    restart: no
    volumes:
      - psql_data_vol:/var/lib/postgresql
      - psql_socket_vol:/var/run/postgresql

  gvmd:
    image: registry.community.greenbone.net/community/gvmd:stable
    restart: on-failure
    volumes:
      - gvmd_data_vol:/var/lib/gvm
      - scap_data_vol:/var/lib/gvm/scap-data/
      - cert_data_vol:/var/lib/gvm/cert-data
      - data_objects_vol:/var/lib/gvm/data-objects/gvmd
      - vt_data_vol:/var/lib/openvas/plugins
      - psql_data_vol:/var/lib/postgresql
      - gvmd_socket_vol:/run/gvmd
      - ospd_openvas_socket_vol:/run/ospd
      - psql_socket_vol:/var/run/postgresql

  gsa:
    image: registry.community.greenbone.net/community/gsa:stable-slim
    environment:
      MOUNT_PATH: "/mnt/web"
      KEEP_ALIVE: 1
    volumes:
      - gsa_data_vol:/mnt/web

  gsad:
    image: registry.community.greenbone.net/community/gsad:stable
    restart: on-failure
    environment:
      GSAD_ARGS: "--listen=0.0.0.0 --http-only --api-only -f"
    volumes:
      - gvmd_socket_vol:/run/gvmd

  nginx:
    image: registry.community.greenbone.net/community/nginx:latest
    ports:
      - 127.0.0.1:443:443
      - 127.0.0.1:9392:9392
    volumes:
      - nginx_config_vol:/etc/nginx/conf.d:ro
      - nginx_certificates_vol:/etc/nginx/certs:ro
      - gsa_data_vol:/usr/share/nginx/html:ro

  openvasd:
    image: registry.community.greenbone.net/community/openvas-scanner:stable
    restart: on-failure
    environment:
      OPENVASD_MODE: service_notus
      GNUPGHOME: /etc/openvas/gnupg
      LISTENING: 0.0.0.0:80
    volumes:
      - openvas_data_vol:/etc/openvas
      - openvas_log_data_vol:/var/log/openvas
      - gpg_data_vol:/etc/openvas/gnupg
      - notus_data_vol:/var/lib/notus

  ospd-openvas:
    image: registry.community.greenbone.net/community/ospd-openvas:stable
    restart: on-failure
    hostname: ospd-openvas.local
    cap_add:
      - NET_ADMIN
      - NET_RAW
    security_opt:
      - seccomp=unconfined
      - apparmor=unconfined
    volumes:
      - gpg_data_vol:/etc/openvas/gnupg
      - vt_data_vol:/var/lib/openvas/plugins
      - notus_data_vol:/var/lib/notus
      - ospd_openvas_socket_vol:/run/ospd
      - redis_socket_vol:/run/redis/
      - openvas_data_vol:/etc/openvas/
      - openvas_log_data_vol:/var/log/openvas

  gvm-tools:
    image: registry.community.greenbone.net/community/gvm-tools
    volumes:
      - gvmd_socket_vol:/run/gvmd
      - ospd_openvas_socket_vol:/run/ospd

volumes:
  gpg_data_vol:
  scap_data_vol:
  cert_data_vol:
  data_objects_vol:
  gvmd_data_vol:
  psql_data_vol:
  vt_data_vol:
  notus_data_vol:
  psql_socket_vol:
  gvmd_socket_vol:
  ospd_openvas_socket_vol:
  redis_socket_vol:
  openvas_data_vol:
  openvas_log_data_vol:
  gsa_data_vol:
  nginx_config_vol:
  nginx_certificates_vol:
```

##### A.I.2. Manifiesto de activos objetivo (servidores vulnerables)

Los tres servidores de referencia se despliegan como contenedores Docker
con direcciones IP estáticas dentro de la red interna creada por el stack
principal de Greenbone, garantizando un segmento de red aislado y
reproducible:

```yaml
# Archivo: docker-compose-vulnsrv.yml
services:
  vuln-srv1:
    image: vuln-srv1
    container_name: vuln-srv1
    restart: unless-stopped
    networks:
      greenbone_net:
        ipv4_address: 172.18.0.200

  vuln-srv2:
    image: vuln-srv2
    container_name: vuln-srv2
    restart: unless-stopped
    networks:
      greenbone_net:
        ipv4_address: 172.18.0.201

  vuln-srv3:
    image: vuln-srv3
    container_name: vuln-srv3
    restart: unless-stopped
    networks:
      greenbone_net:
        ipv4_address: 172.18.0.202

networks:
  greenbone_net:
    external: true
    name: greenbone-community-edition_default
```

##### A.I.3. Manifiesto del orquestador n8n

```yaml
# Archivo: docker-compose.yml
version: "3"

services:
  n8n:
    image: n8nio/n8n
    container_name: n8n
    ports:
      - "5678:5678"
    volumes:
      - ~/.n8n:/home/node/.n8n
    restart: always
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=<REDACTADO>
```

##### A.I.4. Imágenes de los servidores vulnerables (Dockerfiles)

**vuln-srv1** — vsftpd + OpenSSH (Debian Buster):

```dockerfile
FROM debian:buster-slim

RUN sed -i 's/deb.debian.org/archive.debian.org/g; \
    s/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        vsftpd openssh-server iputils-ping net-tools procps && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash labuser && echo "labuser:lab1234" | chpasswd && \
    echo "root:toor1234" | chpasswd

COPY vsftpd.conf /etc/vsftpd.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# SSH deliberadamente vulnerable: algoritmos CBC obsoletos, MACs débiles
RUN echo "Ciphers 3des-cbc,aes128-cbc,aes192-cbc,aes256-cbc" >> /etc/ssh/sshd_config && \
    echo "MACs hmac-md5,hmac-sha1,umac-64@openssh.com" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

EXPOSE 21 22
ENTRYPOINT ["/entrypoint.sh"]
```

**vuln-srv2** — Apache 2.4.49 (CVE-2021-41773) + OpenSSH:

```dockerfile
FROM httpd:2.4.49

RUN sed -i 's/deb.debian.org/archive.debian.org/g; \
    s/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        openssh-server iputils-ping net-tools procps && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash labuser && echo "labuser:lab1234" | chpasswd && \
    echo "root:toor1234" | chpasswd

# SSH con ciphers débiles
RUN echo "Ciphers 3des-cbc,aes128-cbc,aes192-cbc,aes256-cbc" >> /etc/ssh/sshd_config && \
    echo "MACs hmac-md5,hmac-sha1,umac-64@openssh.com" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

# Habilitar Path Traversal CVE-2021-41773
RUN echo '<Directory "/">\n    AllowOverride none\n    Require all granted\n</Directory>' \
    >> /usr/local/apache2/conf/httpd.conf

# ServerTokens Full + TraceEnable
RUN echo "ServerTokens Full" >> /usr/local/apache2/conf/httpd.conf && \
    echo "ServerSignature On" >> /usr/local/apache2/conf/httpd.conf && \
    echo "TraceEnable On" >> /usr/local/apache2/conf/httpd.conf

EXPOSE 80 22
ENTRYPOINT ["/entrypoint.sh"]
```

**vuln-srv3** — Apache 2.4.41 + vsftpd + OpenSSH (Ubuntu 20.04):

```dockerfile
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apache2 vsftpd openssh-server iputils-ping net-tools procps && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash labuser && echo "labuser:lab1234" | chpasswd && \
    echo "root:toor1234" | chpasswd

COPY vsftpd.conf /etc/vsftpd.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# SSH deliberadamente débil
RUN echo "Ciphers 3des-cbc,aes128-cbc,aes192-cbc,aes256-cbc" >> /etc/ssh/sshd_config && \
    echo "MACs hmac-md5,hmac-sha1,umac-64@openssh.com" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

# Directory Listing + ServerTokens Full
RUN echo "ServerTokens Full" >> /etc/apache2/apache2.conf && \
    echo "ServerSignature On" >> /etc/apache2/apache2.conf

EXPOSE 21 22 80
ENTRYPOINT ["/entrypoint.sh"]
```

##### A.I.5. DDL de la tabla de persistencia (PostgreSQL)

```sql
CREATE TABLE IF NOT EXISTS vulnerability_scans (
    id              SERIAL PRIMARY KEY,
    scan_timestamp  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    host            VARCHAR(45)  NOT NULL,
    port            VARCHAR(20),
    vulnerability   TEXT         NOT NULL,
    severity        NUMERIC(3,1),
    description     TEXT,
    solution        TEXT,
    cve_id          VARCHAR(30),
    scan_source     VARCHAR(50)  DEFAULT 'automated'
);

CREATE INDEX idx_vuln_scans_host ON vulnerability_scans(host);
CREATE INDEX idx_vuln_scans_severity ON vulnerability_scans(severity DESC);
CREATE INDEX idx_vuln_scans_cve ON vulnerability_scans(cve_id);
```

> **NOTA:** El JSON exportado del workflow de n8n debe incluirse como **Anexo II** una vez que se exporte desde la interfaz de n8n (Settings → Export Workflow). Exportar y pegar aquí.

---

#### 3c. Corregir la referencia en §3.5.3 (línea ~581)

**Buscar:**
```
Las planillas completas de ambos instrumentos se incorporan como Anexo I
y Anexo II del presente trabajo.
```

**Reemplazar por:**
```
Las planillas completas de ambos instrumentos se incorporan como Anexo III
y Anexo IV del presente trabajo. Los manifiestos de infraestructura como
código (Docker Compose y Dockerfiles) que permiten la reproducción íntegra
del entorno experimental se documentan en el Anexo I, mientras que el flujo
de orquestación exportado de n8n se incluye en el Anexo II.
```

---

## N9 — Inconsistencia de red (Figura 2 vs. §5.2)

### Problema

La Figura 2 tiene un placeholder `[IP A COMPLETAR]` y no se explica la relación con los hosts 172.18.0.200–202 que aparecen en §5.2.

### Datos confirmados

- Los tres hosts objetivo (.200, .201, .202) **son contenedores Docker** con IPs estáticas asignadas dentro de la red bridge `greenbone-community-edition_default` (subred 172.18.0.0/16).
- El escaneo Nmap apunta al rango acotado `172.18.0.200-202` (solo los tres targets).
- NO son VMs; son contenedores que ejecutan servicios deliberadamente vulnerables.

### Solución

#### 9a. Completar el placeholder de la Figura 2

**Reemplazar `[IP A COMPLETAR]` por:**
```
172.18.0.200-202
```

#### 9b. Corregir §3.7 (línea ~629) — Cambiar "máquinas virtuales" por la descripción real

**Buscar:**
```
fueron ejecutadas exclusivamente sobre máquinas virtuales desplegadas
específicamente para los fines de este proyecto, dentro de una red
interna aislada del laboratorio
```

**Reemplazar por:**
```
fueron ejecutadas exclusivamente sobre contenedores Docker desplegados
específicamente para los fines de este proyecto, dentro de una red
bridge aislada del laboratorio
```

#### 9c. Agregar párrafo de aclaración en §5.2 (después de la línea ~714)

**Insertar después de la primera oración de §5.2:**

```
El entorno experimental se despliega íntegramente mediante contenedores
Docker orquestados con Docker Compose, lo que garantiza la
reproducibilidad declarativa del experimento (véase Anexo I). Los tres
hosts objetivo del experimento (172.18.0.200, 172.18.0.201 y
172.18.0.202) corresponden a contenedores con direcciones IP estáticas
asignadas dentro de la red bridge interna
greenbone-community-edition_default (subred 172.18.0.0/16), creada
automáticamente por el stack de Greenbone Community Edition.

Esta decisión de diseño —utilizar contenedores Docker en lugar de
máquinas virtuales— responde a tres criterios técnicos: (a) desde la
perspectiva de las herramientas de escaneo (Nmap y OpenVAS), un
contenedor con dirección IP estática dentro de una red bridge es
funcionalmente indistinguible de un host físico o una VM a nivel de
capa de red, ya que ambos presentan una interfaz de red con dirección IP
propia, responden a solicitudes ARP y exponen servicios en puertos TCP/UDP
de manera idéntica; (b) la infraestructura como código (IaC) mediante
Docker Compose permite que cualquier evaluador reproduzca el entorno
completo del experimento con un único comando (docker compose up), lo
cual no sería posible con la misma inmediatez utilizando máquinas
virtuales; y (c) el despliegue mediante contenedores reduce
significativamente los requisitos de recursos de hardware, permitiendo
ejecutar la totalidad del entorno —motor de análisis, activos objetivo y
orquestador— en un único host de laboratorio.

El rango de red indicado en la Figura 2 (172.18.0.200-202) corresponde
al escaneo Nmap de descubrimiento ejecutado sobre los tres activos de
referencia. Los servicios deliberadamente vulnerables instalados en cada
contenedor se detallan en la Tabla 5.X.
```

#### 9d. Agregar tabla de mapeo de servidores vulnerables

> Insertar como nueva tabla en §5.2 o en el Anexo I:

| Contenedor | IP            | Imagen base        | Servicios expuestos                                     | Vulnerabilidades deliberadas                                                         |
|------------|---------------|--------------------|--------------------------------------------------------|--------------------------------------------------------------------------------------|
| vuln-srv1  | 172.18.0.200  | debian:buster-slim | vsftpd (FTP, :21), OpenSSH (:22)                       | SSH con ciphers CBC obsoletos (3des-cbc, aes*-cbc), MACs débiles (hmac-md5), PermitRootLogin yes |
| vuln-srv2  | 172.18.0.201  | httpd:2.4.49       | Apache HTTPD 2.4.49 (:80), OpenSSH (:22)                | **CVE-2021-41773** (Path Traversal en Apache 2.4.49), ServerTokens Full, TraceEnable On, SSH débil |
| vuln-srv3  | 172.18.0.202  | ubuntu:20.04       | Apache 2.4.41 (:80), vsftpd (:21), OpenSSH (:22)       | Directory Listing habilitado, ServerTokens Full, SSH débil, vsftpd con configuración por defecto  |

---

## N10 — "Red sin conexión a internet" vs. notificación por SMTP

### Problema

§3.7 dice que el entorno "no posee conexión hacia... internet", pero §4.1 describe notificación vía SMTP. Se usa **Mailtrap** (servicio SaaS en mailtrap.io), lo cual **sí requiere conexión a internet**.

### Solución — Opción (b): Corrección honesta de §3.7

Dado que Mailtrap es un servicio cloud, la afirmación de §3.7 de "sin conexión a internet" no es estrictamente correcta. Se debe corregir §3.7 con una excepción explícita y honesta.

#### 10a. Corregir §3.7 (línea ~629)

**Buscar:**
```
Dicho entorno no posee conexión hacia redes de producción, redes
institucionales de uso general ni hacia internet, y fue configurado y
utilizado bajo el conocimiento y autorización de la cátedra y del
director del presente trabajo.
```

**Reemplazar por:**
```
Dicho entorno se mantiene aislado de redes de producción e
institucionales de uso general, y fue configurado y utilizado bajo el
conocimiento y autorización de la cátedra y del director del presente
trabajo. Como excepción puntual, el nodo de notificación por correo
electrónico (sección 4.1) requiere conectividad saliente hacia el
servicio de correo de prueba Mailtrap (mailtrap.io), utilizado como
receptor sandbox de los informes generados por el pipeline. Esta
conexión saliente no implica exposición de los activos del entorno
experimental ni tráfico entrante desde redes externas, y el servicio
Mailtrap fue seleccionado específicamente por su naturaleza de sandbox
(los correos son capturados y no reenviados a destinatarios reales),
lo cual preserva la intención de aislamiento del entorno de laboratorio.
```

#### 10b. Agregar nota aclaratoria en §4.1 (después de la mención del nodo SMTP, línea ~665)

**Insertar después de:**
```
El informe se envía automáticamente mediante un nodo SMTP.
```

**Agregar:**
```
El servidor SMTP utilizado para la entrega de los informes corresponde
al servicio de sandbox de correo Mailtrap (mailtrap.io), que captura
los mensajes en un entorno de pruebas sin reenviarlos a destinatarios
reales. Esta elección permite validar el ciclo completo del pipeline
—incluyendo la generación, el formato y el despacho del informe— sin
requerir infraestructura de correo institucional ni comprometer el
aislamiento de los activos del entorno experimental.
```

---

## N13 — Procedimiento manual no descripto paso a paso

### Problema

Los escaneos manuales (Tablas 5.1 y 5.3) están ejecutados, pero no se describe:
- Si se usó CLI o la interfaz GSA
- Con qué configuración de escaneo
- Cómo se elaboró el «informe final» manual

### Datos confirmados

- Los escaneos manuales se hicieron **desde la CLI con gvm-tools**.
- La configuración de escaneo usada fue **"Full and fast"** (es la que usa el script `automated_scan.gmp.py` y la misma que se usó manualmente para mantener paridad).
- El informe final manual: dado que se usó gvm-tools desde CLI, el reporte se obtuvo como salida XML del protocolo GMP y se procesó manualmente.

### Solución — Agregar descripción paso a paso del procedimiento manual

#### 13a. Insertar en el Capítulo V (antes o después de §5.1, o como nueva subsección §5.1.1)

**Texto a insertar:**

```
Procedimiento del escaneo en condición manual

El procedimiento manual ejecutado en cada una de las cinco repeticiones
de la condición de control se realizó íntegramente desde la línea de
comandos (CLI) mediante la herramienta gvm-tools, conectada al socket
Unix del servicio gvmd de Greenbone Community Edition. A continuación
se describe la secuencia de pasos ejecutada por el operador en cada
corrida:

1. Descubrimiento de activos con Nmap. El operador ejecutó
   manualmente el comando de descubrimiento sobre el rango de red del
   laboratorio:

   nmap -sV -sC 172.18.0.200-202 -oX resultado_nmap.xml

   Las banderas -sV (detección de versión de servicio) y -sC
   (scripts básicos de diagnóstico) son idénticas a las utilizadas por
   el nodo de descubrimiento del pipeline automatizado, garantizando la
   paridad entre condiciones.

2. Identificación de hosts activos. El operador revisó manualmente
   la salida XML de Nmap para identificar los hosts activos y los
   puertos y servicios detectados en cada uno. Las direcciones IP de
   los hosts activos se anotaron para su uso en el paso siguiente.

3. Creación del objetivo de escaneo en Greenbone. Mediante
   gvm-tools, el operador invocó el protocolo GMP para crear un
   target con la lista de hosts identificados:

   gvm-script --gmp-username admin --gmp-password <password> \
     socket --socketpath /run/gvmd/gvmd.sock \
     automated_scan.gmp.py "<hosts>" "<puertos>"

   Nota: En la condición manual, aunque se utilizó el mismo script
   automated_scan.gmp.py como herramienta de ejecución —dado que
   este encapsula las llamadas GMP necesarias (creación de target,
   creación de task, inicio de escaneo y polling)—, la diferencia
   operativa radica en que cada paso previo y posterior al escaneo
   (descubrimiento, parseo de resultados, persistencia, generación de
   informe) fue ejecutado manualmente por el operador, sin
   orquestación de n8n.

4. Configuración de escaneo. La configuración utilizada fue
   "Full and fast" (configuración estándar de Greenbone), con el
   scanner "OpenVAS Default". El alive test se configuró como
   "Consider Alive" para evitar falsos negativos en la detección
   de hosts dentro de la red Docker bridge. Estos parámetros son
   idénticos a los utilizados en la condición automatizada.

5. Espera de finalización y recuperación del reporte. El operador
   monitoreó el progreso del escaneo consultando periódicamente el
   estado de la tarea mediante GMP, y una vez finalizado, recuperó el
   reporte completo en formato XML.

6. Parseo manual de resultados. El operador extrajo manualmente
   del XML del reporte los campos relevantes de cada hallazgo: nombre
   de la vulnerabilidad, severidad CVSS, host y puerto afectado,
   descripción, solución recomendada e identificador CVE. Estos datos
   se registraron en la planilla de observación (véase Anexo III)
   para su tabulación posterior.

7. Registro de tiempos. Para cada etapa, el operador registró
   manualmente las marcas de tiempo de inicio y finalización en la
   planilla de registro de tiempos (véase sección 3.5.1), utilizando
   el reloj del sistema del host de laboratorio como referencia.

Este procedimiento se repitió cinco veces, intercalando las
ejecuciones manuales con las automatizadas en orden alternado,
conforme al diseño experimental descrito en la sección 3.6.1.
```

---

## Resumen de acciones pendientes

| # | Acción | Sección afectada | Estado |
|---|--------|-----------------|--------|
| 1 | Agregar URL del repositorio | §3.7 | ✅ Texto listo |
| 2 | Cambiar "máquinas virtuales" por "contenedores Docker" | §3.7 | ✅ Texto listo |
| 3 | Corregir afirmación de aislamiento de internet | §3.7 | ✅ Texto listo |
| 4 | Completar placeholder de Figura 2 | Figura 2 | ✅ Dato: `172.18.0.200-202` |
| 5 | Agregar párrafo de aclaración de red + justificación Docker | §5.2 | ✅ Texto listo |
| 6 | Agregar tabla de mapeo de servidores | §5.2 o Anexo I | ✅ Texto listo |
| 7 | Agregar aclaración sobre Mailtrap en §4.1 | §4.1 | ✅ Texto listo |
| 8 | Agregar procedimiento manual paso a paso | §5.1 / nueva subsección | ✅ Texto listo |
| 9 | Corregir referencia de Anexos I/II en §3.5.3 | §3.5.3 | ✅ Texto listo |
| 10 | Crear Anexo I con docker-compose + Dockerfiles + DDL | Final del documento | ✅ Texto listo |
| 11 | **Exportar JSON del workflow de n8n** | Anexo II | ⏳ Pendiente de exportar desde n8n |
| 12 | Crear Anexos III y IV (planillas de observación) | Final del documento | ⏳ Depende de las planillas reales |
