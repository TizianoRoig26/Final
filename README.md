## Autor
Grupo: TASTSERV

### Documentación del Proyecto
Hemos generado un informe técnico completo que detalla la arquitectura, las tecnologías empleadas, la descripción de cada nodo del flujo de n8n y la integración con OpenVAS y PostgreSQL.

Puedes acceder al informe aquí: [INFORME_PROYECTO.md](file:///home/tizi/n8n-stack/INFORME_PROYECTO.md).

---

## Guía de Despliegue Paso a Paso

Sigue esta guía para poner en marcha el entorno de automatización de escaneo de vulnerabilidades.

### Requisitos Previos
*   Tener instalado **Docker** y **Docker Compose**.
*   Acceso SSH configurado en el host que ejecutará los escaneos (el flujo usa un nodo SSH para ejecutar comandos locales/remotos).

---

### Paso 1: Levantar la Suite de OpenVAS / Greenbone
El motor de escaneo de vulnerabilidades se ejecuta mediante Docker Compose.

1. Levanta los contenedores en segundo plano:
   ```bash
   docker compose -f docker-compose-openvas.yml up -d
   ```
2. **Espera a la sincronización de feeds:** La primera vez que se inicia, OpenVAS sincronizará la base de datos de firmas de vulnerabilidades (esto puede tomar desde unos minutos hasta más de una hora dependiendo de la velocidad de conexión). Puedes verificar el estado con:
   ```bash
   docker compose -f docker-compose-openvas.yml logs -f gvmd
   ```
3. Asegúrate de configurar las credenciales GMP (usuario `admin` con la contraseña configurada en tus variables o scripts).

---

### Paso 2: Configurar la Base de Datos PostgreSQL
El flujo de n8n registra históricamente los hallazgos en PostgreSQL.

1. Accede a tu consola de PostgreSQL y crea la base de datos necesaria.
2. Ejecuta la siguiente consulta SQL para crear la tabla donde se guardarán los escaneos:
   ```sql
   CREATE TABLE public.vulnerability_scans (
       id SERIAL PRIMARY KEY,
       scan_date TIMESTAMP WITH TIME ZONE NOT NULL,
       host VARCHAR(100) NOT NULL,
       vulnerability_name VARCHAR(255) NOT NULL,
       severity NUMERIC(3, 1) NOT NULL,
       port VARCHAR(20),
       cve VARCHAR(50),
       description TEXT,
       solution TEXT
   );
   ```

---

### Paso 3: Levantar n8n
Levanta el orquestador n8n que ejecutará el flujo automático.

1. Desde la carpeta raíz de `n8n-stack`, ejecuta:
   ```bash
   docker compose up -d
   ```
2. Accede a la interfaz web de n8n ingresando a `http://localhost:5678` en tu navegador.
3. Introduce las credenciales por defecto configuradas en tu docker-compose:
   *   **Usuario:** `Tizi`
   *   **Contraseña:** `<REDACTADO>`

---

### Paso 4: Importar y Configurar el Flujo de Trabajo
Una vez dentro de la interfaz de n8n:

1. Crea un nuevo flujo de trabajo (Workflow).
2. Ve al menú de opciones de la esquina superior derecha y selecciona **Import from File**.
3. Selecciona el archivo JSON ubicado en [n8n/workflows/eZcFfWr0YiA2pAE3.json](file:///home/tizi/n8n-stack/n8n/workflows/eZcFfWr0YiA2pAE3.json).
4. Configura las 3 credenciales requeridas por el flujo en la sección **Credentials** de n8n:
   *   **SSH Password:** La cuenta SSH con permisos para ejecutar `nmap` y correr el contenedor `gvm-tools`.
   *   **PostgreSQL:** Los datos de conexión al servidor de base de datos donde creaste la tabla en el Paso 2.
   *   **SMTP:** Las credenciales de tu servidor de correo saliente para el envío de notificaciones.

---

### Paso 5: Prueba y Ejecución
1. Para verificar que todo funcione de extremo a extremo, haz clic en **Test Workflow** en la parte inferior de n8n.
2. Para que el flujo corra de forma totalmente autónoma todos los días a las 2:00 AM, activa el interruptor **Active** (esquina superior derecha).
