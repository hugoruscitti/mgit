import subprocess

def ejecutar(comando, path='.'):
    return subprocess.check_output(comando.split(), cwd=path).rstrip().decode('utf-8')

def branch(path):
    return ejecutar('git rev-parse --abbrev-ref HEAD', path)

def cantidad_de_cambios_remotos_no_sincronizados(path):
    return int(ejecutar('git rev-list HEAD...origin/master --count', path))
