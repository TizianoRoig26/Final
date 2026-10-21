#!/bin/bash
set -e

# Asegurar directorios requeridos
mkdir -p /var/run/sshd /var/run/vsftpd/empty /var/ftp /var/www/html/secretos
chmod 755 /var/run/vsftpd/empty
chmod 755 /var/ftp

# Generar host keys SSH si faltan
ssh-keygen -A

# Iniciar vsftpd en background
vsftpd /etc/vsftpd.conf &

# Iniciar apache2 en background
service apache2 start

# Iniciar sshd en foreground
exec /usr/sbin/sshd -D -e
