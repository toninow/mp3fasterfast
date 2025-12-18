#!/usr/bin/env python3
"""
Test para ejecutar la aplicación por 5 segundos y ver si se mantiene abierta
"""

import sys
import os
import threading
import time

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def stop_app(app, timeout=5):
    """Detener la aplicación después de timeout segundos"""
    time.sleep(timeout)
    print(f"⏰ Timeout de {timeout}s alcanzado, cerrando aplicación...")
    try:
        app.quit()
        print("✅ Aplicación cerrada correctamente por timeout")
    except Exception as e:
        print(f"❌ Error cerrando aplicación: {str(e)}")

try:
    print("🧪 Iniciando test de aplicación con timeout...")

    from app import MP3FasterFast

    print("🏗️ Creando aplicación...")
    app = MP3FasterFast()
    print("✅ Aplicación creada")

    # Iniciar thread para detener la aplicación después de 5 segundos
    stop_thread = threading.Thread(target=stop_app, args=(app, 5), daemon=True)
    stop_thread.start()

    print("🚀 Iniciando mainloop (se cerrará automáticamente en 5 segundos)...")
    app.mainloop()

    print("👋 Test completado exitosamente")

except Exception as e:
    print(f"❌ ERROR durante el test: {str(e)}")
    import traceback
    traceback.print_exc()
