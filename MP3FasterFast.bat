@echo off
REM MP3 FasterFast - Launcher Principal
REM Versión organizada y portable

echo ========================================
echo     MP3 FASTERFAST v2.0
echo ========================================
echo.
echo Iniciando aplicación...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar estructura de carpetas
if not exist "launchers\MP3FasterFast_Portable.bat" (
    echo ❌ Error: Estructura de carpetas dañada
    echo Revisa que todas las carpetas estén presentes
    pause
    exit /b 1
)

REM Ejecutar launcher portable
call "launchers\MP3FasterFast_Portable.bat"

echo.
echo Aplicación cerrada.
pause
