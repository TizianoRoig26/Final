# Registro de Correcciones y Trazabilidad Metodológica

### [14/11/2026] — `datos/camino_b/registro_escaneos.csv`

La versión anterior contenía 12 filas de septiembre reconstruidas, que asignaban a corridas del experimento reportes de Greenbone que no les correspondían (otras redes y otras fechas). Fueron retiradas y el registro se rehízo solo con las corridas de noviembre (17 filas).

- **Versión corregida**: Commit `d2fa703` (`fix(camino_b): registro formal de corridas de noviembre y manifiesto de integridad`).
- **Hash SHA-256 de la versión corregida**: `dbbbb25c9c6fa3e7fff224730277c030b038b4cd8a7e7cf193e02e4163de9795` (registrado en `datos/camino_b/SHA256SUMS_global.txt`).
- **Trazabilidad en el historial Git**: La versión anterior permanece en el historial en los commits:
  - `93d47bc` (prerregistro y carga inicial)
  - `6c4113c`, `41724c1`, `3da9df7`, `b75ddbc`, `01f7f60`, `09570d5`, `734347b`, `b984286`, `9f18d7b`, `c727249` y `d2023aa` (corridas pareadas M1-M5 y A1-A5 de Camino B e incidencia INC-01)
  - Etiquetas correspondientes (`camino-b-prereg`, `camino-b-M1` a `camino-b-M5`, `camino-b-A1` a `camino-b-A5`).

---

### [17/11/2026] — Eliminación de credencial de PostgreSQL en `HEAD` (`C9`)

En cumplimiento de la revisión de seguridad de entrega (observación C9), se eliminó de `HEAD` la contraseña por defecto de PostgreSQL que permanecía como valor de respaldo en `infra/n8n/docker-compose.yml` (línea 9) y documentada en `docs/VERSIONES.md` (línea 112):

- **Cambios en `HEAD`**:
  - `infra/n8n/docker-compose.yml`: se reemplazó el fallback en texto plano por validación *fail-fast* (`POSTGRES_PASSWORD=${POSTGRES_PASSWORD:?POSTGRES_PASSWORD requerida}`).
  - `docs/VERSIONES.md`: se sustituyó el literal publicado por `Rotada el 17/11/2026; valor no publicado.`
- **Trazabilidad en el historial Git**: El valor histórico previo persiste en los commits donde fue introducido o copiado (`ea31cf6`, `23825ba`, `dc21ccd`) y en los snapshots del árbol comprendidos entre `ea31cf6` y `ad55eb4`.
- **Invalidación**: La rotación de la contraseña en el laboratorio invalida por completo el valor histórico expuesto en dichos commits.

---

### [18/11/2026] — Endurecimiento de `infra/n8n` (`C9`) y fijación de digests en `infra/greenbone` (`C6`)

- **Observación C9 (`infra/n8n/docker-compose.yml` e `infra/n8n/.env.example`)**:
  - Puertos restringidos a interfaz loopback (`127.0.0.1:${N8N_PORT:-5678}:5678` y `127.0.0.1:${POSTGRES_PORT:-5433}:5432`).
  - Imagen `n8nio/n8n` fijada a `2.10.4@sha256:4dfbc931452471c15a760b987711d37364470344db47f1546f98402728e77612` en reemplazo de `:latest`.
  - Eliminados `user: root`, el montaje de `/var/run/docker.sock` y `/usr/bin/docker`, `NODE_FUNCTION_ALLOW_BUILTIN=*`, `NODE_FUNCTION_ALLOW_EXTERNAL=*` y `N8N_BASIC_AUTH_ACTIVE` (el workflow actual opera vía SSH y usa `httpHeaderAuth` en el webhook más User Management nativo de n8n).
- **Observación C6 (`infra/greenbone/docker-compose.yml`)**:
  - Los 21 servicios quedaron fijados con sus digests inmutables `@sha256:...` registrados en `datos/camino_b/ficha_tecnica/docker_images_digests.txt`.
