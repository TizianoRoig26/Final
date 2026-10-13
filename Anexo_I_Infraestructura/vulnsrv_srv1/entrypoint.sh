#!/bin/bash
set -e

# Asegurar directorios requeridos
mkdir -p /var/run/sshd /var/run/vsftpd/empty /var/ftp
chmod 755 /var/run/vsftpd/empty
chmod 755 /var/ftp

# Generar host keys SSH si no existen
ssh-keygen -A

# Iniciar vsftpd en background
vsftpd /etc/vsftpd.conf &

# Iniciar sshd en foreground
exec /usr/sbin/sshd -D -e
