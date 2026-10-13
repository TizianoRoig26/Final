# Resultados Experimentales de Evaluación de Seguridad (TASTSERV)
## Entorno de Pruebas de Laboratorio y Ejecución Comparativa (Manual vs. Automatizada)

El presente documento consolida la totalidad de los resultados experimentales obtenidos a partir del despliegue del entorno de laboratorio con 3 servidores deliberadamente configurados con vulnerabilidades conocidas y la ejecución del programa experimental de 10 corridas (5 en condición manual y 5 en condición automatizada con n8n + GMP + OpenVAS/Greenbone).

La estructura de las tablas responde de manera estricta al diseño experimental e instrumentos de medición documentados en las secciones **3.5.1**, **3.5.2**, **3.6.1** y **5.1** de la Tesis (`Tesis PF TastServ.md`).

---

### 1. Entorno Experimental Desplegado

El entorno de evaluación fue construido mediante contenedores Docker con direccionamiento estático en el segmento de red interna `172.18.0.0/16` (`greenbone-community-edition_default`), garantizando aislamiento, repetibilidad e infraestructura como código:

| Activo | Dirección IP | Sistema Operativo Base | Servicios Expuestos | Perfil Experimental y Vulnerabilidades Principales |
| :--- | :--- | :--- | :--- | :--- |
| **vuln-srv1** | `172.18.0.200` | Debian 10 Buster | vsftpd 3.0.3 (21/tcp), OpenSSH 7.9p1 (22/tcp) | Servidor de archivos y administración remota heredada (CBC mode, FTP anónimo, `PermitRootLogin yes`) |
| **vuln-srv2** | `172.18.0.201` | Debian 10 Buster | Apache httpd 2.4.49 (80/tcp), OpenSSH 7.9p1 (22/tcp) | Servidor web vulnerable a Path Traversal / RCE (**CVE-2021-41773**), métodos TRACE y SSH débil |
| **vuln-srv3** | `172.18.0.202` | Ubuntu 20.04 LTS | vsftpd 3.0.5 (21/tcp), Apache 2.4.41 (80/tcp), OpenSSH 8.2p1 (22/tcp) | Servidor multifunción con concurrencia de servicios FTP, HTTP y SSH, Directory Listing explícito |

---

### 2. Tabla de Vulnerabilidades de Referencia (Ground Truth)
*(Estructura según Sección 3.5.2 de la Tesis — Líneas 553–557)*

Dicho conjunto documenta las 32 debilidades conocidas introducidas deliberadamente en los activos del laboratorio antes de iniciar las ejecuciones experimentales:

| N° | Host (IP) | Servicio/Puerto | Vulnerabilidad esperada | CVE de referencia | Severidad esperada (CVSS) |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **1** | `172.18.0.200` | 21/tcp (FTP) | FTP Unencrypted Cleartext Login | N/A | 4.8 |
| **2** | `172.18.0.200` | 21/tcp (FTP) | Anonymous FTP Login Reporting | CVE-1999-0497 | 6.4 |
| **3** | `172.18.0.200` | 21/tcp (FTP) | FTP Banner Detection (vsftpd 3.0.3) | N/A | 0.0 |
| **4** | `172.18.0.200` | 22/tcp (SSH) | Weak Encryption Algorithm(s) Supported (SSH) | CVE-2008-5161 | 4.3 |
| **5** | `172.18.0.200` | 22/tcp (SSH) | Weak MAC Algorithm(s) Supported (SSH) | N/A | 2.6 |
| **6** | `172.18.0.200` | 22/tcp (SSH) | OpenSSH Detection Consolidation (OpenSSH 7.9p1) | N/A | 0.0 |
| **7** | `172.18.0.200` | 22/tcp (SSH) | SSH Root Login Allowed (`PermitRootLogin yes`) | N/A | 7.5 |
| **8** | `172.18.0.200` | general/icmp | ICMP Timestamp Reply Information Disclosure | CVE-1999-0524 | 2.1 |
| **9** | `172.18.0.200` | general/tcp | TCP Timestamps Information Disclosure | N/A | 2.6 |
| **10** | `172.18.0.201` | 80/tcp (HTTP) | Apache HTTP Server 2.4.49 Directory Traversal / RCE | CVE-2021-41773 | 9.8 |
| **11** | `172.18.0.201` | 80/tcp (HTTP) | HTTP Debugging Methods (TRACE/TRACK) Enabled | CVE-2003-1567 | 5.8 |
| **12** | `172.18.0.201` | 80/tcp (HTTP) | HTTP Security Headers Detection (Falta HSTS/CSP/X-Frame) | N/A | 0.0 |
| **13** | `172.18.0.201` | 80/tcp (HTTP) | Allowed HTTP Methods Enumeration | N/A | 0.0 |
| **14** | `172.18.0.201` | 80/tcp (HTTP) | HTTP Server Banner Enumeration (Apache/2.4.49) | N/A | 0.0 |
| **15** | `172.18.0.201` | 22/tcp (SSH) | Weak Encryption Algorithm(s) Supported (SSH) | CVE-2008-5161 | 4.3 |
| **16** | `172.18.0.201` | 22/tcp (SSH) | Weak MAC Algorithm(s) Supported (SSH) | N/A | 2.6 |
| **17** | `172.18.0.201` | 22/tcp (SSH) | OpenSSH Detection Consolidation (OpenSSH 7.9p1) | N/A | 0.0 |
| **18** | `172.18.0.201` | 22/tcp (SSH) | SSH Root Login Allowed (`PermitRootLogin yes`) | N/A | 7.5 |
| **19** | `172.18.0.201` | general/icmp | ICMP Timestamp Reply Information Disclosure | CVE-1999-0524 | 2.1 |
| **20** | `172.18.0.202` | 21/tcp (FTP) | FTP Unencrypted Cleartext Login | N/A | 4.8 |
| **21** | `172.18.0.202` | 21/tcp (FTP) | Anonymous FTP Login Reporting | CVE-1999-0497 | 6.4 |
| **22** | `172.18.0.202` | 21/tcp (FTP) | FTP Banner Detection (vsftpd 3.0.5) | N/A | 0.0 |
| **23** | `172.18.0.202` | 80/tcp (HTTP) | HTTP Security Headers Detection (Falta HSTS/CSP) | N/A | 0.0 |
| **24** | `172.18.0.202` | 80/tcp (HTTP) | Allowed HTTP Methods Enumeration | N/A | 0.0 |
| **25** | `172.18.0.202` | 80/tcp (HTTP) | HTTP Server Banner Enumeration (Apache/2.4.41) | N/A | 0.0 |
| **26** | `172.18.0.202` | 22/tcp (SSH) | Weak Encryption Algorithm(s) Supported (SSH) | CVE-2008-5161 | 4.3 |
| **27** | `172.18.0.202` | 22/tcp (SSH) | Weak MAC Algorithm(s) Supported (SSH) | N/A | 2.6 |
| **28** | `172.18.0.202` | 22/tcp (SSH) | OpenSSH Detection Consolidation (OpenSSH 8.2p1) | N/A | 0.0 |
| **29** | `172.18.0.202` | 22/tcp (SSH) | SSH Root Login Allowed (`PermitRootLogin yes`) | N/A | 7.5 |
| **30** | `172.18.0.202` | general/icmp | ICMP Timestamp Reply Information Disclosure | CVE-1999-0524 | 2.1 |
| **31** | `172.18.0.202` | general/tcp | TCP Timestamps Information Disclosure | N/A | 2.6 |
| **32** | `172.18.0.202` | 21,22,80/tcp | Evaluación Multiprotocolo Concurrente (FTP+SSH+HTTP) | N/A | 6.4 |

---

### 3. Planilla de Recolección de Efectividad de Detección (Extracto Corrida 1)
*(Estructura según Sección 3.5.2 de la Tesis — Rúbrica 0/1/2)*

**Rúbrica de completitud aplicada:**
- **0:** No detectada.
- **1:** Detectada parcialmente (host y puerto identificados, pero falta o discrepa el CVE/severidad).
- **2:** Detectada completa (coinciden host, puerto, CVE/nombre inequívoco y severidad).

| N° corrida | Condición | N° vuln ref | Puntaje | Observaciones |
| :---: | :---: | :---: | :---: | :--- |
| 1 | Automatizada | 1 | **2** | Identificado en host .200 puerto 21/tcp; CVSS 4.8; login claro reportado. |
| 1 | Automatizada | 2 | **2** | Coincide CVE-1999-0497 en host .200 puerto 21/tcp; CVSS 6.4 (Medium). |
| 1 | Automatizada | 3 | **2** | Banner vsftpd 3.0.3 detectado y clasificado informativo (CVSS 0.0). |
| 1 | Automatizada | 4 | **2** | Detectado soporte de cifradores CBC obsoletos en puerto 22/tcp (CVSS 4.3). |
| 1 | Automatizada | 5 | **2** | Identificados algoritmos MAC débiles (MD5/SHA1) en puerto 22/tcp (CVSS 2.6). |
| 1 | Automatizada | 6 | **2** | Consolidación de OpenSSH 7.9p1 registrada correctamente (CVSS 0.0). |
| 1 | Automatizada | 7 | **0** | **No detectada**: `PermitRootLogin yes` en `sshd_config` no es observable en escaneo de red sin credenciales (requiere authenticated scan). |
| 1 | Automatizada | 8 | **2** | Coincide CVE-1999-0524 sobre ICMP en host .200 (CVSS 2.1). |
| 1 | Automatizada | 9 | **2** | Divulgación de TCP Timestamps identificada en pila de red (CVSS 2.6). |
| 1 | Automatizada | 10 | **2** | Coincide CVE-2021-41773 en Apache 2.4.49 puerto 80/tcp; CVSS 9.8 (Crítica). |
| 1 | Automatizada | 11 | **2** | Coincide CVE-2003-1567 para métodos TRACE/TRACK en Apache (CVSS 5.8). |
| 1 | Automatizada | 12 | **2** | Ausencia de cabeceras HSTS/CSP/X-Frame-Options reportada (CVSS 0.0). |
| 1 | Automatizada | 13 | **2** | Enumeración de métodos HTTP permitidos (GET, POST, TRACE) (CVSS 0.0). |
| 1 | Automatizada | 14 | **2** | Banner Apache/2.4.49 ((Unix)) extraído íntegramente (CVSS 0.0). |
| 1 | Automatizada | 15 | **2** | Cifradores CBC débiles reportados en .201 puerto 22/tcp (CVSS 4.3). |
| 1 | Automatizada | 16 | **2** | Algoritmos MAC obsoletos identificados en .201 puerto 22/tcp (CVSS 2.6). |
| 1 | Automatizada | 17 | **2** | Consolidación de versión SSH registrada (CVSS 0.0). |
| 1 | Automatizada | 18 | **0** | **No detectada**: `PermitRootLogin yes` en .201 no es observable en escaneo remoto sin credenciales. |
| 1 | Automatizada | 19 | **2** | Coincide CVE-1999-0524 en host .201 (CVSS 2.1). |
| 1 | Automatizada | 20 | **2** | Transmisión de credenciales FTP en texto plano en host .202 (CVSS 4.8). |
| 1 | Automatizada | 21 | **2** | Coincide CVE-1999-0497 en host .202 puerto 21/tcp (CVSS 6.4). |
| 1 | Automatizada | 22 | **2** | Banner vsftpd 3.0.5 capturado con precisión (CVSS 0.0). |
| 1 | Automatizada | 23 | **2** | Falta de directivas de seguridad HTTP identificada en .202 (CVSS 0.0). |
| 1 | Automatizada | 24 | **2** | Métodos HTTP permitidos en Apache 2.4.41 enumerados (CVSS 0.0). |
| 1 | Automatizada | 25 | **2** | Banner Apache/2.4.41 ((Ubuntu)) identificado (CVSS 0.0). |
| 1 | Automatizada | 26 | **2** | Soporte de cifrado CBC identificado en OpenSSH 8.2p1 (CVSS 4.3). |
| 1 | Automatizada | 27 | **2** | MACs débiles identificadas en host .202 puerto 22/tcp (CVSS 2.6). |
| 1 | Automatizada | 28 | **2** | Consolidación de OpenSSH 8.2p1 registrada correctamente (CVSS 0.0). |
| 1 | Automatizada | 29 | **0** | **No detectada**: `PermitRootLogin yes` en .202 no es observable en escaneo remoto sin credenciales. |
| 1 | Automatizada | 30 | **2** | Coincide CVE-1999-0524 en host .202 (CVSS 2.1). |
| 1 | Automatizada | 31 | **2** | Divulgación de TCP Timestamps identificada en host .202 (CVSS 2.6). |
| 1 | Automatizada | 32 | **2** | Detección concurrente y discriminada de 3 servicios simultáneos en .202. |

*(Nota: En las 5 corridas manuales y las 5 corridas automatizadas, el resultado fue exactamente el mismo: 29 detecciones completas, 0 parciales y 3 no detectadas por límite de autenticación, logrando un 90.6% en cada corrida; véase matriz completa en Anexo IV).*

---

### 4. Tiempos de Ejecución y Comparación de Corridas (§3.5.1)

#### Registro Consolidado de las 10 Corridas (Alternadas M-A-M-A...)

| Corrida | Condición | Fecha | t_inicio | t_fin | Duración (min:seg) | Duración (seg) | Observaciones |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **M1** | Manual | 2026-09-20 | 15:14:10 | 16:01:25 | **47:15** | 2835 s | Procedimiento manual inicial; tabulación en planilla. |
| **A1** | Automatizada | 2026-09-22 | 19:10:16 | 19:26:43 | **16:27** | 987 s | Nmap: 12s, OpenVAS: 16m15s, n8n/SMTP: 2s. |
| **M2** | Manual | 2026-09-22 | 19:40:05 | 20:25:38 | **45:33** | 2733 s | Parámetros transferidos manualmente a gvm-tools. |
| **A2** | Automatizada | 2026-09-22 | 20:45:10 | 21:01:48 | **16:38** | 998 s | Ciclo nominal sin intervención humana. |
| **M3** | Manual | 2026-09-22 | 21:20:00 | 22:04:12 | **44:12** | 2652 s | Leve ganancia de agilidad del operador en CLI. |
| **A3** | Automatizada | 2026-09-23 | 10:15:30 | 10:31:54 | **16:24** | 984 s | Descubrimiento: 12s, Escaneo: 16m13s. |
| **M4** | Manual | 2026-09-23 | 10:50:15 | 11:33:55 | **43:40** | 2620 s | Tabulación manual de 90 hallazgos brutos. |
| **A4** | Automatizada | 2026-09-23 | 11:55:00 | 12:11:31 | **16:31** | 991 s | Persistencia estructurada en PostgreSQL. |
| **M5** | Manual | 2026-09-23 | 14:10:00 | 14:52:48 | **42:48** | 2568 s | Mejor tiempo manual del operador (efecto aprendizaje). |
| **A5** | Automatizada | 2026-09-23 | 15:15:20 | 15:31:39 | **16:19** | 979 s | Ciclo nominal completado con éxito. |

#### Medidas Descriptivas Comparativas

| Indicador | Condición Manual | Condición Automatizada | Impacto / Diferencia |
| :--- | :---: | :---: | :---: |
| **Promedio ($\bar{x}$)** | **44 min 42 seg (2681.6 s)** | **16 min 28 seg (987.8 s)** | **-28 min 14 seg (-63.16%)** |
| **Desviación Estándar ($s$)** | **1 min 45 seg (104.58 s)** | **0 min 07 seg (7.19 s)** | **Reducción de variabilidad (mayor predictibilidad)** |
| **Tiempo Mínimo** | 42 min 48 seg | 16 min 19 seg | -26 min 29 seg |
| **Tiempo Máximo** | 47 min 15 seg | 16 min 38 seg | -30 min 37 seg |

---

### 5. Evaluación Detallada por Caso de Estudio

#### Caso 1: Servicios FTP (Puertos 21/tcp en .200 y .202)
- **Hallazgos clave**: OpenVAS identificó exitosamente el acceso anónimo habilitado (**CVE-1999-0497**, CVSS 6.4) y el inicio de sesión sin cifrado en texto claro (CVSS 4.8), junto con los banners de servicio respectivos (`vsftpd 3.0.3` en .200 y `vsftpd 3.0.5` en .202).
- **Efectividad en el caso**: **100% (6/6 vulnerabilidades con puntaje 2)**.

#### Caso 2: Servicios SSH (Puertos 22/tcp en .200, .201 y .202)
- **Hallazgos clave**:
  - Detección completa de ciphers obsoletos en modo CBC (**CVE-2008-5161**, CVSS 4.3), algoritmos MAC débiles (HMAC-MD5 / HMAC-SHA1, CVSS 2.6) y discriminación exacta de versión (`OpenSSH 7.9p1` en .200/.201 y `OpenSSH 8.2p1` en .202).
  - Respecto a `PermitRootLogin yes`, el escáner no emite reporte debido a que el perfil `Full and fast` se ejecutó en modalidad remota no autenticada. La lectura de `sshd_config` requiere credenciales de acceso local. Esto asigna un puntaje **0** a las 3 instancias de dicha debilidad, documentando de forma científicamente rigurosa el alcance del escaneo no autenticado.
- **Efectividad en el caso**: **75.0% (9/12 vulnerabilidades con puntaje 2; 3 con puntaje 0)**.

#### Caso 3: Servicios Web HTTP (Puertos 80/tcp en .201 y .202)
- **Hallazgos clave**: En `vuln-srv2` (.201) se identificó de forma activa y con máxima severidad la vulnerabilidad crítica de **Path Traversal y Remote Code Execution en Apache 2.4.49** (**CVE-2021-41773**, CVSS 9.8), así como los métodos de depuración inseguros (**TRACE habilitado**, CVE-2003-1567, CVSS 5.8). En ambos servidores web se detectó la ausencia sistemática de cabeceras defensivas (HSTS, CSP y X-Frame-Options).
- **Efectividad en el caso**: **100% (8/8 vulnerabilidades con puntaje 2)**.

#### Caso 4: Configuraciones de Pila de Red (Hosts .200, .201 y .202)
- **Hallazgos clave**: Se evidenció en todos los activos la respuesta a solicitudes de timestamp ICMP (**CVE-1999-0524**, CVSS 2.1) y la divulgación de TCP Timestamps (CVSS 2.6), permitiendo a un atacante inferir el uptime del host.
- **Efectividad en el caso**: **100% (5/5 vulnerabilidades con puntaje 2)**.

#### Caso 5: Servicios Combinados y Análisis Concurrente (Host .202)
- **Hallazgos clave**: El sistema evaluó con éxito el activo multiprotocolo `172.18.0.202`, discriminando simultáneamente vulnerabilidades en la capa FTP, SSH y HTTP sobre el mismo ciclo de escaneo, sin provocar degradación de servicio ni colisiones de proceso en OpenVAS.
- **Efectividad en el caso**: **100% (1/1 vulnerabilidad con puntaje 2)**.

---

### 6. Métricas Consolidadas Globales

$$\text{Efectividad de Detección (\%)} = \left(\frac{29}{32}\right) \times 100 = \mathbf{90.625\%} \approx \mathbf{90.6\%}$$

$$\text{Reducción de Tiempo Promedio (\%)} = \left(1 - \frac{987.8\text{ s}}{2681.6\text{ s}}\right) \times 100 = \mathbf{63.16\%}$$

| Métrica Global | Condición Manual | Condición Automatizada | Conclusión Metodológica |
| :--- | :---: | :---: | :--- |
| **Total de Activos Evaluados** | 3 | 3 | Entorno idéntico |
| **Total de Puertos Analizados** | 7 | 7 | 21/tcp (x2), 22/tcp (x3), 80/tcp (x2) |
| **Vulnerabilidades de Ground Truth** | 32 | 32 | Marco de referencia unificado |
| **Detecciones Completas (Puntaje 2)** | **29 (90.6%)** | **29 (90.6%)** | **Cero degradación diagnóstica (0.0% diferencia)** |
| **Detecciones Parciales (Puntaje 1)** | 0 (0.0%) | 0 (0.0%) | Coincidencia exacta de firmas y severidades |
| **Falsos Negativos (Puntaje 0)** | 3 (9.4%) | 3 (9.4%) | Límite estructural de escaneo no autenticado |
| **Tiempo Promedio de Ejecución** | **44 min 42 seg** | **16 min 28 seg** | **Ahorro de 28 min 14 seg por corrida (-63.16%)** |
| **Desviación Estándar de Tiempo** | **104.58 seg** | **7.19 seg** | **Mayor estabilidad y predictibilidad en n8n** |
| **Persistencia Estructurada** | Inviable manualmente | 100% automatizada | Tabla `vulnerability_scans` en PostgreSQL |
| **Notificación Ejecutiva** | Redacción manual | 100% automatizada | Despacho por SMTP vía Mailtrap |
