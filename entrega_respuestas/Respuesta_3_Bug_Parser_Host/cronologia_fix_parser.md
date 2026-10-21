# Respuesta 3 — Cronología de la corrección del bug del parser del campo `host`

## Contexto del bug

La sección §4.3 de la tesis documenta que:

> "el campo correspondiente al host afectado no se completaba correctamente
> en la totalidad de los hallazgos parseados desde el reporte GMP, debido a
> que la estructura XML de Greenbone anida un elemento adicional (`<asset/>`)
> dentro del tag `<host>`; este comportamiento fue identificado y corregido
> ajustando la expresión regular de extracción"

## Evidencia del fix en el repositorio

### Commit que corrigió el bug

```
Commit:  7f30afa
Fecha:   2026-09-10 20:50:56 +0000
Autor:   TizianoRoig26 <tizianoroig26@hotmail.com>
Mensaje: fix: improve regex host parsing in vulnerability workflow
         and update report structure documentation and template
```

### Cambio realizado (en el nodo "Parse Results" del workflow n8n)

```diff
 // Regex para capturar el host
-const hostMatch = block.match(/<host[^>]*>([^<]*)<\/host>/);
+const hostMatch = block.match(/<host[^>]*>([\s\S]*?)<\/host>/);

 // Extracción del valor
-host: hostMatch ? hostMatch[1] : 'Unknown',
+host: hostMatch ? hostMatch[1].replace(/<[^>]+>/g, '').trim() : 'Unknown',
```

**Explicación del bug:** La regex original `([^<]*)` dejaba de capturar en cuanto
encontraba un `<` dentro del tag `<host>`. Como Greenbone anida un sub-elemento
`<asset>` dentro de `<host>`, el match se cortaba y el campo host quedaba vacío
o incompleto. La corrección usa `([\s\S]*?)` (captura todo, incluyendo tags internos)
y luego un `.replace(/<[^>]+>/g, '')` para stripear los sub-tags y quedarse solo
con la IP.

## Cronología: fix vs. corridas automatizadas

| Evento | Fecha |
|--------|-------|
| **Fix del parser (commit `7f30afa`)** | **2026-09-10** |
| Corrida 1 | 2026-09-20 |
| Corrida 2 | 2026-09-20 |
| Corrida 3 | 2026-09-20 |
| Corrida 4 | 2026-09-22 |
| Corrida 5 | 2026-09-23 |

## Conclusión

### ✅ Escenario (a) confirmado

La corrección del bug del parser se realizó el **10 de septiembre de 2026**,
es decir, **10 días antes** de la primera corrida automatizada (20/09/2026).

Por lo tanto:

- **Las cinco corridas usaron la versión corregida del parser.**
- **El campo `host` se completó correctamente en todas las corridas.**
- **El puntaje 2 de la rúbrica (que exige que coincida el host) es válido
  para las cinco corridas.**
- **No hay corridas ejecutadas con la versión bugueada del parser.**

No es necesario agregar ningún disclaimer ni aclaración sobre corridas
parcialmente afectadas.

## Historial completo de commits (referencia)

```
7f30afa 2026-09-10  fix: improve regex host parsing in vulnerability workflow...
461fa6d 2026-07-02  Poryecto funcionando
8addb52 2026-07-01  Backup/Commit de workflows y credenciales de n8n
5402a7b 2026-03-09  Add author
228a861 2026-03-09  primer commit
```
