#!/usr/bin/env python3
"""
Script de inicio robusto para MP3 FasterFast
"""

import sys
import os
import subprocess
import time

def check_python():
    """Verificar que Python esté disponible"""
    try:
        result = subprocess.run([sys.executable, '--version'],
                              capture_output=True, text=True, timeout=5)
        version = result.stdout.strip()
        print(f"✅ Python: {version}")
        return True
    except Exception as e:
        print(f"❌ Python no disponible: {e}")
        return False

def check_dependencies():
    """Verificar dependencias críticas"""
    deps = ['customtkinter', 'tkinter', 'sqlite3']
    missing = []

    for dep in deps:
        try:
            if dep == 'tkinter':
                import tkinter
            elif dep == 'customtkinter':
                import customtkinter
            elif dep == 'sqlite3':
                import sqlite3
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - FALTANTE")
            missing.append(dep)

    if missing:
        print(f"\n📦 Instalando dependencias faltantes: {', '.join(missing)}")
        try:
            if 'customtkinter' in missing:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'customtkinter', '--quiet'])
                print("✅ CustomTkinter instalado")
        except Exception as e:
            print(f"❌ Error instalando dependencias: {e}")
            return False

    return True

def test_gui():
    """Probar que la interfaz gráfica funciona"""
    try:
        import customtkinter as ctk
        import tkinter as tk

        print("🖥️  Probando interfaz gráfica...")

        # Configurar tema básico
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Crear ventana de test
        root = ctk.CTk()
        root.title("MP3 FasterFast - Test")
        root.geometry("400x250")

        # Contenido
        title = ctk.CTkLabel(root, text="🎵 MP3 FASTERFAST", font=("Arial", 16, "bold"))
        title.pack(pady=20)

        status = ctk.CTkLabel(root, text="✅ ¡La interfaz funciona!", font=("Arial", 12))
        status.pack(pady=10)

        # Botón para continuar
        def continue_to_app():
            root.destroy()
            launch_main_app()

        btn = ctk.CTkButton(root, text="🚀 CONTINUAR A LA APP", command=continue_to_app, height=35)
        btn.pack(pady=15)

        close_btn = ctk.CTkButton(root, text="❌ SALIR", command=root.quit,
                                fg_color="red", height=30)
        close_btn.pack(pady=5)

        print("✅ Ventana de test creada")
        root.mainloop()
        return True

    except Exception as e:
        print(f"❌ Error en interfaz gráfica: {e}")
        import traceback
        traceback.print_exc()
        return False

def launch_main_app():
    """Lanzar la aplicación principal"""
    try:
        print("\n🚀 Lanzando aplicación principal...")
        # Ejecutar la app principal
        result = subprocess.run([sys.executable, 'MP3FasterFast.pyw'],
                              timeout=30)  # Timeout de 30 segundos
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⚠️  Aplicación iniciada (timeout alcanzado)")
        return True
    except Exception as e:
        print(f"❌ Error lanzando aplicación: {e}")
        return False

def main():
    print("🚀 MP3 FASTERFAST - INICIADOR ROBUSTO")
    print("=" * 50)
    print(f"🕐 {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 {os.getcwd()}")
    print()

    # Verificaciones paso a paso
    if not check_python():
        print("❌ Python no disponible. Descarga desde https://python.org")
        return False

    print()
    if not check_dependencies():
        print("❌ Dependencias faltantes")
        return False

    print()
    if not test_gui():
        print("❌ Interfaz gráfica no funciona")
        print("💡 Posibles causas:")
        print("   - Entorno sin pantalla gráfica (servidor)")
        print("   - Controladores de video desactualizados")
        print("   - Windows en modo headless")
        return False

    print("\n✅ ¡TODO FUNCIONA! Disfruta MP3 FasterFast 🎵")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        input("\nPresiona Enter para salir...")
    else:
        print("\n👋 ¡Aplicación iniciada exitosamente!")
