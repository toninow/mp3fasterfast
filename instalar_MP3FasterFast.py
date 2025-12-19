#!/usr/bin/env python3
"""
MP3 FasterFast - Instalador/Configurator
Configura la aplicación para funcionar en cualquier PC
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python():
    """Verificar Python"""
    print("🐍 Verificando Python...")
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ {result.stdout.strip()}")
        return True
    except:
        print("❌ Python no encontrado")
        return False

def check_dependencies():
    """Verificar dependencias"""
    print("\n📦 Verificando dependencias...")

    required = ["customtkinter", "mutagen", "PIL", "tkinter"]
    missing = []

    for module in required:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing.append(module)

    if missing:
        print(f"\n⚠️  Módulos faltantes: {', '.join(missing)}")
        print("Instálalos con: pip install " + " ".join(missing))
        return False

    return True

def check_executables():
    """Verificar yt-dlp y ffmpeg"""
    print("\n🔧 Verificando ejecutables...")

    script_dir = Path(__file__).parent
    executables = ["yt-dlp.exe", "ffmpeg.exe"]

    for exe in executables:
        exe_path = script_dir / exe
        if exe_path.exists():
            print(f"✅ {exe}")
        else:
            print(f"❌ {exe} - No encontrado en {exe_path}")
            return False

    return True

def create_shortcuts():
    """Crear accesos directos"""
    print("\n🔗 Creando accesos directos...")

    script_dir = Path(__file__).parent
    bat_file = script_dir / "MP3FasterFast_Portable.bat"

    if not bat_file.exists():
        print("❌ Archivo BAT no encontrado")
        return False

    try:
        # En Windows, intentar crear acceso directo
        if os.name == 'nt':
            import winshell
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "MP3 FasterFast.lnk"

            with winshell.shortcut(str(shortcut_path)) as shortcut:
                shortcut.path = str(bat_file)
                shortcut.working_directory = str(script_dir)
                shortcut.description = "MP3 FasterFast - Descargador de música"

            print(f"✅ Acceso directo creado: {shortcut_path}")
        else:
            print("ℹ️  En Linux/macOS, crea un enlace manual al archivo .bat")

    except ImportError:
        print("ℹ️  Instala 'winshell' para crear accesos directos automáticamente")
        print(f"   Archivo ejecutable: {bat_file}")

    return True

def main():
    print("🎵 MP3 FASTERFAST - INSTALADOR")
    print("=" * 40)

    script_dir = Path(__file__).parent
    print(f"📁 Directorio: {script_dir}")
    print()

    # Verificaciones
    checks = [
        check_python,
        check_dependencies,
        check_executables
    ]

    all_passed = True
    for check in checks:
        if not check():
            all_passed = False

    if all_passed:
        print("\n✅ TODAS LAS VERIFICACIONES PASARON")
        create_shortcuts()

        print("\n🎯 INSTRUCCIONES:")
        print("1. Ejecuta: MP3FasterFast_Portable.bat")
        print("2. O usa el acceso directo en el escritorio")
        print("\n¡MP3 FasterFast está listo para usar!")

    else:
        print("\n❌ ALGUNAS VERIFICACIONES FALLARON")
        print("Revisa los errores arriba e instala lo que falte.")

    input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
