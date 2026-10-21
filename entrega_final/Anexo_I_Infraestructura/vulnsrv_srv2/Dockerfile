FROM httpd:2.4.49

# Configurar repositorios de archivo para Buster en la imagen base
RUN sed -i 's/deb.debian.org/archive.debian.org/g; s/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        openssh-server \
        iputils-ping \
        net-tools \
        procps && \
    rm -rf /var/lib/apt/lists/*

# Crear usuario para ssh
RUN useradd -m -s /bin/bash labuser && echo "labuser:lab1234" | chpasswd && \
    echo "root:toor1234" | chpasswd

# Configurar SSH con ciphers debiles
RUN echo "Ciphers 3des-cbc,aes128-cbc,aes192-cbc,aes256-cbc" >> /etc/ssh/sshd_config && \
    echo "MACs hmac-md5,hmac-sha1,umac-64@openssh.com" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

# Configurar Apache httpd.conf:
# 1. Habilitar la vulnerabilidad de Path Traversal CVE-2021-41773 permitiendo acceso en raiz
RUN sed -i 's/<Directory \/>/,+4 s/Require all denied/Require all granted/' /usr/local/apache2/conf/httpd.conf || true && \
    echo '<Directory "/">\n    AllowOverride none\n    Require all granted\n</Directory>' >> /usr/local/apache2/conf/httpd.conf

# 2. Exponer ServerTokens Full y TraceEnable
RUN echo "ServerTokens Full" >> /usr/local/apache2/conf/httpd.conf && \
    echo "ServerSignature On" >> /usr/local/apache2/conf/httpd.conf && \
    echo "TraceEnable On" >> /usr/local/apache2/conf/httpd.conf

# Pagina HTML sencilla
RUN echo '<html><body><h1>Laboratorio TASTSERV - Servidor 2 (Apache 2.4.49)</h1></body></html>' > /usr/local/apache2/htdocs/index.html

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80 22

ENTRYPOINT ["/entrypoint.sh"]
