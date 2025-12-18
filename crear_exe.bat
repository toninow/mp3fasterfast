@echo off
echo ====================================
echo    CREANDO EJECUTABLE .EXE
echo ====================================
echo.

cd /d "%~dp0mp3fasterfast"

echo Verificando PyInstaller...
py -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo Instalando PyInstaller...
    py -m pip install pyinstaller --quiet
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo instalar PyInstaller
        pause
        exit /b 1
    )
)

echo.
echo Creando ejecutable...
echo Esto puede tomar varios minutos...
echo.

pyinstaller --onefile --windowed --icon=fasterfast.png --name="MP3FasterFast" --add-data "fasterfast.png;." --add-data "yt-dlp.exe;." --add-data "ffmpeg.exe;." app.py

if %errorlevel% equ 0 (
    echo.
    echo ====================================
    echo         ¡EXE CREADO EXITOSAMENTE!
    echo ====================================
    echo.
    echo El archivo ejecutable esta en:
    echo %~dp0mp3fasterfast\dist\MP3FasterFast.exe
    echo.
    echo ¡Haz doble clic para ejecutar!
    echo.
) else (
    echo.
    echo ERROR: No se pudo crear el ejecutable
    echo.
)

pause
