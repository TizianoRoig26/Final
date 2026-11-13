# Informe de Escaneo de Vulnerabilidades — Corrida A5 Repetida (Camino B)

**ID de Escaneo**: scan_20261112_203906
**Fecha del Escaneo**: 2026-11-12 23:39:43+00
**Hosts Escaneados**: 3 (172.18.0.200, 172.18.0.201, 172.18.0.202)
**Total de Vulnerabilidades**: 169
**Nota Metodológica**: Corrida ejecutada en limpio tras el reinicio del host registrado en INC-01.

---

## Resumen Ejecutivo

| Severidad | Cantidad | Porcentaje |
|-----------|----------|------------|
| Crítica (9.0-10.0) | 23 | 13.6% |
| Alta (7.0-8.9) | 23 | 13.6% |
| Media (4.0-6.9) | 49 | 29.0% |
| Baja e Informativa (0.0-3.9) | 74 | 43.8% |

---

## Vulnerabilidades Críticas Detectadas (23)

### 1. OpenBSD OpenSSH < 9.3p2 RCE Vulnerability
- **Host**: 172.18.0.200
- **Puerto**: 22/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2023-38408
- **Descripción**: Installed version: 7.9p1
Fixed version:     9.3p2
Installation
path / port:       22/tcp

### 2. Operating System (OS) End of Life (EOL) Detection
- **Host**: 172.18.0.200
- **Puerto**: 
- **Severidad CVSS**: 10.0
- **CVE**: N/A
- **Descripción**: The "Debian GNU/Linux" Operating System on the remote host has reached the end of life.

CPE:               cpe:/o:debian:debian_linux:10
Installed version,
build or SP:       10
EOL date:          2024-06-30
EOL info:          https://en.wikipedia.org/wiki/List_of_Debian_releases#Release_table

### 3. Apache HTTP Server 2.4.0 - 2.4.55 HTTP Request Smuggling Vulnerability - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2023-25690
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.56
Installation
path / port:       80/tcp

### 4. Apache HTTP Server 2.4.49 - 2.4.50 Directory Traversal / RCE Vulnerability - Active Check
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-42013
- **Descripción**: It was possible to read "etc/passwd" through http://vuln-srv2.greenbone-community-edition_default/cgi-bin/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/etc/passwd

Result:

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin...

### 5. Apache HTTP Server 2.4.49 - 2.4.50 Directory Traversal / RCE Vulnerability - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-42013
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.51
Installation
path / port:       80/tcp

### 6. Apache HTTP Server 2.4.49 Directory Traversal / RCE Vulnerability - Active Check
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-41773
- **Descripción**: It was possible to read "etc/passwd" through http://vuln-srv2.greenbone-community-edition_default/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd

Result:

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:...

### 7. Apache HTTP Server 2.4.49 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-41524, CVE-2021-41773
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.50
Installation
path / port:       80/tcp

### 8. Apache HTTP Server < 2.4.54 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2022-26377, CVE-2022-28614, CVE-2022-28615, CVE-2022-29404, CVE-2022-30556, CVE-2022-31813
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.54
Installation
path / port:       80/tcp

### 9. Apache HTTP Server < 2.4.55 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.0
- **CVE**: CVE-2006-20001, CVE-2022-36760, CVE-2022-37436
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.55
Installation
path / port:       80/tcp

### 10. Apache HTTP Server < 2.4.60 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2024-36387, CVE-2024-38473, CVE-2024-38474, CVE-2024-38475, CVE-2024-38476, CVE-2024-38477, CVE-2024-39573
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.60
Installation
path / port:       80/tcp

### 11. Apache HTTP Server <= 2.4.51 Buffer Overflow Vulnerability - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-44790
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.52
Installation
path / port:       80/tcp

### 12. Apache HTTP Server <= 2.4.52 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2022-22719, CVE-2022-22720, CVE-2022-22721, CVE-2022-23943
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.53
Installation
path / port:       80/tcp

### 13. OpenBSD OpenSSH < 9.3p2 RCE Vulnerability
- **Host**: 172.18.0.201
- **Puerto**: 22/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2023-38408
- **Descripción**: Installed version: 7.9p1
Fixed version:     9.3p2
Installation
path / port:       22/tcp

### 14. Operating System (OS) End of Life (EOL) Detection
- **Host**: 172.18.0.201
- **Puerto**: 
- **Severidad CVSS**: 10.0
- **CVE**: N/A
- **Descripción**: The "Debian GNU/Linux" Operating System on the remote host has reached the end of life.

CPE:               cpe:/o:debian:debian_linux:10
Installed version,
build or SP:       10
EOL date:          2024-06-30
EOL info:          https://en.wikipedia.org/wiki/List_of_Debian_releases#Release_table

### 15. Apache HTTP Server 2.4.0 - 2.4.46 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2020-35452, CVE-2021-26690, CVE-2021-26691
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.48
Installation
path / port:       80/tcp

### 16. Apache HTTP Server 2.4.0 - 2.4.55 HTTP Request Smuggling Vulnerability - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2023-25690
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.56
Installation
path / port:       80/tcp

### 17. Apache HTTP Server < 2.4.49 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-34798, CVE-2021-39275, CVE-2021-40438
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.49
Installation
path / port:       80/tcp

### 18. Apache HTTP Server < 2.4.54 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2022-26377, CVE-2022-28614, CVE-2022-28615, CVE-2022-29404, CVE-2022-30556, CVE-2022-31813
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.54
Installation
path / port:       80/tcp

### 19. Apache HTTP Server < 2.4.55 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.0
- **CVE**: CVE-2006-20001, CVE-2022-36760, CVE-2022-37436
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.55
Installation
path / port:       80/tcp

### 20. Apache HTTP Server < 2.4.60 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2024-36387, CVE-2024-38473, CVE-2024-38474, CVE-2024-38475, CVE-2024-38476, CVE-2024-38477, CVE-2024-39573
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.60
Installation
path / port:       80/tcp

### 21. Apache HTTP Server <= 2.4.51 Buffer Overflow Vulnerability - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-44790
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.52
Installation
path / port:       80/tcp

### 22. Apache HTTP Server <= 2.4.52 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2022-22719, CVE-2022-22720, CVE-2022-22721, CVE-2022-23943
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.53
Installation
path / port:       80/tcp

### 23. OpenBSD OpenSSH < 9.3p2 RCE Vulnerability
- **Host**: 172.18.0.202
- **Puerto**: 22/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2023-38408
- **Descripción**: Installed version: 8.2p1
Fixed version:     9.3p2
Installation
path / port:       22/tcp

