#!/usr/bin/env python3

import os
import subprocess
import sys
import re
import platform
import argparse

try:
    from rich import print
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("Instalando dependencias necesarias...")
    subprocess.run("pip install rich", shell=True)
    from rich import print
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn

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
[bold green]BlackGhost[/bold green] - [italic]Auditoría Automática de Red[/italic]
[bold yellow]Autor: MrMoore[/bold yellow] 
""")

def parse_args():
    parser = argparse.ArgumentParser(description="BlackGhost - Escáner automático con Nmap")
    parser.add_argument("ip", help="Dirección IP objetivo")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar salida detallada (verbose)")
    parser.add_argument("-s", "--silent", action="store_true", help="Modo silencioso (sin barra de progreso)")
    return parser.parse_args()

def es_host_activo(ip):
    sistema_local = platform.system().lower()
    comando_ping = ['ping', '-c', '1', ip] if sistema_local != "windows" else ['ping', '-n', '1', ip]

    console.print(f"\n[bold cyan][*][/bold cyan] Realizando ping a {ip}...")
    resultado = subprocess.run(comando_ping, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "ttl" in resultado.stdout.lower():
        ttl_match = re.search(r'ttl=(\d+)', resultado.stdout.lower())
        if ttl_match:
            ttl = int(ttl_match.group(1))
            sistema = "Linux/Unix" if ttl <= 64 else "Windows" if ttl <= 128 else "Desconocido"
            console.print(f"[green][+][/green] Host activo. TTL: {ttl} => [bold]{sistema}[/bold]")
            return True, sistema
    console.print("[red][-] Host inactivo o TTL no detectado.[/red]")
    return False, "Desconocido"

def escaneo_puertos(ip, verbose=False, silent=False):
    salida_allports = f"blackghost_{ip}_allPorts.gnmap"
    comando = f"nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn {ip} -oG {salida_allports}"
    
    if verbose:
        console.print(f"[cyan][*][/cyan] Ejecutando: {comando}")
        subprocess.run(comando, shell=True)
    elif silent:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            progress.add_task(description="Escaneando todos los puertos (nmap -p-)...", total=None)
            subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return salida_allports

def extraer_puertos_abiertos(grepable_file):
    if not os.path.exists(grepable_file):
        return ""
    with open(grepable_file, 'r') as file:
        contenido = file.read()
    puertos = re.findall(r'(\d+)/open', contenido)
    puertos_limpios = sorted(set(puertos), key=int)
    return ",".join(puertos_limpios) if puertos_limpios else ""

def escaneo_detallado(ip, puertos, verbose=False, silent=False):
    salida_targeted = f"blackghost_{ip}_targeted.txt"
    comando = f"nmap -sCV -p{puertos} {ip} -oN {salida_targeted}"

    if verbose:
        console.print(f"[cyan][*][/cyan] Ejecutando: {comando}")
        subprocess.run(comando, shell=True)
    elif silent:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            progress.add_task(description=f"Escaneando servicios en puertos: {puertos}", total=None)
            subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return salida_targeted

def parsear_servicios(ruta_escaneo):
    servicios = []
    if ruta_escaneo and os.path.exists(ruta_escaneo):
        with open(ruta_escaneo, 'r') as archivo:
            for linea in archivo:
                if re.match(r"\d+/tcp", linea):
                    partes = linea.strip().split()
                    puerto = partes[0].split("/")[0]
                    estado = partes[1]
                    servicio = partes[2] if len(partes) >= 3 else "desconocido"
                    version = " ".join(partes[3:]) if len(partes) > 3 else "-"
                    servicios.append({
                        "puerto": puerto,
                        "estado": estado,
                        "servicio": servicio,
                        "version": version
                    })
    return servicios

def resumen_final(ip, sistema, puertos, ruta_targeted):
    console.print("\n[bold green][✔] Auditoría completada con éxito[/bold green]")
    console.print("[bold blue]Resumen de escaneo:[/bold blue]")
    console.print(f"   [cyan]IP Objetivo:[/cyan] [bold]{ip}[/bold]")
    console.print(f"   [cyan]Sistema operativo probable:[/cyan] [bold]{sistema}[/bold]")

    if puertos:
        console.print(f"\n[cyan]Puertos abiertos detectados:[/cyan]")
        servicios = parsear_servicios(ruta_targeted)
        for s in servicios:
            console.print(f"   [bold green]{s['puerto']}/tcp[/bold green] - {s['servicio']} [italic yellow]{s['version']}[/italic yellow]")
    else:
        console.print("   [yellow]No se encontraron puertos abiertos[/yellow]")

def main():
    args = parse_args()
    ip = args.ip
    verbose = args.verbose
    silent = args.silent

    if not silent:
        banner()

    activo, sistema = es_host_activo(ip)
    if not activo:
        if not silent:
            console.print("[red]El host no está activo. Abortando.[/red]")
        sys.exit(1)

    archivo_grepable = escaneo_puertos(ip, verbose=verbose, silent=silent)
    puertos = extraer_puertos_abiertos(archivo_grepable)

    if puertos:
        archivo_targeted = escaneo_detallado(ip, puertos, verbose=verbose, silent=silent)
        resumen_final(ip, sistema, puertos, archivo_targeted)
    else:
        if not silent:
            console.print("[yellow][!] No se encontraron puertos abiertos. No se realizará escaneo detallado.[/yellow]")
        resumen_final(ip, sistema, puertos, None)

if __name__ == "__main__":
    main()
