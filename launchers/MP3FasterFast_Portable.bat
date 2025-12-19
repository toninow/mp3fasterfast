@echo off
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
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON_EXE="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    set PYTHON_EXE="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
) else if exist "C:\Python311\python.exe" (
    set PYTHON_EXE="C:\Python311\python.exe"
) else if exist "C:\Python312\python.exe" (
    set PYTHON_EXE="C:\Python312\python.exe"
) else if exist "C:\Program Files\Python311\python.exe" (
    set PYTHON_EXE="C:\Program Files\Python311\python.exe"
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
