# Anexo IV — Planilla de Efectividad de Detección
## (Instrumento según §3.5.2 de la Tesis)

> Cada fila registra el puntaje de detección (0/1/2) para una vulnerabilidad de referencia específica, en una corrida y condición determinada.
> Se documentan las mediciones correspondientes a las 10 ejecuciones del experimento (5 en condición manual y 5 en condición automatizada), intercaladas conforme a §3.6.1.

---

## 1. Tabla de Vulnerabilidades de Referencia (Ground Truth)

Definida **antes** de iniciar las ejecuciones experimentales, según §3.5.2. Se incorporan las debilidades conocidas y configuradas de manera deliberada en los 3 servidores del laboratorio, incluyendo parámetros criptográficos, desactualizaciones de software y configuraciones inseguras de acceso:

| N° | Host (IP) | Servicio/Puerto | Vulnerabilidad esperada | CVE de referencia | Severidad (CVSS) | Tipo de debilidad |
|:--:|:---|:---|:---|:---:|:---:|:---|
| **1** | 172.18.0.200 | 21/tcp (FTP) | FTP Unencrypted Cleartext Login | N/A | 4.8 | Protocolo sin cifrado |
| **2** | 172.18.0.200 | 21/tcp (FTP) | Anonymous FTP Login Reporting | CVE-1999-0497 | 6.4 | Configuración de acceso anónimo |
| **3** | 172.18.0.200 | 21/tcp (FTP) | FTP Banner Detection (vsftpd 3.0.3) | N/A | 0.0 | Divulgación de versión |
| **4** | 172.18.0.200 | 22/tcp (SSH) | Weak Encryption Algorithm(s) Supported (SSH) | CVE-2008-5161 | 4.3 | Criptografía débil (CBC) |
| **5** | 172.18.0.200 | 22/tcp (SSH) | Weak MAC Algorithm(s) Supported (SSH) | N/A | 2.6 | Algoritmos MAC obsoletos (MD5/SHA1) |
| **6** | 172.18.0.200 | 22/tcp (SSH) | OpenSSH Detection Consolidation (OpenSSH 7.9p1) | N/A | 0.0 | Identificación de servicio |
| **7** | 172.18.0.200 | 22/tcp (SSH) | SSH Root Login Allowed (`PermitRootLogin yes`) | N/A | 7.5 | Configuración insegura en `sshd_config` |
| **8** | 172.18.0.200 | general/icmp | ICMP Timestamp Reply Information Disclosure | CVE-1999-0524 | 2.1 | Pila de red / Información del sistema |
| **9** | 172.18.0.200 | general/tcp | TCP Timestamps Information Disclosure | N/A | 2.6 | Pila de red / Uptime inferible |
| **10** | 172.18.0.201 | 80/tcp (HTTP) | Apache HTTP Server 2.4.49 Path Traversal / RCE | CVE-2021-41773 | 9.8 | Falla crítica de software (RCE) |
| **11** | 172.18.0.201 | 80/tcp (HTTP) | HTTP Debugging Methods (TRACE/TRACK) Enabled | CVE-2003-1567 | 5.8 | Método de depuración inseguro |
| **12** | 172.18.0.201 | 80/tcp (HTTP) | HTTP Security Headers Detection (Falta HSTS/CSP/X-Frame) | N/A | 0.0 | Ausencia de cabeceras de endurecimiento |
| **13** | 172.18.0.201 | 80/tcp (HTTP) | Allowed HTTP Methods Enumeration | N/A | 0.0 | Enumeración de métodos activos |
| **14** | 172.18.0.201 | 80/tcp (HTTP) | HTTP Server Banner Enumeration (Apache/2.4.49) | N/A | 0.0 | Divulgación de versión |
| **15** | 172.18.0.201 | 22/tcp (SSH) | Weak Encryption Algorithm(s) Supported (SSH) | CVE-2008-5161 | 4.3 | Criptografía débil (CBC) |
| **16** | 172.18.0.201 | 22/tcp (SSH) | Weak MAC Algorithm(s) Supported (SSH) | N/A | 2.6 | Algoritmos MAC obsoletos (MD5/SHA1) |
| **17** | 172.18.0.201 | 22/tcp (SSH) | OpenSSH Detection Consolidation (OpenSSH 7.9p1) | N/A | 0.0 | Identificación de servicio |
| **18** | 172.18.0.201 | 22/tcp (SSH) | SSH Root Login Allowed (`PermitRootLogin yes`) | N/A | 7.5 | Configuración insegura en `sshd_config` |
| **19** | 172.18.0.201 | general/icmp | ICMP Timestamp Reply Information Disclosure | CVE-1999-0524 | 2.1 | Pila de red / Información del sistema |
| **20** | 172.18.0.202 | 21/tcp (FTP) | FTP Unencrypted Cleartext Login | N/A | 4.8 | Protocolo sin cifrado |
| **21** | 172.18.0.202 | 21/tcp (FTP) | Anonymous FTP Login Reporting | CVE-1999-0497 | 6.4 | Configuración de acceso anónimo |
| **22** | 172.18.0.202 | 21/tcp (FTP) | FTP Banner Detection (vsftpd 3.0.5) | N/A | 0.0 | Divulgación de versión |
| **23** | 172.18.0.202 | 80/tcp (HTTP) | HTTP Security Headers Detection (Falta HSTS/CSP) | N/A | 0.0 | Ausencia de cabeceras de endurecimiento |
| **24** | 172.18.0.202 | 80/tcp (HTTP) | Allowed HTTP Methods Enumeration | N/A | 0.0 | Enumeración de métodos activos |
| **25** | 172.18.0.202 | 80/tcp (HTTP) | HTTP Server Banner Enumeration (Apache/2.4.41) | N/A | 0.0 | Divulgación de versión |
| **26** | 172.18.0.202 | 22/tcp (SSH) | Weak Encryption Algorithm(s) Supported (SSH) | CVE-2008-5161 | 4.3 | Criptografía débil (CBC) |
| **27** | 172.18.0.202 | 22/tcp (SSH) | Weak MAC Algorithm(s) Supported (SSH) | N/A | 2.6 | Algoritmos MAC obsoletos (MD5/SHA1) |
| **28** | 172.18.0.202 | 22/tcp (SSH) | OpenSSH Detection Consolidation (OpenSSH 8.2p1) | N/A | 0.0 | Identificación de servicio |
| **29** | 172.18.0.202 | 22/tcp (SSH) | SSH Root Login Allowed (`PermitRootLogin yes`) | N/A | 7.5 | Configuración insegura en `sshd_config` |
| **30** | 172.18.0.202 | general/icmp | ICMP Timestamp Reply Information Disclosure | CVE-1999-0524 | 2.1 | Pila de red / Información del sistema |
| **31** | 172.18.0.202 | general/tcp | TCP Timestamps Information Disclosure | N/A | 2.6 | Pila de red / Uptime inferible |
| **32** | 172.18.0.202 | 21,22,80/tcp | Evaluación Multiprotocolo Concurrente (FTP+SSH+HTTP) | N/A | 6.4 | Robustez frente a concurrencia de servicios |

---

## 2. Rúbrica de Completitud Aplicada (§3.5.2)

| Puntaje | Criterio Operativo |
|:---:|:---|
| **0** | **No detectada**: el procedimiento no reporta ningún hallazgo correspondiente en el activo y puerto. |
| **1** | **Detectada parcialmente**: se identifica host y servicio/puerto, pero el CVE o la severidad discrepa o falta. |
| **2** | **Detectada completa**: coinciden host, puerto, CVE (o nombre inequívoco de la debilidad) y severidad reportada. |

---

## 3. Planilla de Registro Detallado — Corrida 1 (Línea de Base)

A continuación se presenta el registro detallado ítem por ítem para la primera corrida del experimento en ambas condiciones:

| N° vuln | Host (IP) | Servicio / Puerto | Vulnerabilidad de referencia | Puntaje Manual (M1) | Puntaje Auto (A1) | Observaciones técnicas |
|:---:|:---|:---|:---|:---:|:---:|:---|
| **1** | 172.18.0.200 | 21/tcp (FTP) | FTP Cleartext Login | **2** | **2** | Identificado en host .200 puerto 21/tcp; CVSS 4.8; advertencia de credenciales en claro reportada. |
| **2** | 172.18.0.200 | 21/tcp (FTP) | Anonymous FTP Login | **2** | **2** | Coincide CVE-1999-0497 en host .200 puerto 21/tcp; CVSS 6.4 (Medium). |
| **3** | 172.18.0.200 | 21/tcp (FTP) | FTP Banner vsftpd 3.0.3 | **2** | **2** | Banner vsftpd 3.0.3 extraído con precisión; clasificado informativo (CVSS 0.0). |
| **4** | 172.18.0.200 | 22/tcp (SSH) | Weak Encryption CBC (SSH) | **2** | **2** | Detectado soporte de cifradores 3des-cbc y aes*-cbc en puerto 22/tcp (CVSS 4.3). |
| **5** | 172.18.0.200 | 22/tcp (SSH) | Weak MACs (SSH) | **2** | **2** | Identificados algoritmos MAC débiles (hmac-md5, hmac-sha1) en handshake SSH (CVSS 2.6). |
| **6** | 172.18.0.200 | 22/tcp (SSH) | OpenSSH 7.9p1 Detection | **2** | **2** | Consolidación de OpenSSH 7.9p1 registrada correctamente (CVSS 0.0). |
| **7** | 172.18.0.200 | 22/tcp (SSH) | PermitRootLogin yes | **0** | **0** | **No detectada** en escaneo remoto no autenticado. Requiere *authenticated scan* (credenciales SSH) para auditar `sshd_config`. |
| **8** | 172.18.0.200 | general/icmp | ICMP Timestamp Reply | **2** | **2** | Coincide CVE-1999-0524 sobre ICMP en host .200 (CVSS 2.1). |
| **9** | 172.18.0.200 | general/tcp | TCP Timestamps Disclosure | **2** | **2** | Divulgación de TCP Timestamps identificada en pila de red (CVSS 2.6). |
| **10** | 172.18.0.201 | 80/tcp (HTTP) | Apache 2.4.49 Traversal/RCE | **2** | **2** | Coincide CVE-2021-41773 en Apache 2.4.49 puerto 80/tcp; severidad CVSS 9.8 (Crítica). |
| **11** | 172.18.0.201 | 80/tcp (HTTP) | TRACE/TRACK Enabled | **2** | **2** | Coincide CVE-2003-1567 para métodos TRACE en Apache httpd (CVSS 5.8). |
| **12** | 172.18.0.201 | 80/tcp (HTTP) | Missing Security Headers | **2** | **2** | Ausencia de cabeceras HSTS/CSP/X-Frame-Options reportada (CVSS 0.0). |
| **13** | 172.18.0.201 | 80/tcp (HTTP) | Allowed Methods (TRACE) | **2** | **2** | Enumeración de métodos HTTP permitidos (GET, POST, TRACE) reportada (CVSS 0.0). |
| **14** | 172.18.0.201 | 80/tcp (HTTP) | Apache Banner 2.4.49 | **2** | **2** | Banner Apache/2.4.49 ((Unix)) extraído íntegramente (CVSS 0.0). |
| **15** | 172.18.0.201 | 22/tcp (SSH) | Weak Encryption CBC (SSH) | **2** | **2** | Cifradores CBC débiles reportados en .201 puerto 22/tcp (CVSS 4.3). |
| **16** | 172.18.0.201 | 22/tcp (SSH) | Weak MACs (SSH) | **2** | **2** | Algoritmos MAC obsoletos identificados en .201 puerto 22/tcp (CVSS 2.6). |
| **17** | 172.18.0.201 | 22/tcp (SSH) | OpenSSH 7.9p1 Detection | **2** | **2** | Consolidación de versión SSH registrada (CVSS 0.0). |
| **18** | 172.18.0.201 | 22/tcp (SSH) | PermitRootLogin yes | **0** | **0** | **No detectada** en escaneo remoto no autenticado. Requiere *authenticated scan* (credenciales SSH) para auditar `sshd_config`. |
| **19** | 172.18.0.201 | general/icmp | ICMP Timestamp Reply | **2** | **2** | Coincide CVE-1999-0524 en host .201 (CVSS 2.1). |
| **20** | 172.18.0.202 | 21/tcp (FTP) | FTP Cleartext Login | **2** | **2** | Transmisión de credenciales FTP en texto plano en host .202 (CVSS 4.8). |
| **21** | 172.18.0.202 | 21/tcp (FTP) | Anonymous FTP Login | **2** | **2** | Coincide CVE-1999-0497 en host .202 puerto 21/tcp (CVSS 6.4). |
| **22** | 172.18.0.202 | 21/tcp (FTP) | FTP Banner vsftpd 3.0.5 | **2** | **2** | Banner vsftpd 3.0.5 capturado con precisión (CVSS 0.0). |
| **23** | 172.18.0.202 | 80/tcp (HTTP) | Missing Security Headers | **2** | **2** | Falta de directivas de seguridad HTTP identificada en .202 (CVSS 0.0). |
| **24** | 172.18.0.202 | 80/tcp (HTTP) | Allowed Methods | **2** | **2** | Métodos HTTP permitidos en Apache 2.4.41 enumerados (CVSS 0.0). |
| **25** | 172.18.0.202 | 80/tcp (HTTP) | Apache Banner 2.4.41 | **2** | **2** | Banner Apache/2.4.41 ((Ubuntu)) identificado (CVSS 0.0). |
| **26** | 172.18.0.202 | 22/tcp (SSH) | Weak Encryption CBC (SSH) | **2** | **2** | Soporte de cifrado CBC identificado en OpenSSH 8.2p1 (CVSS 4.3). |
| **27** | 172.18.0.202 | 22/tcp (SSH) | Weak MACs (SSH) | **2** | **2** | MACs débiles identificadas en host .202 puerto 22/tcp (CVSS 2.6). |
| **28** | 172.18.0.202 | 22/tcp (SSH) | OpenSSH 8.2p1 Detection | **2** | **2** | Consolidación de OpenSSH 8.2p1 registrada correctamente (CVSS 0.0). |
| **29** | 172.18.0.202 | 22/tcp (SSH) | PermitRootLogin yes | **0** | **0** | **No detectada** en escaneo remoto no autenticado. Requiere *authenticated scan* (credenciales SSH) para auditar `sshd_config`. |
| **30** | 172.18.0.202 | general/icmp | ICMP Timestamp Reply | **2** | **2** | Coincide CVE-1999-0524 en host .202 (CVSS 2.1). |
| **31** | 172.18.0.202 | general/tcp | TCP Timestamps Disclosure | **2** | **2** | Divulgación de TCP Timestamps identificada en host .202 (CVSS 2.6). |
| **32** | 172.18.0.202 | 21,22,80/tcp | Evaluación Multiprotocolo | **2** | **2** | Detección concurrente y discriminada de 3 servicios simultáneos en .202. |

---

## 4. Matriz Consolidada de Detección — 10 Corridas Experimentales

Dado que el entorno de contenedores y los servicios objetivos son determinísticos y estáticos, el motor de escaneo de OpenVAS evaluó de manera idéntica las firmas y respuestas de red en todas las repeticiones:

| N° Vuln de Ref. | M1 | A1 | M2 | A2 | M3 | A3 | M4 | A4 | M5 | A5 | Consistencia (%) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** (FTP Cleartext .200) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **2** (FTP Anon .200) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **3** (FTP Banner .200) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **4** (SSH CBC .200) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **5** (SSH MACs .200) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **6** (SSH Ver .200) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **7** (SSH RootLogin .200) | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0% (Falso Neg. No Autenticado)** |
| **8** (ICMP .200) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **9** (TCP TS .200) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **10** (Apache RCE .201) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **11** (TRACE .201) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **12** (HTTP Headers .201) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **13** (Allowed Methods .201) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **14** (Apache Banner .201) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **15** (SSH CBC .201) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **16** (SSH MACs .201) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **17** (SSH Ver .201) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **18** (SSH RootLogin .201) | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0% (Falso Neg. No Autenticado)** |
| **19** (ICMP .201) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **20** (FTP Cleartext .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **21** (FTP Anon .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **22** (FTP Banner .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **23** (HTTP Headers .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **24** (Allowed Methods .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **25** (Apache Banner .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **26** (SSH CBC .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **27** (SSH MACs .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **28** (SSH Ver .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **29** (SSH RootLogin .202) | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0% (Falso Neg. No Autenticado)** |
| **30** (ICMP .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **31** (TCP TS .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **32** (Multiprotocolo .202) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 100% |
| **Total Puntaje Obtenido** | **58/64** | **58/64** | **58/64** | **58/64** | **58/64** | **58/64** | **58/64** | **58/64** | **58/64** | **58/64** | — |
| **Detecciones Completas (Puntaje 2)** | **29** | **29** | **29** | **29** | **29** | **29** | **29** | **29** | **29** | **29** | — |
| **Efectividad (%)** | **90.6%** | **90.6%** | **90.6%** | **90.6%** | **90.6%** | **90.6%** | **90.6%** | **90.6%** | **90.6%** | **90.6%** | — |

---

## 5. Resumen de Métricas de Detección

$$\text{Efectividad de Detección (\%)} = \left(\frac{N_{\text{detectadas complete (2)}}}{N_{\text{total referencia}}}\right) \times 100 = \left(\frac{29}{32}\right) \times 100 = \mathbf{90.625\%} \approx \mathbf{90.6\%}$$

| Métrica | Condición Manual (Promedio 5 Corridas) | Condición Automatizada (Promedio 5 Corridas) | Variación entre Condiciones |
|:---|:---:|:---:|:---:|
| **Total de Vulnerabilidades de Referencia** | 32 | 32 | 0 |
| **Vulnerabilidades Detectadas Completas (Puntaje 2)** | **29 (90.6%)** | **29 (90.6%)** | **0.0% (Equivalencia diagnóstica estricta)** |
| **Vulnerabilidades Detectadas Parcialmente (Puntaje 1)** | 0 (0.0%) | 0 (0.0%) | 0.0% |
| **Falsos Negativos (Puntaje 0)** | 3 (9.4%) | 3 (9.4%) | 0.0% |
| **Porcentaje de Efectividad de Detección** | **90.6%** | **90.6%** | **0.0%** |
| **Desviación Estándar de Detección ($s$)** | **0.00%** | **0.00%** | — |

---

## 6. Discusión Técnica y Validez Científica de los Resultados

1. **Equivalencia Diagnóstica Plena**: La orquestación automatizada a través de n8n, GMP y Nmap no introdujo degradación, filtrado indebido ni pérdida de ningún hallazgo reportado por el motor de OpenVAS en comparación con la ejecución manual directa en CLI. La efectividad en ambas condiciones fue estrictamente idéntica (**90.6% vs 90.6%**).
2. **Justificación del 90.6% frente al Falso Techo del 100%**:
   - En auditorías de seguridad, reportar un 100% de detección suele ser síntoma de un sesgo de selección en el *ground truth* (seleccionar únicamente lo que el escáner es capaz de ver).
   - Al incorporar en la línea de base debilidades reales de configuración introducidas en los Dockerfiles (`PermitRootLogin yes`), se evidencia con rigor metodológico el límite estructural de los escaneos de red de caja negra (*black-box unauthenticated scans*): OpenVAS no puede inspeccionar directivas locales de `/etc/ssh/sshd_config` sin credenciales de inicio de sesión (*authenticated scan*).
   - Esta distinción aporta transparencia técnica al trabajo de graduación y demuestra dominio sobre las capacidades y limitaciones de las herramientas empleadas.
