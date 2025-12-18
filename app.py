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

# Configurar CustomTkinter con tema oscuro simplificado
try:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")  # Usar tema verde integrado
    print("Tema CustomTkinter configurado correctamente")
except Exception as e:
    print(f"Error configurando tema: {str(e)}")
    # Fallback a configuración básica
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

class MP3FasterFast(ctk.CTk):
    def __init__(self):
        try:
            super().__init__()
            print("Ventana principal creada correctamente")
        except Exception as e:
            print(f"Error creando ventana principal: {str(e)}")
            raise

        self.title("MP3 FasterFast")
        self.geometry("900x700")
        self.resizable(False, False)
        print("Configuración básica de ventana completada")

        # Cola para comunicación thread-safe
        self.log_queue = queue.Queue()

        # Cargar icono de la aplicación
        try:
            icon_path = BASE_DIR / "logo-fasterfast.png"
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

        # Inicializar downloader
        self.downloader = Downloader(self.log_message)
        print("Downloader inicializado")

        # Inicializar valores por defecto antes de crear widgets
        self.default_quality = 'Mejor'
        self.default_format = 'MP3 (Audio)'
        print("Valores por defecto inicializados")

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

        # Cargar configuraciones después de crear widgets
        try:
            self.load_settings()
            print("Configuraciones cargadas")
        except Exception as e:
            print(f"Error cargando configuraciones: {str(e)}")

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

        # Mensaje de bienvenida rápido
        self.after(50, lambda: self.log_message("[READY] Listo para descargar"))

        # Iniciar procesamiento de cola de logs
        self.after(100, self.process_log_queue)

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
        print("Creando frame principal...")
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        print("Frame principal creado")


        # Contenedor principal horizontal
        print("Creando contenedor principal...")
        main_container = ctk.CTkFrame(main_frame)
        main_container.pack(pady=(20, 10), padx=20, fill="both", expand=True)

        # Panel izquierdo - Controles principales
        print("Creando panel izquierdo...")
        left_panel = ctk.CTkFrame(main_container, width=280)
        left_panel.pack(side="left", fill="y", padx=(0, 15))
        print("Panel izquierdo creado")

        # Logo en el panel izquierdo
        print("Cargando logo...")
        try:
            logo_path = BASE_DIR / "logo-fasterfast.png"
            print(f"Buscando logo en: {logo_path}")
            if logo_path.exists():
                print("Logo encontrado, cargando imagen...")
                logo_image = ctk.CTkImage(Image.open(logo_path), size=(180, 180))
                logo_label = ctk.CTkLabel(left_panel, image=logo_image, text="")
                logo_label.pack(pady=(20, 15))
                print("Logo cargado exitosamente")
            else:
                print(f"Logo NO encontrado en {logo_path}")
                # Logo de texto como respaldo
                logo_label = ctk.CTkLabel(left_panel, text="🎵\nMP3\nFASTERFAST",
                                         font=("Arial", 20, "bold"), text_color="#00ff00")
                logo_label.pack(pady=(20, 15))
        except Exception as e:
            print(f"Error cargando logo: {str(e)}")
            # Logo de texto como respaldo
            logo_label = ctk.CTkLabel(left_panel, text="🎵\nMP3\nFASTERFAST",
                                     font=("Arial", 20, "bold"), text_color="#00ff00")
            logo_label.pack(pady=(20, 15))

        # Sección de configuración
        config_section = ctk.CTkFrame(left_panel, fg_color="#001100", border_width=1, border_color="#00aa00")
        config_section.pack(fill="x", padx=15, pady=(0, 15))

        config_title = ctk.CTkLabel(config_section, text="[CONFIGURACION]",
                                   font=("Arial", 12, "bold"))
        config_title.pack(pady=(10, 5))

        # Tipo de descarga
        type_label = ctk.CTkLabel(config_section, text="Formato de descarga:",
                                font=("Arial", 10, "bold"))
        type_label.pack(pady=(5, 3), anchor="w", padx=10)

        self.download_type = ctk.CTkComboBox(config_section,
                                           values=["[MP3] Audio", "[MP4] Video", "[PLAYLIST MP3]", "[PLAYLIST MP4]"],
                                           state="readonly", width=220)
        self.download_type.set("[MP3] Audio")
        self.download_type.pack(pady=(0, 10), padx=10)

        # Configuración de calidad por defecto (se actualiza dinámicamente)
        quality_label = ctk.CTkLabel(config_section, text="Calidad por defecto:",
                                   font=("Arial", 10, "bold"), text_color="#00ff00")
        quality_label.pack(pady=(5, 3), anchor="w", padx=10)

        self.default_quality_combo = ctk.CTkComboBox(config_section,
                                                   values=self._get_quality_options(),
                                                   width=200)
        self.default_quality_combo.set(self.default_quality)
        self.default_quality_combo.pack(pady=(0, 10), padx=10)

        # Actualizar calidad cuando cambia el formato
        self.download_type.bind("<<ComboboxSelected>>", self._update_quality_options)

        # Botón guardar configuración
        save_config_btn = ctk.CTkButton(config_section, text="💾 Guardar Config",
                                       command=self.save_settings, height=30,
                                       fg_color="#004400", border_width=1, border_color="#00aa00")
        save_config_btn.pack(pady=(5, 10), padx=10)

        # Sección de progreso
        progress_section = ctk.CTkFrame(left_panel)
        progress_section.pack(fill="x", padx=15, pady=(0, 15))

        progress_title = ctk.CTkLabel(progress_section, text="[PROGRESO]",
                                     font=("Arial", 12, "bold"))
        progress_title.pack(pady=(10, 8))

        # Barra de progreso
        progress_label = ctk.CTkLabel(progress_section, text="Estado de descarga:",
                                    font=("Arial", 10, "bold"))
        progress_label.pack(pady=(0, 5), anchor="w", padx=10)

        self.progress_bar = ctk.CTkProgressBar(progress_section, width=220, height=18)
        self.progress_bar.pack(pady=(0, 8), padx=10)
        self.progress_bar.set(0)

        self.progress_text = ctk.CTkLabel(progress_section, text="Esperando URLs...",
                                        font=("Arial", 9, "bold"))
        self.progress_text.pack(pady=(0, 10), padx=10)


        # Indicador de canción actual
        self.current_song_label = ctk.CTkLabel(progress_section,
                                             text="Cancion actual: Ninguna",
                                             font=("Arial", 9))
        self.current_song_label.pack(pady=(0, 5), padx=10, anchor="w")

        # Progreso de canción individual
        self.song_progress_label = ctk.CTkLabel(progress_section,
                                              text="Progreso cancion: 0%",
                                              font=("Arial", 9))
        self.song_progress_label.pack(pady=(0, 10), padx=10, anchor="w")

        # Panel derecho - URLs y descargas
        print("Creando panel derecho...")
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", expand=True)
        print("Panel derecho creado")

        # Panel superior - URLs
        urls_panel = ctk.CTkFrame(right_panel)
        urls_panel.pack(fill="x", pady=(0, 15), padx=10)

        # Header URLs con ícono
        urls_header_frame = ctk.CTkFrame(urls_panel, fg_color="transparent")
        urls_header_frame.pack(fill="x", pady=10, padx=15)

        ctk.CTkLabel(urls_header_frame, text="[URL]",
                    font=("Arial", 14, "bold")).pack(side="left")

        urls_title = ctk.CTkLabel(urls_header_frame, text="ENTRADA DE URLs",
                                 font=("Arial", 16, "bold"))
        urls_title.pack(side="left", padx=(10, 0))


        # Área de URL simple
        url_frame = ctk.CTkFrame(urls_panel)
        url_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Instrucción simple
        instruction = ctk.CTkLabel(url_frame, text="Pega la URL de YouTube:",
                                 font=("Arial", 12, "bold"))
        instruction.pack(pady=(10, 5), anchor="w", padx=10)

        # Frame horizontal: URL + Botón
        input_frame = ctk.CTkFrame(url_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Campo de URL simple
        self.url_entry = ctk.CTkEntry(input_frame, placeholder_text="https://www.youtube.com/watch?v=...",
                                    height=40, font=("Arial", 11))
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Botón de descargar al lado derecho
        self.download_single_btn = ctk.CTkButton(input_frame, text="[DESCARGAR]",
                                               command=self.download_single_url, height=40,
                                               font=("Arial", 12, "bold"))
        self.download_single_btn.pack(side="right", padx=(0, 0))

        # Información de ejemplo
        example = ctk.CTkLabel(url_frame,
                             text="Ejemplo: https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                             font=("Arial", 9), text_color="#00aa00")
        example.pack(pady=(0, 10), anchor="w", padx=10)




        # SECCIÓN DE DESCARGAS ACTIVAS
        downloads_section = ctk.CTkFrame(urls_panel, fg_color="#001100", border_width=1, border_color="#00aa00")
        downloads_section.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        downloads_header = ctk.CTkFrame(downloads_section, fg_color="transparent")
        downloads_header.pack(fill="x", pady=8, padx=10)

        ctk.CTkLabel(downloads_header, text="📥",
                    font=("Arial", 16)).pack(side="left")

        ctk.CTkLabel(downloads_header, text="DESCARGAS ACTIVAS",
                    font=("Arial", 14, "bold"), text_color="#00ff00").pack(side="left", padx=(8, 0))

        # Frame para la lista de descargas activas
        self.active_downloads_frame = ctk.CTkScrollableFrame(downloads_section, height=200)
        self.active_downloads_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Diccionario para trackear descargas activas
        self.active_downloads = {}  # url -> widget_info

        # Panel inferior - Log y Historial
        bottom_panel = ctk.CTkFrame(main_frame)
        bottom_panel.pack(pady=(10, 20), padx=20, fill="both", expand=True)

        # Área de log
        log_section = ctk.CTkFrame(bottom_panel)
        log_section.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        log_header = ctk.CTkFrame(log_section, fg_color="transparent")
        log_header.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(log_header, text="📋",
                    font=("Arial", 14)).pack(side="left")

        ctk.CTkLabel(log_header, text="LOG DE ACTIVIDAD",
                    font=("Arial", 14, "bold")).pack(side="left", padx=(8, 0))

        # Botones para el log
        log_buttons_frame = ctk.CTkFrame(log_header, fg_color="transparent")
        log_buttons_frame.pack(side="right")

        ctk.CTkButton(log_buttons_frame, text="[COPIAR]", width=100, height=30,
                     command=self.copy_log).pack(side="left", padx=(0, 5))

        ctk.CTkButton(log_buttons_frame, text="[LIMPIAR]", width=100, height=30,
                     command=self.clear_log).pack(side="right")

        self.log_text = ctk.CTkTextbox(log_section, height=100, wrap="word")
        self.log_text.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        # Permitir selección y copia, pero no edición manual
        self.log_text.configure(state="normal")  # Permitir selección
        self.log_text.bind("<Key>", lambda e: "break")  # Bloquear escritura manual
        self.log_text.bind("<Control-a>", self.select_all_log)  # Seleccionar todo

        # Historial
        history_section = ctk.CTkFrame(bottom_panel)
        history_section.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Header del historial
        history_header = ctk.CTkFrame(history_section, fg_color="transparent")
        history_header.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(history_header, text="📚",
                    font=("Arial", 14)).pack(side="left")

        ctk.CTkLabel(history_header, text="HISTORIAL DE DESCARGAS",
                    font=("Arial", 14, "bold")).pack(side="left", padx=(8, 0))

        self.history_count = ctk.CTkLabel(history_header, text="0 archivos",
                                         font=("Arial", 11))
        self.history_count.pack(side="right", padx=(0, 10))

        ctk.CTkButton(history_header, text="[ACTUALIZAR]", width=120, height=30,
                     command=self.load_history).pack(side="right", padx=(0, 10))
        ctk.CTkButton(history_header, text="Actualizar", width=90, height=25,
                     command=self.load_history).pack(side="right", padx=(5, 0))
        self.history_count = ctk.CTkLabel(history_header, text="0 elementos",
                                         font=("Arial", 10), text_color="gray70")
        self.history_count.pack(side="right")

        # Frame para el contenido del historial
        history_frame = ctk.CTkFrame(history_section)
        history_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

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
        # Verificar si log_text existe (para evitar errores durante inicialización)
        if not hasattr(self, 'log_text') or self.log_text is None:
            print(f"LOG: {message}")  # Fallback a consola
            return

        try:
            self.log_text.configure(state="normal")
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.log_text.insert("end", f"[{timestamp}] {message}\n")
            self.log_text.configure(state="normal")  # Mantener editable para copia
            self.log_text.see("end")  # Scroll automático al final
        except Exception as e:
            print(f"Error en log_message: {e}")
            print(f"LOG: {message}")  # Fallback a consola

    def clear_log(self):
        """Limpiar el registro de actividad"""
        self.log_text.configure(state="normal")
        self.log_text.delete("0.0", "end")
        self.log_text.configure(state="normal")  # Mantener editable para copia
        self.log_message("[CLEAR] Registro limpiado")

    def copy_log(self):
        """Copiar todo el contenido del log al portapapeles"""
        try:
            self.log_text.configure(state="normal")
            log_content = self.log_text.get("0.0", "end").strip()

            # Intentar usar pyperclip primero
            try:
                import pyperclip
                pyperclip.copy(log_content)
                self.log_message("[OK] [LOG] Log copiado al portapapeles (pyperclip)")
            except ImportError:
                # Fallback al portapapeles de tkinter
                try:
                    self.clipboard_clear()
                    self.clipboard_append(log_content)
                    self.log_message("[OK] [LOG] Log copiado al portapapeles (tkinter)")
                except Exception as e:
                    self.log_message(f"[CANCEL] [LOG] Error copiando al portapapeles: {str(e)}")

            self.log_text.configure(state="normal")

        except Exception as e:
            self.log_message(f"[CANCEL] [LOG] Error copiando log: {str(e)}")

    def select_all_log(self, event=None):
        """Seleccionar todo el contenido del log"""
        self.log_text.tag_add("sel", "1.0", "end")
        return "break"

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

                # Actualizar progreso general
                progress = (i - 1) / len(urls)
                self.after(0, lambda p=progress: self.progress_bar.set(p))
                self.after(0, lambda: self.progress_text.configure(text=f"{i}/{len(urls)} completado"))

                # Actualizar canción actual
                self.after(0, lambda u=url: self.current_song_label.configure(text=f"Canción actual: {u[:30]}..."))
                self.after(0, lambda: self.song_progress_label.configure(text="Progreso canción: Iniciando..."))
                self.after(0, lambda u=url: self.current_status.configure(text=f"📥 Descargando: {u[:35]}...", text_color="blue"))

                self.log_message(f"[DOWNLOAD] Iniciando descarga {i}/{len(urls)}: {url[:50]}...")

                try:
                    # Simular progreso de canción (0% -> descargando -> 100%)
                    self.after(0, lambda: self.song_progress_label.configure(text="Progreso canción: 0%"))

                    success = downloader.download_video(url, download_type, source_type)

                    if success:
                        self.completed_downloads += 1
                        self.after(0, lambda: self.song_progress_label.configure(text="Progreso canción: 100% ✅"))
                        self.after(0, lambda: self.current_song_label.configure(text="Canción actual: Completada ✅"))
                        self.log_message(f"[OK] ¡Completado! {url[:50]}...")
                    else:
                        self.failed_downloads += 1
                        self.after(0, lambda: self.song_progress_label.configure(text="Progreso canción: Error ❌"))
                        self.log_message(f"[CANCEL] Error en descarga: {url[:50]}...")
                except Exception as e:
                    self.failed_downloads += 1
                    self.after(0, lambda: self.song_progress_label.configure(text="Progreso canción: Error ❌"))
                    self.log_message(f"[CRASH] Error crítico: {url[:50]} - {str(e)}")

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
            self.log_message(f"[CRASH] Error general: {str(e)}")
        finally:
            # Rehabilitar botón
            self.after(0, lambda: self.download_btn.configure(state="normal", text="🚀 Iniciar Descargas"))




    def download_single_url(self):
        """Descargar una sola URL con indicadores visuales"""
        self.log_message("[INFO] Iniciando proceso de descarga...")

        url = self.url_entry.get().strip()
        self.log_message(f"📝 URL obtenida: {url[:50]}{'...' if len(url) > 50 else ''}")

        if not url:
            self.log_message("[CANCEL] ERROR: No se encontró URL. Pega una URL primero")
            return

        if not ('youtube.com' in url or 'youtu.be' in url):
            self.log_message("[CANCEL] ERROR: Solo URLs de YouTube son soportadas")
            return

        self.log_message("[OK] URL válida detectada")
        self.log_message("[BUILD] Creando widget de descarga...")

        # Crear widget visual para esta descarga
        download_widget = self.create_download_widget(url)
        self.log_message("[OK] Widget de descarga creado")

        # Deshabilitar botón mientras descarga
        self.download_single_btn.configure(state="disabled", text="⏳ DESCARGANDO...")
        self.log_message("[LOCK] Botón de descarga deshabilitado")

        # Iniciar descarga en thread separado
        import threading
        self.log_message("[START] Iniciando thread de descarga...")
        thread = threading.Thread(target=self._download_single_thread, args=(url, download_widget))
        thread.daemon = True
        thread.start()
        self.log_message("[OK] Thread de descarga iniciado")

    def create_download_widget(self, url):
        """Crear widget visual avanzado para mostrar progreso de descarga"""
        # Frame principal para esta descarga
        download_frame = ctk.CTkFrame(self.active_downloads_frame, fg_color="#0a0a0a",
                                     border_width=2, border_color="#00ff00")
        download_frame.pack(fill="x", pady=5, padx=5)

        # Frame superior: Imagen + Información
        top_frame = ctk.CTkFrame(download_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=(10, 5))

        # Imagen del thumbnail (izquierda)
        thumbnail_label = ctk.CTkLabel(top_frame, text="🎵", font=("Arial", 40), width=80, height=60)
        thumbnail_label.pack(side="left", padx=(0, 10))

        # Información del video (derecha)
        info_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)

        # Título del video
        title_label = ctk.CTkLabel(info_frame, text="Cargando título...",
                                 font=("Arial", 12, "bold"), text_color="#ffffff",
                                 anchor="w", justify="left", wraplength=200)
        title_label.pack(fill="x", pady=(0, 3))

        # URL del video
        url_label = ctk.CTkLabel(info_frame, text=f"URL: {url[:60]}{'...' if len(url) > 60 else ''}",
                               font=("Arial", 9), text_color="#00aa00",
                               anchor="w", justify="left")
        url_label.pack(fill="x", pady=(0, 5))

        # Frame inferior: Controles y progreso
        bottom_frame = ctk.CTkFrame(download_frame, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Calidad (cambia según formato seleccionado)
        quality_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        quality_frame.pack(fill="x", pady=(0, 5))

        quality_label = ctk.CTkLabel(quality_frame, text="Calidad:",
                                   font=("Arial", 9), text_color="#ffffff")
        quality_label.pack(side="left", padx=(0, 5))

        # Calidad dinámica según formato
        quality_options = self._get_quality_options()

        quality_combo = ctk.CTkComboBox(quality_frame,
                                      values=quality_options,
                                      width=80, height=25,
                                      font=("Arial", 8))
        quality_combo.set(self.default_quality)
        quality_combo.pack(side="left")

        # Barra de progreso
        progress_bar = ctk.CTkProgressBar(bottom_frame, width=400, height=18)
        progress_bar.pack(pady=(5, 3))
        progress_bar.set(0)

        # Estado y controles
        status_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        status_frame.pack(fill="x")

        # Estado
        status_label = ctk.CTkLabel(status_frame, text="⏳ Preparando descarga...",
                                  font=("Arial", 9), text_color="#00aaff")
        status_label.pack(side="left")

        # Botón cancelar
        cancel_btn = ctk.CTkButton(status_frame, text="❌", width=30, height=25,
                                 command=lambda: self.cancel_download(url))
        cancel_btn.pack(side="right")

        # Guardar referencias
        widget_info = {
            'frame': download_frame,
            'thumbnail': thumbnail_label,
            'title': title_label,
            'url_label': url_label,
            'progress': progress_bar,
            'status': status_label,
            'quality': quality_combo,
            'cancel_btn': cancel_btn,
            'url': url
        }

        self.active_downloads[url] = widget_info
        return widget_info

    def _download_single_thread(self, url, widget_info):
        """Thread para descargar una sola URL"""
        try:
            print("🔥 [DEBUG] Thread de descarga iniciado")
            self.log_message("[DEBUG] Thread de descarga iniciado")
            print("🔥 [SEARCH] Obteniendo información del video...")
            self.log_message("[SEARCH] Obteniendo información del video...")
            # Actualizar estado
            self.after(0, lambda: widget_info['status'].configure(text="🔍 Obteniendo información...", text_color="#ffff00"))
            print("🔥 [DEBUG] Estado actualizado a 'Obteniendo información...'")
            self.log_message("[DEBUG] Estado actualizado a 'Obteniendo información...'")

            # Obtener información del video
            print("🔥 [DEBUG] Llamando a get_video_info...")
            self.log_message("[DEBUG] Llamando a get_video_info...")
            video_info = self.get_video_info(url)
            print(f"🔥 [DEBUG] get_video_info retornó: {video_info is not None}")
            self.log_message(f"[DEBUG] get_video_info retornó: {video_info is not None}")
            if video_info:
                print("🔥 [DEBUG] Video info es válido, procesando...")
                self.log_message("[DEBUG] Video info es válido, procesando...")
                title = video_info.get('title', 'Título desconocido')
                print(f"🔥 [TITLE] Título obtenido: {title[:50]}{'...' if len(title) > 50 else ''}")
                self.log_message(f"[TITLE] Título obtenido: {title[:50]}{'...' if len(title) > 50 else ''}")
                # Actualizar título
                self.after(0, lambda: widget_info['title'].configure(text=title))
                print("🔥 [DEBUG] Título actualizado en widget")
                self.log_message("[DEBUG] Título actualizado en widget")

                # Cambiar estado a "Procesando..."
                self.after(0, lambda: widget_info['status'].configure(text="⚙️ Procesando información...", text_color="#00ff00"))
                print("🔥 [DEBUG] Estado cambiado a 'Procesando información...'")
                self.log_message("[DEBUG] Estado cambiado a 'Procesando información...'")

                # Actualizar thumbnail si está disponible
                thumbnail_url = video_info.get('thumbnail')
                print(f"🔥 [DEBUG] Thumbnail URL: {thumbnail_url}")
                self.log_message(f"[DEBUG] Thumbnail URL: {thumbnail_url}")
                if thumbnail_url:
                    print("🔥 [IMAGE] Thumbnail encontrado, cargando...")
                    self.log_message("[IMAGE] Thumbnail encontrado, cargando...")
                    self.load_thumbnail(widget_info, thumbnail_url)
                    print("🔥 [DEBUG] load_thumbnail completado")
                    self.log_message("[DEBUG] load_thumbnail completado")
                else:
                    print("🔥 [INFO] No se encontró thumbnail, continuando sin imagen")
                    self.log_message("[INFO] No se encontró thumbnail, continuando sin imagen")
                print("🔥 [DEBUG] Procesamiento de video_info completado")
                self.log_message("[DEBUG] Procesamiento de video_info completado")
            else:
                self.log_message("[CANCEL] Error obteniendo información del video")
                self.after(0, lambda: widget_info['title'].configure(text="Error obteniendo título"))
                self.log_message("[DEBUG] Error procesado, terminando thread")

            # Obtener tipo de descarga del combo principal
            download_type = self.download_type.get()
            self.log_message(f"[CONFIG] Tipo de descarga seleccionado: {download_type}")

            quality = widget_info['quality'].get()
            self.log_message(f"[INFO] Calidad seleccionada: {quality}")

            if download_type == "[MP3] Audio":
                source_type = "url"
                # Configurar calidad de audio - "Mejor" usa 320kbps
                if quality == "Mejor" or quality == "320kbps":
                    download_format = "mp3_320"
                elif quality == "256kbps":
                    download_format = "mp3_256"
                elif quality == "192kbps":
                    download_format = "mp3_192"
                elif quality == "128kbps":
                    download_format = "mp3_128"
                else:
                    # Fallback por defecto
                    download_format = "mp3_320"
                self.log_message(f"[AUDIO] Configurado para MP3 {quality} -> {download_format}")
            elif download_type == "🎬 Video (MP4)":
                source_type = "url"
                download_format = "video"
                # Usar calidad seleccionada
                if quality != "Mejor":
                    download_format = f"video_{quality.lower()}"
                    self.log_message(f"[VIDEO] Configurado para video {quality}")
                else:
                    self.log_message("[VIDEO] Configurado para video mejor calidad")
            else:
                source_type = "url"
                download_format = "mp3"
                self.log_message("[AUDIO] Configurado por defecto a MP3")

            # Actualizar progreso
            print("🔥 [DEBUG] Actualizando progreso a 20%...")
            self.log_message("[DEBUG] Actualizando progreso a 20%...")
            self.after(0, lambda: widget_info['progress'].set(0.2))
            self.after(0, lambda: widget_info['status'].configure(text="[DOWNLOAD] Iniciando descarga...", text_color="#00aaff"))
            print("🔥 [START] Iniciando descarga con yt-dlp...")
            self.log_message("[START] Iniciando descarga con yt-dlp...")
            print(f"🔥 [DEBUG] Configuración: tipo={download_type}, formato={download_format}, calidad={quality}")
            self.log_message(f"[DEBUG] Configuración: tipo={download_type}, formato={download_format}, calidad={quality}")

            # Verificar que el widget se actualizó
            self.after(100, lambda: self.log_message(f"[DEBUG] Estado del widget después de actualización: {widget_info['status'].cget('text') if 'status' in widget_info else 'NO STATUS'}"))

            # Descargar
            print("🔥 [DOWNLOAD] Llamando a downloader.download_video...")
            print(f"🔥 [DOWNLOAD] Parámetros: url={url[:30]}..., formato={download_format}, tipo={source_type}")
            try:
                success = self.downloader.download_video(url, download_format, source_type)
                print(f"🔥 [DOWNLOAD] Método retornó: {success}")
                self.log_message(f"[STATUS] Resultado de descarga: {'[OK] Éxito' if success else '[CANCEL] Falló'}")
            except Exception as e:
                print(f"🔥 [ERROR] Excepción en download_video: {e}")
                success = False
                self.log_message(f"[CRASH] Error llamando download_video: {str(e)}")

            if success:
                # Completado
                self.after(0, lambda: widget_info['progress'].set(1.0))
                self.after(0, lambda: widget_info['status'].configure(text="✅ ¡Completado!", text_color="#00ff00"))
                self.after(0, lambda: widget_info['frame'].configure(fg_color="#002200", border_color="#00ff00"))  # Fondo verde
                self.log_message(f"[OK] Descarga completada: {url[:50]}...")
            else:
                # Error
                self.after(0, lambda: widget_info['progress'].set(0))
                self.after(0, lambda: widget_info['status'].configure(text="❌ Error en descarga", text_color="#ff4444"))
                self.after(0, lambda: widget_info['frame'].configure(fg_color="#220000", border_color="#ff4444"))  # Fondo rojo
                self.log_message(f"[CANCEL] Error descargando: {url[:50]}...")

        except Exception as e:
            self.after(0, lambda: widget_info['status'].configure(text=f"💥 Error: {str(e)[:30]}", text_color="#ff4444"))
            self.log_message(f"[CRASH] Error en descarga: {str(e)}")
        finally:
            # Re-habilitar botón
            self.after(0, lambda: self.download_single_btn.configure(state="normal", text="🚀 DESCARGAR"))

            # Recargar historial
            self.after(0, self.load_history)

    def cancel_download(self, url):
        """Cancelar una descarga en progreso"""
        if url in self.active_downloads:
            widget_info = self.active_downloads[url]
            self.after(0, lambda: widget_info['status'].configure(text="❌ Cancelado por usuario", text_color="#ff4444"))
            self.after(0, lambda: widget_info['frame'].configure(fg_color="#220000", border_color="#ff4444"))
            # Aquí iría la lógica para detener el proceso de yt-dlp
            self.log_message(f"[CANCEL] Descarga cancelada: {url[:50]}...")

    def load_settings(self):
        """Cargar configuraciones guardadas"""
        try:
            self.log_message("[CONFIG] Cargando configuraciones...")
            settings = load_config()

            self.default_quality = settings.get('default_quality', 'Mejor')
            self.default_format = settings.get('default_format', 'MP3 (Audio)')

            self.log_message("[OK] Configuraciones cargadas:")
            self.log_message(f"   📹 Calidad por defecto: {self.default_quality}")
            self.log_message(f"   [AUDIO] Formato por defecto: {self.default_format}")

            print(f"Configuraciones cargadas: calidad={self.default_quality}, formato={self.default_format}")
        except Exception as e:
            self.default_quality = 'Mejor'
            self.default_format = 'MP3 (Audio)'
            self.log_message("⚠️ Error cargando configuración, usando valores por defecto")
            self.log_message(f"   📹 Calidad: {self.default_quality}")
            self.log_message(f"   [AUDIO] Formato: {self.default_format}")
            print(f"Usando configuraciones por defecto: {e}")

    def get_video_info(self, url):
        """Obtener información del video de YouTube con timeout"""
        import threading
        import time

        # Variable para almacenar el resultado
        result = {'info': None, 'error': None, 'completed': False}

        def extract_info():
            try:
                self.log_message("[SEARCH] Consultando información del video...")
                import yt_dlp

                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,  # Suprimir warnings
                    'extract_flat': False,
                    'socket_timeout': 25,  # Timeout aumentado a 25 segundos
                    'retries': 3  # 3 reintentos
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    self.log_message("[CONNECT] Extrayendo información del video...")
                    info = ydl.extract_info(url, download=False)

                    video_info = {
                        'title': info.get('title', 'Sin título'),
                        'thumbnail': info.get('thumbnail'),
                        'duration': info.get('duration'),
                        'uploader': info.get('uploader')
                    }

                    result['info'] = video_info
                    result['completed'] = True

                    self.log_message("[OK] Información obtenida:")
                    self.log_message(f"   [TITLE] Título: {video_info['title'][:30]}{'...' if len(video_info['title']) > 30 else ''}")
                    self.log_message(f"   [USER] Uploader: {video_info['uploader'] or 'Desconocido'}")
                    self.log_message(f"   [IMAGE] Thumbnail: {'[OK] Disponible' if video_info['thumbnail'] else '[ERROR] No disponible'}")

            except Exception as e:
                result['error'] = str(e)
                self.log_message(f"[ERROR] Error en extracción: {str(e)}")

        # Ejecutar en thread separado con timeout
        self.log_message("[WAIT] Iniciando consulta de información...")
        thread = threading.Thread(target=extract_info, daemon=True)
        thread.start()

        # Esperar con timeout más generoso
        start_time = time.time()
        while not result['completed'] and (time.time() - start_time) < 30:  # 30 segundos timeout
            time.sleep(0.1)  # Chequear cada 100ms
            if result['error']:
                self.log_message(f"[DEBUG] Error detectado en thread: {result['error']}")
                break

        if not result['completed']:
            self.log_message("[INFO] Timeout rapido: Iniciando descarga sin metadata completa")
            # Intentar extraer al menos el ID del video de la URL para un título básico
            video_id = self.extract_video_id(url)
            fallback_title = f"Video {video_id}" if video_id else "Video sin título"
            return {
                'title': fallback_title,  # Sin [TIMEOUT] para ser más limpio
                'thumbnail': None,
                'duration': None,
                'uploader': 'Desconocido'
            }

        if result['error']:
            self.log_message(f"[ERROR] Falló consulta de información: {result['error']}")
            return {
                'title': f'Error: {result["error"][:30]}',
                'thumbnail': None,
                'duration': None,
                'uploader': 'Error'
            }

        self.log_message(f"[DEBUG] get_video_info retornando: {result['info'] is not None}")
        self.log_message(f"[DEBUG] get_video_info retornando: {result['info'] is not None}")
        if result['info']:
            self.log_message(f"[DEBUG] Datos retornados: title='{result['info'].get('title', 'N/A')[:30]}...', thumbnail={'SI' if result['info'].get('thumbnail') else 'NO'}")
        return result['info']

    def extract_video_id(self, url):
        """Extraer ID del video de la URL de YouTube"""
        import re

        # Patrones para diferentes formatos de URL de YouTube
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def load_thumbnail(self, widget_info, thumbnail_url):
        """Cargar y mostrar thumbnail del video"""
        try:
            print("🔥 [IMAGE] Descargando thumbnail...")
            self.log_message("[IMAGE] Descargando thumbnail...")
            print(f"🔥 [DEBUG] URL del thumbnail: {thumbnail_url}")
            self.log_message(f"[DEBUG] URL del thumbnail: {thumbnail_url}")
            from PIL import Image
            import requests
            from io import BytesIO

            # Descargar imagen
            print("🔥 [DOWNLOAD] Descargando imagen del thumbnail...")
            self.log_message("[DOWNLOAD] Descargando imagen del thumbnail...")
            response = requests.get(thumbnail_url, timeout=5)
            print(f"🔥 [STATUS] Thumbnail descargado: {len(response.content)} bytes")
            self.log_message(f"[STATUS] Thumbnail descargado: {len(response.content)} bytes")

            img = Image.open(BytesIO(response.content))
            print(f"🔥 [DEBUG] Imagen cargada: {img.size} -> {img.mode}")
            self.log_message(f"[DEBUG] Imagen cargada: {img.size} -> {img.mode}")

            # Redimensionar
            print("🔥 🔧 Redimensionando thumbnail...")
            self.log_message("🔧 Redimensionando thumbnail...")
            img = img.resize((80, 60), Image.Resampling.LANCZOS)
            print(f"🔥 [DEBUG] Imagen redimensionada: {img.size}")
            self.log_message(f"[DEBUG] Imagen redimensionada: {img.size}")

            # Convertir a CTkImage
            print("🔥 [DEBUG] CTkImage creado correctamente")
            ctk_img = ctk.CTkImage(img, size=(80, 60))
            self.log_message("[DEBUG] CTkImage creado correctamente")

            # Verificar que el widget existe
            if 'thumbnail' in widget_info and widget_info['thumbnail'] is not None:
                print("🔥 [DEBUG] Widget thumbnail encontrado, actualizando...")
                self.log_message("[DEBUG] Widget thumbnail encontrado, actualizando...")
                self.after(0, lambda: widget_info['thumbnail'].configure(image=ctk_img, text=""))
                print("🔥 [OK] Thumbnail aplicado al widget")
                self.log_message("[OK] Thumbnail aplicado al widget")
            else:
                print("🔥 [ERROR] Widget thumbnail no encontrado en widget_info")
                self.log_message("[ERROR] Widget thumbnail no encontrado en widget_info")

        except Exception as e:
            self.log_message(f"[CANCEL] ERROR cargando thumbnail: {str(e)}")
            print(f"Error cargando thumbnail: {e}")
            import traceback
            traceback.print_exc()
            # Mantener el emoji por defecto

    def save_settings(self):
        """Guardar configuraciones"""
        try:
            quality = self.default_quality_combo.get()
            formato = self.download_type.get()

            self.log_message(f"[SAVE] Guardando configuración...")
            self.log_message(f"   📹 Calidad: {quality}")
            self.log_message(f"   [AUDIO] Formato: {formato}")

            settings = {
                'default_quality': quality,
                'default_format': formato
            }

            save_config(settings)
            self.default_quality = settings['default_quality']
            self.default_format = settings['default_format']

            self.log_message("[OK] Configuración guardada exitosamente")
            self.log_message(f"   [UPDATE] Nueva calidad por defecto: {self.default_quality}")
            self.log_message(f"   [UPDATE] Nuevo formato por defecto: {self.default_format}")

        except Exception as e:
            self.log_message(f"[CANCEL] ERROR guardando configuración: {str(e)}")
            import traceback
            traceback.print_exc()

    def _get_quality_options(self):
        """Obtener opciones de calidad según formato actual"""
        download_type = self.download_type.get()
        if "MP3" in download_type:
            return ["Mejor", "320kbps", "256kbps", "192kbps", "128kbps"]
        else:
            return ["Mejor", "1080p", "720p", "480p", "360p"]

    def _update_quality_options(self, event=None):
        """Actualizar opciones de calidad cuando cambia el formato"""
        new_options = self._get_quality_options()
        self.default_quality_combo.configure(values=new_options)

        # Si la calidad actual no es válida para el nuevo formato, resetear
        current_quality = self.default_quality_combo.get()
        if current_quality not in new_options:
            self.default_quality_combo.set("Mejor")


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
    # Logging inicial detallado
    print("🚀 MP3 FASTERFAST v2.0")
    print("=" * 50)
    import sys, os  # Imports necesarios para el bloque main
    print(f"🕐 {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Directorio: {os.getcwd()}")
    print(f"🖥️  Plataforma: {sys.platform}")
    print()

    try:
        print("🔧 Verificando imports básicos...")
        import customtkinter as ctk
        print("✅ CustomTkinter importado")

        import tkinter as tk
        print("✅ Tkinter importado")

        from downloader import Downloader
        print("✅ Downloader importado")

        from database import Database
        print("✅ Database importado")

        print()
        print("🎨 Configurando tema...")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        print("✅ Tema configurado")

        print()
        print("🏗️  Creando aplicación principal...")
        app = MP3FasterFast()
        print("✅ Aplicación creada exitosamente")

        print()
        print("🖼️  Construyendo interfaz...")
        print("   Si ves este mensaje y NO aparece una ventana,")
        print("   hay un problema con el entorno gráfico.")
        print()
        print("⏳ Iniciando mainloop...")

        # Mostrar que estamos vivos
        app.after(1000, lambda: print("✅ Ventana debería estar visible ahora"))

        app.mainloop()

        print()
        print("👋 Aplicación cerrada normalmente")

    except KeyboardInterrupt:
        print("\n⏹️  Interrumpido por usuario (Ctrl+C)")
    except ImportError as e:
        print(f"\n❌ ERROR DE IMPORTACIÓN: {e}")
        print("💡 Ejecuta: py diagnostico.py")
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {str(e)}")
        print("\n🔍 Detalles técnicos:")
        import traceback
        traceback.print_exc()

        print("\n" + "="*50)
        print("💡 SOLUCIONES RECOMENDADAS:")
        print("   1. Ejecuta: py diagnostico.py")
        print("   2. Verifica: py -c \"import customtkinter; print('OK')\"")
        print("   3. Reinstala dependencias:")
        print("      py -m pip install --force-reinstall customtkinter mutagen pillow")
        print("   4. Si usas Windows, verifica que tengas una pantalla gráfica")
        print("="*50)

    input("\nPresiona Enter para salir...")
