from datetime import datetime, timedelta
import os
from utils import setup_logger

# Configurar el logger
logger = setup_logger(__name__)

from qbittorrentapi import Client as QbittorrentClient

def connect_qbittorrent():
    host = os.getenv("QBITTORRENT_HOST")
    user = os.getenv("QBITTORRENT_USER")
    password = os.getenv("QBITTORRENT_PASSWORD")
    
    client = QbittorrentClient(host=host, username=user, password=password)
    try:
        client.auth_log_in()
        logger.debug("Conexión exitosa con qBittorrent")
        return client
    except Exception as e:
        logger.error(f"Error conectando a qBittorrent: {str(e)}")
        raise

def calculate_time_offsets(days_threshold):
    # Convertir a entero primero
    days = int(days_threshold)
    now = datetime.now().timestamp()
    days_from = now - (days * 86400)
    days_to = days_from - 86400
    return days_from, days_to

def manage_torrents(action, days_threshold, cache_mount=None):
    client = connect_qbittorrent()
    days_from, days_to = calculate_time_offsets(days_threshold)
    
    torrents = client.torrents_info(sort='added_on', reverse=True)
    filtered = filter_torrents(torrents, days_from, days_to, cache_mount)
    
    if action == "pausar":
        stop_start_torrents(filtered, pause=True)
    elif action == "resumir":
        stop_start_torrents(filtered, pause=False)

def filter_torrents(torrent_list, timeoffset_from, timeoffset_to, cache_mount):
    def is_en_cache(torrent):
        if not cache_mount:
            return True
            
        # Verificar que al menos un archivo del torrent exista en el cache
        for archivo in torrent.files:
            ruta_completa = os.path.join(cache_mount, archivo.name)
            if os.path.exists(ruta_completa):
                return True
        return False

    return [t for t in torrent_list 
            if (timeoffset_to <= t.added_on <= timeoffset_from) 
            and is_en_cache(t)]


def stop_start_torrents(torrent_list, pause=True):
    action = "Pausando" if pause else "Resumiendo"
    for torrent in torrent_list:
        logger.debug(f"{action}: {torrent.name}")
        torrent.pause() if pause else torrent.resume()
