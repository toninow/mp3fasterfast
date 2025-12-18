#!/usr/bin/env python3
"""
Versión minimalista de MP3 FasterFast para debugging
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MP3FasterFastMinimal(ctk.CTk):
    def __init__(self):
        super().__init__()

        print("🏗️ Inicializando aplicación minimalista...")

        self.title("MP3 FasterFast - Minimal")
        self.geometry("600x400")
        self.resizable(False, False)

        print("📐 Configurando geometría...")

        # Título
        title_label = ctk.CTkLabel(self, text="🎵 MP3 FasterFast", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        print("📝 Agregando título...")

        # Área de URLs
        url_frame = ctk.CTkFrame(self)
        url_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(url_frame, text="URLs a descargar:").pack(anchor="w", padx=10, pady=5)

        self.url_text = ctk.CTkTextbox(url_frame, height=80)
        self.url_text.pack(fill="x", padx=10, pady=5)
        self.url_text.insert("0.0", "Pega URLs aquí...\n\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ")

        print("📝 Agregando área de texto...")

        # Botón
        self.download_btn = ctk.CTkButton(self, text="🚀 Probar", command=self.test_action)
        self.download_btn.pack(pady=20)

        print("🔘 Agregando botón...")

        # Área de log
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkLabel(log_frame, text="Log:").pack(anchor="w", padx=10, pady=5)

        self.log_text = ctk.CTkTextbox(log_frame, height=80)
        self.log_text.pack(fill="both", padx=10, pady=5, expand=True)

        print("📋 Agregando área de log...")

        # Protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        print("✅ Inicialización completada")

        # Mensaje inicial
        self.log("🎵 Aplicación minimalista iniciada")

    def log(self, message):
        """Agregar mensaje al log"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        print(f"📝 LOG: {message}")

    def test_action(self):
        """Acción de prueba"""
        self.log("🔘 Botón presionado")
        urls = self.url_text.get("0.0", "end").strip()
        self.log(f"📄 URLs encontradas: {len(urls.split())} líneas")
        self.log("✅ Test completado")

    def on_closing(self):
        """Manejar cierre"""
        print("👋 Cerrando aplicación...")
        self.destroy()

if __name__ == "__main__":
    try:
        print("🚀 Iniciando aplicación minimalista...")
        app = MP3FasterFastMinimal()
        print("✅ Aplicación creada, iniciando mainloop...")
        app.mainloop()
        print("👋 Aplicación cerrada normalmente")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")
