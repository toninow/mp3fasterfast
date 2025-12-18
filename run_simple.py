#!/usr/bin/env python3
"""
Versión simplificada de MP3 FasterFast para diagnosticar problemas
"""

import sys
import os

# Configurar codificación para Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

print("🚀 Iniciando MP3 FasterFast (versión simplificada)...")

try:
    import customtkinter as ctk
    print("✅ CustomTkinter cargado")
except ImportError as e:
    print(f"❌ Error importando CustomTkinter: {e}")
    sys.exit(1)

try:
    # Tema simple
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    print("✅ Tema configurado")
except Exception as e:
    print(f"❌ Error configurando tema: {e}")

try:
    # Crear ventana principal
    root = ctk.CTk()
    root.title("MP3 FasterFast - Test")
    root.geometry("600x400")
    print("✅ Ventana creada")
except Exception as e:
    print(f"❌ Error creando ventana: {e}")
    sys.exit(1)

try:
    # Widgets básicos
    title = ctk.CTkLabel(root, text="🎵 MP3 FASTERFAST", font=("Arial", 20, "bold"))
    title.pack(pady=20)

    status = ctk.CTkLabel(root, text="✅ Aplicación funcionando correctamente", font=("Arial", 12))
    status.pack(pady=10)

    # Área de URLs simplificada
    url_label = ctk.CTkLabel(root, text="URLs para descargar:")
    url_label.pack(pady=(20, 5))

    url_text = ctk.CTkTextbox(root, height=100)
    url_text.pack(pady=(0, 20), padx=20, fill="x")
    url_text.insert("0.0", "Pega tus URLs de YouTube aquí...")

    # Botón de descarga
    download_btn = ctk.CTkButton(root, text="🚀 INICIAR DESCARGAS",
                                command=lambda: print("Botón presionado"))
    download_btn.pack(pady=10)

    print("✅ Widgets creados")
except Exception as e:
    print(f"❌ Error creando widgets: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("🎯 Aplicación lista. Cerrando en 10 segundos...")
print("Si ves esta ventana, ¡la aplicación funciona!")

# Auto-cerrar después de 10 segundos
def close_app():
    print("👋 Cerrando aplicación...")
    root.quit()

root.after(10000, close_app)

try:
    root.mainloop()
    print("✅ Mainloop terminado correctamente")
except Exception as e:
    print(f"❌ Error en mainloop: {e}")
    import traceback
    traceback.print_exc()
