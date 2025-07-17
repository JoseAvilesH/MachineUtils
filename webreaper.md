# webreaper

`webreaper` es una herramienta de reconocimiento web ofensivo escrita en Python. Automatiza tareas de enumeración sobre un objetivo web utilizando `WhatWeb` para fingerprinting de tecnologías y `Gobuster` para descubrir rutas ocultas en el servidor.

## Funcionalidad

- Verifica si el objetivo responde por HTTP o HTTPS.
- Identifica tecnologías, servidor web, ubicación, título, y otros metadatos con `WhatWeb`.
- Escanea directorios y archivos con extensiones comunes (`php`, `html`, `txt`) mediante `Gobuster`.
- Muestra y guarda un resumen en un archivo de texto.
- Salida en consola con formato usando `rich`.

## Uso

```bash
python3 webreaper.py <IP_o_dominio>
