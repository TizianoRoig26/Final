# Informe de Escaneo de Vulnerabilidades — Corrida A1 (Camino B)

**ID de Escaneo**: scan_20261112_155403
**Fecha del Escaneo**: 12/11/2026, 18:54:02 UTC
**Hosts Escaneados**: 3 (172.18.0.200, 172.18.0.201, 172.18.0.202)
**Total de Vulnerabilidades**: 167

---

## Resumen Ejecutivo

| Severidad | Cantidad | Porcentaje |
|-----------|----------|------------|
| Crítica (9.0-10.0) | 23 | 13.8% |
| Alta (7.0-8.9) | 23 | 13.8% |
| Media (4.0-6.9) | 49 | 29.3% |
| Baja e Informativa (0.0-3.9) | 72 | 43.1% |

---

## Vulnerabilidades Críticas Detectadas (23)

### 1. Apache HTTP Server 2.4.0 - 2.4.46 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2020-35452, CVE-2021-26690, CVE-2021-26691
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.48
Installation
path / port:       80/tcp...

### 2. Apache HTTP Server 2.4.0 - 2.4.55 HTTP Request Smuggling Vulnerability - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2023-25690
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.56
Installation
path / port:       80/tcp...

### 3. Apache HTTP Server 2.4.0 - 2.4.55 HTTP Request Smuggling Vulnerability - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2023-25690
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.56
Installation
path / port:       80/tcp...

### 4. Apache HTTP Server 2.4.49 - 2.4.50 Directory Traversal / RCE Vulnerability - Active Check
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-42013
- **Descripción**: It was possible to read "etc/passwd" through http://vuln-srv2.greenbone-community-edition_default/cgi-bin/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/.%%32%65/etc/passwd

Result:

root:x:0:0:root:/ro...

### 5. Apache HTTP Server 2.4.49 - 2.4.50 Directory Traversal / RCE Vulnerability - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-42013
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.51
Installation
path / port:       80/tcp...

### 6. Apache HTTP Server 2.4.49 Directory Traversal / RCE Vulnerability - Active Check
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-41773
- **Descripción**: It was possible to read "etc/passwd" through http://vuln-srv2.greenbone-community-edition_default/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd

Result:

root:x:0:0:root:/root:/bin...

### 7. Apache HTTP Server 2.4.49 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-41524, CVE-2021-41773
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.50
Installation
path / port:       80/tcp...

### 8. Apache HTTP Server < 2.4.49 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-34798, CVE-2021-39275, CVE-2021-40438
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.49
Installation
path / port:       80/tcp...

### 9. Apache HTTP Server < 2.4.54 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2022-26377, CVE-2022-28614, CVE-2022-28615, CVE-2022-29404, CVE-2022-30556, CVE-2022-31813
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.54
Installation
path / port:       80/tcp...

### 10. Apache HTTP Server < 2.4.54 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2022-26377, CVE-2022-28614, CVE-2022-28615, CVE-2022-29404, CVE-2022-30556, CVE-2022-31813
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.54
Installation
path / port:       80/tcp...

### 11. Apache HTTP Server < 2.4.55 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.0
- **CVE**: CVE-2006-20001, CVE-2022-36760, CVE-2022-37436
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.55
Installation
path / port:       80/tcp...

### 12. Apache HTTP Server < 2.4.55 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.0
- **CVE**: CVE-2006-20001, CVE-2022-36760, CVE-2022-37436
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.55
Installation
path / port:       80/tcp...

### 13. Apache HTTP Server < 2.4.60 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2024-36387, CVE-2024-38473, CVE-2024-38474, CVE-2024-38475, CVE-2024-38476, CVE-2024-38477, CVE-2024-39573
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.60
Installation
path / port:       80/tcp...

### 14. Apache HTTP Server < 2.4.60 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2024-36387, CVE-2024-38473, CVE-2024-38474, CVE-2024-38475, CVE-2024-38476, CVE-2024-38477, CVE-2024-39573
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.60
Installation
path / port:       80/tcp...

### 15. Apache HTTP Server <= 2.4.51 Buffer Overflow Vulnerability - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-44790
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.52
Installation
path / port:       80/tcp...

### 16. Apache HTTP Server <= 2.4.51 Buffer Overflow Vulnerability - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2021-44790
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.52
Installation
path / port:       80/tcp...

### 17. Apache HTTP Server <= 2.4.52 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.202
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2022-22719, CVE-2022-22720, CVE-2022-22721, CVE-2022-23943
- **Descripción**: Installed version: 2.4.41
Fixed version:     2.4.53
Installation
path / port:       80/tcp...

### 18. Apache HTTP Server <= 2.4.52 Multiple Vulnerabilities - Linux
- **Host**: 172.18.0.201
- **Puerto**: 80/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2022-22719, CVE-2022-22720, CVE-2022-22721, CVE-2022-23943
- **Descripción**: Installed version: 2.4.49
Fixed version:     2.4.53
Installation
path / port:       80/tcp...

### 19. OpenBSD OpenSSH < 9.3p2 RCE Vulnerability
- **Host**: 172.18.0.201
- **Puerto**: 22/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2023-38408
- **Descripción**: Installed version: 7.9p1
Fixed version:     9.3p2
Installation
path / port:       22/tcp...

### 20. OpenBSD OpenSSH < 9.3p2 RCE Vulnerability
- **Host**: 172.18.0.200
- **Puerto**: 22/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2023-38408
- **Descripción**: Installed version: 7.9p1
Fixed version:     9.3p2
Installation
path / port:       22/tcp...

### 21. OpenBSD OpenSSH < 9.3p2 RCE Vulnerability
- **Host**: 172.18.0.202
- **Puerto**: 22/tcp
- **Severidad CVSS**: 9.8
- **CVE**: CVE-2023-38408
- **Descripción**: Installed version: 8.2p1
Fixed version:     9.3p2
Installation
path / port:       22/tcp...

### 22. Operating System (OS) End of Life (EOL) Detection
- **Host**: 172.18.0.201
- **Puerto**: 
- **Severidad CVSS**: 10.0
- **CVE**: N/A
- **Descripción**: The "Debian GNU/Linux" Operating System on the remote host has reached the end of life.

CPE:               cpe:/o:debian:debian_linux:10
Installed version,
build or SP:       10
EOL date:          20...

### 23. Operating System (OS) End of Life (EOL) Detection
- **Host**: 172.18.0.200
- **Puerto**: 
- **Severidad CVSS**: 10.0
- **CVE**: N/A
- **Descripción**: The "Debian GNU/Linux" Operating System on the remote host has reached the end of life.

CPE:               cpe:/o:debian:debian_linux:10
Installed version,
build or SP:       10
EOL date:          20...

