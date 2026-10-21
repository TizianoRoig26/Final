# 📦 ENTREGA — Respuestas a Aclaraciones y Observaciones del Tribunal

> Carpeta con las respuestas documentadas a las aclaraciones técnicas previas
> y a las 9 observaciones formales del tribunal de tesis para el proyecto TASTSERV.

---

## Estructura de la carpeta

```
entrega_respuestas/
│
├── README.md                              ← Este archivo (índice general)
│
├── Respuesta_1_Sed_Dockerfile_srv2/       ← Línea sed inválida en vuln-srv2
│   ├── analisis_linea_sed.md              ← Análisis técnico del problema
│   └── Dockerfile.corregido               ← Dockerfile sin la línea problemática
│
├── Respuesta_2_Vsftpd_srv3/              ← vsftpd.conf de vuln-srv3
│   └── verificacion_vsftpd.md            ← Confirmación de que el archivo es correcto
│
├── Respuesta_3_Bug_Parser_Host/          ← Fecha de corrección del parser
│   └── cronologia_fix_parser.md          ← Evidencia git + análisis de impacto en corridas
│
└── Respuesta_4_Observaciones_Tribunal/   ← Respuestas a las 9 Observaciones del Tribunal
    └── informe_respuestas_observaciones.md ← Informe exhaustivo punto por punto (1 al 9)
```

---

## Resumen de respuestas

| # | Temática | Respuesta / Dictamen Técnico |
|---|----------|------------------------------|
| **1** | ¿Dejar la línea `sed` rara en srv2 o sacarla? | **Sacarla.** Es un no-op con `\|\| true` que no aporta nada y puede generar preguntas en defensa. |
| **2** | ¿Hay otra versión de `vsftpd.conf` para srv3 con banner 3.0.5? | **No hace falta.** El archivo que ya existe dice `ftpd_banner=vsftpd 3.0.5`, coincide con la Tabla 5.2.2. |
| **3** | ¿Cuándo se corrigió el bug del parser del campo host? | **El 10/09/2026** (commit `7f30afa`), **10 días antes** de la corrida 1. Las corridas están cubiertas. |
| **4** | **Observaciones 1 a 9 del Tribunal** | **Respondidas íntegramente.** Detalle de n8n, salida real de `\d vulnerability_scans` en PostgreSQL 17, análisis acoplado de scripts GMP, depuración de archivos simulados y sanitización de credenciales. |

---

## Fecha de actualización

2026-10-21
