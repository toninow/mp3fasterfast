import sys
import json
import os
from pathlib import Path

# Detectar si estamos en un ejecutable empaquetado o en desarrollo
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

# Rutas relativas
CONFIG_FILE = BASE_DIR / "config.json"
DATA_DIR = BASE_DIR / "data"
DB_FILE = DATA_DIR / "downloads.db"
DOWNLOADS_DIR = BASE_DIR / "downloads"
MP3_DIR = DOWNLOADS_DIR / "MP3"
VIDEOS_DIR = DOWNLOADS_DIR / "Videos"
PLAYLISTS_DIR = DOWNLOADS_DIR / "Playlists"
CHANNELS_DIR = DOWNLOADS_DIR / "Canales"

# Ejecutables externos
YT_DLP_EXE = BASE_DIR / "yt-dlp.exe"
FFMPEG_EXE = BASE_DIR / "ffmpeg.exe"

def ensure_directories():
    """Crear directorios necesarios si no existen"""
    directories = [DATA_DIR, DOWNLOADS_DIR, MP3_DIR, VIDEOS_DIR, PLAYLISTS_DIR, CHANNELS_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def load_config():
    """Cargar configuración desde config.json"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"downloads_path": str(DOWNLOADS_DIR)}

def save_config(config):
    """Guardar configuración en config.json"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

def validate_dependencies():
    """Validar que existan los ejecutables necesarios"""
    missing = []
    if not YT_DLP_EXE.exists():
        missing.append("yt-dlp.exe")
    if not FFMPEG_EXE.exists():
        missing.append("ffmpeg.exe")
    return missing

def get_download_path(download_type, source_type):
    """Obtener ruta de descarga basada en tipo"""
    if download_type == "mp3":
        if source_type in ["canal", "playlist"]:
            return PLAYLISTS_DIR if source_type == "playlist" else CHANNELS_DIR
        else:
            return MP3_DIR
    else:  # video
        if source_type in ["canal", "playlist"]:
            return PLAYLISTS_DIR if source_type == "playlist" else CHANNELS_DIR
        else:
            return VIDEOS_DIR
