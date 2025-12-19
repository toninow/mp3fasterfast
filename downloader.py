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

    def apply_thumbnail_to_file(self, url, file_path, download_type, video_info=None):
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

            # Determinar nombre del archivo descargado ANTES de procesar thumbnails
            title = info.get('title', 'Unknown')
            print(f"🔥 [THUMBNAIL] Título del archivo: {title}")

            # Buscar thumbnail en múltiples campos posibles
            thumbnail_url = info.get('thumbnail')

            # Si no hay thumbnail directo, buscar en la lista de thumbnails
            if not thumbnail_url and info.get('thumbnails'):
                # Buscar el thumbnail de mejor calidad (preferir JPG sobre WEBP, y mayor resolución)
                thumbnails = info.get('thumbnails', [])
                if thumbnails:
                    # Filtrar primero por JPG (mejor calidad que WEBP)
                    jpg_thumbnails = [t for t in thumbnails if t.get('url', '').endswith('.jpg')]
                    if jpg_thumbnails:
                        # De los JPG, tomar el de mayor resolución
                        jpg_thumbnails.sort(key=lambda x: x.get('height', 0) * x.get('width', 0), reverse=True)
                        thumbnail_url = jpg_thumbnails[0].get('url')
                    else:
                        # Si no hay JPG, tomar el mejor WEBP
                        thumbnails.sort(key=lambda x: x.get('height', 0) * x.get('width', 0), reverse=True)
                        thumbnail_url = thumbnails[0].get('url')

            print(f"🔥 [THUMBNAIL] Thumbnail URL encontrada: {thumbnail_url}")
            if thumbnail_url:
                print(f"🔥 [THUMBNAIL] Tipo: {'JPG' if thumbnail_url.endswith('.jpg') else 'WEBP'}")
                # Buscar resolución aproximada
                if info.get('thumbnails'):
                    for t in info.get('thumbnails', []):
                        if t.get('url') == thumbnail_url:
                            w, h = t.get('width', '?'), t.get('height', '?')
                            print(f"🔥 [THUMBNAIL] Resolución: {w}x{h}")
                            break

            if not thumbnail_url:
                print("🔥 [THUMBNAIL] No hay thumbnail URL disponible, creando imagen genérica")
                print(f"🔥 [THUMBNAIL] Total thumbnails disponibles: {len(info.get('thumbnails', []))}")
                # Crear imagen genérica basada en el título
                temp_path = self.create_generic_thumbnail(title)
                if not temp_path:
                    self.log("No se pudo crear thumbnail genérico")
                    return
                print("🔥 [THUMBNAIL] Imagen genérica creada")
                thumbnail_url = "generic"  # Marcar como genérico para no intentar descargarlo
            else:
                # Descargar thumbnail a archivo temporal
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                    temp_path = temp_file.name

                if not self.download_thumbnail(thumbnail_url, temp_path):
                    self.log("Error descargando thumbnail")
                    return
            # Determinar el archivo objetivo
            if file_path is None:
                # Buscar el archivo descargado más reciente
                from utils import get_download_path
                download_path = get_download_path("video" if download_type in ["video", "video_mp4", "playlist_mp4"] else "mp3", "url")
                expected_extension = 'mp3' if download_type.startswith('mp3') else 'mp4'
                downloaded_files = list(download_path.glob(f"*.{expected_extension}"))

                if downloaded_files:
                    file_path = max(downloaded_files, key=lambda f: f.stat().st_mtime)
                    print(f"🔥 [THUMBNAIL] Archivo encontrado dinámicamente: {file_path}")
                else:
                    print("🔥 [THUMBNAIL] Ningún archivo descargado encontrado")
                    self.log("Archivo descargado no encontrado")
                    return
            else:
                print(f"🔥 [THUMBNAIL] Archivo objetivo: {file_path}")

            if not file_path.exists():
                print("🔥 [THUMBNAIL] Archivo no encontrado")
                self.log("Archivo descargado no encontrado")
                return

            # Determinar si es MP3 o MP4 basado en la extensión
            is_mp3 = file_path.suffix.lower() == '.mp3'
            print(f"🔥 [THUMBNAIL] Detectado como {'audio MP3' if is_mp3 else 'video MP4'}")

            # Aplicar thumbnail según tipo de archivo
            if is_mp3:
                success = self.apply_thumbnail_to_mp3(str(file_path), temp_path)
            else:
                success = self.apply_thumbnail_to_mp4(str(file_path), temp_path)

            if success:
                self.log("Portada aplicada exitosamente")
            else:
                self.log("Error aplicando portada")

            # Limpiar archivo temporal (solo si no es genérico)
            if thumbnail_url:
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

    def create_generic_thumbnail(self, title):
        """Crear thumbnail genérico basado en el título"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import tempfile
            import os

            # Crear imagen base 640x640 (YouTube standard)
            img = Image.new('RGB', (640, 640), color='#1a1a1a')
            draw = ImageDraw.Draw(img)

            # Intentar usar fuente del sistema, fallback a default
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()

            # Obtener iniciales del título
            words = title.split()[:3]  # Máximo 3 palabras
            initials = ''.join(word[0].upper() for word in words if word)

            # Calcular posición centrada
            bbox = draw.textbbox((0, 0), initials, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (640 - text_width) // 2
            y = (640 - text_height) // 2

            # Dibujar texto
            draw.text((x, y), initials, fill='#ffffff', font=font)

            # Dibujar borde decorativo
            draw.rectangle([20, 20, 620, 620], outline='#ff4444', width=4)

            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_path = temp_file.name
                img.save(temp_path, 'JPEG', quality=90)

            return temp_path

        except Exception as e:
            self.log(f"Error creando thumbnail genérico: {str(e)}")
            return None

    def extract_info(self, url):
        """Extraer información del video/playlist sin descargar"""
        try:
            # LIMPIAR URL: Solo remover parámetros problemáticos, mantener list= si es playlist
            # Para extract_info, mantener la URL completa para que yt-dlp pueda procesar playlists
            clean_url = url

            print(f"🔥 [EXTRACT] URL limpia para extract_info: {clean_url}")

            cmd = [
                str(YT_DLP_EXE),
                '--no-warnings',
                '--no-download',
                '--print-json',
                '--ffmpeg-location', str(FFMPEG_EXE),
                '--write-thumbnail',  # Forzar obtención de thumbnail
                '--convert-thumbnails', 'jpg',  # Convertir thumbnail a JPG
                clean_url
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
        import subprocess
        try:
            # Determinar opciones según tipo
            download_path = get_download_path("video" if download_type in ["video", "video_mp4", "playlist_mp4"] else "mp3", source_type)

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
                                      encoding='utf-8', errors='replace', timeout=30)

                print(f"🔥 [DOWNLOADER] Código de retorno: {result.returncode}")

                # Debug detallado si hay error
                if result.returncode != 0:
                    print(f"🔥 [DOWNLOADER] ERROR: yt-dlp falló con código {result.returncode}")
                    print(f"🔥 [DOWNLOADER] Comando completo: {' '.join(cmd)}")

                    if result.stderr:
                        stderr_lines = result.stderr.strip().split('\n')
                        print(f"🔥 [DOWNLOADER] STDERR - Últimas líneas:")
                        for line in stderr_lines[-5:]:
                            if line.strip():
                                print(f"  ❌ {line}")

                    if result.stdout:
                        stdout_lines = result.stdout.strip().split('\n')
                        print(f"🔥 [DOWNLOADER] STDOUT - Últimas líneas:")
                        for line in stdout_lines[-3:]:
                            if line.strip():
                                print(f"  📝 {line}")

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
                        # Para aplicar thumbnail, usaremos el archivo que se descargue
                        # Por ahora, no podemos saber el nombre exacto, así que pasaremos la URL y video_info
                        # apply_thumbnail_to_file buscará el archivo después
                        self.apply_thumbnail_to_file(url, None, download_type, video_info)
                        print("🔥 [DOWNLOADER] Portada procesada")
                    else:
                        print("🔥 [DOWNLOADER] Sin conexión, saltando portada")
                        self.log("Sin conexión a internet - omitiendo descarga de portada")

                    # VERIFICAR que el archivo realmente existe antes de guardar en BD
                    # En lugar de asumir el nombre, buscar el archivo descargado en el directorio
                    expected_extension = 'mp3' if download_type.startswith('mp3') else 'mp4'

                    print(f"🔥 [DOWNLOADER] Buscando archivos con extensión: .{expected_extension}")

                    # Buscar archivos con la extensión correcta en el directorio de descarga
                    downloaded_files = list(download_path.glob(f"*.{expected_extension}"))

                    if downloaded_files:
                        # Tomar el archivo más reciente (último descargado)
                        downloaded_file = max(downloaded_files, key=lambda f: f.stat().st_mtime)
                        print(f"🔥 [DOWNLOADER] ✅ Archivo encontrado: {downloaded_file.name}")
                        self.log(f"Archivo descargado encontrado: {downloaded_file.name}")

                        # Usar el título del video_info si está disponible, sino extraer del nombre del archivo
                        title = video_info.get('title', 'Video sin título') if video_info else downloaded_file.stem
                        artist = video_info.get('uploader', 'Artista desconocido') if video_info else 'Artista desconocido'
                        db_type = 'mp3' if expected_extension == 'mp3' else 'video'

                        print("🔥 [DOWNLOADER] Guardando info en BD...")
                        self.db.add_download(url, title, artist, db_type, source_type, str(downloaded_file))
                        print("🔥 [DOWNLOADER] ✅ Info guardada en BD")
                    else:
                        print(f"🔥 [DOWNLOADER] ❌ ERROR: Ningún archivo .{expected_extension} encontrado en {download_path}")
                        self.log(f"ERROR: Archivo descargado no encontrado en {download_path}")
                        return False  # Fallar si no se creó el archivo
                    print("🔥 [DOWNLOADER] Método retornando True")
                    return True
                else:
                    print(f"🔥 [DOWNLOADER] Error en descarga, código: {result.returncode}")
                    self.log(f"Error en descarga: código {result.returncode}")
                    return False

            except subprocess.TimeoutExpired:
                print("🔥 [DOWNLOADER] Timeout: Proceso cancelado después de 30 segundos")
                self.log("Error: Timeout en descarga (30 segundos)")
                return False
            except Exception as e:
                print(f"🔥 [DOWNLOADER] Error en descarga: {e}")
                self.log(f"Error en descarga: {str(e)}")
                return False

        except Exception as e:
            self.log(f"Error general en download_video: {str(e)}")
            return False

    def close(self):
        """Cerrar conexiones"""
        if self.db:
            self.db.close()
