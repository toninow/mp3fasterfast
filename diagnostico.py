#!/usr/bin/env python3
"""
Script de diagnóstico para MP3 FasterFast
"""

import sys
import os
import time

print("🔍 DIAGNÓSTICO DE MP3 FASTERFAST")
print("=" * 50)

# Verificar entorno
print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")
print(f"Working directory: {os.getcwd()}")
print()

# Verificar imports
print("📦 Verificando imports...")
try:
    import tkinter as tk
    print("✅ tkinter OK")
except ImportError as e:
    print(f"❌ tkinter ERROR: {e}")

try:
    import customtkinter as ctk
    print("✅ customtkinter OK")
except ImportError as e:
    print(f"❌ customtkinter ERROR: {e}")

try:
    from PIL import Image
    print("✅ PIL OK")
except ImportError as e:
    print(f"❌ PIL ERROR: {e}")

try:
    import sqlite3
    print("✅ sqlite3 OK")
except ImportError as e:
    print(f"❌ sqlite3 ERROR: {e}")

try:
    from downloader import Downloader
    print("✅ downloader OK")
except ImportError as e:
    print(f"❌ downloader ERROR: {e}")

try:
    from database import Database
    print("✅ database OK")
except ImportError as e:
    print(f"❌ database ERROR: {e}")

print()

# Verificar archivos necesarios
print("📁 Verificando archivos...")
files_to_check = [
    "fasterfast.png",
    "yt-dlp.exe",
    "ffmpeg.exe",
    "app.py"
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"✅ {file} existe")
    else:
        print(f"❌ {file} NO existe")

print()

# Verificar directorios
print("📂 Verificando directorios...")
dirs_to_check = [
    "downloads",
    "downloads/MP3",
    "downloads/Videos",
    "downloads/Playlists"
]

for dir_path in dirs_to_check:
    if os.path.exists(dir_path):
        print(f"✅ {dir_path} existe")
    else:
        print(f"❌ {dir_path} NO existe")

print()

# Probar CustomTkinter
print("🖥️  Probando CustomTkinter...")
try:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    print("✅ Tema configurado")

    root = ctk.CTk()
    root.title("Test - MP3 FasterFast")
    root.geometry("400x300")
    print("✅ Ventana creada")

    # Crear widgets básicos
    title = ctk.CTkLabel(root, text="🎵 MP3 FASTERFAST", font=("Arial", 16, "bold"))
    title.pack(pady=20)

    status = ctk.CTkLabel(root, text="✅ Diagnóstico completado", font=("Arial", 12))
    status.pack(pady=10)

    button = ctk.CTkButton(root, text="Cerrar", command=root.quit)
    button.pack(pady=10)

    print("✅ Widgets creados")
    print("🎯 La ventana debería estar visible ahora...")
    print("   Si no la ves, hay un problema con la interfaz gráfica")

    # Auto-cerrar en 10 segundos
    root.after(10000, lambda: print("⏰ Auto-cerrando en 3 segundos..."))
    root.after(13000, root.quit)

    root.mainloop()
    print("✅ Mainloop terminado correctamente")

except Exception as e:
    print(f"❌ ERROR en CustomTkinter: {e}")
    import traceback
    traceback.print_exc()

print()
print("🎯 RESULTADO DEL DIAGNÓSTICO:")
print("- Si viste la ventana: La interfaz funciona")
print("- Si no viste la ventana: Problema con CustomTkinter o entorno gráfico")
print("- Si hay errores arriba: Necesitas instalar dependencias")
print()
input("Presiona Enter para salir...")
