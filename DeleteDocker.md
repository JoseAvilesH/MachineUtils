# deletedocker

`deletedocker` es una herramienta en Python que realiza una limpieza total del entorno Docker en tu sistema, eliminando contenedores, imágenes, volúmenes y redes no utilizadas.

## Funcionalidad

- Verifica si Docker está instalado y funcionando correctamente.
- Elimina todos los contenedores detenidos.
- Detiene y elimina contenedores en ejecución.
- Elimina imágenes no utilizadas.
- Elimina volúmenes y redes huérfanas.
- Muestra el proceso con mensajes claros usando `rich`.

## Uso

```bash
python3 deletedocker.py
