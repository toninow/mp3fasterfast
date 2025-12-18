import subprocess
import json
import re
from pathlib import Path
from utils import YT_DLP_EXE, FFMPEG_EXE, get_download_path
from database import Database

class Downloader:
    def __init__(self, log_callback=None):
        self.log_callback = log_callback
        self.db = Database()

    def log(self, message):
        """Log de mensajes"""
        if self.log_callback:
            self.log_callback(message)

    def extract_info(self, url):
        """Extraer información del video/playlist sin descargar"""
        try:
            cmd = [
                str(YT_DLP_EXE),
                '--no-download',
                '--print-json',
                '--ffmpeg-location', str(FFMPEG_EXE),
                url
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

            if result.returncode == 0:
                # Si es playlist, yt-dlp devuelve múltiples JSON
                lines = result.stdout.strip().split('\n')
                videos = []
                for line in lines:
                    if line.strip():
                        try:
                            video_info = json.loads(line)
                            videos.append(video_info)
                        except json.JSONDecodeError:
                            continue

                if videos:
                    return videos[0] if len(videos) == 1 else videos
                else:
                    return None
            else:
                self.log(f"Error extrayendo info: {result.stderr}")
                return None

        except Exception as e:
            self.log(f"Error extrayendo info: {str(e)}")
            return None

    def download_video(self, url, download_type="video", source_type="url"):
        """Descargar video"""
        try:
            # Determinar opciones según tipo
            download_path = get_download_path("video" if download_type in ["video", "playlist_mp4"] else "mp3", source_type)

            cmd = [str(YT_DLP_EXE)]

            # Configurar formato
            if download_type == "mp3":
                cmd.extend(['-x', '--audio-format', 'mp3', '--audio-quality', '0'])
            elif download_type == "video":
                cmd.extend(['-f', 'best[height<=720]'])  # Mejor calidad hasta 720p
            elif download_type == "video_mp4":
                cmd.extend(['-f', 'best[ext=mp4][height<=720]/best[height<=720][ext=mp4]'])
            elif download_type == "playlist_mp3":
                cmd.extend(['-x', '--audio-format', 'mp3', '--audio-quality', '0', '--yes-playlist'])
            elif download_type == "playlist_mp4":
                cmd.extend(['-f', 'best[ext=mp4][height<=720]/best[height<=720][ext=mp4]', '--yes-playlist'])

            # Opciones comunes
            cmd.extend([
                '--ffmpeg-location', str(FFMPEG_EXE),
                '-o', str(download_path / '%(title)s.%(ext)s'),
                '--no-playlist' if source_type == "url" and not download_type.startswith("playlist") else '--yes-playlist',
                url
            ])

            self.log(f"Ejecutando: {' '.join(cmd)}")

            # Ejecutar descarga
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     text=True, encoding='utf-8', bufsize=1, universal_newlines=True)

            # Leer output en tiempo real
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log(output.strip())

            if process.returncode == 0:
                self.log("Descarga completada exitosamente")

                # Extraer información y guardar en BD
                info = self.extract_info(url)
                if info:
                    if isinstance(info, list):
                        # Playlist
                        for video in info:
                            title = video.get('title', 'Unknown')
                            artist = video.get('uploader', 'Unknown')
                            file_path = str(download_path / f"{title}.{'mp3' if 'mp3' in download_type else 'mp4'}")
                            self.db.add_download(url, title, artist,
                                               "mp3" if "mp3" in download_type else "video",
                                               source_type, file_path)
                    else:
                        # Video individual
                        title = info.get('title', 'Unknown')
                        artist = info.get('uploader', 'Unknown')
                        file_path = str(download_path / f"{title}.{'mp3' if download_type == 'mp3' else 'mp4'}")
                        self.db.add_download(url, title, artist,
                                           "mp3" if download_type == "mp3" else "video",
                                           source_type, file_path)

                return True
            else:
                self.log(f"Error en descarga: código {process.returncode}")
                return False

        except Exception as e:
            self.log(f"Error en descarga: {str(e)}")
            return False

    def close(self):
        """Cerrar conexiones"""
        if self.db:
            self.db.close()
