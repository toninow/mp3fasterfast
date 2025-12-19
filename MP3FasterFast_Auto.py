#!/usr/bin/env python3
"""
MP3 FasterFast - Auto-Launcher
Detecta Python automáticamente y ejecuta la aplicación
"""

import sys
import os
import subprocess
from pathlib import Path

def find_python():
    """Buscar Python en el sistema"""
    possible_paths = [
        r"C:\Python311\python.exe",
        r"C:\Python312\python.exe",
        r"C:\Python310\python.exe",
        r"C:\Program Files\Python311\python.exe",
        r"C:\Program Files\Python312\python.exe",
        r"C:\Program Files\Python310\python.exe",
        "/usr/bin/python3",
        "/usr/local/bin/python3",
        "/opt/homebrew/bin/python3",
        "python3",
        "python",
    ]

    for path in possible_paths:
        expanded_path = os.path.expandvars(path)
        try:
            result = subprocess.run([expanded_path, "--version"],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and "Python" in result.stdout:
                return expanded_path
        except:
            continue
    return None

def main():
    print("🎵 MP3 FASTERFAST - AUTO-LAUNCHER")
    print("=" * 40)

    # Obtener directorio del script
    script_dir = Path(__file__).parent
    app_py = script_dir / "app.py"

    if not app_py.exists():
        print(f"❌ Error: No se encuentra app.py en {script_dir}")
        input("Presiona Enter para salir...")
        return

    # Buscar Python
    print("🔍 Buscando Python en el sistema...")
    python_exe = find_python()

    if not python_exe:
        print("❌ Error: Python no encontrado en el sistema")
        print("💡 Intenta usar MP3FasterFast.bat o ejecuta manualmente:")
        print(f"   & 'C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Programs\\Python311\\python.exe' app.py")
        input("Presiona Enter para salir...")
        return

    print(f"✅ Python encontrado: {python_exe}")

    # Verificar versión
    try:
        result = subprocess.run([python_exe, "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"📋 Versión: {version}")
    except:
        pass

    # Ejecutar aplicación
    print("\n🚀 Iniciando MP3 FasterFast...")
    try:
        subprocess.run([python_exe, str(app_py)], cwd=str(script_dir))
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando la aplicación: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
