@echo off
REM MP3 FasterFast - Launcher simple
echo ========================================
echo  MP3 FASTERFAST - INICIADOR SIMPLE
echo ========================================
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Ruta de Python (ajusta si es necesario)
set PYTHON_EXE=C:\Users\%USERNAME%\AppData\Local\Programs\Python311\python.exe

echo Verificando Python...
if not exist "%PYTHON_EXE%" (
    echo ❌ Python no encontrado en: %PYTHON_EXE%
    echo.
    echo 💡 Opciones:
    echo   1. Instala Python en la ubicación esperada
    echo   2. Edita este archivo .bat para cambiar PYTHON_EXE
    echo   3. Usa MP3FasterFast_Auto.py que detecta Python automaticamente
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

echo 🚀 Iniciando MP3 FasterFast...
echo.

REM Ejecutar la aplicación
"%PYTHON_EXE%" app.py

echo.
echo 👋 Aplicación cerrada
pause