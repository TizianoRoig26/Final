# Registro de Correcciones y Trazabilidad Metodológica

### [14/11/2026] — `datos/camino_b/registro_escaneos.csv`

La versión anterior contenía 12 filas de septiembre reconstruidas, que asignaban a corridas del experimento reportes de Greenbone que no les correspondían (otras redes y otras fechas). Fueron retiradas y el registro se rehízo solo con las corridas de noviembre (17 filas).

- **Versión corregida**: Commit `d2fa703` (`fix(camino_b): registro formal de corridas de noviembre y manifiesto de integridad`).
- **Hash SHA-256 de la versión corregida**: `dbbbb25c9c6fa3e7fff224730277c030b038b4cd8a7e7cf193e02e4163de9795` (registrado en `datos/camino_b/SHA256SUMS_global.txt`).
- **Trazabilidad en el historial Git**: La versión anterior permanece en el historial en los commits:
  - `93d47bc` (prerregistro y carga inicial)
  - `6c4113c`, `41724c1`, `3da9df7`, `b75ddbc`, `01f7f60`, `09570d5`, `734347b`, `b984286`, `9f18d7b`, `c727249` y `d2023aa` (corridas pareadas M1-M5 y A1-A5 de Camino B e incidencia INC-01)
  - Etiquetas correspondientes (`camino-b-prereg`, `camino-b-M1` a `camino-b-M5`, `camino-b-A1` a `camino-b-A5`).
