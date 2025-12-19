#!/usr/bin/env python3
"""
MP3 FasterFast - Versión Portable y Dinámica
Detecta automáticamente Python y funciona en cualquier PC
"""

import sys
import os
import subprocess
from pathlib import Path

def find_python_executable():
    """Buscar ejecutable de Python en el sistema"""
    possible_paths = [
        # Rutas comunes de instalación
        r"C:\Python311\python.exe",
        r"C:\Python312\python.exe",
        r"C:\Python310\python.exe",
        r"C:\Program Files\Python311\python.exe",
        r"C:\Program Files\Python312\python.exe",
        r"C:\Program Files\Python310\python.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe",
        # macOS/Linux
        "/usr/bin/python3",
        "/usr/local/bin/python3",
        "/opt/homebrew/bin/python3",
        # Buscar en PATH
        "python3",
        "python",
    ]

    for path in possible_paths:
        # Expandir variables de entorno
        expanded_path = os.path.expandvars(path)

        try:
            # Verificar si el ejecutable existe y funciona
            result = subprocess.run([expanded_path, "--version"],
                                  capture_output=True, text=True, timeout=5)

            if result.returncode == 0 and "Python" in result.stdout:
                return expanded_path
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue

    return None

def check_dependencies(python_exe):
    """Verificar que Python tenga las dependencias necesarias"""
    required_modules = [
        "customtkinter",
        "mutagen",
        "PIL",
        "tkinter"
    ]

    print("🔍 Verificando dependencias de Python...")

    for module in required_modules:
        try:
            result = subprocess.run([python_exe, "-c", f"import {module}"],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                print(f"   ✅ {module}")
            else:
                print(f"   ❌ {module} - Error: {result.stderr.strip()}")
                return False
        except Exception as e:
            print(f"   ❌ {module} - Error: {str(e)}")
            return False

    return True

def create_auto_launcher():
    """Crear launcher automático que detecta Python"""
    launcher_code = '''#!/usr/bin/env python3
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
        r"C:\\Python311\\python.exe",
        r"C:\\Python312\\python.exe",
        r"C:\\Python310\\python.exe",
        r"C:\\Program Files\\Python311\\python.exe",
        r"C:\\Program Files\\Python312\\python.exe",
        r"C:\\Program Files\\Python310\\python.exe",
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
        print("\\nInstala Python desde: https://python.org")
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
    print("\\n🚀 Iniciando MP3 FasterFast...")
    try:
        subprocess.run([python_exe, str(app_py)], cwd=str(script_dir))
    except KeyboardInterrupt:
        print("\\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando la aplicación: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
'''

    launcher_path = Path(__file__).parent / "MP3FasterFast_Auto.py"
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_code)

    print(f"✅ Launcher creado: {launcher_path}")
    return launcher_path

def create_bat_launcher():
    """Crear archivo .bat que funcione en cualquier PC"""
    bat_code = '''@echo off
echo ========================================
echo    MP3 FASTERFAST - PORTABLE
echo ========================================
echo.
echo Buscando Python en tu sistema...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Buscar Python en rutas comunes
set PYTHON_EXE=

REM Windows - Rutas comunes
if exist "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" (
    set PYTHON_EXE="C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
) else if exist "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" (
    set PYTHON_EXE="C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
) else if exist "C:\\Python311\\python.exe" (
    set PYTHON_EXE="C:\\Python311\\python.exe"
) else if exist "C:\\Python312\\python.exe" (
    set PYTHON_EXE="C:\\Python312\\python.exe"
) else if exist "C:\\Program Files\\Python311\\python.exe" (
    set PYTHON_EXE="C:\\Program Files\\Python311\\python.exe"
) else (
    REM Buscar en PATH
    where python >nul 2>&1
    if %ERRORLEVEL% == 0 (
        set PYTHON_EXE=python
    ) else (
        echo ❌ ERROR: Python no encontrado
        echo.
        echo Instala Python desde: https://python.org
        echo Asegúrate de marcar "Add Python to PATH"
        echo.
        pause
        exit /b 1
    )
)

echo ✅ Python encontrado: %PYTHON_EXE%
echo.

REM Verificar que existe app.py
if not exist "app.py" (
    echo ❌ ERROR: app.py no encontrado en %~dp0
    pause
    exit /b 1
)

REM Ejecutar la aplicación
echo 🚀 Iniciando MP3 FasterFast...
echo.
%PYTHON_EXE% app.py

echo.
echo 👋 Aplicación cerrada.
pause
'''

    bat_path = Path(__file__).parent / "MP3FasterFast_Portable.bat"
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(bat_code)

    print(f"✅ Launcher BAT creado: {bat_path}")
    return bat_path

def create_installer_script():
    """Crear script para configurar en otro PC"""
    installer_code = '''#!/usr/bin/env python3
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
    print("\\n📦 Verificando dependencias...")

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
        print(f"\\n⚠️  Módulos faltantes: {', '.join(missing)}")
        print("Instálalos con: pip install " + " ".join(missing))
        return False

    return True

def check_executables():
    """Verificar yt-dlp y ffmpeg"""
    print("\\n🔧 Verificando ejecutables...")

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
    print("\\n🔗 Creando accesos directos...")

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
        print("\\n✅ TODAS LAS VERIFICACIONES PASARON")
        create_shortcuts()

        print("\\n🎯 INSTRUCCIONES:")
        print("1. Ejecuta: MP3FasterFast_Portable.bat")
        print("2. O usa el acceso directo en el escritorio")
        print("\\n¡MP3 FasterFast está listo para usar!")

    else:
        print("\\n❌ ALGUNAS VERIFICACIONES FALLARON")
        print("Revisa los errores arriba e instala lo que falte.")

    input("\\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
'''

    installer_path = Path(__file__).parent / "instalar_MP3FasterFast.py"
    with open(installer_path, 'w', encoding='utf-8') as f:
        f.write(installer_code)

    print(f"✅ Instalador creado: {installer_path}")
    return installer_path

def create_diagnostic_script():
    """Crear script de diagnóstico para detectar problemas"""
    diagnostic_code = '''#!/usr/bin/env python3
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
    print("\\n📦 VERIFICANDO MÓDULOS REQUERIDOS...")

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
        print(f"\\n⚠️  MÓDULOS FALTANTES: {', '.join(missing_modules)}")
        print("\\n📋 PARA INSTALAR:")
        print(f"   pip install {' '.join(missing_modules)}")
        return False

    return True

def check_executables():
    """Verificar ejecutables requeridos"""
    print("\\n🔧 VERIFICANDO EJECUTABLES...")

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
        print(f"\\n⚠️  EJECUTABLES FALTANTES: {', '.join(missing_executables)}")
        return False

    return True

def check_disk_space():
    """Verificar espacio en disco"""
    print("\\n💾 VERIFICANDO ESPACIO EN DISCO...")

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
    print("\\n" + "="*60)
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
        print(f"\\n🔍 Revisando {name}...")
        result = check_func()
        results.append(result)
        status = "✅ PASA" if result else "❌ FALLA"
        print(f"Resultado {name}: {status}")

    print("\\n" + "="*60)

    if all(results):
        print("🎉 ¡SISTEMA COMPATIBLE!")
        print("MP3 FasterFast debería funcionar correctamente en este PC.")
        print("\\n🚀 Ejecuta: MP3FasterFast_Portable.bat")
    else:
        print("⚠️  PROBLEMAS DETECTADOS")
        print("Este PC no tiene todo lo necesario para ejecutar MP3 FasterFast.")
        print("\\n🔧 SOLUCIONES:")

        if not results[0]:  # Python
            print("\\n🐍 PYTHON:")
            print("   1. Descarga desde: https://python.org")
            print("   2. Durante instalación: marca 'Add Python to PATH'")
            print("   3. Versión recomendada: Python 3.11")

        if not results[1]:  # Módulos
            print("\\n📦 DEPENDENCIAS:")
            print("   Abre CMD/PowerShell y ejecuta:")
            print("   pip install customtkinter mutagen pillow")

        if not results[2]:  # Ejecutables
            print("\\n🔧 EJECUTABLES:")
            print("   Los archivos yt-dlp.exe y ffmpeg.exe deben estar")
            print("   en la misma carpeta que la aplicación.")

        if not results[3]:  # Disco
            print("\\n💾 ESPACIO:")
            print("   Libera al menos 1GB de espacio en disco.")

        print("\\n❓ Si necesitas ayuda, revisa el archivo README.md")

    print("\\n" + "="*60)

    input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    generate_report()
'''

    diagnostic_path = Path(__file__).parent / "diagnostic_MP3FasterFast.py"
    with open(diagnostic_path, 'w', encoding='utf-8') as f:
        f.write(diagnostic_code)

    print(f"✅ Script de diagnóstico creado: {diagnostic_path}")
    return diagnostic_path

def create_requirements_file():
    """Crear archivo requirements.txt"""
    requirements = '''# MP3 FasterFast - Dependencias Python
# Instala con: pip install -r requirements.txt

customtkinter>=5.2.0
mutagen>=1.46.0
Pillow>=10.0.0

# Dependencias opcionales para mejor funcionamiento
requests>=2.31.0
'''

    req_path = Path(__file__).parent / "requirements.txt"
    with open(req_path, 'w', encoding='utf-8') as f:
        f.write(requirements)

    print(f"✅ Archivo requirements.txt creado: {req_path}")
    return req_path

def main():
    print("🎵 MP3 FASTERFAST - CONFIGURACIÓN PORTABLE Y DIAGNÓSTICO")
    print("=" * 60)

    script_dir = Path(__file__).parent
    print(f"📁 Directorio actual: {script_dir}")
    print()

    # Buscar Python
    print("🔍 Buscando Python en el sistema...")
    python_exe = find_python_executable()

    if python_exe:
        print(f"✅ Python encontrado: {python_exe}")

        # Verificar versión básica
        try:
            result = subprocess.run([python_exe, "--version"], capture_output=True, text=True)
            print(f"📋 Versión: {result.stdout.strip()}")
        except:
            pass

        # Verificar dependencias
        if check_dependencies(python_exe):
            print("✅ Todas las dependencias instaladas")

            # Crear archivos de soporte
            print("\n🏗️  Creando archivos de soporte...")

            diagnostic = create_diagnostic_script()
            requirements = create_requirements_file()
            launcher_py = create_auto_launcher()
            launcher_bat = create_bat_launcher()
            installer = create_installer_script()

            print("\n📦 ARCHIVOS CREADOS:")
            print(f"   🔍 {diagnostic.name} - Diagnóstico del sistema")
            print(f"   📋 requirements.txt - Lista de dependencias")
            print(f"   🚀 {launcher_py.name} - Launcher automático")
            print(f"   🪟 {launcher_bat.name} - Launcher Windows")
            print(f"   ⚙️  {installer.name} - Instalador/configurador")

            print("\n🎯 PARA USAR EN OTRO PC:")
            print("1. Copia TODA la carpeta a otro ordenador")
            print("2. Ejecuta: python diagnostic_MP3FasterFast.py")
            print("3. Si todo está bien, ejecuta: MP3FasterFast_Portable.bat")
            print("4. Si faltan cosas, sigue las instrucciones del diagnóstico")

        else:
            print("❌ Faltan dependencias. Instálalas con:")
            print("   pip install customtkinter mutagen pillow")
            print("\nO usa el archivo requirements.txt generado")

    else:
        print("❌ Python no encontrado en rutas comunes")
        print("\n🔧 SOLUCIONES:")
        print("1. Instala Python desde: https://python.org")
        print("2. Durante instalación: marca 'Add Python to PATH'")
        print("3. Versión recomendada: Python 3.11")
        print("4. O ejecuta el diagnóstico: python diagnostic_MP3FasterFast.py")

    print("\n💡 CONSEJO:")
    print("Si el otro PC no tiene Python, considera crear un ejecutable")
    print("independiente con PyInstaller o auto-py-to-exe")

if __name__ == "__main__":
    main()
