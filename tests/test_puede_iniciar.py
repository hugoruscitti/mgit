import sys
sys.path.insert(0, '.')

from src import utilidades

def test_sumar():
	assert 2+2 == 4

def test_puede_invocar_comandos():
	salida = utilidades.ejecutar('ls')
	assert salida

	branch = utilidades.branch('.')
	assert branch == "master"

	cambios = utilidades.cantidad_de_cambios_remotos_no_sincronizados('.')
	assert cambios == 0
