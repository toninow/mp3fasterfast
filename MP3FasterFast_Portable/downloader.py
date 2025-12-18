import subprocess
import json
import re
import urllib.request
import urllib.error
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

    def check_internet_connection(self):
        """Verificar si hay conexión a internet"""
        try:
            urllib.request.urlopen('http://www.google.com', timeout=5)
            return True
        except urllib.error.URLError:
            return False

    def download_thumbnail(self, thumbnail_url, output_path):
        """Descargar thumbnail/portada"""
        try:
            with urllib.request.urlopen(thumbnail_url, timeout=10) as response:
                with open(output_path, 'wb') as f:
                    f.write(response.read())
            return True
        except Exception as e:
            self.log(f"Error descargando thumbnail: {str(e)}")
            return False

    def apply_thumbnail_to_mp3(self, mp3_path, thumbnail_path):
        """Aplicar thumbnail como portada a archivo MP3"""
        try:
            from mutagen.mp3 import MP3
            from mutagen.id3 import APIC, ID3

            # Cargar archivo MP3
            audio = MP3(mp3_path, ID3=ID3)

            # Leer imagen
            with open(thumbnail_path, 'rb') as img_file:
                img_data = img_file.read()

            # Crear tag de imagen
            audio.tags.add(
                APIC(
                    encoding=3,  # UTF-8
                    mime='image/jpeg',  # o 'image/png' dependiendo del formato
                    type=3,  # Cover (front)
                    desc='Cover',
                    data=img_data
                )
            )

            # Guardar cambios
            audio.save()
            self.log("Portada aplicada al archivo MP3")
            return True

        except Exception as e:
            self.log(f"Error aplicando portada MP3: {str(e)}")
            return False

    def apply_thumbnail_to_mp4(self, mp4_path, thumbnail_path):
        """Aplicar thumbnail como poster a archivo MP4"""
        try:
            # Usar ffmpeg para agregar thumbnail como metadata
            cmd = [
                str(FFMPEG_EXE),
                '-i', str(mp4_path),
                '-i', str(thumbnail_path),
                '-map', '0',
                '-map', '1',
                '-c', 'copy',
                '-disposition:v:1', 'attached_pic',
                '-metadata:s:v', 'title=Album cover',
                '-metadata:s:v', 'comment=Cover (front)',
                str(mp4_path) + '_temp.mp4'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

            if result.returncode == 0:
                # Reemplazar archivo original
                import os
                os.replace(str(mp4_path) + '_temp.mp4', str(mp4_path))
                self.log("Portada aplicada al archivo MP4")
                return True
            else:
                self.log(f"Error aplicando portada MP4: {result.stderr}")
                return False

        except Exception as e:
            self.log(f"Error aplicando portada MP4: {str(e)}")
            return False

    def apply_thumbnail_to_file(self, url, download_path, download_type):
        """Aplicar thumbnail al archivo descargado"""
        try:
            # Extraer información del video para obtener thumbnail
            info = self.extract_info(url)
            if not info or isinstance(info, list):
                return

            thumbnail_url = info.get('thumbnail')
            if not thumbnail_url:
                self.log("No se encontró thumbnail para este video")
                return

            # Determinar nombre del archivo descargado
            title = info.get('title', 'Unknown')
            if download_type == "mp3":
                file_path = download_path / f"{title}.mp3"
                is_mp3 = True
            else:
                file_path = download_path / f"{title}.mp4"
                is_mp3 = False

            if not file_path.exists():
                self.log("Archivo descargado no encontrado")
                return

            # Descargar thumbnail a archivo temporal
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_path = temp_file.name

            if self.download_thumbnail(thumbnail_url, temp_path):
                # Aplicar thumbnail según tipo de archivo
                if is_mp3:
                    success = self.apply_thumbnail_to_mp3(file_path, temp_path)
                else:
                    success = self.apply_thumbnail_to_mp4(file_path, temp_path)

                if success:
                    self.log("Portada aplicada exitosamente")
                else:
                    self.log("Error aplicando portada")
            else:
                self.log("Error descargando thumbnail")

            # Limpiar archivo temporal
            try:
                import os
                os.unlink(temp_path)
            except:
                pass

        except Exception as e:
            self.log(f"Error en apply_thumbnail_to_file: {str(e)}")

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

                # Descargar y aplicar portada si hay conexión a internet
                if self.check_internet_connection():
                    self.log("Conexión a internet detectada - descargando portada...")
                    self.apply_thumbnail_to_file(url, download_path, download_type)
                else:
                    self.log("Sin conexión a internet - omitiendo descarga de portada")

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
