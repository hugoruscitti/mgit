import subprocess
import os

def ejecutar(comando, path='.'):
    return subprocess.check_output(comando.split(), cwd=path, stderr=subprocess.PIPE).rstrip().decode('utf-8')

def branch(path):
    return ejecutar('git rev-parse --abbrev-ref HEAD', path)

def cantidad_de_cambios_remotos_no_sincronizados(path, branch):
    #ejecutar('git fetch origin', path)
    comando = 'git rev-list HEAD...origin/{} --count'.format(branch)
    return int(ejecutar(comando, path))

def obtener_ultimo_tag(path):
    comando = 'git describe --tags --abbrev=0'
    return ejecutar(comando, path)

def obtener_commits_desde_el_tag(path, tag):
    comando = 'git log {}..HEAD --oneline'.format(tag)
    cambios = ejecutar(comando, path).split('\n')

    if cambios != ['']:
        return len(cambios)
    else:
        return 0

def async_sincronizar(path):
    p = subprocess.Popen(['git', 'fetch', 'origin'], cwd=path, stderr=subprocess.PIPE)
    return p

def realizar_pull_y_push(path, branch):
    comando = 'git pull origin {}'.format(branch)
    ejecutar(comando, path)

    comando = 'git push origin {}'.format(branch)
    return ejecutar(comando, path)

def listar_directorios_git(path):

    def es_working_dir(x):
        return os.path.isdir(x) and os.path.exists("{}/.git".format(x))

    archivos = os.listdir(path)
    archivos = [os.path.join(path, x) for x in archivos]
    directorios = [os.path.abspath(x) for x in archivos if es_working_dir(x)]

    directorios.sort()

    return directorios

def obtener_cambios_sin_commits(path):
    return len([x for x in ejecutar('git status --short', path).split('\n') if x])

def obtener_nombre(path):
    return os.path.basename(path)
