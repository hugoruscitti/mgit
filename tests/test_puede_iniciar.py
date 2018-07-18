import sys

from src import utilidades
from src import main

def test_sumar():
	assert 2+2 == 4

def test_puede_invocar_comandos():
	salida = utilidades.ejecutar('ls')
	assert salida

	branch = utilidades.branch('.')
	assert branch == "master"

	cambios = utilidades.cantidad_de_cambios_remotos_no_sincronizados('.')
	assert cambios == 0

def test_puede_listar_directorios():
	directorios = utilidades.listar_directorios_git('.')

	for x in directorios:
		print(utilidades.obtener_nombre(x))
		print(utilidades.branch(x))
		print(utilidades.cantidad_de_cambios_remotos_no_sincronizados(x))
		print(utilidades.obtener_cambios_sin_commits(x))

def test_puede_obtener_nombre():
	assert utilidades.obtener_nombre('/Users/demo/proyecto') == 'proyecto'

def test_puede_invocar_el_comando_principal():
	main.main()
