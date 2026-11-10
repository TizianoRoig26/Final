# Evidencia Experimental — Corrida del 05/11/2026

Registro documental y probatorio correspondiente a la ejecución del flujo automatizado de escaneo (`scan_20261105_223632`) y las acciones de saneamiento del entorno.

## Archivos Contenidos

1. **`correo_reporte_20261105.md`**:
   - Cuerpo íntegro del correo electrónico despachado automáticamente por el nodo SMTP de n8n al servidor sandbox Mailtrap (`scan_20261105_223632`, fecha 05/11/2026 22:36:56).
   - Contiene el resumen ejecutivo, métricas por severidad (146 vulnerabilidades detectadas con filtro `hmlg`), detalle de hallazgos por host y recomendaciones.

2. **Capturas de Pantalla (`image.png`, `image-1.png`, `image-2.png`)**:
   - `image.png`: Evidencia de saneamiento de credenciales y rotación de contraseña de base de datos PostgreSQL.
   - `image-1.png`: Verificación de purga del historial de commits con `git-filter-repo` (sustitución de credenciales planas por `<REDACTADO>`).
   - `image-2.png`: Evidencia de ejecución exitosa en el panel de n8n e inspección de logs en el entorno de pruebas.

