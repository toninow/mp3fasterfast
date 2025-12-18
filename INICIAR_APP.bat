@echo off
title MP3 FasterFast - Iniciador

echo.
echo ===============================================
echo      MP3 FASTERFAST - INICIADOR
echo ===============================================
echo.

cd /d "%~dp0"
echo Directorio: %cd%
echo.

echo Verificando Python...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    echo.
    echo Solucion:
    echo    1. Descarga Python desde https://python.org
    echo    2. Marca "Add Python to PATH" al instalar
    echo    3. Reinicia la terminal
    echo.
    pause
    exit /b 1
)
echo Python OK
echo.

echo Verificando dependencias...
echo    CustomTkinter...
py -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo CustomTkinter no instalado - instalando...
    py -m pip install customtkinter --quiet
    if %errorlevel% neq 0 (
        echo ERROR: Fallo instalacion de CustomTkinter
        pause
        exit /b 1
    )
    echo CustomTkinter instalado
) else (
    echo CustomTkinter OK
)

echo    Mutagen...
py -c "import mutagen" >nul 2>&1
if %errorlevel% neq 0 (
    echo Mutagen no instalado - instalando...
    py -m pip install mutagen --quiet
    if %errorlevel% neq 0 (
        echo ERROR: Fallo instalacion de Mutagen
        pause
        exit /b 1
    )
    echo Mutagen instalado
) else (
    echo Mutagen OK
)

echo    Pillow...
py -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pillow no instalado - instalando...
    py -m pip install pillow --quiet
    if %errorlevel% neq 0 (
        echo ERROR: Fallo instalacion de Pillow
        pause
        exit /b 1
    )
    echo Pillow instalado
) else (
    echo Pillow OK
)

echo    yt-dlp...
py -c "import yt_dlp" >nul 2>&1
if %errorlevel% neq 0 (
    echo yt-dlp no instalado - instalando...
    py -m pip install yt-dlp --quiet --disable-pip-version-check
    if %errorlevel% neq 0 (
        echo Intentando instalacion alternativa...
        py -c "import subprocess; subprocess.run(['py', '-m', 'pip', 'install', '--upgrade', 'pip'], check=False)"
        py -m pip install yt-dlp --quiet --no-cache-dir
        if %errorlevel% neq 0 (
            echo ERROR: No se pudo instalar yt-dlp
            echo La aplicacion funcionara con funcionalidades limitadas
            echo Presiona una tecla para continuar...
            pause >nul
        ) else (
            echo yt-dlp instalado
        )
    ) else (
        echo yt-dlp instalado
    )
) else (
    echo yt-dlp OK
)

echo.
echo Iniciando MP3 FasterFast...
echo.

REM Iniciar la aplicacion directamente
py MP3FasterFast.pyw

echo.
echo Aplicacion cerrada.
pause
