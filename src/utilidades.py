import subprocess
import os

def ejecutar(comando, path='.'):
    return subprocess.check_output(comando.split(), cwd=path).rstrip().decode('utf-8')

def branch(path):
    return ejecutar('git rev-parse --abbrev-ref HEAD', path)

def cantidad_de_cambios_remotos_no_sincronizados(path, branch):
    comando = 'git rev-list HEAD...origin/{} --count'.format(branch)
    return int(ejecutar(comando, path))

def listar_directorios_git(path):

    def es_working_dir(x):
        return os.path.isdir(x) and os.path.exists("{}/.git".format(x))

    archivos = os.listdir(path)
    archivos = [os.path.join(path, x) for x in archivos]
    directorios = [os.path.abspath(x) for x in archivos if es_working_dir(x)]

    return directorios

def obtener_cambios_sin_commits(path):
    return len([x for x in ejecutar('git status --short', path).split('\n') if x])

def obtener_nombre(path):
    return os.path.basename(path)
