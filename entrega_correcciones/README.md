# 📦 ENTREGA — Correcciones a Observaciones de la Tesis TASTSERV

> Carpeta autónoma con todo el material necesario para responder a las
> observaciones N3, N9, N10 y N13 de la revisión de la tesis.

---

## Estructura de la carpeta

```
entrega_correcciones/
│
├── README.md                          ← Este archivo (índice general)
├── CORRECCIONES_OBSERVACIONES_TESIS.md ← Texto listo para copiar/pegar en la tesis
│
├── Anexo_I_Infraestructura/           ← Todo el código IaC del proyecto
│   ├── docker-compose-openvas.yml     ← Stack Greenbone CE (20+ servicios)
│   ├── docker-compose-vulnsrv.yml     ← 3 servidores vulnerables (IPs estáticas)
│   ├── docker-compose-n8n.yml         ← Orquestador n8n
│   ├── ddl_vulnerability_scans.sql    ← DDL de PostgreSQL (tabla de persistencia)
│   ├── vulnsrv_srv1/                  ← vuln-srv1: vsftpd + SSH (Debian Buster)
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   └── vsftpd.conf
│   ├── vulnsrv_srv2/                  ← vuln-srv2: Apache 2.4.49 + SSH (CVE-2021-41773)
│   │   ├── Dockerfile
│   │   └── entrypoint.sh
│   └── vulnsrv_srv3/                  ← vuln-srv3: Apache 2.4.41 + vsftpd + SSH (Ubuntu)
│       ├── Dockerfile
│       ├── entrypoint.sh
│       └── vsftpd.conf
│
├── Anexo_II_Workflow/                 ← Workflow n8n (JSON)
│   └── PENDIENTE_exportar_workflow.md ← ⚠️ Instrucciones para exportar
│
├── Anexo_III_Planilla_Tiempos/        ← Instrumento §3.5.1
│   └── planilla_tiempos_ejecucion.md  ← Corrida 1 completada + 9 pendientes
│
├── Anexo_IV_Planilla_Deteccion/       ← Instrumento §3.5.2
│   └── planilla_efectividad_deteccion.md ← Ground truth (29 vulns) + corrida 1
│
├── Anexo_V_Script_GMP/               ← Script de automatización OpenVAS
│   └── automated_scan.gmp.py         ← Script Python (gvm-tools / GMP)
│
└── Evidencia_Resultados/             ← Resultados experimentales consolidados
    └── resultados_pruebas.md          ← Corrida 1 completa con métricas
```

---

## Qué resuelve cada observación

| Obs. | Problema | Dónde se resuelve |
|------|----------|-------------------|
| **N3** | Anexos prometidos pero inexistentes, repo sin URL | `CORRECCIONES_OBSERVACIONES_TESIS.md` §3a-3c + todo `Anexo_I/` |
| **N9** | Placeholder de IP en Figura 2, Docker vs VMs no explicado | `CORRECCIONES_OBSERVACIONES_TESIS.md` §9a-9d |
| **N10** | "Sin internet" vs SMTP con Mailtrap | `CORRECCIONES_OBSERVACIONES_TESIS.md` §10a-10b |
| **N13** | Procedimiento manual no descripto | `CORRECCIONES_OBSERVACIONES_TESIS.md` §13a |

---

## Acciones pendientes antes de entregar

- [ ] **Exportar el JSON del workflow de n8n** → guardar en `Anexo_II_Workflow/workflow_tastserv.json`
- [ ] **Completar las 9 corridas experimentales restantes** (4 automatizadas + 5 manuales) → llenar las planillas en `Anexo_III` y `Anexo_IV`
- [ ] **Aplicar los cambios de texto** de `CORRECCIONES_OBSERVACIONES_TESIS.md` en el documento principal de la tesis

---

## Repositorio público

**URL:** https://github.com/TizianoRoig26/Final.git

---

## Mapeo de servidores vulnerables (resumen rápido)

| Contenedor | IP           | Servicios | Vulnerabilidad principal |
|-----------|--------------|-----------|-------------------------|
| vuln-srv1 | 172.18.0.200 | FTP + SSH | SSH CBC/MACs débiles, FTP anónimo |
| vuln-srv2 | 172.18.0.201 | HTTP + SSH | **CVE-2021-41773** (Apache 2.4.49 Path Traversal) |
| vuln-srv3 | 172.18.0.202 | HTTP + FTP + SSH | Directory listing, SSH débil, FTP anónimo |
