@echo off
echo ===========================================
echo    MP3 FASTERFAST - INICIANDO...
echo ===========================================
cd /d "%~dp0"
echo Directorio: %cd%
echo.

echo Verificando Python...
py --version
if errorlevel 1 (
    echo ERROR: Python no encontrado
    echo Instala Python desde https://python.org
    pause
    exit /b 1
)
echo.

echo Iniciando aplicacion...
py app_minimal.py

echo.
echo Aplicacion cerrada.
pause
