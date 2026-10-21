# Respuesta 1 — Línea `sed` inválida en el Dockerfile de vuln-srv2

## Línea en cuestión

```dockerfile
# Línea 25 del Dockerfile original
RUN sed -i 's/<Directory \/>/,+4 s/Require all denied/Require all granted/' /usr/local/apache2/conf/httpd.conf || true && \
    echo '<Directory "/">\n    AllowOverride none\n    Require all granted\n</Directory>' >> /usr/local/apache2/conf/httpd.conf
```

## Análisis técnico

La sintaxis `s/<Directory \/>/,+4 s/Require all denied/Require all granted/` es **inválida** para una invocación de `sed -i` con un solo patrón. Presenta los siguientes problemas:

1. **Mezcla de sintaxis**: combina un address range de `sed` interactivo (`,+4`, que significa "desde el match hasta 4 líneas después") con un comando `s/` de reemplazo, todo dentro de una sola expresión `s/`.
2. **El patrón `s/` espera tres campos**: `s/patrón/reemplazo/flags`. Acá el "reemplazo" contiene otro `s/`, lo cual lo convierte en una sustitución literal sin sentido.
3. **El `|| true` confirma que falla**: quien lo escribió sabía que el comando podía fallar, y agregó `|| true` para que el build de Docker no se detuviera. Esto significa que la línea es un **no-op silencioso** — nunca modifica el archivo.

## ¿Qué habilita realmente la vulnerabilidad?

La vulnerabilidad de **Path Traversal (CVE-2021-41773)** se habilita con la **segunda parte** del comando, que sí es válida:

```dockerfile
echo '<Directory "/">\n    AllowOverride none\n    Require all granted\n</Directory>' >> /usr/local/apache2/conf/httpd.conf
```

Este `echo` agrega un bloque `<Directory "/">` con `Require all granted` al final del `httpd.conf`, permitiendo el acceso sin restricciones al filesystem raíz a través de Apache 2.4.49, que es el requisito para explotar CVE-2021-41773.

## Decisión

**Se recomienda eliminar la línea del `sed`** por los siguientes motivos:

- No aporta ninguna funcionalidad (es un no-op).
- Puede generar una pregunta incómoda durante la defensa oral si alguien la lee con atención.
- La vulnerabilidad queda igualmente habilitada por el `echo` que le sigue.
- Mantenerla "por fidelidad" no agrega valor, porque lo que realmente corrieron fue el `echo`, no el `sed`.

## Dockerfile corregido

Se adjunta en esta misma carpeta como `Dockerfile.corregido`. Los cambios son:

```diff
 # Configurar Apache httpd.conf:
 # 1. Habilitar la vulnerabilidad de Path Traversal CVE-2021-41773 permitiendo acceso en raiz
-RUN sed -i 's/<Directory \/>/,+4 s/Require all denied/Require all granted/' /usr/local/apache2/conf/httpd.conf || true && \
-    echo '<Directory "/">\n    AllowOverride none\n    Require all granted\n</Directory>' >> /usr/local/apache2/conf/httpd.conf
+RUN echo '<Directory "/">\n    AllowOverride none\n    Require all granted\n</Directory>' >> /usr/local/apache2/conf/httpd.conf
```
