@echo off
echo ====================================
echo     MP3 FasterFast - Iniciando...
echo ====================================
echo.

REM Obtener directorio del script (para ejecutar desde cualquier lugar)
set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Cambiar al directorio del proyecto
if exist "%SCRIPT_DIR%\mp3fasterfast" (
    cd /d "%SCRIPT_DIR%\mp3fasterfast"
    echo Ejecutando desde: %SCRIPT_DIR%\mp3fasterfast
) else (
    cd /d "%SCRIPT_DIR%"
    echo Ejecutando desde: %SCRIPT_DIR%
)

echo.
REM Verificar dependencias de Python
echo Verificando dependencias de Python...

py -c "import customtkinter, mutagen, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias faltantes...
    py -m pip install customtkinter mutagen Pillow --quiet
    if %errorlevel% neq 0 (
        echo ERROR: No se pudieron instalar las dependencias
        echo.
        echo Solucion: Ejecuta como administrador:
        echo py -m pip install customtkinter mutagen Pillow
        echo.
        pause
        goto :eof
    )
    echo Dependencias instaladas correctamente.
    echo.
)

REM Verificar si Python está disponible
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python encontrado, iniciando aplicacion...
    python app.py
    goto :eof
)

REM Intentar con py
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python (py) encontrado, iniciando aplicacion...
    py MP3FasterFast.pyw
    goto :eof
)

REM Si no se encontró Python
echo ERROR: Python no esta instalado o no esta en el PATH
echo.
echo Soluciones:
echo 1. Instala Python desde: https://python.org
echo 2. Asegurate de marcar "Add Python to PATH" durante la instalacion
echo 3. O usa "py" en lugar de "python"
echo.
pause
goto :eof
