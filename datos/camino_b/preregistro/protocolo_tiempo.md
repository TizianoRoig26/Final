# Protocolo de Medición del Tiempo de Ejecución — Réplica Pareada «Camino B»

**Proyecto:** TASTSERV — Réplica Experimental Pareada  
**Fecha de Preregistro:** 12 de Noviembre de 2026  
**Operador:** Tiziano Roig  
**Entorno:** Host unificado (Linux x86_64, red bridge Docker `172.18.0.0/16`)

---

## 1. Definición Formal de Marcas Temporales

Con el fin de garantizar una definición única y estandarizada en todo el trabajo (en concordancia con las secciones 3.3, 3.4 y 3.5.1 de la tesis), se establecen los siguientes instantes de medición:

### A. Instante Inicial ($t_0$)
- **Condición Manual ($M_i$):** Instante exacto en que el operador presiona Enter para lanzar el comando de descubrimiento Nmap (`nmap -sV -sC 172.18.0.200-202 ...`). Se registra mediante la función `mark T0_inicio` con el comando del sistema `date -u +%FT%T.%3NZ`.
- **Condición Automatizada ($A_i$):** Instante exacto en que el operador presiona Enter para disparar el webhook de n8n (`curl -s -X POST http://localhost:5678/webhook/trigger-scan ...`). Se registra con `mark T0_inicio` usando `date -u +%FT%T.%3NZ`.

### B. Instante Final de Escaneo ($t_{\text{fin}}$)
- **Definición común:** Momento en que el motor OpenVAS/Greenbone completa el escaneo y la tarea pasa al estado `Done` en el gestor `gvmd`.
- **Fuente de verdad:** Campo `end_time` de la tabla `reports` en la base de datos `gvmd` de PostgreSQL (almacenado como Unix epoch en UTC), equivalente a la etiqueta `<scan_end>` del reporte XML de Greenbone. Se contrasta con el `date` del sistema al momento de retorno del comando en el host.

### C. Finalización del Pipeline Automatizado ($t_{\text{flujo\_fin}}$)
- **Condición Automatizada ($A_i$):** Instante registrado en la columna `stoppedAt` de la tabla `execution_entity` en la base SQLite de n8n, correspondiente a la finalización de todos los nodos del workflow (descubrimiento, parseo, escaneo, persistencia en PostgreSQL y notificación SMTP).

---

## 2. Variables de Tiempo Reportadas

Para cada corrida se calcularán y reportarán las siguientes métricas:

1. **$T_{\text{medido}}$ (Tiempo de Escaneo Comparativo):**
   $$T_{\text{medido}} = t_{\text{fin}} - t_0$$
   Representa el intervalo transcurrido desde el inicio del proceso hasta la disponibilidad del reporte de vulnerabilidades en el motor. Constituye la métrica directamente comparable entre la condición manual y la automatizada.

2. **$T_{\text{flujo}}$ (Tiempo de Flujo Completo — solo Condición Automatizada):**
   $$T_{\text{flujo}} = t_{\text{flujo\_fin}} - t_0$$
   Representa el tiempo total del pipeline automatizado incluyendo la ingesta estructurada en base de datos relacional y el despacho del correo.

3. **Desglose de Etapas en Condición Manual:**
   - $T_{\text{nmap}} = T1_{\text{nmap\_fin}} - T0_{\text{inicio}}$ (tiempo de descubrimiento de puertos)
   - $T_{\text{traspaso}} = T2_{\text{lanzamiento}} - T1_{\text{nmap\_fin}}$ (latencia humana de inspección de puertos e invocación de GMP)
   - $T_{\text{openvas}} = T3_{\text{comando\_retorna}} - T2_{\text{lanzamiento}}$ (duración del escaneo OpenVAS)

---

## 3. Condiciones de Validez y Reloj

- **Reloj Unificado:** Todas las marcas temporales se registran en Tiempo Universal Coordinado (UTC), utilizando el reloj del sistema operativo host compartido por los contenedores Docker, n8n y el operador.
- **Fuera del intervalo medido en Manual:** Las tareas de exportación de reportes, extracción de sumas SHA-256 y tabulación de la rúbrica quedan fuera del tiempo medido, dado que en esta réplica el operador no realiza persistencia en base de datos.
