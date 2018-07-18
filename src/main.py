from colorama import Fore, Back, Style

import sys
import utilidades

path = sys.argv[-1]

def main():
	repositorios = utilidades.listar_directorios_git(path)
	print("")

	for x in repositorios:
		branch = utilidades.branch(x)
		nombre = utilidades.obtener_nombre(x)
		cambios = utilidades.cantidad_de_cambios_remotos_no_sincronizados(x)
		cambios_sin_commits = utilidades.obtener_cambios_sin_commits(x)

		if cambios > 0:
			estado_remoto = f'{Fore.YELLOW}↧ pull pendiente{Style.RESET_ALL}'
		else:
			estado_remoto = f'{Fore.GREEN}✓ remoto sincronizado {Style.RESET_ALL}'

		if cambios_sin_commits > 0:
			estado_local = f'{Fore.RED}↺ local sin sincronizar{Style.RESET_ALL}'
		else:
			estado_local = f'{Fore.GREEN}✓ local sincronizado{Style.RESET_ALL}'


		print(" {} \t\t {} {} \t [{}]".format(nombre, estado_remoto, estado_local, branch))

	print("")


if __name__ == '__main__':
	main()
