#!/usr/bin/env python3

import subprocess
import sys
import re
from rich import print
from rich.console import Console
from datetime import datetime

console = Console()

def banner():
    console.print("""
[bold cyan]
      |    |
     )_)  )_)
    )___))___)
   )____)_____)
  _____|____|____
\\______________/
 ~~~~~~~~~~~~~~~
[/bold cyan]
[bold green]webreaper[/bold green] - [italic]Reconocimiento Web Ofensivo Automatizado[/italic]
[bold yellow]Autor: MrMoore[/bold yellow]
""")


def ejecutar_comando(comando, titulo=None, filtrar=None):
    if titulo:
        console.print(f"\n[bold cyan][*] {titulo}[/bold cyan]")
    resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    salida = resultado.stdout
    if filtrar:
        return "\n".join([l for l in salida.splitlines() if filtrar(l)])
    return salida.strip()


def verificar_url(ip):
    test_http = f"curl -s --connect-timeout 3 -o /dev/null -w '%{{http_code}}' http://{ip}"
    http_code = subprocess.getoutput(test_http)
    if http_code.startswith("2") or http_code.startswith("3"):
        return f"http://{ip}"

    test_https = f"curl -sk --connect-timeout 3 -o /dev/null -w '%{{http_code}}' https://{ip}"
    https_code = subprocess.getoutput(test_https)
    if https_code.startswith("2") or https_code.startswith("3"):
        return f"https://{ip}"

    return None


def ejecutar_whatweb(url):
    comando = f"whatweb --no-color {url}"
    salida_raw = ejecutar_comando(comando, f"Fingerprint con WhatWeb ({url})")
    return parsear_whatweb(salida_raw)


def parsear_whatweb(salida_raw):
    if not salida_raw:
        return "WhatWeb no devolvió resultados."

    parsed = {}
    partes = salida_raw.split(" ", 1)
    parsed["URL"] = partes[0].strip() if partes else "N/A"

    if len(partes) > 1:
        plugins = partes[1].split(", ")
        for p in plugins:
            if "[" in p:
                nombre, valor = p.split("[", 1)
                parsed[nombre.strip()] = valor.strip("[]")
            else:
                parsed[p.strip()] = "Sí"

    resumen = f"URL: {parsed.get('URL', 'N/A')}\n"
    if "Title" in parsed:
        resumen += f"Título: {parsed['Title']}\n"
    if "HTTPServer" in parsed:
        resumen += f"Servidor Web: {parsed['HTTPServer']}\n"
    if "Apache" in parsed:
        resumen += f"Apache: {parsed['Apache']}\n"
    if "Country" in parsed:
        resumen += f"Ubicación IP: {parsed['Country']}\n"
    if "Email" in parsed:
        resumen += f"Contacto: {parsed['Email']}\n"
    if "HTML5" in parsed:
        resumen += f"Tecnologías detectadas: HTML5\n"

    return resumen.strip()


def ejecutar_gobuster(url):
    wordlist = "/usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt"
    exts = "php,txt,html"
    threads = 50
    comando = f"gobuster dir -u {url} -w {wordlist} -t {threads} -x {exts} -q"
    raw = ejecutar_comando(comando, f"Escaneo de rutas con Gobuster ({url})")
    
    rutas = []
    for linea in raw.splitlines():
        match = re.search(r'(/[\S]*)\s+\(Status:\s*(\d+)', linea)
        if match:
            path, status = match.group(1), match.group(2)
            rutas.append(f"{path.ljust(12)} (Status: {status})")
    return "\n".join(rutas)


def guardar_resumen_txt(ip, resumen_txt):
    archivo = f"webreaper_report_{ip.replace('.', '_')}.txt"
    with open(archivo, 'w') as f:
        f.write(resumen_txt)
    console.print(f"\n[green][✔] Resumen guardado en:[/green] [bold]{archivo}[/bold]")


def main():
    banner()

    if len(sys.argv) != 2:
        print("Uso: webreaper <IP_o_dominio>")
        sys.exit(1)

    objetivo = sys.argv[1]
    url = verificar_url(objetivo)

    if not url:
        console.print(f"[red]No se pudo conectar por HTTP ni HTTPS a {objetivo}. Abortando.[/red]")
        sys.exit(1)

    fingerprint = ejecutar_whatweb(url)
    rutas = ejecutar_gobuster(url)

    resumen_txt = f"""=== RESUMEN DE ESCANEO WEB ===
Fecha/Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Objetivo: {objetivo}

--- WhatWeb ---
{fingerprint}

--- Rutas encontradas por Gobuster ---
{rutas.strip()}
"""

    # Mostrar y guardar
    console.print("\n[bold green]=== RESUMEN FINAL ===[/bold green]")
    console.print(resumen_txt)
    guardar_resumen_txt(objetivo, resumen_txt)


if __name__ == "__main__":
    main()
