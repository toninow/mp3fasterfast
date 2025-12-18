@echo off
echo 🚀 MP3 FASTERFAST - INICIO SIMPLE
echo ===================================
echo.

cd /d "%~dp0"

echo 🔍 Verificando Python...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado
    echo 📥 Descarga desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python OK
echo.

echo 🎯 Iniciando aplicacion...
echo    Si no se abre la ventana, presiona Ctrl+C
echo.

py -c "
import sys
sys.path.insert(0, '.')
print('📦 Importando modulos...')
try:
    import customtkinter as ctk
    import tkinter as tk
    from downloader import Downloader
    from database import Database
    print('✅ Todos los imports OK')
    
    print('🎨 Configurando tema...')
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('green')
    
    print('🏗️ Creando ventana...')
    root = ctk.CTk()
    root.title('MP3 FasterFast - Test')
    root.geometry('600x400')
    
    # Contenido simple
    title = ctk.CTkLabel(root, text='🎵 MP3 FASTERFAST FUNCIONANDO!', font=('Arial', 18))
    title.pack(pady=20)
    
    status = ctk.CTkLabel(root, text='✅ Aplicacion iniciada correctamente', font=('Arial', 12))
    status.pack(pady=10)
    
    # Boton para abrir la app completa
    def open_full_app():
        root.destroy()
        import subprocess
        subprocess.Popen(['py', 'MP3FasterFast.pyw'])
    
    btn = ctk.CTkButton(root, text='🚀 ABRIR APLICACION COMPLETA', command=open_full_app, height=40)
    btn.pack(pady=20)
    
    close_btn = ctk.CTkButton(root, text='❌ CERRAR', command=root.quit, fg_color='red')
    close_btn.pack(pady=10)
    
    print('✅ Ventana lista - deberias verla ahora')
    root.mainloop()
    
except Exception as e:
    print(f'❌ ERROR: {e}')
    import traceback
    traceback.print_exc()
    input('Presiona Enter...')
"

echo.
echo 👋 Test completado
pause
