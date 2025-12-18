# MP3 FasterFast Launcher
# Ejecuta la aplicación Python con mejor detección

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "    MP3 FasterFast - Iniciando..." -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir
Write-Host "Directorio: $scriptDir" -ForegroundColor Gray
Write-Host ""

# Verificar e instalar dependencias
Write-Host "Verificando dependencias de Python..." -ForegroundColor Yellow

try {
    & py -c "import customtkinter, mutagen, PIL" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Instalando dependencias faltantes..." -ForegroundColor Yellow
        & py -m pip install customtkinter mutagen Pillow --quiet
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: No se pudieron instalar las dependencias" -ForegroundColor Red
            Write-Host ""
            Write-Host "Solucion: Ejecuta como administrador:" -ForegroundColor White
            Write-Host "py -m pip install customtkinter mutagen Pillow" -ForegroundColor White
            Write-Host ""
            Read-Host "Presiona Enter para salir"
            exit 1
        }
        Write-Host "Dependencias instaladas correctamente." -ForegroundColor Green
        Write-Host ""
    }
}
catch {
    Write-Host "ERROR: Problema verificando dependencias" -ForegroundColor Red
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Función para probar comando
function Test-Command {
    param($command)
    try {
        & $command --version 2>$null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

# Intentar diferentes formas de ejecutar Python
$pythonCommands = @("python", "python3", "py")

foreach ($cmd in $pythonCommands) {
    if (Test-Command $cmd) {
        Write-Host "Python encontrado ($cmd), iniciando aplicacion..." -ForegroundColor Green
        Write-Host ""
        & $cmd app.py
        exit
    }
}

# Si no se encontró Python
Write-Host "ERROR: Python no esta instalado o no esta en el PATH" -ForegroundColor Red
Write-Host ""
Write-Host "Soluciones:" -ForegroundColor Yellow
Write-Host "1. Instala Python desde: https://python.org" -ForegroundColor White
Write-Host "2. Asegurate de marcar 'Add Python to PATH' durante la instalacion" -ForegroundColor White
Write-Host "3. O ejecuta desde CMD con: py app.py" -ForegroundColor White
Write-Host ""
Read-Host "Presiona Enter para salir"
