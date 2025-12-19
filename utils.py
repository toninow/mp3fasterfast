#!/usr/bin/env python3
"""
Utilidades para MP3 FasterFast
"""
import os
from pathlib import Path

# Directorios base
BASE_DIR = Path(__file__).parent

# Estructura organizada
DATA_DIR = BASE_DIR / "data"
DOWNLOADS_DIR = BASE_DIR / "downloads"
BIN_DIR = BASE_DIR / "bin"

# Subdirectorios de descargas
MP3_DIR = DOWNLOADS_DIR / "MP3"
VIDEOS_DIR = DOWNLOADS_DIR / "Videos"
PLAYLISTS_DIR = DOWNLOADS_DIR / "Playlists"
CANALES_DIR = DOWNLOADS_DIR / "Canales"

# Archivos ejecutables (buscar en bin/ primero, luego en raíz)
YT_DLP_EXE = BIN_DIR / "yt-dlp.exe"
if not YT_DLP_EXE.exists():
    YT_DLP_EXE = BASE_DIR / "yt-dlp.exe"

FFMPEG_EXE = BIN_DIR / "ffmpeg.exe"
if not FFMPEG_EXE.exists():
    FFMPEG_EXE = BASE_DIR / "ffmpeg.exe"

# Base de datos
DB_FILE = DATA_DIR / "downloads.db"

def ensure_directories():
    """Crear directorios necesarios si no existen"""
    directories = [DATA_DIR, DOWNLOADS_DIR, MP3_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def get_download_path(audio_type="mp3", source_type="url"):
    """Obtener ruta de descarga según tipo"""
    base_path = DOWNLOADS_DIR

    if audio_type in ["mp3", "mp3_320", "mp3_256", "mp3_192", "mp3_128"]:
        return base_path / "MP3"
    elif audio_type.startswith("video"):
        return base_path / "Videos"
    elif audio_type.startswith("playlist"):
        return base_path / "Playlists"
    else:
        return base_path / "Canales"

def validate_dependencies():
    """Validar que las dependencias necesarias existan"""
    dependencies = {
        "yt-dlp": YT_DLP_EXE,
        "ffmpeg": FFMPEG_EXE
    }

    missing = []
    for name, path in dependencies.items():
        if not path.exists():
            missing.append(name)

    return missing

def load_config():
    """Cargar configuración (placeholder)"""
    return {
        "quality": "Mejor",
        "format": "MP3 (Audio)"
    }

def save_config(config):
    """Guardar configuración (placeholder)"""
    pass

def check_internet_connection():
    """Verificar conexión a internet"""
    try:
        import urllib.request
        urllib.request.urlopen('http://www.google.com', timeout=5)
        return True
    except:
        return False
