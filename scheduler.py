import threading
import time
from datetime import datetime
from downloader import Downloader
from database import Database

class Scheduler:
    def __init__(self, log_callback=None):
        self.log_callback = log_callback
        self.db = None  # No crear conexión aquí
        self.timers = []
        self.running = True

        # Iniciar hilo de verificación
        self.check_thread = threading.Thread(target=self.check_scheduled_downloads, daemon=True)
        self.check_thread.start()

    def log(self, message):
        """Log de mensajes"""
        if self.log_callback:
            self.log_callback(message)

    def schedule_download(self, url, download_type, scheduled_time):
        """Programar una descarga"""
        try:
            # Convertir string a datetime
            if isinstance(scheduled_time, str):
                scheduled_datetime = datetime.fromisoformat(scheduled_time)
            else:
                scheduled_datetime = scheduled_time

            # Calcular delay en segundos
            now = datetime.now()
            delay = (scheduled_datetime - now).total_seconds()

            if delay <= 0:
                self.log("La fecha programada ya pasó")
                return False

            # Guardar en base de datos (conexión local)
            db = Database()
            scheduled_id = db.add_scheduled_download(url, download_type, scheduled_datetime.isoformat())
            db.close()

            # Crear timer
            timer = threading.Timer(delay, self.execute_scheduled_download,
                                   args=(scheduled_id, url, download_type))
            timer.start()
            self.timers.append(timer)

            self.log(f"Descarga programada para {scheduled_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            return True

        except Exception as e:
            self.log(f"Error programando descarga: {str(e)}")
            return False

    def execute_scheduled_download(self, scheduled_id, url, download_type):
        """Ejecutar descarga programada"""
        try:
            self.log(f"Ejecutando descarga programada: {url}")

            # Determinar tipo de fuente
            source_type = "url"
            if "playlist" in download_type:
                source_type = "playlist"

            # Crear downloader y ejecutar
            downloader = Downloader(self.log_callback)
            success = downloader.download_video(url, download_type, source_type)
            downloader.close()

            # Eliminar de programadas si fue exitosa
            if success:
                self.db.remove_scheduled_download(scheduled_id)
                self.log("Descarga programada completada")
            else:
                self.log("Error en descarga programada")

        except Exception as e:
            self.log(f"Error ejecutando descarga programada: {str(e)}")

    def check_scheduled_downloads(self):
        """Verificar descargas programadas pendientes cada minuto"""
        while self.running:
            try:
                # Crear conexión local para este thread
                db = Database()
                scheduled = db.get_scheduled_downloads()
                db.close()

                for download in scheduled:
                    download_id, url, download_type, scheduled_time, created_date = download
                    scheduled_datetime = datetime.fromisoformat(scheduled_time)

                    # Si ya pasó la hora, ejecutarla
                    if datetime.now() >= scheduled_datetime:
                        self.execute_scheduled_download(download_id, url, download_type)

                time.sleep(60)  # Verificar cada minuto

            except Exception as e:
                self.log(f"Error verificando descargas programadas: {str(e)}")
                time.sleep(60)

    def cancel_all_timers(self):
        """Cancelar todos los timers"""
        self.running = False
        for timer in self.timers:
            if timer.is_alive():
                timer.cancel()
        self.timers.clear()

    def close(self):
        """Cerrar scheduler"""
        self.cancel_all_timers()
        # No hay conexión compartida que cerrar
