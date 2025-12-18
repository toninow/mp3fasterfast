import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from customtkinter import CTkImage
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from PIL import Image
from utils import MP3_DIR

class MetadataEditor(ctk.CTkToplevel):
    def __init__(self, mp3_file_path):
        super().__init__()

        self.mp3_file = mp3_file_path
        self.title("Editar Metadatos MP3")
        self.geometry("500x400")
        self.resizable(False, False)

        # Cargar metadatos existentes
        self.load_metadata()

        # Crear interfaz
        self.create_widgets()

        # Centrar ventana
        self.center_window()

    def center_window(self):
        """Centrar ventana en pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def load_metadata(self):
        """Cargar metadatos del archivo MP3"""
        self.metadata = {
            'title': '',
            'artist': '',
            'album': '',
            'comment': ''
        }
        self.album_art = None

        try:
            # Cargar metadatos básicos
            audio = EasyID3(self.mp3_file)
            self.metadata['title'] = audio.get('title', [''])[0]
            self.metadata['artist'] = audio.get('artist', [''])[0]
            self.metadata['album'] = audio.get('album', [''])[0]
            self.metadata['comment'] = audio.get('comment', [''])[0]

            # Intentar cargar portada
            mp3_audio = MP3(self.mp3_file, ID3=ID3)
            for tag in mp3_audio.tags.values():
                if isinstance(tag, APIC):
                    self.album_art = tag.data
                    break

        except Exception as e:
            print(f"Error cargando metadatos: {e}")

    def create_widgets(self):
        """Crear widgets de la interfaz"""
        # Título
        ctk.CTkLabel(self, text="Editar Metadatos MP3", font=("Arial", 16, "bold")).pack(pady=10)

        # Mostrar portada si existe
        if self.album_art:
            try:
                # Crear imagen desde bytes
                import io
                img = Image.open(io.BytesIO(self.album_art))
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                photo = CTkImage(img, size=(150, 150))

                # Frame para la portada
                cover_frame = ctk.CTkFrame(self, fg_color="transparent")
                cover_frame.pack(pady=5)

                ctk.CTkLabel(cover_frame, text="Portada del Álbum:").pack()
                cover_label = ctk.CTkLabel(cover_frame, image=photo, text="")
                cover_label.pack(pady=5)

            except Exception as e:
                print(f"Error mostrando portada: {e}")

        # Frame principal
        frame = ctk.CTkFrame(self)
        frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Campos de entrada
        ctk.CTkLabel(frame, text="Título:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.title_entry = ctk.CTkEntry(frame, width=300)
        self.title_entry.insert(0, self.metadata['title'])
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Artista:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.artist_entry = ctk.CTkEntry(frame, width=300)
        self.artist_entry.insert(0, self.metadata['artist'])
        self.artist_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Álbum:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.album_entry = ctk.CTkEntry(frame, width=300)
        self.album_entry.insert(0, self.metadata['album'])
        self.album_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Comentario:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.comment_entry = ctk.CTkEntry(frame, width=300)
        self.comment_entry.insert(0, self.metadata['comment'])
        self.comment_entry.grid(row=3, column=1, padx=10, pady=5)

        # Botones
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Guardar", command=self.save_metadata).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=10)

    def save_metadata(self):
        """Guardar metadatos en el archivo MP3"""
        try:
            audio = EasyID3(self.mp3_file)

            # Actualizar metadatos
            audio['title'] = self.title_entry.get().strip()
            audio['artist'] = self.artist_entry.get().strip()
            audio['album'] = self.album_entry.get().strip()
            audio['comment'] = self.comment_entry.get().strip()

            audio.save()

            messagebox.showinfo("Éxito", "Metadatos guardados correctamente")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error guardando metadatos: {str(e)}")
