# Diseño Metodológico y Arquitectura del Laboratorio Experimental — TASTSERV

Este documento detalla los fundamentos conceptuales, decisiones de ingeniería y el diseño metodológico adoptado para la construcción del entorno de evaluación experimental del proyecto **TASTSERV** (*Total Automated Security Testing Service*).

---

## 1. Fundamentos y Objetivos del Diseño

El objetivo central del laboratorio experimental es permitir la comparación cuantitativa y cualitativa entre el procedimiento tradicional de escaneo manual de vulnerabilidades y el pipeline de evaluación automatizado orquestado mediante **n8n** y **OpenVAS / Greenbone Community Edition**, midiendo:
1. **Eficiencia temporal**: Tiempo de ciclo total desde el descubrimiento de red hasta la emisión del reporte.
2. **Efectividad de detección**: Capacidad para identificar un conjunto de referencia predefinido (*Ground Truth*) de debilidades de seguridad.
3. **Consistencia operativa**: Eliminación de errores de parametrización humana y sesgos de transcripción.

---

## 2. Decisiones de Arquitectura: Contenedores vs. Máquinas Virtuales

La infraestructura experimental fue diseñada íntegramente sobre **contenedores Docker** comunicados a través de una red tipo bridge dedicada (`greenbone-community-edition_default`, subred `172.18.0.0/16`). Esta decisión respondió a tres criterios metodológicos fundamentales:

1. **Equivalencia Funcional en Capa de Red**:
   Desde la perspectiva de los motores de auditoría activa (Nmap y los scripts NVT de OpenVAS), un contenedor con pila de red propia y dirección IP estática en una red bridge es indistinguible de un host físico o una máquina virtual completa. Los paquetes TCP SYN, negociaciones de banner, handshakes SSH y peticiones HTTP se comportan idénticamente.
2. **Reproducibilidad Declarativa (Infraestructura como Código)**:
   El uso de Dockerfiles y manifiestos de Docker Compose permite versionar formalmente la configuración exacta de cada objetivo, garantizando que cualquier tribunal evaluador o investigador pueda reproducir el escenario con un único comando (`docker compose up -d --build`).
3. **Optimización de Recursos y Aislamiento**:
   Permite desplegar la suite completa de Greenbone (12 microservicios), la base de datos PostgreSQL, el orquestador n8n y los 3 servidores vulnerables en un único equipo de desarrollo, manteniendo aislamiento estricto entre el plano de escaneo y los objetivos auditados.

---

## 3. Topología de Red y Roles de los Servidores Vulnerables

El laboratorio modela un entorno corporativo heterogéneo representativo compuesto por tres activos con direcciones IPv4 estáticas:

```
                      [ Red Bridge: 172.18.0.0/16 ]
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │ (172.18.0.200)           │ (172.18.0.201)           │ (172.18.0.202)
         ▼                          ▼                          ▼
  ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
  │  vuln-srv1   │           │  vuln-srv2   │           │  vuln-srv3   │
  │ Debian Buster│           │ Apache 2.4.49│           │ Ubuntu 20.04 │
  │ Puertos:     │           │ Puertos:     │           │ Puertos:     │
  │ • 21/tcp FTP │           │ • 80/tcp HTTP│           │ • 21/tcp FTP │
  │ • 22/tcp SSH │           │ • 22/tcp SSH │           │ • 22/tcp SSH │
  │              │           │              │           │ • 80/tcp HTTP│
  └──────────────┘           └──────────────┘           └──────────────┘
```

### 3.1. Servidor 1 (`vuln-srv1` — 172.18.0.200): Servicios de Transferencia y Shell Legado
- **Imagen Base**: Debian Buster (`debian:buster-slim`).
- **Servicios Evaluados**:
  - `vsftpd 3.0.3` (21/tcp): Configurado con acceso anónimo permitido (`anonymous_enable=YES`) y transmisión en texto claro (`ssl_enable=NO`).
  - `OpenSSH 7.9p1` (22/tcp): Configurado deliberadamente con algoritmos de cifrado y MACs obsoletas (3DES-CBC, AES-CBC, HMAC-MD5, HMAC-SHA1).

### 3.2. Servidor 2 (`vuln-srv2` — 172.18.0.201): Servidor Web Crítico (Explotable)
- **Imagen Base**: `httpd:2.4.49` oficial de Apache.
- **Servicios Evaluados**:
  - `Apache HTTP Server 2.4.49` (80/tcp): Desplegado para evaluar la detección de **CVE-2021-41773** (Path Traversal y RCE). La directiva `<Directory />` en `httpd.conf` fue configurada a `Require all granted` para habilitar la explotación activa. Además, se habilitó el método de depuración HTTP TRACE (`TraceEnable On`).
  - `OpenSSH` (22/tcp): Cifrados débiles y autenticación por contraseña.
  - Auditoría local: Directorio `/secretos/config.txt`.

### 3.3. Servidor 3 (`vuln-srv3` — 172.18.0.202): Evaluación Multiprotocolo
- **Imagen Base**: Ubuntu 20.04 LTS (`ubuntu:20.04`).
- **Servicios Evaluados**:
  - `Apache HTTP Server 2.4.41` (80/tcp): Configuración con banners detallados (`ServerTokens Full`, `ServerSignature On`) e indexación de directorios activada.
  - `vsftpd` (21/tcp): Usuario de laboratorio `labuser` con login en texto plano.
  - `OpenSSH 8.2p1` (22/tcp): Algoritmos CBC heredados.
  - Auditoría local: Directorio `/secretos/config.txt`.

---

## 4. Definición del Ground Truth (Conjunto de Referencia de 28 Vulnerabilidades)

Para medir la efectividad sin incurrir en sesgos post-hoc, se definió a priori un conjunto cerrado de **28 vulnerabilidades de referencia**, clasificadas formalmente por su naturaleza de origen:

1. **Tipo A — Debilidades de Configuración y Software (12 ítems)**:
   Fallas introducidas deliberadamente en los archivos de configuración (`vsftpd.conf`, `sshd_config`, `httpd.conf`) o asociadas a versiones con CVEs documentados (p. ej., CVE-1999-0497 en FTP, CVE-2021-41773 en Apache, o CVE-2003-1567 por método TRACE).
2. **Tipo B — Registros Informativos y Banners (11 ítems)**:
   Entradas que el motor clasifica con severidad 0.0 (Log) pero cuya recolección resulta crítica para el reconocimiento de servicios (banners de vsftpd, versiones de Apache, cabeceras de seguridad faltantes).
3. **Tipo C — Comportamiento de Pila TCP/IP del Kernel Anfitrión (5 ítems)**:
   Hallazgos derivados de la configuración del núcleo Linux anfitrión compartido por los contenedores Docker (respuestas ICMP timestamp CVE-1999-0524 y TCP Timestamps `sysctl net.ipv4.tcp_timestamps = 1`).

> [!NOTE]
> **Debilidades deliberadas no incluidas en el cálculo de efectividad**:
> Las contraseñas débiles por SSH (`root:toor1234`), los archivos internos en `/secretos` y configuraciones locales se mantuvieron fuera del conjunto de 28 vulnerabilidades de referencia, dado que el escaneo evaluado fue de tipo **no autenticado (black-box)**, donde OpenVAS no ejecuta fuerza bruta de credenciales ni auditoría de archivos locales del sistema de archivos.

---

## 5. El Pipeline de Automatización (n8n + OpenVAS + PostgreSQL)

El flujo de trabajo diseñado en **n8n** opera en cinco etapas secuenciales totalmente desacopladas:

1. **Descubrimiento Activo (Nmap)**:
   Escanea la subred activa (`-sV -sC`) para identificar hosts en línea y puertos abiertos, generando un documento XML estructurado.
2. **Parametrización Dinámica**:
   Nodos de código en JavaScript normalizan las tuplas `(host, port)` eliminando objetivos redundantes y estructuran la llamada al script GMP.
3. **Análisis Profundo (OpenVAS / Greenbone GMP)**:
   El wrapper `automated_scan.sh` invoca mediante un socket Unix a `automated_scan.gmp.py`, ejecutando las pruebas NVT seleccionadas con exclusión mutua (`flock`).
4. **Transformación y Persistencia (PostgreSQL)**:
   El reporte XML devuelto se transforma en objetos JSON y se almacena en la tabla relacional `vulnerability_scans` con clave primaria, marca temporal e índices optimizados.
5. **Notificación y Alertas (SMTP)**:
   Se genera automáticamente un informe ejecutivo estructurado en Markdown y HTML con la distribución de hallazgos por nivel de severidad y host, despachándose al buzón correspondiente.

