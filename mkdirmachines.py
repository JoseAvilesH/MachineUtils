#!/usr/bin/env python3
import os
from rich.console import Console

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
[bold green]mkdirmachines[/bold green] - [italic]Creador de estructura de carpetas para máquinas objetivo[/italic]
[bold yellow]Autor: MrMoore[/bold yellow]
""")

def crear_estructura_carpetas():
    nombre_principal = input("[+] Introduce el nombre de la máquina o carpeta principal: ").strip()

    # Si la carpeta principal ya existe, salir con advertencia
    if os.path.exists(nombre_principal):
        console.print(f"[red][-] La carpeta [bold]{nombre_principal}[/bold] ya existe. Abortando para evitar sobreescritura.[/red]")
        return

    subcarpetas = ['scripts', 'data', 'scaneo']

    try:
        for sub in subcarpetas:
            ruta = os.path.join(nombre_principal, sub)
            os.makedirs(ruta)
            console.print(f"[green][+][/green] Carpeta creada: [cyan]{ruta}[/cyan]")

        console.print("\n[bold green][✔] Estructura de carpetas generada correctamente.[/bold green]")

    except Exception as e:
        console.print(f"[red][-] Error al crear carpetas:[/red] {e}")

if __name__ == "__main__":
    banner()
    crear_estructura_carpetas()
