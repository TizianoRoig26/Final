FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apache2 \
        vsftpd \
        openssh-server \
        iputils-ping \
        net-tools \
        procps && \
    rm -rf /var/lib/apt/lists/*

# Crear usuario ftp y ssh de prueba
RUN useradd -m -s /bin/bash labuser && echo "labuser:lab1234" | chpasswd && \
    echo "root:toor1234" | chpasswd

# Copiar configuraciones
COPY vsftpd.conf /etc/vsftpd.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Configurar SSH deliberadamente debil
RUN echo "Ciphers 3des-cbc,aes128-cbc,aes192-cbc,aes256-cbc" >> /etc/ssh/sshd_config && \
    echo "MACs hmac-md5,hmac-sha1,umac-64@openssh.com" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

# Configurar Apache: Directory Listing (Indexes habilitado) y ServerTokens Full
RUN echo "ServerTokens Full" >> /etc/apache2/apache2.conf && \
    echo "ServerSignature On" >> /etc/apache2/apache2.conf && \
    echo '<Directory /var/www/html>\n    Options Indexes FollowSymLinks\n    AllowOverride None\n    Require all granted\n</Directory>' > /etc/apache2/conf-available/security-lab.conf && \
    a2enconf security-lab

# Crear archivos de prueba en web para verificar directory listing
RUN echo '<html><body><h1>Laboratorio TASTSERV - Servidor 3 (Apache 2.4.41 + FTP + SSH)</h1></body></html>' > /var/www/html/index.html && \
    mkdir -p /var/www/html/backup && \
    echo "backup_db_dummy.sql" > /var/www/html/backup/datos.txt

EXPOSE 21 22 80

ENTRYPOINT ["/entrypoint.sh"]
