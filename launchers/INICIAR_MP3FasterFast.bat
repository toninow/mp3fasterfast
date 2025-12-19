@echo off
echo ========================================
echo     MP3 FASTERFAST - INICIADOR
echo ========================================
echo.
echo Iniciando MP3 FasterFast...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Ejecutar Python con la aplicación
"C:\Users\MP-INFORMATICA\AppData\Local\Programs\Python\Python311\python.exe" app.py

echo.
echo Aplicacion cerrada.
pause
