from utils import setup_logger
from logic_seed import manage_torrents
from utils import setup_logger
import os
import time
import subprocess

logger = setup_logger(__name__)

# Función para realizar el movimiento de archivos según antigüedad
def sync_old_files():

    source_dir = os.environ.get('SOURCE_PATH', '/origen')
    dest_dir = os.environ.get('DEST_PATH', '/destino')
    days_threshold = int(os.environ.get('DAYS_THRESHOLD'))
    cache_mount = os.getenv("CACHE_MOUNT")
    prueba_mode = os.getenv("PRUEBA", "0") == "1"
    debug = os.getenv("DEBUG")
    
    # Verificar que los directorios existen
    if not os.path.exists(source_dir):
        logger.error(f"El directorio origen {source_dir} no existe o es inválido")
        raise Exception(f"El directorio origen {source_dir} no existe o es inválido")
    
    if not os.path.exists(dest_dir):
        logger.error(f"El directorio destino {dest_dir} no existe o es inválido")
        raise Exception(f"El directorio destino {dest_dir} no existe o es inválido")

    logger.debug(f"SOURCE_PATH desde entorno: {source_dir}")
    logger.debug(f"DEST_PATH desde entorno: {dest_dir}")
    logger.debug(f"Days old to move: {days_threshold}")
    
    days_threshold_ajustado = days_threshold - 1

    # Preparar el comando find
    find_cmd = ['find', source_dir, '-type', 'f', '-mtime', f'+{days_threshold_ajustado}', '-print0']

    try:
        # Pausar los torrents antes de mover los archivos y guardar la lista
        logger.info("Iniciando pausa de torrents...")
        paused_torrents = manage_torrents("pausar", days_threshold, cache_mount)
        time.sleep(5)

        # Ejecutar el comando find para listar los archivos
        logger.debug(f"Ejecutando comando: {' '.join(find_cmd)}")
        with subprocess.Popen(find_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as find_process:
            find_output, find_error = find_process.communicate()

            if find_process.returncode != 0:
                logger.error(f"Error en find: {find_error.decode()}")
                raise Exception("Error ejecutando find")

            # Filtrar cualquier carácter no válido (por si acaso)
            safe_output = find_output.decode()  # Decodificar la salida de find a texto
            logger.debug(f"Archivos encontrados:\n{'\n'.join(safe_output.strip('\0').split('\0'))}")

            # Eliminar el prefijo /origen de las rutas encontradas
            relative_files = [os.path.relpath(f, source_dir) for f in safe_output.split('\0') if f]

            if not relative_files:
                logger.debug("No hay archivos para mover.")
                return

            # Preparar el comando rsync con progreso
            rsync_cmd = [
                'rsync',
                '-avH',
                '--progress',
                '--files-from=-',
                '--from0',
                '--remove-source-files',
                source_dir + '/',
                dest_dir + '/'
            ]
                # Añadir dry-run si está activado PRUEBA
            if prueba_mode:
                rsync_cmd.insert(1, '--dry-run')
                logger.info("🐞 Modo PRUEBA activado - dry-run")

            try:
                logger.info("Iniciando movimiento de archivos...")
                logger.debug(f"Ejecutando comando rsync: {' '.join(rsync_cmd)}")
                with subprocess.Popen(
                    rsync_cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                ) as rsync_process:
                    # Escribir la lista de archivos en stdin
                    rsync_process.stdin.write("\0".join(relative_files) + "\0")
                    rsync_process.stdin.close()

                    # Leer y loguear cada línea de salida en tiempo real
                    while True:
                        line = rsync_process.stdout.readline()
                        if not line and rsync_process.poll() is not None:
                            break
                        if line:
                            # Solo mostrar el progreso de rsync si DEBUG es 2
                            if debug == "2":
                                logger.debug(f"Progreso rsync: {line.strip()}")

                    # Verificar código de salida
                    if rsync_process.returncode != 0:
                        raise subprocess.CalledProcessError(rsync_process.returncode, rsync_cmd)
                logger.info("Finalizado movimiento de archivos...")    
            except subprocess.CalledProcessError as e:
                logger.error(f"Error en rsync: {str(e)}")
                raise

            # Eliminar directorios vacíos SOLO si no es prueba
            if not prueba_mode:
            # Después de mover los archivos, eliminar los directorios vacíos en origen
                time.sleep(5)
                remove_empty_dirs_cmd = [
                    'find', 
                    source_dir, 
                    '-mindepth', '1',  # <-- Excluir el directorio raíz
                    '-type', 'd', 
                    '-empty', 
                    '-delete'
                ]
                logger.info("Eliminando directorios vacíos...")
                logger.debug(f"Ejecutando comando para eliminar directorios vacíos: {' '.join(remove_empty_dirs_cmd)}")
                subprocess.run(remove_empty_dirs_cmd, check=True)
            else:
                logger.info("🐞 Modo PRUEBA: Saltando eliminación de directorios")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error en rsync: {e.stderr}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        raise
    finally:
        logger.info("Resumiendo torrents pausados...")
        time.sleep(5)
        manage_torrents("resumir", days_threshold, cache_mount, specific_torrents=paused_torrents)
    
    logger.info("Proceso finalizado. Esperando la siguiente programación...")

if __name__ == "__main__":
    sync_old_files()