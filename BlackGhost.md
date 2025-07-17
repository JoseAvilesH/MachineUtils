# BlackGhost

`BlackGhost` es una herramienta de auditoría automática de red escrita en Python. Utiliza Nmap para detectar hosts activos, identificar puertos abiertos y escanear servicios en máquinas objetivo, mostrando los resultados de forma clara y ordenada.

## Funcionalidad

- Detecta si el host está activo mediante ping.
- Realiza un escaneo completo de todos los puertos (`nmap -p-`).
- Extrae puertos abiertos y realiza un escaneo detallado de servicios (`nmap -sCV`).
- Identifica el sistema operativo probable basándose en el TTL.
- Muestra un resumen claro de servicios, puertos y versiones.
- Incluye opciones de modo silencioso y detallado.
- Interfaz amigable usando la librería `rich`.

## Uso

```bash
python3 blackghost.py <IP> [-v] [-s]
