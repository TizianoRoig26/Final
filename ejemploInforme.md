[
  {
    "report": "
# Informe de Escaneo de Vulnerabilidades

**Fecha del Escaneo**: 18/9/2026, 04:09:53
**Hosts Escaneados**: 4
**Total de Vulnerabilidades**: 68

---

## Resumen Ejecutivo

| Severidad | Cantidad | Porcentaje |
|-----------|----------|------------|
| Crítica (9.0-10.0) | 0 | 0.0% |
| Alta (7.0-8.9) | 0 | 0.0% |
| Media (4.0-6.9) | 2 | 2.9% |
| Baja e Informativa (0.0-3.9) | 66 | 97.1% |

---

## Vulnerabilidades Críticas
*No se encontraron vulnerabilidades críticas.*


## Vulnerabilidades Altas
*No se encontraron vulnerabilidades altas.*


## Vulnerabilidades Medias

### 1. FTP Unencrypted Cleartext Login

**Host**: 192.168.56.102:21/tcp
**Severidad**: 4.8/10.0
**CVE**: N/A

**Descripcion**:
The remote FTP service accepts logins without a previous sent 'AUTH TLS' command. Response(s):

Non-anonymous sessions: 331 Please specify the password.
Anonymous sessions:     331 Please specify the password.

**Solucion Recomendada**:
Enable FTPS or enforce the connection via the 'AUTH TLS' command. Please see
  the manual of the FTP service for more information.

---


### 2. FTP Unencrypted Cleartext Login

**Host**: 192.168.56.10:21/tcp
**Severidad**: 4.8/10.0
**CVE**: N/A

**Descripcion**:
The remote FTP service accepts logins without a previous sent 'AUTH TLS' command. Response(s):

Non-anonymous sessions: 331 Please specify the password.
Anonymous sessions:     331 Please specify the password.

**Solucion Recomendada**:
Enable FTPS or enforce the connection via the 'AUTH TLS' command. Please see
  the manual of the FTP service for more information.

---


## Vulnerabilidades Bajas e Informativas

### 1. Allowed HTTP Methods Enumeration

**Host**: 192.168.56.102:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
The following list contains the URLs and corresponding supported HTTP methods.

URL                    | HTTP Methods
---------------------------------------------------------------------------------
http://192.168.56.102/ | POST,OPTIONS,HEAD,GET (obtained via HTTP OPTIONS method)

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 2. Allowed HTTP Methods Enumeration

**Host**: 192.168.56.101:5678/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
The following list contains the URLs and corresponding supported HTTP methods.

URL                         | HTTP Methods
--------------------------------------------------------------------
http://192.168.56.101:5678/ | GET,HEAD,POST,PUT,DELETE,OPTIONS,TRACE

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 3. Allowed HTTP Methods Enumeration

**Host**: 192.168.56.10:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
The following list contains the URLs and corresponding supported HTTP methods.

URL                   | HTTP Methods
--------------------------------------------------------------------------------
http://192.168.56.10/ | POST,OPTIONS,HEAD,GET (obtained via HTTP OPTIONS method)

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 4. Apache HTTP Server Detection Consolidation

**Host**: 192.168.56.10:general/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Detected Apache HTTP Server

Version:       2.4.58
Location:      80/tcp
CPE:           cpe:/a:apache:http_server:2.4.58

Concluded from version/product identification result:
Server: Apache/2.4.58 (Ubuntu)

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 5. Apache HTTP Server Detection Consolidation

**Host**: 192.168.56.102:general/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Detected Apache HTTP Server

Version:       2.4.58
Location:      80/tcp
CPE:           cpe:/a:apache:http_server:2.4.58

Concluded from version/product identification result:
Server: Apache/2.4.58 (Ubuntu)

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 6. CPE Inventory

**Host**: 192.168.56.102:general/CPE-T
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
192.168.56.102|cpe:/a:apache:http_server:2.4.58
192.168.56.102|cpe:/a:ietf:secure_shell_protocol:2.0
192.168.56.102|cpe:/a:openbsd:openssh:9.6p1
192.168.56.102|cpe:/a:vsftpd_project:vsftpd:3.0.5
192.168.56.102|cpe:/o:canonical:ubuntu_linux:24.04

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 7. CPE Inventory

**Host**: 192.168.56.101:general/CPE-T
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
192.168.56.101|cpe:/a:ietf:secure_shell_protocol:2.0
192.168.56.101|cpe:/a:openbsd:openssh:10.0p2
192.168.56.101|cpe:/o:debian:debian_linux:13

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 8. CPE Inventory

**Host**: 192.168.56.10:general/CPE-T
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
192.168.56.10|cpe:/a:apache:http_server:2.4.58
192.168.56.10|cpe:/a:ietf:secure_shell_protocol:2.0
192.168.56.10|cpe:/a:openbsd:openssh:9.6p1
192.168.56.10|cpe:/a:vsftpd_project:vsftpd:3.0.5
192.168.56.10|cpe:/o:canonical:ubuntu_linux:24.04

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 9. FTP Banner Detection

**Host**: 192.168.56.10:21/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Remote FTP server banner:

220 (vsFTPd 3.0.5)

This is probably (a):

- vsftpd

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 10. FTP Banner Detection

**Host**: 192.168.56.102:21/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Remote FTP server banner:

220 (vsFTPd 3.0.5)

This is probably (a):

- vsftpd

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 11. Hostname Determination Reporting

**Host**: 192.168.56.10:general/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Hostname determination for IP 192.168.56.10:

Hostname|Source
192.168.56.10|IP-address

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 12. Hostname Determination Reporting

**Host**: 192.168.56.101:general/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Hostname determination for IP 192.168.56.101:

Hostname|Source
192.168.56.101|IP-address

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 13. Hostname Determination Reporting

**Host**: 192.168.56.102:general/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Hostname determination for IP 192.168.56.102:

Hostname|Source
192.168.56.102|IP-address

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 14. HTTP Security Headers Detection

**Host**: 192.168.56.102:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Missing Headers                   | More Information
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Content-Security-Policy           | http...

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 15. HTTP Security Headers Detection

**Host**: 192.168.56.10:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Missing Headers                   | More Information
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Content-Security-Policy           | http...

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 16. HTTP Security Headers Detection

**Host**: 192.168.56.101:5678/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Header Name                       | Header Value
------------------------------------------------
Cross-Origin-Opener-Policy        | same-origin
Cross-Origin-Resource-Policy      | same-origin
Referrer-Policy                   | no-referrer
X-Content-Type-Options            | nosniff
X-Frame-Option...

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 17. HTTP Server Banner Enumeration

**Host**: 192.168.56.102:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
It was possible to enumerate the following HTTP server banner(s):

Server banner                  | Enumeration technique
-------------------------------------------------------------------------------------------------
Server: Apache/2.4.58 (Ubuntu) | Invalid HTTP 00.5 GET request (non-existent HTT...

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 18. HTTP Server Banner Enumeration

**Host**: 192.168.56.10:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
It was possible to enumerate the following HTTP server banner(s):

Server banner                  | Enumeration technique
-------------------------------------------------------------------------------------------------
Server: Apache/2.4.58 (Ubuntu) | Invalid HTTP 00.5 GET request (non-existent HTT...

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 19. HTTP Server type and version

**Host**: 192.168.56.10:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
The remote HTTP Server banner is:

Server: Apache/2.4.58 (Ubuntu)

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 20. HTTP Server type and version

**Host**: 192.168.56.102:80/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
The remote HTTP Server banner is:

Server: Apache/2.4.58 (Ubuntu)

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 21. ICMP Timestamp Reply Information Disclosure

**Host**: 192.168.56.101:general/icmp
**Severidad**: 2.1/10.0
**CVE**: CVE-1999-0524

**Descripcion**:
The following response / ICMP packet has been received:
- ICMP Type: 14
- ICMP Code: 0

**Solucion Recomendada**:
Various mitigations are possible:

  - Disable the support for ICMP timestamp on the remote host completely

  - Protect the remote host by a firewall, and block ICMP packets passing through the firewall in
  either direction (either completely or only for untrusted networks)

---


### 22. ICMP Timestamp Reply Information Disclosure

**Host**: 192.168.56.10:general/icmp
**Severidad**: 2.1/10.0
**CVE**: CVE-1999-0524

**Descripcion**:
The following response / ICMP packet has been received:
- ICMP Type: 14
- ICMP Code: 0

**Solucion Recomendada**:
Various mitigations are possible:

  - Disable the support for ICMP timestamp on the remote host completely

  - Protect the remote host by a firewall, and block ICMP packets passing through the firewall in
  either direction (either completely or only for untrusted networks)

---


### 23. ICMP Timestamp Reply Information Disclosure

**Host**: 192.168.56.102:general/icmp
**Severidad**: 2.1/10.0
**CVE**: CVE-1999-0524

**Descripcion**:
The following response / ICMP packet has been received:
- ICMP Type: 14
- ICMP Code: 0

**Solucion Recomendada**:
Various mitigations are possible:

  - Disable the support for ICMP timestamp on the remote host completely

  - Protect the remote host by a firewall, and block ICMP packets passing through the firewall in
  either direction (either completely or only for untrusted networks)

---


### 24. OpenSSH Detection Consolidation

**Host**: 192.168.56.101:general/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Detected OpenSSH Server

Version:       10.0p2
Location:      22/tcp
CPE:           cpe:/a:openbsd:openssh:10.0p2

Concluded from version/product identification result:
SSH-2.0-OpenSSH_10.0p2 Debian-7+deb13u4

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 25. OpenSSH Detection Consolidation

**Host**: 192.168.56.102:general/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Detected OpenSSH Server

Version:       9.6p1
Location:      22/tcp
CPE:           cpe:/a:openbsd:openssh:9.6p1

Concluded from version/product identification result:
SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.19

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 26. OpenSSH Detection Consolidation

**Host**: 192.168.56.10:general/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Detected OpenSSH Server

Version:       9.6p1
Location:      22/tcp
CPE:           cpe:/a:openbsd:openssh:9.6p1

Concluded from version/product identification result:
SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.19

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 27. OS Detection Consolidation and Reporting

**Host**: 192.168.56.102:general/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Best matching OS:

OS:           Ubuntu 24.04
Version:      24.04
CPE:          cpe:/o:canonical:ubuntu_linux:24.04
Found by VT:  1.3.6.1.4.1.25623.1.0.105586 (Operating System (OS) Detection (SSH Banner))
Concluded from SSH banner on port 22/tcp: SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.19
Setting ke...

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 28. OS Detection Consolidation and Reporting

**Host**: 192.168.56.10:general/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Best matching OS:

OS:           Ubuntu 24.04
Version:      24.04
CPE:          cpe:/o:canonical:ubuntu_linux:24.04
Found by VT:  1.3.6.1.4.1.25623.1.0.105586 (Operating System (OS) Detection (SSH Banner))
Concluded from SSH banner on port 22/tcp: SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.19
Setting ke...

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 29. OS Detection Consolidation and Reporting

**Host**: 192.168.56.101:general/tcp
**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
Best matching OS:

OS:           Debian GNU/Linux 13
Version:      13
CPE:          cpe:/o:debian:debian_linux:13
Found by VT:  1.3.6.1.4.1.25623.1.0.105586 (Operating System (OS) Detection (SSH Banner))
Concluded from SSH banner on port 22/tcp: SSH-2.0-OpenSSH_10.0p2 Debian-7+deb13u4
Setting key \"H...

**Solucion Recomendada**:
*Sin solución especificada.*

---


### 30. PQC Key Exchange (KEX) Algorithm(s) Supported (SSH)

**Host**: Unknown:Unknown**Severidad**: 0/10.0
**CVE**: N/A

**Descripcion**:
*Sin descripción.*

**Solucion Recomendada**:
*Sin solución especificada.*

---
*...y 36 vulnerabilidades bajas e informativas adicionales.*


## Recomendaciones Generales

1. Priorizar la remediación de vulnerabilidades críticas y altas inmediatamente.
2. Aplicar parches de seguridad para mitigar las vulnerabilidades de severidad media (como la transmisión de credenciales FTP en texto claro).
3. Revisar los hallazgos bajos e informativos (ej. banners expuestos, métodos HTTP permitidos) para reducir la superficie de ataque y mejorar el bastionado (hardening) de los servidores.
4. Implementar políticas de actualización regular.
5. Realizar escaneos de seguimiento después de aplicar correcciones.

---

## Hosts Analizados


### 192.168.56.102
- Total vulnerabilidades: 23
- Críticas: 0
- Altas: 0
- Medias: 1
- Bajas/Informativas: 22


### 192.168.56.101
- Total vulnerabilidades: 16
- Críticas: 0
- Altas: 0
- Medias: 0
- Bajas/Informativas: 16


### 192.168.56.10
- Total vulnerabilidades: 23
- Críticas: 0
- Altas: 0
- Medias: 1
- Bajas/Informativas: 22


### Unknown
- Total vulnerabilidades: 6
- Críticas: 0
- Altas: 0
- Medias: 0
- Bajas/Informativas: 6


---

*Informe generado automáticamente por el sistema de escaneo de vulnerabilidades*
",
    "scanDate": "2026-09-18T16:09:53Z",
    "summary": {
      "total": 68,
      "critical": 0,
      "high": 0,
      "medium": 2,
      "low": 66
    }
  }
]