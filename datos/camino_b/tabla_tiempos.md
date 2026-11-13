# Tabla de Tiempos y Rendimiento — Réplica Pareada «Camino B» (TASTSERV)

**Fecha de Ejecución**: 12 de Noviembre de 2026  
**Operador**: Tiziano Roig  
**Entorno**: Monomáquina física (`vbox`), OpenVAS / Greenbone Community Containers, Nmap 7.95, n8n 1.70.0  
**Archivo de Datos CSV**: [`datos/camino_b/ensayo/tiempos_replica_camino_b.csv`](file:///home/tizi/n8n-stack/datos/camino_b/ensayo/tiempos_replica_camino_b.csv)

---

## 1. Tabla Cronológica Pareada y Alternada (10 Corridas)

| Par | Corrida | Condición | Inicio (UTC) | Fin (UTC) | $T_{\text{Nmap}}$ | $T_{\text{escaneo}}$ (gvmd puro) | $T_{\text{medido}}$ (Total) | $T_{\text{flujo}}$ (Ciclo n8n + DB) | Ahorro Pareado vs Manual (Segundos) | Ahorro Pareado vs Manual (%) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Par 1** | **$M_1$** | Manual | 18:18:33 | 18:42:41 | 13.2 s | 24m 08s (1.448 s) | **24m 08s** (1.448 s) | *No aplica* | *Base Par 1* | *Base Par 1* |
| **Par 1** | **$A_1$** | Automatizada | 18:53:49 | 19:14:02 | *Integrado* | 20m 12s (1.212 s) | **20m 12s** (1.212 s) | **20m 19s** (1.219 s) | **-235.5 s** (-3m 56s) | **-16.3 %** |
| **Par 2** | **$M_2$** | Manual | 19:27:44 | 19:46:04 | 12.5 s | 18m 20s (1.100 s) | **18m 20s** (1.100 s) | *No aplica* | *Base Par 2* | *Base Par 2* |
| **Par 2** | **$A_2$** | Automatizada | 19:50:18 | 20:09:08 | *Integrado* | 18m 50s (1.130 s) | **18m 50s** (1.130 s) | **19m 02s** (1.142 s) | **+29.7 s** (+30s) | **+2.7 %** |
| **Par 3** | **$M_3$** | Manual | 20:17:23 | 20:40:50 | 12.2 s | 23m 27s (1.407 s) | **23m 27s** (1.407 s) | 23m 35s (1.415 s) | *Base Par 3* | *Base Par 3* |
| **Par 3** | **$A_3$** | Automatizada | 20:45:38 | 21:02:34 | *Integrado* | 16m 55s (1.015 s) | **16m 55s** (1.015 s) | **17m 00s** (1.020 s) | **-391.5 s** (-6m 32s) | **-27.8 %** |
| **Par 4** | **$M_4$** | Manual | 21:19:37 | 21:46:47 | 12.2 s | 17m 40s (1.060 s) | **27m 09s** (1.629 s)* | 27m 15s (1.635 s) | *Base Par 4* | *Base Par 4* |
| **Par 4** | **$A_4$** | Automatizada | 21:50:35 | 22:14:18 | *Integrado* | 23m 42s (1.422 s) | **23m 42s** (1.422 s) | **24m 00s** (1.440 s) | **-206.8 s** (-3m 27s) | **-12.7 %** |
| **Par 5** | **$M_5$** | Manual | 22:31:46 | 23:02:24 | 139.3 s | 27m 19s (1.639 s) | **30m 37s** (1.837 s)* | 30m 37s (1.837 s) | *Base Par 5* | *Base Par 5* |
| **Par 5** | **$A_5$** | Automatizada | 23:38:54 | 23:56:25 | *Integrado* | 17m 31s (1.051 s) | **17m 31s** (1.051 s)** | **17m 51s** (1.071 s) | **-786.4 s** (-13m 06s) | **-42.8 %** |

---

### Notas Metodológicas de las Corridas $M_4$, $M_5$ y $A_5$

- **\*Intervalo de Operación Humana en Manuales ($M_4$ y $M_5$)**:
  - En **$M_4$**, el escaneo puro del motor OpenVAS en gvmd tomó **17m 40s (1.060 s)** (18m 09s desde lanzamiento del script). El total registrado de 27m 09s incluye el intervalo humano de inspección del reporte Nmap previo al lanzamiento. Comparando el escaneo puro de $M_4$ (17m 40s) frente a $A_4$ (23m 42s por mayor tiempo en plugins de directory traversal), la variación fue de +333.2 s (+30.6%).
  - En **$M_5$**, el escaneo puro del motor OpenVAS tomó **27m 19s (1.639 s)**. Frente a la corrida limpia de $A_5$ (17m 31s), la automatización ahorró **-9m 48s (-35.9%)** en tiempo de escaneo puro del motor, y **-13m 06s (-42.8%)** frente al tiempo total de la corrida manual.
- **\*\*Incidente y Repetición en Par 5 ($A_5$)**:
  - **Intento 1 de $A_5$ (Afectado por INC-01)**: Inicio `23:08:32 UTC`, Fin `23:26:42 UTC`, Duración `18m 09s (1.089 s)`. Se produjo un reinicio de la máquina anfitriona afectando los servicios y el monitoreo en segundo plano. Los artefactos brutos del intento 1 se preservaron en [`datos/camino_b/automatizada/corrida_5_intento1_reinicio/`](file:///home/tizi/n8n-stack/datos/camino_b/automatizada/corrida_5_intento1_reinicio/).
  - **Repetición Oficial de $A_5$**: Se ejecutó en limpio a las `23:38:54 UTC`, finalizando a las `23:56:25 UTC` (**17m 31s / 1.051 s**).

---

## 2. Comparativa Estadística Global (Manual vs Automatizada)

```
========================================================================================
MÉTRICA TEMPORAL                       CONDICIÓN MANUAL          CONDICIÓN AUTOMATIZADA
========================================================================================
Tiempo Medio de Escaneo (T_medido):    1.484,1 s (24 min 44 s)   1.166,0 s (19 min 26 s)
Desviación Estándar (s):               274,1 s                   162,2 s
Coeficiente de Variación (CV):         18.5 %                    13.9 %
Ahorro Medio de la Automatización:     -318,1 s (-5 min 18 s, -21.4% de reducción promedio)
Máximo Ahorro Pareado Observado:       -786,4 s (-13 min 06 s, -42.8% en Par 5)
========================================================================================
```

---

## 3. Desglose de Fases por Corrida

| Corrida | Fase 1: Descubrimiento Nmap | Fase 2: Escaneo Greenbone (gvmd) | Fase 3: Ingesta DB PostgreSQL (n8n) | Tiempo Total Medido |
|:---:|:---:|:---:|:---:|:---:|
| **$M_1$** | 13.2 s | 24m 08s | *Manual (sin persistencia)* | **24m 08s** |
| **$A_1$** | *Integrado en flujo* | 20m 12s | 6.3 s | **20m 12s** |
| **$M_2$** | 12.5 s | 18m 20s | *Manual (sin persistencia)* | **18m 20s** |
| **$A_2$** | *Integrado en flujo* | 18m 50s | 11.7 s | **18m 50s** |
| **$M_3$** | 12.2 s | 23m 27s | *Manual (sin persistencia)* | **23m 27s** |
| **$A_3$** | *Integrado en flujo* | 16m 55s | 5.3 s | **16m 55s** |
| **$M_4$** | 12.2 s (+ 8m 48s inspección) | 17m 40s | *Manual (sin persistencia)* | **27m 09s** |
| **$A_4$** | *Integrado en flujo* | 23m 42s | 17.4 s | **23m 42s** |
| **$M_5$** | 139.3 s | 27m 19s | *Manual (sin persistencia)* | **30m 37s** |
| **$A_5$** | *Integrado en flujo* | 17m 31s | 20.1 s | **17m 31s** |

---

## 4. Trazabilidad Criptográfica de Archivos de Tiempo

- Manifiesto global: [`datos/camino_b/SHA256SUMS_global.txt`](file:///home/tizi/n8n-stack/datos/camino_b/SHA256SUMS_global.txt)
- Manifiesto de tiempos: [`datos/camino_b/ensayo/tiempos_replica_camino_b.csv`](file:///home/tizi/n8n-stack/datos/camino_b/ensayo/tiempos_replica_camino_b.csv)
- Marcas temporales individuales: `datos/camino_b/{manual,automatizada}/corrida_*/marcas_tiempo.txt`
