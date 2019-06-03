from colorama import Fore, Back, Style
from tabulate import tabulate
from yaspin import yaspin
from yaspin.spinners import Spinners
import subprocess

import sys
import utilidades

path = sys.argv[1]

# Limite del nombre de repositorio
LIMITE = 20

def main():
	repositorios = utilidades.listar_directorios_git(path)
	print("")

	items = []

	if len(sys.argv) > 2:
		filtro = sys.argv[2]
		mensaje = "Consultando repositorios con el filtro {} ...".format(filtro)
		repositorios = [r for r in repositorios if filtro in r]
	else:
		filtro = None
		mensaje = f"Consultando {len(repositorios)} repositorios"

	with yaspin(Spinners.arc, text=mensaje + "...", color="blue") as spinner:
		procesos = []
		return_codes = []

		for x in repositorios:
			proceso = utilidades.async_sincronizar(x)
			procesos.append(proceso)

		total = len(repositorios)

		for proceso in procesos:
			return_codes.append(proceso.wait())
			spinner.text = f"{mensaje} {len(return_codes)}/{total} ..."

		for (indice, x) in enumerate(repositorios):
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
						estado_remoto = f'{Fore.YELLOW}✓ realizó pull {Style.RESET_ALL}'
						utilidades.realizar_pull(x, branch)
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
