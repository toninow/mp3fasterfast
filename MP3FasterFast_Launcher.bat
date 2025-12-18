@echo off
echo ====================================
echo     MP3 FASTERFAST LAUNCHER
echo ====================================
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

echo Verificando Python...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    echo Instala Python desde: https://python.org
    pause
    exit /b 1
)

echo Python encontrado ✓

echo Verificando dependencias...
py -c "import customtkinter, mutagen, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    py -m pip install customtkinter mutagen Pillow --quiet
    if %errorlevel% neq 0 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

echo Dependencias OK ✓

echo.
echo Iniciando MP3 FasterFast...
echo Presiona Ctrl+C para cerrar
echo.

py MP3FasterFast.pyw

echo.
echo Aplicacion cerrada.
pause
