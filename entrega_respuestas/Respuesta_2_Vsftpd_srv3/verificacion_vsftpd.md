# Respuesta 2 — Verificación del `vsftpd.conf` de vuln-srv3

## Pregunta

> Me falta el `vsftpd.conf` de vuln-srv3. Solo tengo una versión que dice
> `ftpd_banner=vsftpd 3.0.3`, pero según la Tabla 5.2.2 vuln-srv3 usa
> vsftpd 3.0.5. ¿Hay otra versión?

## Verificación

El archivo `vsftpd.conf` que existe en el repositorio — tanto en la carpeta
de trabajo (`vulnsrv/srv3/vsftpd.conf`) como en la entrega anterior
(`entrega_correcciones/Anexo_I_Infraestructura/vulnsrv_srv3/vsftpd.conf`) —
**ya contiene el banner correcto**:

```ini
# Línea 12 de vsftpd.conf
ftpd_banner=vsftpd 3.0.5
```

## Contenido completo del archivo actual

```ini
listen=YES
listen_ipv6=NO
anonymous_enable=YES
anon_root=/var/ftp
local_enable=YES
write_enable=YES
local_umask=022
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=YES
ftpd_banner=vsftpd 3.0.5
ssl_enable=NO
pasv_enable=YES
pasv_min_port=21200
pasv_max_port=21210
```

## Conclusión

**No se requiere ninguna acción.** El archivo ya coincide con lo declarado en
la Tabla 5.2.2 (vsftpd 3.0.5). El banner `ftpd_banner=vsftpd 3.0.5` está
presente en la línea 12.

> **Nota:** El banner `ftpd_banner` en vsftpd es un string cosmético — lo que
> determina la versión real del servicio es el paquete instalado por `apt-get`
> dentro del Dockerfile (imagen `ubuntu:20.04`, que incluye vsftpd 3.0.3 en
> sus repos). Sin embargo, el banner se usa para simular la versión declarada
> en la tabla del laboratorio, lo cual es coherente con el diseño del entorno
> de pruebas.
