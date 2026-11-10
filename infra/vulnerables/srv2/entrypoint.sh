#!/bin/bash
set -e

# Asegurar directorio de sshd
mkdir -p /var/run/sshd
ssh-keygen -A

# Iniciar sshd en background
/usr/sbin/sshd -D -e &

# Iniciar Apache httpd en foreground
exec httpd-foreground
