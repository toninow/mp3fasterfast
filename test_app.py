#!/usr/bin/env python3
"""
Script de prueba simple para verificar que la aplicación se abre
"""

import sys
import os

# Configurar codificación
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

sys.path.insert(0, os.getcwd())

try:
    print("🔍 Probando apertura de aplicación...")

    import customtkinter as ctk
    print("✅ CustomTkinter importado correctamente")

    # Configurar tema básico
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    print("✅ Tema configurado correctamente")

    # Crear ventana simple de prueba
    root = ctk.CTk()
    root.title("Test MP3 FasterFast")
    root.geometry("400x300")

    label = ctk.CTkLabel(root, text="✅ Aplicación funcionando correctamente!")
    label.pack(pady=20)

    button = ctk.CTkButton(root, text="Cerrar", command=root.quit)
    button.pack(pady=10)

    print("✅ Ventana de prueba creada correctamente")
    print("🎯 La aplicación debería abrirse ahora...")

    root.mainloop()

except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
