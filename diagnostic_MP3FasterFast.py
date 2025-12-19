#!/usr/bin/env python3
"""
MP3 FasterFast - Diagnóstico del Sistema
Verifica si el PC tiene todo lo necesario para ejecutar la aplicación
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

def check_python_version():
    """Verificar versión de Python"""
    print("🐍 VERIFICANDO PYTHON...")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    print(f"   Versión instalada: {version_str}")
    print(f"   Ejecutable: {sys.executable}")
    print(f"   Plataforma: {platform.platform()}")

    if version.major >= 3 and version.minor >= 10:
        print("   ✅ Versión compatible (Python 3.10+)")
        return True
    else:
        print("   ❌ Versión incompatible. Se requiere Python 3.10 o superior")
        return False

def check_required_modules():
    """Verificar módulos requeridos"""
    print("\n📦 VERIFICANDO MÓDULOS REQUERIDOS...")

    required_modules = {
        "customtkinter": "Interfaz gráfica moderna",
        "mutagen": "Manipulación de metadatos MP3",
        "PIL": "Procesamiento de imágenes (Pillow)",
        "tkinter": "Interfaz gráfica base"
    }

    missing_modules = []

    for module, description in required_modules.items():
        try:
            __import__(module)
            print(f"   ✅ {module} - {description}")
        except ImportError:
            print(f"   ❌ {module} - {description}")
            missing_modules.append(module)

    if missing_modules:
        print(f"\n⚠️  MÓDULOS FALTANTES: {', '.join(missing_modules)}")
        print("\n📋 PARA INSTALAR:")
        print(f"   pip install {' '.join(missing_modules)}")
        return False

    return True

def check_executables():
    """Verificar ejecutables requeridos"""
    print("\n🔧 VERIFICANDO EJECUTABLES...")

    script_dir = Path(__file__).parent
    executables = {
        "yt-dlp.exe": "Descargador de YouTube",
        "ffmpeg.exe": "Convertidor audio/video"
    }

    missing_executables = []

    for exe, description in executables.items():
        exe_path = script_dir / exe
        if exe_path.exists():
            # Verificar que funciona
            try:
                result = subprocess.run([str(exe_path), "--version"],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"   ✅ {exe} - {description}")
                else:
                    print(f"   ❌ {exe} - {description} (no funciona)")
                    missing_executables.append(exe)
            except:
                print(f"   ❌ {exe} - {description} (error ejecutando)")
                missing_executables.append(exe)
        else:
            print(f"   ❌ {exe} - {description} (no encontrado)")
            missing_executables.append(exe)

    if missing_executables:
        print(f"\n⚠️  EJECUTABLES FALTANTES: {', '.join(missing_executables)}")
        return False

    return True

def check_disk_space():
    """Verificar espacio en disco"""
    print("\n💾 VERIFICANDO ESPACIO EN DISCO...")

    try:
        stat = os.statvfs(Path.cwd())
        free_space = (stat.f_bavail * stat.f_frsize) / (1024**3)  # GB

        print(".1f"
        if free_space > 1.0:  # Al menos 1GB
            print("   ✅ Espacio suficiente")
            return True
        else:
            print("   ❌ Espacio insuficiente (se recomienda al menos 1GB)")
            return False
    except:
        print("   ⚠️  No se pudo verificar espacio en disco")
        return True

def generate_report():
    """Generar reporte completo"""
    print("\n" + "="*60)
    print("📋 REPORTE DIAGNOSTICO - MP3 FASTERFAST")
    print("="*60)

    checks = [
        ("Python", check_python_version),
        ("Módulos", check_required_modules),
        ("Ejecutables", check_executables),
        ("Disco", check_disk_space)
    ]

    results = []
    for name, check_func in checks:
        print(f"\n🔍 Revisando {name}...")
        result = check_func()
        results.append(result)
        status = "✅ PASA" if result else "❌ FALLA"
        print(f"Resultado {name}: {status}")

    print("\n" + "="*60)

    if all(results):
        print("🎉 ¡SISTEMA COMPATIBLE!")
        print("MP3 FasterFast debería funcionar correctamente en este PC.")
        print("\n🚀 Ejecuta: MP3FasterFast_Portable.bat")
    else:
        print("⚠️  PROBLEMAS DETECTADOS")
        print("Este PC no tiene todo lo necesario para ejecutar MP3 FasterFast.")
        print("\n🔧 SOLUCIONES:")

        if not results[0]:  # Python
            print("\n🐍 PYTHON:")
            print("   1. Descarga desde: https://python.org")
            print("   2. Durante instalación: marca 'Add Python to PATH'")
            print("   3. Versión recomendada: Python 3.11")

        if not results[1]:  # Módulos
            print("\n📦 DEPENDENCIAS:")
            print("   Abre CMD/PowerShell y ejecuta:")
            print("   pip install customtkinter mutagen pillow")

        if not results[2]:  # Ejecutables
            print("\n🔧 EJECUTABLES:")
            print("   Los archivos yt-dlp.exe y ffmpeg.exe deben estar")
            print("   en la misma carpeta que la aplicación.")

        if not results[3]:  # Disco
            print("\n💾 ESPACIO:")
            print("   Libera al menos 1GB de espacio en disco.")

        print("\n❓ Si necesitas ayuda, revisa el archivo README.md")

    print("\n" + "="*60)

    input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    generate_report()
