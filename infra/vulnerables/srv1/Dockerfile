FROM debian:buster-slim

# Configurar repositorios de archivo para Buster
RUN sed -i 's/deb.debian.org/archive.debian.org/g; s/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
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

# Configurar SSH deliberadamente vulnerable a algoritmos obsoletos (CBC, MACs debiles)
RUN echo "Ciphers 3des-cbc,aes128-cbc,aes192-cbc,aes256-cbc" >> /etc/ssh/sshd_config && \
    echo "MACs hmac-md5,hmac-sha1,umac-64@openssh.com" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

EXPOSE 21 22

ENTRYPOINT ["/entrypoint.sh"]
