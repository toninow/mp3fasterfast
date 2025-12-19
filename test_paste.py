#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del botón de pegar
"""

import tkinter as tk

def test_clipboard():
    """Probar diferentes métodos para acceder al portapapeles"""
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana

    print("=== PRUEBA DE PORTAPAPELES ===")

    # Método 1: tkinter
    try:
        content = root.clipboard_get()
        print(f"✅ Tkinter: '{content[:50]}...'")
    except Exception as e:
        print(f"❌ Tkinter falló: {e}")

    # Método 2: pyperclip
    try:
        import pyperclip
        content = pyperclip.paste()
        print(f"✅ Pyperclip: '{content[:50]}...'")
    except Exception as e:
        print(f"❌ Pyperclip falló: {e}")

    # Método 3: PowerShell
    try:
        import subprocess
        result = subprocess.run(
            ["powershell", "-Command", "Get-Clipboard"],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            content = result.stdout.strip()
            print(f"✅ PowerShell: '{content[:50]}...'")
        else:
            print("❌ PowerShell falló: código de retorno no cero")
    except Exception as e:
        print(f"❌ PowerShell falló: {e}")

    root.destroy()
    print("\n💡 Si tienes una URL copiada, debería aparecer arriba.")

if __name__ == "__main__":
    test_clipboard()
