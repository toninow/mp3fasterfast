#!/usr/bin/env python3
"""
MP3 FasterFast - Ejecutable Python directo
"""

import sys
import os
import subprocess

# Cambiar al directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Verificar e instalar dependencias
print("Verificando dependencias...")
try:
    import customtkinter, mutagen, PIL
    print("Dependencias OK")
except ImportError:
    print("Instalando dependencias...")
    subprocess.run([sys.executable, "-m", "pip", "install", "customtkinter", "mutagen", "Pillow", "--quiet"], check=True)
    print("Dependencias instaladas")

# Ejecutar la aplicación
print("Iniciando MP3 FasterFast...")
exec(open("app.py").read())
