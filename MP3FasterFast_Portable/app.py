import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from customtkinter import CTkImage
from datetime import datetime, timedelta
import threading
import queue
from PIL import Image
from downloader import Downloader
from database import Database
from metadata import MetadataEditor
from scheduler import Scheduler
from utils import ensure_directories, validate_dependencies, load_config, save_config, MP3_DIR, BASE_DIR

# Configurar CustomTkinter con tema negro y verde neón
ctk.set_appearance_mode("dark")

# Tema personalizado negro y verde neón
custom_theme = {
    "CTk": {
        "fg_color": ["#000000", "#000000"]  # Negro fondo
    },
    "CTkFrame": {
        "fg_color": ["#0a0a0a", "#0a0a0a"],  # Negro más claro para frames
        "border_color": ["#00ff00", "#00ff00"]  # Verde neón borde
    },
    "CTkButton": {
        "fg_color": ["#00aa00", "#00ff00"],  # Verde neón
        "hover_color": ["#00ff00", "#00aa00"],  # Verde neón hover
        "border_color": ["#00ff00", "#00ff00"],  # Verde neón borde
        "text_color": ["#000000", "#ffffff"],  # Negro/Blanco texto
        "text_color_disabled": ["#666666", "#666666"]
    },
    "CTkLabel": {
        "fg_color": ["transparent", "transparent"],
        "text_color": ["#00ff00", "#00ff00"]  # Verde neón para texto
    },
    "CTkEntry": {
        "fg_color": ["#1a1a1a", "#1a1a1a"],  # Negro grisáceo
        "border_color": ["#00ff00", "#00ff00"],  # Verde neón borde
        "text_color": ["#ffffff", "#ffffff"],  # Blanco texto
        "placeholder_text_color": ["#666666", "#666666"]
    },
    "CTkTextbox": {
        "fg_color": ["#1a1a1a", "#1a1a1a"],  # Negro grisáceo
        "border_color": ["#00ff00", "#00ff00"],  # Verde neón borde
        "text_color": ["#ffffff", "#ffffff"],  # Blanco texto
        "scrollbar_button_color": ["#00ff00", "#00ff00"],  # Verde neón scrollbar
        "scrollbar_button_hover_color": ["#00aa00", "#00aa00"]
    },
    "CTkProgressBar": {
        "fg_color": ["#1a1a1a", "#1a1a1a"],  # Negro grisáceo fondo
        "progress_color": ["#00ff00", "#00ff00"]  # Verde neón progreso
    },
    "CTkScrollableFrame": {
        "fg_color": ["#0a0a0a", "#0a0a0a"],
        "border_color": ["#00ff00", "#00ff00"]
    },
    "CTkScrollbar": {
        "fg_color": ["transparent", "transparent"],
        "button_color": ["#00ff00", "#00ff00"],
        "button_hover_color": ["#00aa00", "#00aa00"]
    }
}

# Aplicar tema personalizado
for widget_type, colors in custom_theme.items():
    if hasattr(ctk, f'set_default_color_theme_for_{widget_type.lower()}'):
        getattr(ctk, f'set_default_color_theme_for_{widget_type.lower()}')(colors)

# Tema general verde neón
ctk.set_default_color_theme("green")

class MP3FasterFast(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MP3 FasterFast")
        self.geometry("900x700")
        self.resizable(False, False)

        # Cola para comunicación thread-safe
        self.log_queue = queue.Queue()

        # Cargar icono de la aplicación
        try:
            icon_path = BASE_DIR / "fasterfast.png"
            if icon_path.exists():
                # Cargar imagen como icono
                icon_photo = tk.PhotoImage(file=str(icon_path))
                self.iconphoto(True, icon_photo)
                print("Icono cargado correctamente")
            else:
                print("Icono no encontrado")
        except Exception as e:
            print(f"Error cargando icono: {str(e)}")

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
            import traceback
            traceback.print_exc()
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

        # Configurar ventana básica
        print("Iniciando MP3 FasterFast...")

        # Mensaje de bienvenida (después de configurar todo)
        self.after(100, lambda: self.log_message("🚀 MP3 FasterFast iniciado correctamente"))
        self.after(100, lambda: self.log_message("💡 Pega tus URLs de YouTube para comenzar a descargar"))

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

        # Header principal con gradiente visual
        header_frame = ctk.CTkFrame(main_frame, fg_color="#001100", border_width=2, border_color="#00ff00")
        header_frame.pack(pady=(15, 10), padx=20, fill="x")

        # Título con ícono
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(pady=10)

        ctk.CTkLabel(title_container, text="🚀",
                    font=("Arial", 24)).pack(side="left", padx=(0, 10))

        title_text = ctk.CTkFrame(title_container, fg_color="transparent")
        title_text.pack(side="left")

        ctk.CTkLabel(title_text, text="MP3 FASTERFAST",
                    font=("Arial", 20, "bold"), text_color="#00ff00").pack(anchor="w")
        ctk.CTkLabel(title_text, text="Descargador Profesional de Música y Videos",
                    font=("Arial", 10), text_color="#00aa00").pack(anchor="w")

        ctk.CTkLabel(title_container, text="🎵",
                    font=("Arial", 24)).pack(side="right", padx=(10, 0))

        # Contenedor principal horizontal
        main_container = ctk.CTkFrame(main_frame)
        main_container.pack(pady=15, padx=20, fill="both", expand=True)

        # Panel izquierdo - Controles principales
        left_panel = ctk.CTkFrame(main_container, width=280, border_width=2, border_color="#00ff00")
        left_panel.pack(side="left", fill="y", padx=(0, 15))

        # Logo en el panel izquierdo
        try:
            logo_path = BASE_DIR / "fasterfast.png"
            if logo_path.exists():
                logo_image = ctk.CTkImage(Image.open(logo_path), size=(180, 180))
                logo_label = ctk.CTkLabel(left_panel, image=logo_image, text="")
                logo_label.pack(pady=(20, 15))
        except Exception as e:
            print(f"Error cargando logo: {str(e)}")

        # Sección de configuración
        config_section = ctk.CTkFrame(left_panel, fg_color="#001100", border_width=1, border_color="#00aa00")
        config_section.pack(fill="x", padx=15, pady=(0, 15))

        config_title = ctk.CTkLabel(config_section, text="⚙️ CONFIGURACIÓN",
                                   font=("Arial", 12, "bold"), text_color="#00ff00")
        config_title.pack(pady=(10, 5))

        # Tipo de descarga
        type_label = ctk.CTkLabel(config_section, text="Formato de descarga:",
                                font=("Arial", 10, "bold"), text_color="#00ff00")
        type_label.pack(pady=(5, 3), anchor="w", padx=10)

        self.download_type = ctk.CTkComboBox(config_section,
                                           values=["🎵 MP3 (Audio)", "🎬 Video (MP4)", "📂 Playlist MP3", "📂 Playlist MP4"],
                                           state="readonly", width=220,
                                           fg_color="#1a1a1a", border_color="#00ff00")
        self.download_type.set("🎵 MP3 (Audio)")
        self.download_type.pack(pady=(0, 15), padx=10)

        # Sección de progreso
        progress_section = ctk.CTkFrame(left_panel, fg_color="#001100", border_width=1, border_color="#00aa00")
        progress_section.pack(fill="x", padx=15, pady=(0, 15))

        progress_title = ctk.CTkLabel(progress_section, text="📊 PROGRESO",
                                     font=("Arial", 12, "bold"), text_color="#00ff00")
        progress_title.pack(pady=(10, 8))

        # Barra de progreso
        progress_label = ctk.CTkLabel(progress_section, text="Estado de descarga:",
                                    font=("Arial", 10, "bold"), text_color="#00ff00")
        progress_label.pack(pady=(0, 5), anchor="w", padx=10)

        self.progress_bar = ctk.CTkProgressBar(progress_section, width=220, height=18)
        self.progress_bar.pack(pady=(0, 8), padx=10)
        self.progress_bar.set(0)

        self.progress_text = ctk.CTkLabel(progress_section, text="Esperando URLs...",
                                        font=("Arial", 9, "bold"), text_color="#00aa00")
        self.progress_text.pack(pady=(0, 10), padx=10)

        # Estado actual
        self.current_status = ctk.CTkLabel(progress_section, text="🔴 Sistema listo - Esperando acción",
                                         font=("Arial", 10, "bold"),
                                         text_color="#666666")
        self.current_status.pack(pady=(0, 10), padx=10)

        # Panel derecho - URLs y descargas
        right_panel = ctk.CTkFrame(main_container, border_width=2, border_color="#00ff00")
        right_panel.pack(side="right", fill="both", expand=True)

        # Panel superior - URLs
        urls_panel = ctk.CTkFrame(right_panel, fg_color="#001100", border_width=1, border_color="#00aa00")
        urls_panel.pack(fill="x", pady=(0, 15), padx=10)

        # Header URLs con ícono
        urls_header_frame = ctk.CTkFrame(urls_panel, fg_color="transparent")
        urls_header_frame.pack(fill="x", pady=10, padx=15)

        ctk.CTkLabel(urls_header_frame, text="🔗",
                    font=("Arial", 18)).pack(side="left")

        urls_title = ctk.CTkLabel(urls_header_frame, text="ENTRADA DE URLs",
                                 font=("Arial", 16, "bold"), text_color="#00ff00")
        urls_title.pack(side="left", padx=(10, 0))

        self.url_counter = ctk.CTkLabel(urls_header_frame, text="0 URLs",
                                       font=("Arial", 12, "bold"), text_color="#00aa00")
        self.url_counter.pack(side="right")

        # Área de URLs múltiples (ahora es la única)
        urls_frame = ctk.CTkFrame(urls_panel, fg_color="#0a0a0a")
        urls_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Instrucciones
        instructions = ctk.CTkLabel(urls_frame,
                                   text="Pega tus enlaces de YouTube aquí (uno por línea):\n\n" +
                                        "• Videos individuales\n" +
                                        "• Playlists completas\n" +
                                        "• Canales enteros\n\n" +
                                        "Ejemplos:\n" +
                                        "https://www.youtube.com/watch?v=VIDEO_ID\n" +
                                        "https://www.youtube.com/playlist?list=PLAYLIST_ID",
                                   font=("Arial", 10), text_color="#00aa00",
                                   justify="left")
        instructions.pack(pady=10, padx=10, anchor="w")

        # Área de texto para URLs
        self.urls_textbox = ctk.CTkTextbox(urls_frame, height=120)
        self.urls_textbox.pack(fill="x", padx=10, pady=(0, 10))
        self.urls_textbox.bind("<KeyRelease>", self.update_url_counter)
        self.urls_textbox.bind("<FocusIn>", self.clear_placeholder)
        self.urls_textbox.bind("<Button-1>", self.clear_placeholder)

        # Placeholder inicial
        self.placeholder_active = True
        self.set_placeholder_text()

        # Área de texto para URLs
        self.urls_textbox = ctk.CTkTextbox(urls_frame, height=140, border_width=2, border_color="#00aa00")
        self.urls_textbox.pack(fill="x", padx=10, pady=(0, 15))
        self.urls_textbox.bind("<KeyRelease>", self.update_url_counter)
        self.urls_textbox.bind("<FocusIn>", self.clear_placeholder)
        self.urls_textbox.bind("<Button-1>", self.clear_placeholder)

        # Placeholder inicial
        self.placeholder_active = True
        self.set_placeholder_text()

        # Información de ayuda
        help_frame = ctk.CTkFrame(urls_frame, fg_color="#001100", border_width=1, border_color="#00aa00")
        help_frame.pack(fill="x", padx=10, pady=(0, 15))

        help_left = ctk.CTkFrame(help_frame, fg_color="transparent")
        help_left.pack(side="left", fill="x", expand=True, padx=10, pady=5)

        ctk.CTkLabel(help_left, text="💡 Múltiples URLs separadas por líneas",
                    font=("Arial", 9), text_color="#00aa00").pack(anchor="w")

        help_right = ctk.CTkFrame(help_frame, fg_color="transparent")
        help_right.pack(side="right", fill="x", expand=True, padx=10, pady=5)

        ctk.CTkLabel(help_right, text="📊 Descarga secuencial automática",
                    font=("Arial", 9), text_color="#00aa00").pack(anchor="e")

        # Botones de acción con mejor diseño
        btns_frame = ctk.CTkFrame(urls_frame, fg_color="transparent")
        btns_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Botón principal de descarga
        self.download_btn = ctk.CTkButton(btns_frame, text="🚀 INICIAR DESCARGAS",
                                         command=self.start_multiple_downloads, height=45,
                                         font=("Arial", 12, "bold"),
                                         fg_color="#00ff00", hover_color="#00aa00",
                                         text_color="#000000")
        self.download_btn.pack(fill="x", pady=(0, 10))

        # Botones secundarios
        secondary_btns = ctk.CTkFrame(btns_frame, fg_color="transparent")
        secondary_btns.pack(fill="x")

        self.clear_btn = ctk.CTkButton(secondary_btns, text="🗑️ LIMPIAR",
                                      command=self.clear_urls, height=35,
                                      fg_color="#1a1a1a", border_width=2, border_color="#00aa00",
                                      hover_color="#00aa00")
        self.clear_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.paste_btn = ctk.CTkButton(secondary_btns, text="📋 PEGAR",
                                      command=self.paste_urls, height=35,
                                      fg_color="#1a1a1a", border_width=2, border_color="#00aa00",
                                      hover_color="#00aa00")
        self.paste_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # Panel inferior - Log y Historial
        bottom_panel = ctk.CTkFrame(main_frame, fg_color="#001100", border_width=1, border_color="#00aa00")
        bottom_panel.pack(pady=(10, 20), padx=20, fill="both", expand=True)

        # Área de log
        log_section = ctk.CTkFrame(bottom_panel, fg_color="#0a0a0a")
        log_section.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        log_header = ctk.CTkFrame(log_section, fg_color="transparent")
        log_header.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(log_header, text="📋",
                    font=("Arial", 14)).pack(side="left")

        ctk.CTkLabel(log_header, text="LOG DE ACTIVIDAD",
                    font=("Arial", 14, "bold"), text_color="#00ff00").pack(side="left", padx=(8, 0))

        ctk.CTkButton(log_header, text="🗑️ LIMPIAR LOG", width=120, height=30,
                     command=self.clear_log, fg_color="#1a1a1a", border_width=1,
                     border_color="#00aa00", hover_color="#00aa00").pack(side="right")

        self.log_text = ctk.CTkTextbox(log_section, height=100, wrap="word",
                                      border_width=1, border_color="#00aa00",
                                      fg_color="#000000")
        self.log_text.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        self.log_text.configure(state="disabled")  # Solo lectura

        # Historial
        history_section = ctk.CTkFrame(bottom_panel, fg_color="#0a0a0a")
        history_section.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Header del historial
        history_header = ctk.CTkFrame(history_section, fg_color="transparent")
        history_header.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(history_header, text="📚",
                    font=("Arial", 14)).pack(side="left")

        ctk.CTkLabel(history_header, text="HISTORIAL DE DESCARGAS",
                    font=("Arial", 14, "bold"), text_color="#00ff00").pack(side="left", padx=(8, 0))

        self.history_count = ctk.CTkLabel(history_header, text="0 archivos",
                                         font=("Arial", 11), text_color="#00aa00")
        self.history_count.pack(side="right", padx=(0, 10))

        ctk.CTkButton(history_header, text="🔄 ACTUALIZAR", width=120, height=30,
                     command=self.load_history, fg_color="#1a1a1a", border_width=1,
                     border_color="#00aa00", hover_color="#00aa00").pack(side="right", padx=(0, 10))
        ctk.CTkButton(history_header, text="Actualizar", width=90, height=25,
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
                    if hasattr(self, 'log_text') and self.log_text:
                        self.log_text.configure(state="normal")
                        self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
                        self.log_text.configure(state="disabled")
                        self.log_text.see("end")
                except queue.Empty:
                    break
        except Exception as e:
            # Si hay error, intentar log normal
            try:
                if hasattr(self, 'log_message'):
                    self.log_message(f"Error procesando cola: {str(e)}")
            except:
                print(f"Error en process_log_queue: {str(e)}")

        # Continuar procesando cada 100ms (solo si la app sigue activa)
        try:
            if hasattr(self, 'tk') and self.tk:
                self.after(100, self.process_log_queue)
        except Exception as e:
            # Si after falla, detener el procesamiento
            print(f"Deteniendo process_log_queue: {str(e)}")

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
        self.log_message("Registro limpiado")

    def start_multiple_downloads(self):
        """Iniciar descargas múltiples"""
        if self.placeholder_active:
            messagebox.showwarning("Advertencia", "Ingresa URLs válidas para descargar")
            return

        urls_text = self.urls_textbox.get("0.0", "end").strip()
        if not urls_text:
            messagebox.showwarning("Advertencia", "El área de URLs está vacía")
            return

        # Procesar y filtrar URLs válidas
        lines = [line.strip() for line in urls_text.split('\n') if line.strip()]
        valid_urls = [url for url in lines if 'youtube.com' in url or 'youtu.be' in url]

        if not valid_urls:
            messagebox.showerror("Error", "No se encontraron URLs válidas de YouTube")
            return

        # Confirmar descarga masiva
        if len(valid_urls) > 1:
            confirm = messagebox.askyesno("Confirmar descarga masiva",
                                        f"Se descargarán {len(valid_urls)} elementos.\n¿Continuar?")
            if not confirm:
                return

        # Inicializar progreso
        self.total_downloads = len(valid_urls)
        self.completed_downloads = 0
        self.failed_downloads = 0
        self.current_download = 0

        self.progress_bar.set(0)
        self.progress_text.configure(text="Iniciando...")
        self.current_status.configure(text="Estado: Procesando", text_color="orange")

        # Mapear tipos de descarga
        download_type_map = {
            "MP3 (Audio)": "mp3",
            "Video (MP4)": "video_mp4",
            "Playlist MP3": "playlist_mp3",
            "Playlist MP4": "playlist_mp4"
        }

        download_type = download_type_map[self.download_type.get()]

        # Determinar tipo de fuente (si es playlist, usar ese tipo)
        source_type = "playlist" if "Playlist" in download_type else "url"

        # Deshabilitar botón
        self.download_btn.configure(state="disabled", text="⏳ Descargando...")

        # Ejecutar en hilo
        threading.Thread(target=self.multiple_downloads_worker,
                        args=(valid_urls, download_type, source_type), daemon=True).start()

    def multiple_downloads_worker(self, urls, download_type, source_type):
        """Worker para múltiples descargas con progreso en tiempo real"""
        try:
            downloader = Downloader(self.log_message)

            self.log_message(f"Iniciando descarga de {len(urls)} elementos...")

            for i, url in enumerate(urls, 1):
                self.current_download = i

                # Actualizar progreso
                progress = (i - 1) / len(urls)
                self.after(0, lambda p=progress: self.progress_bar.set(p))
                self.after(0, lambda: self.progress_text.configure(text=f"{i}/{len(urls)} completado"))
                self.after(0, lambda u=url: self.current_status.configure(text=f"📥 Descargando: {u[:35]}...", text_color="blue"))

                self.log_message(f"📥 Iniciando descarga {i}/{len(urls)}: {url[:50]}...")

                try:
                    success = downloader.download_video(url, download_type, source_type)
                    if success:
                        self.completed_downloads += 1
                        self.log_message(f"✅ ¡Completado! {url[:50]}...")
                    else:
                        self.failed_downloads += 1
                        self.log_message(f"❌ Error en descarga: {url[:50]}...")
                except Exception as e:
                    self.failed_downloads += 1
                    self.log_message(f"💥 Error crítico: {url[:50]} - {str(e)}")

                # Pequeña pausa para actualizar UI
                import time
                time.sleep(0.1)

            downloader.close()

            # Recargar historial
            self.after(0, self.load_history)

            # Actualizar progreso final
            self.after(0, lambda: self.progress_bar.set(1.0))
            self.after(0, lambda: self.progress_text.configure(text="Completado"))
            self.after(0, lambda: self.current_status.configure(text="Estado: Finalizado", text_color="green"))

            # Resumen final
            if self.failed_downloads == 0:
                self.log_message(f"🎉 ¡PROCESO COMPLETADO! Todas las {self.completed_downloads} descargas fueron exitosas")
            else:
                self.log_message(f"⚠️ Proceso terminado: {self.completed_downloads} exitosas, {self.failed_downloads} fallidas")

        except Exception as e:
            self.after(0, lambda: self.current_status.configure(text="Estado: Error", text_color="red"))
            self.log_message(f"💥 Error general: {str(e)}")
        finally:
            # Rehabilitar botón
            self.after(0, lambda: self.download_btn.configure(state="normal", text="🚀 Iniciar Descargas"))

    def set_placeholder_text(self):
        """Establecer texto placeholder en el área de URLs múltiples"""
        if self.placeholder_active:
            self.urls_textbox.delete("0.0", "end")
            self.urls_textbox.insert("0.0", "Pega aquí las URLs de YouTube (una por línea)...\n\nEjemplos:\n• https://www.youtube.com/watch?v=dQw4w9WgXcQ\n• https://youtu.be/dQw4w9WgXcQ\n• https://www.youtube.com/playlist?list=PLrAXtmRdnEQy4qtr5GrLOg0J8jIvT8Lr")
            self.urls_textbox.configure(text_color="gray70")

    def clear_placeholder(self, event=None):
        """Limpiar placeholder cuando el usuario empieza a escribir"""
        if self.placeholder_active:
            self.urls_textbox.delete("0.0", "end")
            self.urls_textbox.configure(text_color=("gray10", "gray90"))  # Color normal
            self.placeholder_active = False

    def clear_urls(self):
        """Limpiar el área de URLs múltiples"""
        self.urls_textbox.delete("0.0", "end")
        self.placeholder_active = True
        self.set_placeholder_text()
        self.update_url_counter()
        self.log_message("URLs limpiadas")

    def paste_urls(self):
        """Pegar URLs desde el portapapeles"""
        try:
            import pyperclip
            clipboard_content = pyperclip.paste()
            if self.placeholder_active:
                self.clear_placeholder()
            current_content = self.urls_textbox.get("0.0", "end").strip()
            if current_content and not current_content.endswith("\n"):
                self.urls_textbox.insert("end", "\n")
            self.urls_textbox.insert("end", clipboard_content)
            self.update_url_counter()
        except ImportError:
            # Fallback si no hay pyperclip
            try:
                clipboard_content = self.clipboard_get()
                if self.placeholder_active:
                    self.clear_placeholder()
                current_content = self.urls_textbox.get("0.0", "end").strip()
                if current_content and not current_content.endswith("\n"):
                    self.urls_textbox.insert("end", "\n")
                self.urls_textbox.insert("end", clipboard_content)
                self.update_url_counter()
            except:
                self.log_message("❌ Error accediendo al portapapeles")
        except Exception as e:
            self.log_message(f"❌ Error pegando URLs: {str(e)}")

    def update_url_counter(self, event=None):
        """Actualizar contador de URLs en tiempo real"""
        if self.placeholder_active:
            self.url_counter.configure(text="0 URLs")
            return

        urls_text = self.urls_textbox.get("0.0", "end").strip()

        if urls_text:
            # Filtrar URLs válidas (contienen youtube.com o youtu.be)
            lines = [line.strip() for line in urls_text.split('\n') if line.strip()]
            valid_urls = [url for url in lines if 'youtube.com' in url or 'youtu.be' in url]
            count = len(valid_urls)

            self.url_counter.configure(text=f"{count} URLs")
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
                    self.log_message("Descarga eliminada del historial")
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
                        self.log_message(f"Editando metadatos: {title}")
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
