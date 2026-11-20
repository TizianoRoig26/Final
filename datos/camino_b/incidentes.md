# Registro de Incidentes y Excepciones — Réplica Pareada «Camino B»

Este documento registra cronológicamente cualquier anomalía técnica, fallo de red, colisión de procesos, o interrupción ocurrida durante la preparación y ejecución de la serie experimental pareada de Camino B.

---

## Política de Tratamiento de Incidentes (Sección 6 del Plan)
1. **Fallo previo al inicio de escaneo:** Si ocurre un error antes de que el motor inicie el escaneo (ej. fallo de sintaxis en Nmap, timeout en token de webhook), se subsana la causa y se relanza la corrida en la misma posición del cronograma.
2. **Fallo durante o posterior al escaneo:** Si el escaneo se interrumpe con el motor ya activo, la corrida **no se descarta**: se registra como inválida con su causa documentada y los artefactos parciales se conservan. La repetición se ejecuta al final de la serie declarando formalmente la ruptura de alternancia.
3. **Regla de integridad:** **Ninguna corrida se descarta por su resultado de detección o de tiempo.**

---

## Bitácora de Eventos

| N° Incidente | Fecha / Hora (UTC) | Corrida Afectada | Tipo de Evento | Descripción Técnica y Causa Raíz | Acción Correctiva Aplicada | Estado |
|---|---|---|---|---|---|---|
| `INC-00` | 2026-11-12 18:14 | Calibración Previa | Parámetro GMP | Invocación de `get_report` en gvm-script con retorno pretransformado de lxml | Se ajustó `export_openvas_report.gmp.py` para usar `etree.tostring` directo y preservar objetos con `KEEP_GVM_OBJECTS=1`. | Resuelto |
| `INC-01` | 2026-11-12 23:25 | Corrida A5 (Intento 1) | Reinicio de Máquina | Reinicio del sistema anfitrión durante la ventana de ejecución de A5, afectando tareas en segundo plano. | Se preservan los artefactos del intento 1 en `corrida_5_intento1_reinicio/` y se repite la corrida A5 en limpio. | Resuelto |
| `INC-02` | 2026-11-12, revisión posterior | Serie completa | Cambio de código no registrado | El commit `b6460d8` se aplicó después de A2 para introducir `KEEP_GVM_OBJECTS` y no fue consignado oportunamente en este registro. | Se documenta el cambio y su momento respecto de A2; no se reclasifica ninguna corrida por este motivo. | Registrado |
