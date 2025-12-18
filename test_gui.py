#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación se inicia correctamente
sin intentar mostrar la interfaz gráfica completa.
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧪 Probando inicialización de MP3 FasterFast...")

try:
    # Importar módulos
    print("📦 Importando módulos...")
    import customtkinter as ctk
    print("✅ CustomTkinter importado")

    from utils import validate_dependencies, ensure_directories
    print("✅ Utils importado")

    from database import Database
    print("✅ Database importado")

    # Verificar dependencias
    print("🔍 Verificando dependencias...")
    missing = validate_dependencies()
    if missing:
        print(f"❌ Faltan dependencias: {missing}")
        sys.exit(1)
    print("✅ Todas las dependencias presentes")

    # Crear directorios
    print("📁 Creando directorios...")
    ensure_directories()
    print("✅ Directorios creados")

    # Probar base de datos
    print("💾 Probando base de datos...")
    db = Database()
    downloads = db.get_all_downloads()
    db.close()
    print(f"✅ Base de datos funcionando ({len(downloads)} descargas)")

    # Probar creación de ventana básica (sin mostrar)
    print("🖼️ Probando creación de ventana...")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Crear ventana básica sin mostrarla
    test_window = ctk.CTk()
    test_window.title("MP3 FasterFast - Test")
    test_window.geometry("100x100")

    # Probar widgets básicos
    test_label = ctk.CTkLabel(test_window, text="Test")
    test_textbox = ctk.CTkTextbox(test_window, height=50)
    test_textbox.insert("0.0", "Test content")

    print("✅ Widgets creados correctamente")

    # Cerrar ventana sin mostrar
    test_window.destroy()
    print("✅ Ventana cerrada correctamente")

    print("\n🎉 ¡TODOS LOS TESTS PASARON!")
    print("La aplicación debería funcionar correctamente.")
    print("\n💡 Si no ves la ventana, verifica:")
    print("   - Que tengas un entorno gráfico disponible")
    print("   - Que no estés en un servidor headless")
    print("   - Que tengas Python con tkinter instalado")

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
