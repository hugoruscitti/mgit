from colorama import Fore, Back, Style
from tabulate import tabulate
from yaspin import yaspin
from yaspin.spinners import Spinners
import subprocess
import time
import math

import sys
import utilidades

path = sys.argv[1]

# Limite del nombre de repositorio
LIMITE = 30
CANTIDAD_DE_PROCESOS_EN_PARALELO = 10


def obtener_grupo_de_procesos(procesos, repositorios):
	while len(procesos) < CANTIDAD_DE_PROCESOS_EN_PARALELO:
		if len(repositorios) > 0:
			repositorio = repositorios.pop()
			proceso = utilidades.async_sincronizar(repositorio)
			procesos.append(proceso)
		else:
			return

def obtener_progreso(cantidad, total):
	width = 6
	progress = cantidad / total

	progress = max(progress, 0.04)
    # 0 <= progress <= 1
	progress = min(1, max(0, progress))
	whole_width = math.floor(progress * width)
	remainder_width = (progress * width) % 1
	part_width = math.floor(remainder_width * 8)
	part_char = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉"][part_width]
	if (width - whole_width - 1) < 0:
		part_char = ""
	line = "" + "█" * whole_width + part_char + " " * (width - whole_width - 1) + "▏"
	return line


def main():
	repositorios = utilidades.listar_directorios_git(path)
	print("")

	items = []

	if len(sys.argv) > 2:
		filtro = sys.argv[2]
		mensaje = "Sincronizando repositorios con el filtro {} ".format(filtro)
		repositorios = [r for r in repositorios if filtro in r]
	else:
		filtro = None
		mensaje = f"Sincronizando repositorios"

	with yaspin(Spinners.arc, text=mensaje + "...", color="blue") as spinner:
		procesos = []
		return_codes = []

		total = len(repositorios)
		repositorios_originales = repositorios[:]

		while repositorios:
			obtener_grupo_de_procesos(procesos, repositorios)

			# mientras existan procesos en ejecución:
			while len(procesos) > 0:
				for proceso_en_ejecucion in procesos[:]:

					if proceso_en_ejecucion.poll() is not None:
						# Si un proceso finaliza
						return_codes.append(proceso_en_ejecucion.wait())
						procesos.remove(proceso_en_ejecucion)
						# Intenta volver a cargar el pool de procesos
						obtener_grupo_de_procesos(procesos, repositorios)
						progreso = obtener_progreso(len(return_codes), total)
						spinner.text = f"{mensaje}: {progreso}"
						continue
					else:
						# Si el comando sigue ejecutando, espera para ir al siguiente proceso en ejecución.
						progreso = obtener_progreso(len(return_codes), total)
						spinner.text = f"{mensaje}: {progreso}"
						time.sleep(.1)


		for (indice, x) in enumerate(repositorios_originales):
			nombre = utilidades.obtener_nombre(x)
			descripcion_tag = '-'

			if len(nombre) > LIMITE:
				nombre_corto = nombre[:LIMITE-3] + "..."
			else:
				nombre_corto = nombre

			try:
				branch = utilidades.branch(x)
			except subprocess.CalledProcessError as error:
				error = f'{Fore.RED}⊗ error{Style.RESET_ALL}'
				items.append([nombre_corto, error, error, error, error])
				continue


			try:
				if return_codes[indice] > 0:
					estado_remoto = f'{Fore.RED}⊗ error{Style.RESET_ALL}'
					estado_local = f'{Fore.RED}⊗ error{Style.RESET_ALL}'
				else:
					cambios = utilidades.cantidad_de_cambios_remotos_no_sincronizados(x, branch)
					cambios_sin_commits = utilidades.obtener_cambios_sin_commits(x)

					if cambios > 0:
						estado_remoto = f'{Fore.YELLOW}✓ se sincronizó {Style.RESET_ALL}'
						utilidades.realizar_pull_y_push(x, branch)
					else:
						estado_remoto = f'{Fore.GREEN}✓ sync{Style.RESET_ALL}'

					try:
						tag = utilidades.obtener_ultimo_tag(x)
						cantidad = utilidades.obtener_commits_desde_el_tag(x, tag)

						if cantidad > 0:
							descripcion_tag = f'{Fore.YELLOW}' + "{} - {} ↺".format(tag, cantidad) + f'{Style.RESET_ALL}'
						else:
							descripcion_tag = f'{Fore.GREEN}' + '{} ✓'.format(tag) + f'{Style.RESET_ALL}'

					except subprocess.CalledProcessError:
						tag = ""


					if cambios_sin_commits > 0:
						estado_local = f'{Fore.RED}↺ no sync{Style.RESET_ALL}'
					else:
						estado_local = f'{Fore.GREEN}✓ sync{Style.RESET_ALL}'

			except subprocess.CalledProcessError:
				estado_remoto = f'{Fore.RED}⊗ error{Style.RESET_ALL}'
				estado_local = f'{Fore.RED}⊗ error{Style.RESET_ALL}'

			items.append([nombre_corto, estado_remoto, estado_local, branch, descripcion_tag])


	print(tabulate(items, headers=['Repositorio', 'Remoto', 'Local', 'Branch', 'Último tag']))
	print("")


if __name__ == '__main__':
	main()
