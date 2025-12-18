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
        self.center_window()

        # Inicializar componentes
        self.db = Database()
        self.scheduler = Scheduler(self.thread_safe_log)

        # Validar dependencias
        missing_deps = validate_dependencies()
        if missing_deps:
            messagebox.showerror("Dependencias faltantes",
                               f"Faltan los siguientes archivos en la carpeta del programa:\n{chr(10).join(missing_deps)}")
            self.destroy()
            return

        # Crear directorios
        ensure_directories()

        # Crear interfaz
        self.create_widgets()

        # Cargar historial
        self.load_history()

        # Iniciar procesamiento de cola de logs
        self.after(100, self.process_log_queue)

        # Protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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

        # Título
        ctk.CTkLabel(main_frame, text="MP3 FasterFast", font=("Arial", 20, "bold")).pack(pady=10)

        # Frame de entrada
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(pady=10, padx=20, fill="x")

        # URL
        ctk.CTkLabel(input_frame, text="URL:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.url_entry = ctk.CTkEntry(input_frame, width=500)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=2)

        # Tipo de descarga
        ctk.CTkLabel(input_frame, text="Tipo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.download_type = ctk.CTkComboBox(input_frame,
                                           values=["Video (mejor calidad)", "Video MP4", "MP3 (solo video)",
                                                  "Playlist MP3", "Playlist MP4"],
                                           state="readonly")
        self.download_type.set("MP3 (solo video)")
        self.download_type.grid(row=1, column=1, padx=10, pady=5)

        # Botón descargar
        self.download_btn = ctk.CTkButton(input_frame, text="Descargar", command=self.start_download)
        self.download_btn.grid(row=1, column=2, padx=10, pady=5)

        # Programar descarga
        schedule_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        schedule_frame.grid(row=2, column=0, columnspan=3, pady=10)

        ctk.CTkLabel(schedule_frame, text="Programar para:").pack(side="left", padx=5)

        # Fecha y hora
        date_frame = ctk.CTkFrame(schedule_frame, fg_color="transparent")
        date_frame.pack(side="left", padx=5)

        self.date_entry = ctk.CTkEntry(date_frame, width=100, placeholder_text="YYYY-MM-DD")
        self.date_entry.pack(side="left", padx=2)

        self.time_entry = ctk.CTkEntry(date_frame, width=80, placeholder_text="HH:MM")
        self.time_entry.pack(side="left", padx=2)

        self.schedule_btn = ctk.CTkButton(schedule_frame, text="Programar", command=self.schedule_download)
        self.schedule_btn.pack(side="left", padx=10)

        # Área de log
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkLabel(log_frame, text="Log de estado:").pack(anchor="w", padx=10, pady=5)

        self.log_text = ctk.CTkTextbox(log_frame, height=150)
        self.log_text.pack(padx=10, pady=5, fill="both", expand=True)

        # Historial
        history_frame = ctk.CTkFrame(main_frame)
        history_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkLabel(history_frame, text="Historial de descargas:").pack(anchor="w", padx=10, pady=5)

        # Treeview para historial
        columns = ("ID", "Title", "Artist", "Type", "Date", "Path")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)

        # Configurar columnas
        self.history_tree.heading("ID", text="ID")
        self.history_tree.column("ID", width=0, stretch=False)  # Ocultar columna ID
        self.history_tree.heading("Title", text="Title")
        self.history_tree.column("Title", width=150)
        self.history_tree.heading("Artist", text="Artist")
        self.history_tree.column("Artist", width=150)
        self.history_tree.heading("Type", text="Type")
        self.history_tree.column("Type", width=80)
        self.history_tree.heading("Date", text="Date")
        self.history_tree.column("Date", width=120)
        self.history_tree.heading("Path", text="Path")
        self.history_tree.column("Path", width=200)

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
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
                self.log_text.see("end")
        except queue.Empty:
            pass

        # Continuar procesando cada 100ms
        self.after(100, self.process_log_queue)

    def log_message(self, message):
        """Agregar mensaje al log (desde el hilo principal)"""
        self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see("end")

    def start_download(self):
        """Iniciar descarga en hilo separado"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Ingresa una URL válida")
            return

        download_type_map = {
            "Video (mejor calidad)": "video",
            "Video MP4": "video_mp4",
            "MP3 (solo video)": "mp3",
            "Playlist MP3": "playlist_mp3",
            "Playlist MP4": "playlist_mp4"
        }

        download_type = download_type_map[self.download_type.get()]

        # Determinar tipo de fuente
        source_type = "url"
        if "Playlist" in self.download_type.get():
            source_type = "playlist"

        # Deshabilitar botón
        self.download_btn.configure(state="disabled", text="Descargando...")

        # Ejecutar en hilo
        threading.Thread(target=self.download_worker, args=(url, download_type, source_type), daemon=True).start()

    def download_worker(self, url, download_type, source_type):
        """Worker para descarga"""
        try:
            downloader = Downloader(self.log_message)
            success = downloader.download_video(url, download_type, source_type)
            downloader.close()

            if success:
                self.log_message("Descarga completada")
                # Recargar historial
                self.after(0, self.load_history)
            else:
                self.log_message("Error en la descarga")

        except Exception as e:
            self.log_message(f"Error: {str(e)}")
        finally:
            # Rehabilitar botón
            self.after(0, lambda: self.download_btn.configure(state="normal", text="Descargar"))

    def schedule_download(self):
        """Programar descarga"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Ingresa una URL válida")
            return

        date_str = self.date_entry.get().strip()
        time_str = self.time_entry.get().strip()

        if not date_str or not time_str:
            messagebox.showerror("Error", "Ingresa fecha y hora")
            return

        try:
            scheduled_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

            download_type_map = {
                "Video (mejor calidad)": "video",
                "Video MP4": "video_mp4",
                "MP3 (solo video)": "mp3",
                "Playlist MP3": "playlist_mp3",
                "Playlist MP4": "playlist_mp4"
            }

            download_type = download_type_map[self.download_type.get()]

            if self.scheduler.schedule_download(url, download_type, scheduled_datetime):
                messagebox.showinfo("Éxito", f"Descarga programada para {scheduled_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
                # Limpiar campos
                self.url_entry.delete(0, "end")
                self.date_entry.delete(0, "end")
                self.time_entry.delete(0, "end")
            else:
                messagebox.showerror("Error", "No se pudo programar la descarga")

        except ValueError as e:
            messagebox.showerror("Error", f"Formato de fecha/hora inválido: {str(e)}")

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

            # Insertar en treeview (incluyendo ID oculto)
            self.history_tree.insert("", "end", values=(download_id, title or "Unknown", artist or "Unknown",
                                                      download_type, formatted_date, file_path or ""))

    def remove_download(self):
        """Eliminar descarga seleccionada del historial"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una descarga para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar esta descarga del historial?"):
            try:
                # Obtener ID de la descarga (primera columna oculta)
                item = self.history_tree.item(selection[0])
                download_id = item['values'][0]  # Asumiendo que el ID está en la primera columna

                # Eliminar de base de datos
                self.db.remove_download(download_id)

                # Recargar historial
                self.load_history()

                self.log_message("Descarga eliminada del historial")

            except Exception as e:
                messagebox.showerror("Error", f"Error eliminando descarga: {str(e)}")

    def on_tree_double_click(self, event):
        """Manejar doble clic en historial"""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            values = item['values']

            download_id = values[0]  # ID está en la primera columna
            title = values[1]
            artist = values[2]
            download_type = values[3]
            file_path = values[5]  # Path está en la columna 5

            # Solo abrir editor si es MP3
            if download_type == "mp3" and file_path and file_path.endswith('.mp3'):
                try:
                    MetadataEditor(file_path)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir el editor: {str(e)}")

    def on_closing(self):
        """Manejar cierre de aplicación"""
        if self.scheduler:
            self.scheduler.close()
        if self.db:
            self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = MP3FasterFast()
    app.mainloop()
