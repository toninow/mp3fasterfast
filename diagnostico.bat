@echo off
echo ====================================
echo  DIAGNOSTICO MP3 FasterFast
echo ====================================
echo.

echo [1/4] Verificando directorio actual...
cd /d "%~dp0"
echo Directorio: %CD%
echo.

echo [2/4] Buscando archivos importantes...
if exist app.py (
    echo ✓ app.py encontrado
) else (
    echo ✗ app.py NO encontrado
)

if exist fasterfast.png (
    echo ✓ fasterfast.png encontrado
) else (
    echo ✗ fasterfast.png NO encontrado
)

if exist yt-dlp.exe (
    echo ✓ yt-dlp.exe encontrado
) else (
    echo ✗ yt-dlp.exe NO encontrado
)

if exist ffmpeg.exe (
    echo ✓ ffmpeg.exe encontrado
) else (
    echo ✗ ffmpeg.exe NO encontrado
)
echo.

echo [3/4] Verificando Python...
python --version 2>nul
if %errorlevel% equ 0 (
    echo ✓ python disponible
) else (
    echo ✗ python NO disponible
)

py --version 2>nul
if %errorlevel% equ 0 (
    echo ✓ py disponible
) else (
    echo ✗ py NO disponible
)
echo.

echo [4/4] Probando sintaxis de app.py...
py -c "import ast; ast.parse(open('app.py', encoding='utf-8').read()); print('Sintaxis correcta')" 2>nul
if %errorlevel% equ 0 (
    echo ✓ Sintaxis de app.py correcta
) else (
    echo ✗ Error de sintaxis en app.py
)
echo.

echo ====================================
echo      RESULTADOS DEL DIAGNOSTICO
echo ====================================
echo.
echo Si hay errores marcados con ✗, esos son los problemas a solucionar.
echo.
echo Presiona cualquier tecla para probar ejecutar la aplicacion...
pause >nul

echo.
echo [EXTRA] Intentando ejecutar app.py...
echo Si se cierra inmediatamente, hay un error en tiempo de ejecucion.
echo.

if exist app.py (
    py app.py 2>&1
    echo.
    echo Codigo de salida: %errorlevel%
) else (
    echo ERROR: app.py no encontrado
)

echo.
echo Fin del diagnostico.
pause
