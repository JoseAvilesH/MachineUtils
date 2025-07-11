#!/usr/bin/env python3
import subprocess
import sys
import shutil
from rich.console import Console

console = Console()

def banner():
    console.print("""
[bold green]
       _______
      /       \\
     /  R.I.P  \\
    /___________\\
    ||         ||
    ||  Docker ||
    ||         ||
    ||         ||
    ||_________||
    |___________|
[/bold green]
[bold cyan]deletedocker[/bold cyan] - [italic]Limpieza total de Docker[/italic]
[bold yellow]Autor: MrPython[/bold yellow]
""")

def verificar_docker():
    if not shutil.which("docker"):
        console.print("[bold red][!] Docker no está instalado o no está en el PATH.[/bold red]")
        sys.exit(1)
    try:
        subprocess.run("docker info", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        console.print("[bold red][!] Docker está instalado pero el daemon no se está ejecutando o no tienes permisos.[/bold red]")
        sys.exit(1)

def ejecutar_comando(comando, mostrar=True):
    try:
        resultado = subprocess.run(comando, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")
        if mostrar and resultado.stdout.strip():
            console.print(f"[bold green]{resultado.stdout.strip()}[/bold green]")
    except subprocess.CalledProcessError as e:
        if e.stderr.strip():
            console.print(f"[bold red][!] Error ejecutando: {comando}[/bold red]\n{e.stderr.strip()}")

def limpiar_contenedores():
    console.print("[cyan][*] Eliminando contenedores detenidos...[/cyan]")
    ejecutar_comando("docker container prune -f")

    console.print("[cyan][*] Deteniendo contenedores en ejecución (si hay)...[/cyan]")
    contenedores = subprocess.getoutput("docker ps -q")
    if contenedores:
        ejecutar_comando("docker stop $(docker ps -q)")
        console.print("[cyan][*] Eliminando todos los contenedores...[/cyan]")
        ejecutar_comando("docker rm $(docker ps -a -q)")
    else:
        console.print("[green][✓] No hay contenedores en ejecución.[/green]")

def limpiar_imagenes():
    console.print("[cyan][*] Eliminando imágenes sin uso...[/cyan]")
    ejecutar_comando("docker image prune -a -f")

def limpiar_volumenes():
    console.print("[cyan][*] Eliminando volúmenes no utilizados...[/cyan]")
    ejecutar_comando("docker volume prune -f")

def limpiar_redes():
    console.print("[cyan][*] Eliminando redes no utilizadas...[/cyan]")
    ejecutar_comando("docker network prune -f")

def limpieza_completa():
    banner()
    console.print("[bold blue][+] Verificando entorno Docker...[/bold blue]")
    verificar_docker()
    console.print("[bold blue][+] Iniciando limpieza completa de Docker...[/bold blue]")
    limpiar_contenedores()
    limpiar_imagenes()
    limpiar_volumenes()
    limpiar_redes()
    console.print("[bold green][✓] Limpieza de Docker finalizada.[/bold green]")

if __name__ == "__main__":
    limpieza_completa()
