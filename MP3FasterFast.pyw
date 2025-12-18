#!/usr/bin/env python3
"""
MP3 FasterFast - Ejecutable principal (sin consola)
"""

import sys
import os

# Configurar codificación UTF-8 para Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Agregar directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

# Ejecutar la aplicación principal
exec(open("app.py", encoding="utf-8").read(), {'__name__': '__main__'})