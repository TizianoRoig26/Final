# 📂 Punto 8: Saneamiento del Repositorio y Gestión de Credenciales

## 1. Requerimiento
> *"Repo: sacar planilla_tiempos_ejecucion.md, planilla_efectividad_deteccion.md y resultados_pruebas.md (los que tienen datos simulados). Limpiar el historial de contraseñas con git filter-repo o recrear el repo. Cambiar las contraseñas (GMP admin, n8n, Mailtrap, Postgres)."*

---

## 2. Estado de Eliminación de Archivos con Datos Simulados

### Archivos identificados y retirados del árbol de trabajo (`working tree`):
Los siguientes archivos, que contenían proyecciones teóricas y matrices extrapoladas, fueron removidos de las carpetas de entrega del proyecto:
* `entrega_final/Anexo_III_Planilla_Tiempos/planilla_tiempos_ejecucion.md` (Eliminado)
* `entrega_final/Anexo_IV_Planilla_Deteccion/planilla_efectividad_deteccion.md` (Eliminado)
* `entrega_final/Evidencia_Resultados/resultados_pruebas.md` (Eliminado)
* `entrega_correcciones/Anexo_III_Planilla_Tiempos/planilla_tiempos_ejecucion.md` (Eliminado)
* `entrega_correcciones/Anexo_IV_Planilla_Deteccion/planilla_efectividad_deteccion.md` (Eliminado)
* `entrega_correcciones/Evidencia_Resultados/resultados_pruebas.md` (Eliminado)

---

## 3. Estado del Historial de Git y Limpieza (`git filter-repo`)

### Diagnóstico Actual:
* En el working directory actual los archivos ya no existen.
* Sin embargo, en el historial de objetos de Git (`.git/objects`), dichos archivos y ciertos commits previos (por ejemplo, commit `945a79e` con tag `experimento-2026-09`) aún los conservan.
* Para realizar la purga definitiva e irreversible en el historial del repositorio antes de la publicación final o entrega al tribunal, se debe ejecutar el siguiente procedimiento:

```bash
# 1. Asegurar tener instalado git-filter-repo
pip install git-filter-repo

# 2. Purgar archivos simulados de la historia completa
git filter-repo --invert-paths \
  --path-match "planilla_tiempos_ejecucion.md" \
  --path-match "planilla_efectividad_deteccion.md" \
  --path-match "resultados_pruebas.md" \
  --force

# 3. Forzar garbage collection y eliminar referencias viejas
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

*Alternativa recomendada:* Si se prefiere una entrega completamente limpia sin arrastrar metadatos antiguos de desarrollo, se puede recrear el repositorio con un commit inicial limpio:
```bash
# Crear rama huérfana limpia
git checkout --orphan entrega_limpia
git add -A
git commit -m "chore: entrega final TASTSERV sanitizada"
```

---

## 4. Auditoría y Estado de Rotación de Credenciales

Para garantizar las mejores prácticas de DevSecOps, se identifican las credenciales del entorno y su estado:

| Servicio | Estado Actual en Entorno | Acción Realizada / Pendiente |
|----------|--------------------------|-------------------------------|
| **PostgreSQL** (`security_db`) | Rotada el 05/11/2026 | Contraseña rotada en motor (`ALTER USER`), sincronizada en `docker-compose.yml` y en el almacén de credenciales de n8n. |
| **OpenVAS / GMP** | Cuenta `admin` local | Pendiente de rotación en `gvmd` y `/home/tizi/.gvm.env`. |
| **n8n Auth** | Modo local de laboratorio | Autenticación gestionada en instancia n8n. |
| **Mailtrap / SMTP** | Credenciales de sandbox de pruebas | Sandbox de prueba académica; rotación de API key pendiente. |

**Nota sobre los scripts actuales:**  
El script [automated_scan.sh](file:///home/tizi/n8n-stack/entrega_13-10/PUNTO_5_SCRIPTS_GVM/automated_scan.sh) ya no recibe credenciales por línea de comandos ni las deja expuestas en el historial de procesos (`ps aux`), sino que las toma de variables de entorno protegidas o del archivo con permisos restringidos `/home/tizi/.gvm.env`.
