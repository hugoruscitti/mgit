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

	with yaspin(Spinners.arc, text="Consultando repositorios", color="blue") as spinner:
		procesos = []
		return_codes = []

		for x in repositorios:
			proceso = utilidades.async_sincronizar(x)
			procesos.append(proceso)

		for proceso in procesos:
			return_codes.append(proceso.wait())

		for (indice, x) in enumerate(repositorios):
			branch = utilidades.branch(x)
			nombre = utilidades.obtener_nombre(x)
			descripcion_tag = '-'

			try:
				if return_codes[indice] > 0:
					estado_remoto = f'{Fore.RED}⊗ error{Style.RESET_ALL}'
					estado_local = f'{Fore.RED}⊗ error{Style.RESET_ALL}'
				else:
					cambios = utilidades.cantidad_de_cambios_remotos_no_sincronizados(x, branch)
					cambios_sin_commits = utilidades.obtener_cambios_sin_commits(x)

					try:
						tag = utilidades.obtener_ultimo_tag(x)
						cantidad = utilidades.obtener_commits_desde_el_tag(x, tag)

						if cantidad > 0:
							descripcion_tag = f'{Fore.YELLOW}' + "{} - {} ↺".format(tag, cantidad) + f'{Style.RESET_ALL}'
						else:
							descripcion_tag = f'{Fore.GREEN}' + '{} ✓'.format(tag) + f'{Style.RESET_ALL}'

					except subprocess.CalledProcessError:
						tag = ""

					if cambios > 0:

						if 'pull' in sys.argv:
							estado_remoto = f'{Fore.YELLOW}✓{Style.RESET_ALL}'
							utilidades.realizar_pull(x, branch)
						else:
							estado_remoto = f'{Fore.RED}↺ remotor{Style.RESET_ALL}'
					else:
						estado_remoto = f'{Fore.GREEN}✓ remoto{Style.RESET_ALL}'

					if cambios_sin_commits > 0:
						estado_local = f'{Fore.RED}↺ local{Style.RESET_ALL}'
					else:
						estado_local = f'{Fore.GREEN}✓ local{Style.RESET_ALL}'

			except subprocess.CalledProcessError:
				estado_remoto = f'{Fore.RED}⊗ error{Style.RESET_ALL}'
				estado_local = f'{Fore.RED}⊗ error{Style.RESET_ALL}'


			if len(nombre) > LIMITE:
				nombre = nombre[:LIMITE-3] + "..."

			items.append([nombre, estado_remoto, estado_local, branch, descripcion_tag])


	print(tabulate(items, headers=['Repositorio', 'Remoto', 'Local', 'Branch', 'Último tag']))
	print("")


if __name__ == '__main__':
	main()
