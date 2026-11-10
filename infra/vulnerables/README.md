# Infraestructura de Servidores Vulnerables (Objetivos de Escaneo)

Entorno reproducible con tres contenedores Docker que representan los objetivos evaluados en el laboratorio de pruebas de TASTSERV sobre la subred `172.18.0.0/16` (`greenbone-community-edition_default`).

## Resumen de Servicios y Configuraciones

| Contenedor | IP Fija | Servicios / Puertos | Base OS / Software | Configuraciones y Vulnerabilidades Introducidas |
|---|---|---|---|---|
| **vuln-srv1** | `172.18.0.200` | 21/tcp (FTP)<br>22/tcp (SSH) | Debian Buster | • vsftpd 3.0.3 (`vsftpd.conf`: login anónimo habilitado).<br>• OpenSSH con Ciphers débiles (3DES, CBC) y MACs obsoletas (MD5, SHA1). |
| **vuln-srv2** | `172.18.0.201` | 80/tcp (HTTP)<br>22/tcp (SSH) | `httpd:2.4.49` (oficial Apache) | • **Apache HTTP Server 2.4.49** con directiva `<Directory />` configurada a `Require all granted` (vulnerable a **CVE-2021-41773** Path Traversal y RCE).<br>• OpenSSH con Ciphers débiles y acceso root por contraseña.<br>• Directorio `/secretos/config.txt`. |
| **vuln-srv3** | `172.18.0.202` | 21/tcp (FTP)<br>22/tcp (SSH)<br>80/tcp (HTTP) | Ubuntu 20.04 | • **Apache HTTP Server 2.4.41** con `ServerTokens Full`, `ServerSignature On` y `Options Indexes` habilitado.<br>• vsftpd con usuario `labuser` y credenciales por defecto.<br>• OpenSSH con algoritmos y MACs obsoletas.<br>• Directorio `/secretos/config.txt`. |

## Instrucciones de Despliegue

1. Asegurarse de que la red externa de Greenbone exista:
   ```bash
   docker network inspect greenbone-community-edition_default >/dev/null 2>&1 || \
   docker network create --subnet=172.18.0.0/16 greenbone-community-edition_default
   ```

2. Construir e iniciar los tres contenedores:
   ```bash
   docker compose up -d --build
   ```

3. Verificar que los contenedores estén en ejecución y respondiendo en las IPs asignadas:
   ```bash
   docker ps --filter "name=vuln-srv"
   ping -c 1 172.18.0.200
   ping -c 1 172.18.0.201
   ping -c 1 172.18.0.202
   ```

