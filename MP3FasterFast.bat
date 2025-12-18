@echo off
echo ====================================
echo     MP3 FasterFast - Iniciando...
echo ====================================
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

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
    py app.py
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
