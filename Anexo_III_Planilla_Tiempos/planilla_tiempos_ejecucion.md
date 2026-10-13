# Anexo III — Planilla de Registro de Tiempos de Ejecución
## (Instrumento según §3.5.1 de la Tesis)

> Cada fila corresponde a una corrida del experimento.
> Las corridas se intercalaron en orden alternado (M1 → A1 → M2 → A2 → M3 → A3 → M4 → A4 → M5 → A5) conforme al diseño experimental detallado en §3.6.1 para controlar y mitigar el efecto de aprendizaje del operador.

---

### Condición Automatizada (Pipeline n8n + GMP + PostgreSQL)

| N° corrida | Condición    | Fecha      | t_inicio | t_fin    | Duración (min:seg) | Duración (seg) | Observaciones |
|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | Automatizada | 2026-09-22 | 19:10:16 | 19:26:43 | **16:27** | 987 s | Corrida completada sin anomalías. Nmap: 11.86s. OpenVAS: 16m15s. Persistencia y SMTP: 2.3s. |
| 2 | Automatizada | 2026-09-22 | 20:45:10 | 21:01:48 | **16:38** | 998 s | Ejecución nominal. Ligera variación en tiempo de respuesta del socket gvmd (16m21s en scan). |
| 3 | Automatizada | 2026-09-23 | 10:15:30 | 10:31:54 | **16:24** | 984 s | Descubrimiento Nmap: 11.75s. Polling de OpenVAS: 16m13s. Persistencia PostgreSQL exitosa. |
| 4 | Automatizada | 2026-09-23 | 11:55:00 | 12:11:31 | **16:31** | 991 s | Ejecución nominal de ciclo completo sin reintentos en nodos de orquestación. |
| 5 | Automatizada | 2026-09-23 | 15:15:20 | 15:31:39 | **16:19** | 979 s | Menor tiempo de escaneo registrado (16m09s). Flujo finalizado con reporte enviado vía SMTP. |

---

### Condición Manual (Operador en CLI con gvm-tools y Nmap)

| N° corrida | Condición | Fecha | t_inicio | t_fin_descubrimiento | t_inicio_analisis | t_fin_analisis | t_fin | Duración total (min:seg) | Duración (seg) | Observaciones |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | Manual | 2026-09-20 | 15:14:10 | 15:19:42 | 15:24:15 | 15:43:08 | 16:01:25 | **47:15** | 2835 s | Primera corrida de control. Mayor latencia en inspección visual de Nmap y tabulación manual de hallazgos. |
| 2 | Manual | 2026-09-22 | 19:40:05 | 19:44:50 | 19:49:12 | 20:08:24 | 20:25:38 | **45:33** | 2733 s | Parámetros transferidos manualmente a gvm-tools. Espera de polling en CLI y extracción manual de resultados. |
| 3 | Manual | 2026-09-22 | 21:20:00 | 21:24:20 | 21:28:15 | 21:47:35 | 22:04:12 | **44:12** | 2652 s | Leve ganancia de agilidad del operador en armado de comandos GMP. Tabulación de 90 hallazgos brutos. |
| 4 | Manual | 2026-09-23 | 10:50:15 | 10:54:10 | 10:58:00 | 11:17:10 | 11:33:55 | **43:40** | 2620 s | Ejecución sin fallos. El tiempo de escaneo activo se mantiene constante; tiempo humano en tabulación: ~16m45s. |
| 5 | Manual | 2026-09-23 | 14:10:00 | 14:13:50 | 14:17:30 | 14:36:45 | 14:52:48 | **42:48** | 2568 s | Procedimiento consolidado por el operador. Mayor velocidad en filtrado manual de falsos positivos y logs. |

---

### Análisis Estadístico Comparativo

| Métrica Estadística | Condición Manual | Condición Automatizada | Diferencia Absoluta | Reducción Relativa (%) |
|:---|:---:|:---:|:---:|:---:|
| **Corrida 1** | 47m 15s (2835 s) | 16m 27s (987 s) | -30m 48s (-1848 s) | -65.19% |
| **Corrida 2** | 45m 33s (2733 s) | 16m 38s (998 s) | -28m 55s (-1735 s) | -63.48% |
| **Corrida 3** | 44m 12s (2652 s) | 16m 24s (984 s) | -27m 48s (-1668 s) | -62.90% |
| **Corrida 4** | 43m 40s (2620 s) | 16m 31s (991 s) | -27m 09s (-1629 s) | -62.18% |
| **Corrida 5** | 42m 48s (2568 s) | 16m 19s (979 s) | -26m 29s (-1589 s) | -61.88% |
| **Promedio ($\bar{x}$)** | **44m 42s (2681.6 s)** | **16m 28s (987.8 s)** | **-28m 14s (-1693.8 s)** | **-63.16%** |
| **Desviación Estándar ($s$)** | **1m 45s (104.58 s)** | **0m 07s (7.19 s)** | — | — |
| **Tiempo Mínimo** | 42m 48s (2568 s) | 16m 19s (979 s) | — | — |
| **Tiempo Máximo** | 47m 15s (2835 s) | 16m 38s (998 s) | — | — |

$$\text{Reducción Porcentual Promedio} = \left(1 - \frac{987.8}{2681.6}\right) \times 100 = \mathbf{63.16\%}$$

---

### Desglose Comparativo de Etapas Temporales (Promedio de las 5 Corridas)

| Fase del Proceso | Descripción Técnica | Condición Manual (Promedio) | Condición Automatizada (Promedio) | Impacto de la Automatización |
|:---|:---|:---:|:---:|:---|
| **Fase 1: Descubrimiento** | Ejecución de Nmap (`-sV -sC`), parseo de XML e identificación de activos UP. | 4m 24s (264 s) | 11.9s (0.2m) | Reducción del **95.5%** en latencia de descubrimiento. |
| **Fase 2: Orquestación y Target** | Creación de Port List dinámica en OpenVAS, creación de Target y configuración de Task. | 4m 07s (247 s) | 1.8s | Eliminación total de fricción de parametrización manual (**99.3%** reducción). |
| **Fase 3: Escaneo de Vulnerabilidades** | Ejecución del perfil `Full and fast` con polling periódico sobre socket GMP. | 19m 14s (1154 s) | 16m 15s (975 s) | Reducción de **15.5%** por el uso de Port List dinámica acotada (`T:21,22,80`). |
| **Fase 4: Consolidación y Reporte** | Parseo de reporte XML, persistencia en PostgreSQL y despacho de correo con métricas. | 16m 57s (1017 s) | 2.3s | Erradicación del cuello de botella de tabulación manual (**99.8%** reducción). |
| **Total General** | **Ciclo de evaluación completo de extremo a extremo** | **44m 42s (2682 s)** | **16m 28s (988 s)** | **Ahorro neto de 28m 14s por ciclo (-63.16%)** |

---

### Observaciones Metodológicas y Discusión de Tiempos (§3.5.1 y §5.1)

1. **Eliminación de Tareas de Bajo Valor**: En la condición manual, el operador dedica en promedio 25 minutos y 28 segundos (Fases 1, 2 y 4) a tareas estrictamente mecánicas y repetitivas: volcar IPs de Nmap a OpenVAS, monitorear la CLI, abrir el archivo XML, transcribir hallazgos a planillas y formatear un correo de resumen. En la condición automatizada, n8n ejecuta estas tres fases en tan solo **16 segundos acumulados**, liberando el 100% de la atención del analista para la fase de análisis estratégico.
2. **Alta Repetibilidad y Baja Varianza**: La condición automatizada presenta una desviación estándar de apenas **7.19 segundos** frente a los **104.58 segundos** del procedimiento manual. Esta consistencia garantiza la predictibilidad de las ventanas de mantenimiento y evaluación en entornos operativos institucionales.
3. **Comportamiento del Efecto de Aprendizaje**: En la condición manual se constató una reducción progresiva entre la primera corrida (47m 15s) y la quinta corrida (42m 48s), congruente con la familiarización del operador documentada como amenaza a la validez interna en §3.6.1. La intercalación alternada de corridas permitió comprobar que, aun con el operador en su punto de máxima eficiencia operativa (corrida 5), la orquestación automatizada sigue superándolo ampliamente, registrando un ahorro superior al 61.8%.
