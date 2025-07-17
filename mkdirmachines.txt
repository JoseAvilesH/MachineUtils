# mkdirmachines

`mkdirmachines` es una herramienta en Python que genera automáticamente una estructura de carpetas organizada para máquinas objetivo en ejercicios de pentesting o laboratorios.

## Funcionalidad

- Solicita al usuario el nombre de la carpeta principal.
- Crea tres subcarpetas dentro de ella: `scripts`, `data` y `scaneo`.
- Verifica si la carpeta principal ya existe para evitar sobreescritura.
- Muestra mensajes en consola con formato de colores usando la librería `rich`.

## Uso

```bash
python3 mkdirmachines.py
