import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime, timedelta
import threading
import queue
from downloader import Downloader
from database import Database
from metadata import MetadataEditor
from scheduler import Scheduler
from utils import ensure_directories, validate_dependencies, load_config, save_config, MP3_DIR

# Configurar CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MP3FasterFast(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MP3 FasterFast")
        self.geometry("900x700")
        self.resizable(False, False)

        # Cola para comunicación thread-safe
        self.log_queue = queue.Queue()

        # Centrar ventana
        print("Centrando ventana...")
        self.center_window()
        print("Ventana centrada")

        # Inicializar componentes
        self.db = Database()

        # Validar dependencias
        print("Validando dependencias...")
        missing_deps = validate_dependencies()
        if missing_deps:
            error_msg = f"Faltan los siguientes archivos en la carpeta del programa:\n{chr(10).join(missing_deps)}"
            print(f"ERROR: {error_msg}")
            try:
                messagebox.showerror("Dependencias faltantes", error_msg)
            except:
                print("No se pudo mostrar messagebox (entorno sin GUI)")
            self.destroy()
            return
        print("Dependencias validadas")

        # Crear directorios
        print("Creando directorios...")
        ensure_directories()
        print("Directorios creados")

        # Crear interfaz (con manejo de errores)
        try:
            self.create_widgets()
            print("Widgets creados")
        except Exception as e:
            print(f"Error creando widgets: {str(e)}")
            raise

        # Cargar historial (con manejo de errores)
        try:
            self.load_history()
            print("Historial cargado")
        except Exception as e:
            print(f"Error cargando historial: {str(e)}")
            # Continuar sin historial si hay error

        # Protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Mensaje de bienvenida (después de configurar todo)
        self.after(100, lambda: self.log_message("🎵 MP3 FasterFast iniciado correctamente"))
        self.after(100, lambda: self.log_message("💡 Pega múltiples URLs para descargar en lote"))

        # Iniciar procesamiento de cola de logs después de que la ventana esté lista
        self.after(200, self.process_log_queue)

    def center_window(self):
        """Centrar ventana en pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Título y subtítulo
        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(pady=15)

        ctk.CTkLabel(title_frame, text="🎵 MP3 FasterFast",
                    font=("Arial", 22, "bold")).pack()
        ctk.CTkLabel(title_frame, text="Descargador de Música y Videos Portable",
                    font=("Arial", 11), text_color="gray70").pack(pady=(5, 0))

        # Panel de descarga
        download_frame = ctk.CTkFrame(main_frame)
        download_frame.pack(pady=15, padx=20, fill="x")

        # Título del panel
        ctk.CTkLabel(download_frame, text="Descargar Contenido",
                    font=("Arial", 14, "bold")).pack(pady=10)

        # Tipo de descarga
        type_frame = ctk.CTkFrame(download_frame, fg_color="transparent")
        type_frame.pack(pady=5, fill="x")

        ctk.CTkLabel(type_frame, text="Tipo de descarga:",
                    font=("Arial", 11)).pack(side="left", padx=10)
        self.download_type = ctk.CTkComboBox(type_frame,
                                           values=["MP3 (Audio)", "Video (MP4)", "Playlist MP3", "Playlist MP4"],
                                           state="readonly", width=150)
        self.download_type.set("MP3 (Audio)")
        self.download_type.pack(side="right", padx=10)

        # URLs múltiples
        urls_frame = ctk.CTkFrame(download_frame)
        urls_frame.pack(pady=10, fill="x", padx=10)

        # Header con contador
        urls_header = ctk.CTkFrame(urls_frame, fg_color="transparent")
        urls_header.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(urls_header, text="URLs a descargar (una por línea):",
                    font=("Arial", 11, "bold")).pack(side="left")
        self.url_counter = ctk.CTkLabel(urls_header, text="0 URLs",
                                       font=("Arial", 10), text_color="gray70")
        self.url_counter.pack(side="right")

        self.urls_textbox = ctk.CTkTextbox(urls_frame, height=140)
        self.urls_textbox.pack(fill="x", padx=10, pady=5)
        # Insertar texto de placeholder manualmente
        self.urls_textbox.insert("0.0", "Pega aquí las URLs de YouTube...\n\nEjemplos:\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ\nhttps://youtu.be/dQw4w9WgXcQ\nhttps://www.youtube.com/playlist?list=...")
        self.urls_textbox.bind("<KeyRelease>", self.update_url_counter)

        # Información de ayuda
        help_frame = ctk.CTkFrame(urls_frame, fg_color="transparent")
        help_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(help_frame, text="💡 Puedes pegar múltiples URLs separadas por líneas",
                    font=("Arial", 9), text_color="gray70").pack(side="left")
        ctk.CTkLabel(help_frame, text="📊 Se descargarán en orden secuencial",
                    font=("Arial", 9), text_color="gray70").pack(side="right")

        # Botones de acción
        buttons_frame = ctk.CTkFrame(download_frame, fg_color="transparent")
        buttons_frame.pack(pady=15)

        self.download_btn = ctk.CTkButton(buttons_frame, text="🚀 Iniciar Descargas",
                                         command=self.start_multiple_downloads,
                                         height=40, font=("Arial", 12, "bold"))
        self.download_btn.pack(side="left", padx=10)

        self.clear_btn = ctk.CTkButton(buttons_frame, text="🗑️ Limpiar URLs",
                                      command=self.clear_urls, fg_color="transparent",
                                      border_width=2, height=40)
        self.clear_btn.pack(side="left", padx=10)

        # Área de log
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)

        log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_header.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(log_header, text="📋 Registro de actividad",
                    font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkButton(log_header, text="🗑️ Limpiar", width=80, height=25,
                     command=self.clear_log).pack(side="right")

        self.log_text = ctk.CTkTextbox(log_frame, height=120, wrap="word")
        self.log_text.pack(padx=10, pady=5, fill="both", expand=True)
        self.log_text.configure(state="disabled")  # Solo lectura

        # Historial
        history_frame = ctk.CTkFrame(main_frame)
        history_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Header del historial
        history_header = ctk.CTkFrame(history_frame, fg_color="transparent")
        history_header.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(history_header, text="📚 Historial de descargas",
                    font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkButton(history_header, text="🔄 Actualizar", width=90, height=25,
                     command=self.load_history).pack(side="right", padx=(5, 0))
        self.history_count = ctk.CTkLabel(history_header, text="0 elementos",
                                         font=("Arial", 10), text_color="gray70")
        self.history_count.pack(side="right")

        # Treeview para historial
        columns = ("Título", "Artista", "Tipo", "Fecha", "Ubicación")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)

        # Configurar columnas
        self.history_tree.heading("Título", text="Título")
        self.history_tree.column("Título", width=200)
        self.history_tree.heading("Artista", text="Artista")
        self.history_tree.column("Artista", width=150)
        self.history_tree.heading("Tipo", text="Tipo")
        self.history_tree.column("Tipo", width=80)
        self.history_tree.heading("Fecha", text="Fecha")
        self.history_tree.column("Fecha", width=120)
        self.history_tree.heading("Ubicación", text="Ubicación")
        self.history_tree.column("Ubicación", width=250)

        # Scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side="left", padx=10, pady=5, fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botón eliminar
        button_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
        button_frame.pack(pady=5)

        ctk.CTkButton(button_frame, text="Eliminar del historial", command=self.remove_download,
                     fg_color="red", hover_color="darkred").pack(side="right", padx=10)

        # Bind doble clic para editar MP3
        self.history_tree.bind("<Double-1>", self.on_tree_double_click)

    def thread_safe_log(self, message):
        """Agregar mensaje al log de manera thread-safe"""
        self.log_queue.put(message)

    def process_log_queue(self):
        """Procesar mensajes de la cola de logs"""
        try:
            # Procesar máximo 10 mensajes por llamada para no bloquear la UI
            for _ in range(10):
                try:
                    message = self.log_queue.get_nowait()
                    self.log_text.configure(state="normal")
                    self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
                    self.log_text.configure(state="disabled")
                    self.log_text.see("end")
                except queue.Empty:
                    break
        except Exception as e:
            # Si hay error, intentar log normal
            try:
                self.log_message(f"Error procesando cola: {str(e)}")
            except:
                pass

        # Continuar procesando cada 100ms
        try:
            self.after(100, self.process_log_queue)
        except Exception as e:
            # Si after falla, detener el procesamiento
            print(f"Error en after(): {str(e)}")

    def log_message(self, message):
        """Agregar mensaje al log (desde el hilo principal)"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.configure(state="disabled")
        self.log_text.see("end")

    def clear_log(self):
        """Limpiar el registro de actividad"""
        self.log_text.configure(state="normal")
        self.log_text.delete("0.0", "end")
        self.log_text.configure(state="disabled")
        self.log_message("🧹 Registro limpiado")

    def start_multiple_downloads(self):
        """Iniciar descargas múltiples"""
        urls_text = self.urls_textbox.get("0.0", "end").strip()
        if not urls_text:
            messagebox.showerror("Error", "Ingresa al menos una URL")
            return

        # Procesar URLs
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        if not urls:
            messagebox.showerror("Error", "No se encontraron URLs válidas")
            return

        # Mapear tipos de descarga
        download_type_map = {
            "MP3 (Audio)": "mp3",
            "Video (MP4)": "video_mp4",
            "Playlist MP3": "playlist_mp3",
            "Playlist MP4": "playlist_mp4"
        }

        download_type = download_type_map[self.download_type.get()]

        # Determinar tipo de fuente
        source_type = "playlist" if "Playlist" in self.download_type.get() else "url"

        # Deshabilitar botón
        self.download_btn.configure(state="disabled", text="⏳ Procesando...")

        # Ejecutar en hilo
        threading.Thread(target=self.multiple_downloads_worker,
                        args=(urls, download_type, source_type), daemon=True).start()

    def multiple_downloads_worker(self, urls, download_type, source_type):
        """Worker para múltiples descargas"""
        try:
            downloader = Downloader(self.log_message)
            completed = 0
            failed = 0

            self.log_message(f"🚀 Iniciando descarga de {len(urls)} elementos...")

            for i, url in enumerate(urls, 1):
                self.log_message(f"📥 Descargando {i}/{len(urls)}: {url[:50]}...")
                try:
                    success = downloader.download_video(url, download_type, source_type)
                    if success:
                        completed += 1
                        self.log_message(f"✅ Completado: {url[:50]}...")
                    else:
                        failed += 1
                        self.log_message(f"❌ Error: {url[:50]}...")
                except Exception as e:
                    failed += 1
                    self.log_message(f"💥 Error crítico en {url[:50]}...: {str(e)}")

            downloader.close()

            # Recargar historial
            self.after(0, self.load_history)

            # Resumen final
            self.log_message(f"🎉 Proceso terminado: {completed} exitosas, {failed} fallidas")

        except Exception as e:
            self.log_message(f"💥 Error general: {str(e)}")
        finally:
            # Rehabilitar botón
            self.after(0, lambda: self.download_btn.configure(state="normal", text="🚀 Iniciar Descargas"))

    def clear_urls(self):
        """Limpiar el área de URLs"""
        self.urls_textbox.delete("0.0", "end")
        # Re-insertar placeholder
        self.urls_textbox.insert("0.0", "Pega aquí las URLs de YouTube...\n\nEjemplos:\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ\nhttps://youtu.be/dQw4w9WgXcQ\nhttps://www.youtube.com/playlist?list=...")
        self.update_url_counter()
        self.log_message("🗑️ URLs limpiadas")

    def update_url_counter(self, event=None):
        """Actualizar contador de URLs en tiempo real"""
        urls_text = self.urls_textbox.get("0.0", "end").strip()
        placeholder = "Pega aquí las URLs de YouTube..."

        # Si solo está el placeholder, contar como vacío
        if urls_text.startswith(placeholder):
            urls_text = urls_text[len(placeholder):].strip()

        if urls_text:
            urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
            count = len(urls)
            self.url_counter.configure(text=f"{count} URL{'s' if count != 1 else ''}")
        else:
            self.url_counter.configure(text="0 URLs")


    def load_history(self):
        """Cargar historial de descargas"""
        # Limpiar treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Cargar desde BD
        downloads = self.db.get_all_downloads()

        for download in downloads:
            download_id, url, title, artist, download_type, source, file_path, download_date = download

            # Formatear fecha
            try:
                date_obj = datetime.fromisoformat(download_date)
                formatted_date = date_obj.strftime("%Y-%m-%d %H:%M")
            except:
                formatted_date = download_date

            # Obtener ubicación relativa
            try:
                from pathlib import Path
                location = str(Path(file_path).relative_to(Path.cwd() / "downloads")) if file_path else ""
            except:
                location = file_path or ""

            # Insertar en treeview
            self.history_tree.insert("", "end", values=(title or "Sin título", artist or "Desconocido",
                                                      download_type, formatted_date, location))

        # Actualizar contador
        count = len(downloads)
        self.history_count.configure(text=f"{count} elemento{'s' if count != 1 else ''}")

    def remove_download(self):
        """Eliminar descarga seleccionada del historial"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una descarga para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar esta descarga del historial?"):
            try:
                # Obtener valores de la fila seleccionada
                item = self.history_tree.item(selection[0])
                values = item['values']
                title, artist, download_type, date_str, location = values

                # Buscar el ID en la base de datos usando los criterios disponibles
                downloads = self.db.get_all_downloads()
                download_id = None

                for download in downloads:
                    db_id, url, db_title, db_artist, db_type, source, file_path, download_date = download
                    if (db_title == title and db_artist == artist and db_type == download_type):
                        download_id = db_id
                        break

                if download_id:
                    # Eliminar de base de datos
                    self.db.remove_download(download_id)
                    # Recargar historial
                    self.load_history()
                    self.log_message("🗑️ Descarga eliminada del historial")
                else:
                    messagebox.showerror("Error", "No se pudo encontrar la descarga en la base de datos")

            except Exception as e:
                messagebox.showerror("Error", f"Error eliminando descarga: {str(e)}")

    def on_tree_double_click(self, event):
        """Manejar doble clic en historial para editar metadatos MP3"""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            values = item['values']

            title, artist, download_type, date_str, location = values

            # Solo abrir editor si es MP3
            if download_type == "mp3" and location:
                # Construir ruta completa
                from pathlib import Path
                full_path = Path.cwd() / "downloads" / location

                if full_path.exists() and full_path.suffix.lower() == '.mp3':
                    try:
                        MetadataEditor(str(full_path))
                        self.log_message(f"🎵 Editando metadatos: {title}")
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo abrir el editor: {str(e)}")
                else:
                    messagebox.showwarning("Advertencia", "Archivo MP3 no encontrado")

    def on_closing(self):
        """Manejar cierre de aplicación"""
        if self.db:
            self.db.close()
        self.destroy()

if __name__ == "__main__":
    try:
        print("Iniciando MP3 FasterFast...")
        app = MP3FasterFast()
        print("Aplicacion creada, iniciando interfaz...")
        app.mainloop()
        print("Aplicacion cerrada normalmente")
    except Exception as e:
        print(f"ERROR FATAL: {str(e)}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")
