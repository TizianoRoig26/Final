# Anexo II — Workflow de n8n (JSON exportado)

## ⚠️ PENDIENTE: Exportar el workflow desde n8n

Para generar este anexo:

1. Abrir la interfaz web de n8n en `http://localhost:5678`
2. Abrir el workflow de escaneo automatizado (TASTSERV)
3. Click en los **tres puntos** (⋮) del menú del workflow → **Export**
4. Guardar el archivo `.json` exportado en esta carpeta
5. Renombrar el archivo a `workflow_tastserv.json`

### Alternativa por CLI

Si n8n no está corriendo, el workflow se puede extraer directamente
desde los archivos de configuración:

```bash
# Los workflows se guardan en ~/.n8n/database.sqlite
# o en el directorio montado como volumen en Docker
ls ~/.n8n/
```

### ¿Por qué es importante?

El tribunal necesita verificar:
- La estructura de nodos del pipeline (10 nodos)
- La configuración del Cron Trigger (expresión `0 2 * * *`)
- Los nodos de código JavaScript que parsean Nmap y OpenVAS
- La configuración del nodo SMTP (Mailtrap)
- El mapeo de columnas del nodo PostgreSQL
