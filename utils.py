import logging
import os
from colorama import Fore, Style, init
from dotenv import load_dotenv

# Inicializar colorama
init(strip=False)  # Asegura que los códigos ANSI no se eliminen en macOS

load_dotenv()

DEBUG = int(os.getenv("DEBUG", "0"))  # Ahora manejamos 0, 1, 2

COLORS = {
    logging.DEBUG: Fore.GREEN,
    logging.INFO: Fore.WHITE,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT,
}
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelno, Fore.WHITE)
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

def setup_logger(name: str):
    logger = logging.getLogger(name)
    
    # Configurar nivel según el valor de DEBUG
    if DEBUG == 2:
        logger.setLevel(logging.DEBUG)
    elif DEBUG == 1:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = ColoredFormatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Control exhaustivo de librerías de terceros
    third_party_loggers = [
        'qbittorrentapi',
        'urllib3',
        'requests',
        'urllib3.connectionpool',
        'qbittorrentapi.decorators'
    ]
    
    for lib in third_party_loggers:
        lib_logger = logging.getLogger(lib)
        lib_logger.setLevel(logging.WARNING)
        lib_logger.propagate = False
        for handler in lib_logger.handlers[:]:
            lib_logger.removeHandler(handler)

    return logger

