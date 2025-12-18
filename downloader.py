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

            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

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

    def apply_thumbnail_to_file(self, url, download_path, download_type, video_info=None):
        """Aplicar thumbnail al archivo descargado"""
        try:
            print(f"🔥 [THUMBNAIL] Iniciando apply_thumbnail_to_file para {url[:30]}...")
            # Usar la info del video pasada como parámetro, o extraerla si no está disponible
            if video_info:
                info = video_info
                print("🔥 [THUMBNAIL] Usando info del video ya disponible")
            else:
                print("🔥 [THUMBNAIL] Extrayendo info del video...")
                info = self.extract_info(url)
                print(f"🔥 [THUMBNAIL] extract_info retornó: {info is not None}")

            if not info or isinstance(info, list):
                print("🔥 [THUMBNAIL] Info del video no válida")
                return

            thumbnail_url = info.get('thumbnail')
            print(f"🔥 [THUMBNAIL] Thumbnail URL: {thumbnail_url}")
            if not thumbnail_url:
                print("🔥 [THUMBNAIL] No hay thumbnail URL")
                self.log("No se encontró thumbnail para este video")
                return

            # Determinar nombre del archivo descargado
            title = info.get('title', 'Unknown')
            print(f"🔥 [THUMBNAIL] Título del archivo: {title}")
            if download_type == "mp3":
                file_path = download_path / f"{title}.mp3"
                is_mp3 = True
            else:
                file_path = download_path / f"{title}.mp4"
                is_mp3 = False

            print(f"🔥 [THUMBNAIL] Buscando archivo: {file_path}")
            if not file_path.exists():
                print("🔥 [THUMBNAIL] Archivo no encontrado")
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
                print("🔥 [THUMBNAIL] Archivo temporal limpiado")
            except:
                pass

            print("🔥 [THUMBNAIL] apply_thumbnail_to_file completado exitosamente")

        except Exception as e:
            print(f"🔥 [THUMBNAIL] ERROR en apply_thumbnail_to_file: {e}")
            self.log(f"Error en apply_thumbnail_to_file: {str(e)}")

    def extract_info(self, url):
        """Extraer información del video/playlist sin descargar"""
        try:
            cmd = [
                str(YT_DLP_EXE),
                '--no-warnings',
                '--no-download',
                '--print-json',
                '--ffmpeg-location', str(FFMPEG_EXE),
                url
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=45)

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

        except subprocess.TimeoutExpired:
            self.log("Timeout extrayendo información del video (30s)")
            return None
        except Exception as e:
            self.log(f"Error extrayendo info: {str(e)}")
            return None

    def download_video(self, url, download_type="video", source_type="url", video_info=None):
        """Descargar video"""
        try:
            # Determinar opciones según tipo
            download_path = get_download_path("video" if download_type in ["video", "playlist_mp4"] else "mp3", source_type)

            cmd = [str(YT_DLP_EXE), '--no-warnings']

            # Configurar formato
            if download_type == "mp3":
                cmd.extend(['-x', '--audio-format', 'mp3', '--audio-quality', '0'])
            elif download_type.startswith("mp3_"):
                # Formatos específicos de MP3: mp3_320, mp3_256, etc.
                quality = download_type.split("_")[1]  # Extraer calidad (320, 256, etc.)
                cmd.extend(['-x', '--audio-format', 'mp3', '--audio-quality', quality])
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

            # Ejecutar descarga con timeout
            print(f"🔥 [DOWNLOADER] Ejecutando subprocess.run con timeout...")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True,
                                      encoding='utf-8', errors='replace', timeout=90)
                print(f"🔥 [DOWNLOADER] Subprocess completado, código: {result.returncode}")

                # Log output
                if result.stdout:
                    output_lines = result.stdout.strip().split('\n')
                    for i, line in enumerate(output_lines[:5]):  # Solo primeros 5
                        print(f"🔥 [DOWNLOADER] Output {i+1}: {line[:100]}...")
                        self.log(line)

                if result.returncode == 0:
                    print("🔥 [DOWNLOADER] Descarga exitosa, procesando portada...")
                    self.log("Descarga completada exitosamente")

                    # Descargar y aplicar portada si hay conexión a internet
                    if self.check_internet_connection():
                        print("🔥 [DOWNLOADER] Conexión OK, descargando portada...")
                        self.log("Conexión a internet detectada - descargando portada...")
                        # Pasar la info del video que ya tenemos en lugar de volver a extraerla
                        self.apply_thumbnail_to_file(url, download_path, download_type, video_info)
                        print("🔥 [DOWNLOADER] Portada procesada")
                    else:
                        print("🔥 [DOWNLOADER] Sin conexión, saltando portada")
                        self.log("Sin conexión a internet - omitiendo descarga de portada")

                    # Extraer información y guardar en BD
                    print("🔥 [DOWNLOADER] Extrayendo info para BD...")
                    info = self.extract_info(url)
                    if info:
                        print(f"🔥 [DOWNLOADER] Guardando en BD: {info.get('title', 'N/A')[:30]}...")
                        self.db.add_download(info['title'], url, download_type, source_type)
                        print("🔥 [DOWNLOADER] Info guardada en BD")
                    else:
                        print("🔥 [DOWNLOADER] No se pudo extraer info para BD")
                    print("🔥 [DOWNLOADER] Método retornando True")
                    return True
                else:
                    print(f"🔥 [DOWNLOADER] Error en descarga, código: {result.returncode}")
                    self.log(f"Error en descarga: código {result.returncode}")
                    return False

            except subprocess.TimeoutExpired:
                print("🔥 [DOWNLOADER] Timeout: Proceso cancelado después de 60 segundos")
                self.log("Error: Timeout en descarga (60 segundos)")
                return False
            except Exception as e:
                print(f"🔥 [DOWNLOADER] Excepción en download_video: {e}")
                self.log(f"Error en descarga: {str(e)}")
                return False

        except Exception as e:
            self.log(f"Error general en download_video: {str(e)}")
            return False

    def close(self):
        """Cerrar conexiones"""
        if self.db:
            self.db.close()
