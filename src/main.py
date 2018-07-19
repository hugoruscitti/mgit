from colorama import Fore, Back, Style
from tabulate import tabulate
from yaspin import yaspin
from yaspin.spinners import Spinners

import sys
import utilidades

path = sys.argv[-1]

def main():
	repositorios = utilidades.listar_directorios_git(path)
	print("")

	items = []

	with yaspin(Spinners.arc, text="Consultando repositorios", color="blue") as spinner:
		for x in repositorios:
			branch = utilidades.branch(x)
			nombre = utilidades.obtener_nombre(x)
			cambios = utilidades.cantidad_de_cambios_remotos_no_sincronizados(x, branch)
			cambios_sin_commits = utilidades.obtener_cambios_sin_commits(x)

			if cambios > 0:
				estado_remoto = f'{Fore.YELLOW}↧ requiere pull{Style.RESET_ALL}'
			else:
				estado_remoto = f'{Fore.GREEN}✓ remoto{Style.RESET_ALL}'

			if cambios_sin_commits > 0:
				estado_local = f'{Fore.RED}↺ local{Style.RESET_ALL}'
			else:
				estado_local = f'{Fore.GREEN}✓ local{Style.RESET_ALL}'


			items.append([nombre, estado_remoto, estado_local, branch])
			#print(" {} \t\t {} {} \t [{}]".format(nombre, estado_remoto, estado_local, branch))


	print(tabulate(items, headers=['Repositorio', 'Estado Remoto', 'Estado Local', 'Branch']))
	print("")


if __name__ == '__main__':
	main()
