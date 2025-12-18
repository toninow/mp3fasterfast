#!/usr/bin/env python3
"""
Script de debugging para MP3 FasterFast
Captura y muestra errores detallados durante la inicialización
"""

import sys
import os
import traceback
import time

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🐛 DEBUG: Iniciando MP3 FasterFast con logging detallado...")
print(f"🐛 DEBUG: Python version: {sys.version}")
print(f"🐛 DEBUG: Working directory: {os.getcwd()}")

try:
    print("\n📦 DEBUG: Importando módulos...")

    print("📦 DEBUG: Importando customtkinter...")
    import customtkinter as ctk
    print(f"✅ DEBUG: CustomTkinter {ctk.__version__} importado")

    print("📦 DEBUG: Importando utils...")
    from utils import validate_dependencies, ensure_directories, BASE_DIR, YT_DLP_EXE, FFMPEG_EXE
    print("✅ DEBUG: Utils importado")

    print("📦 DEBUG: Importando database...")
    from database import Database
    print("✅ DEBUG: Database importado")

    print("📦 DEBUG: Importando otros módulos...")
    from downloader import Downloader
    from metadata import MetadataEditor
    from scheduler import Scheduler
    print("✅ DEBUG: Todos los módulos importados")

    print("\n🔍 DEBUG: Verificando dependencias...")
    print(f"🔍 DEBUG: BASE_DIR = {BASE_DIR}")
    print(f"🔍 DEBUG: YT_DLP_EXE = {YT_DLP_EXE} (exists: {YT_DLP_EXE.exists()})")
    print(f"🔍 DEBUG: FFMPEG_EXE = {FFMPEG_EXE} (exists: {FFMPEG_EXE.exists()})")

    missing = validate_dependencies()
    if missing:
        print(f"❌ DEBUG: Dependencias faltantes: {missing}")
        input("Presiona Enter para continuar...")
        sys.exit(1)
    print("✅ DEBUG: Todas las dependencias presentes")

    print("\n📁 DEBUG: Creando directorios...")
    ensure_directories()
    print("✅ DEBUG: Directorios creados")

    print("\n💾 DEBUG: Probando base de datos...")
    db = Database()
    downloads = db.get_all_downloads()
    print(f"✅ DEBUG: Base de datos funcionando ({len(downloads)} descargas)")
    db.close()

    print("\n🖼️ DEBUG: Configurando CustomTkinter...")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    print("✅ DEBUG: CustomTkinter configurado")

    print("\n🏗️ DEBUG: Creando aplicación...")
    from app import MP3FasterFast

    print("🏗️ DEBUG: Instanciando MP3FasterFast...")
    app = MP3FasterFast()
    print("✅ DEBUG: Aplicación creada exitosamente")

    print("\n🚀 DEBUG: Iniciando mainloop...")
    print("💡 DEBUG: Si la ventana se cierra inmediatamente, hay un error en mainloop")
    print("💡 DEBUG: Presiona Ctrl+C para salir si es necesario")

    app.mainloop()

    print("\n✅ DEBUG: Aplicación cerrada normalmente")

except Exception as e:
    print(f"\n❌ DEBUG: ERROR CRÍTICO: {str(e)}")
    print("\n📋 DEBUG: Traceback completo:")
    traceback.print_exc()

    print(f"\n🔍 DEBUG: Información del sistema:")
    print(f"🔍 DEBUG: Python executable: {sys.executable}")
    print(f"🔍 DEBUG: Python path: {sys.path[:3]}...")  # Solo primeros 3 para no saturar

    print("\n💡 DEBUG: Posibles soluciones:")
    print("💡 DEBUG: 1. Verifica que tengas entorno gráfico (no headless)")
    print("💡 DEBUG: 2. Actualiza CustomTkinter: pip install --upgrade customtkinter")
    print("💡 DEBUG: 3. Verifica que yt-dlp.exe y ffmpeg.exe existan")
    print("💡 DEBUG: 4. Ejecuta como administrador")

    input("\nPresiona Enter para salir...")

    sys.exit(1)
