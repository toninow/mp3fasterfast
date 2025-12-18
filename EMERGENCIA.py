#!/usr/bin/env python3
"""
Modo de emergencia - Versión ultra simple de MP3 FasterFast
"""

import sys
import os

print("🚨 MODO EMERGENCIA - MP3 FASTERFAST")
print("=" * 40)

try:
    # Imports mínimos
    import tkinter as tk
    print("✅ Tkinter OK")

    import customtkinter as ctk
    print("✅ CustomTkinter OK")

    # Configuración básica
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")  # Tema más seguro

    # Ventana de emergencia
    root = ctk.CTk()
    root.title("MP3 FasterFast - EMERGENCIA")
    root.geometry("500x350")

    # Contenido mínimo
    title = ctk.CTkLabel(root, text="🚨 MODO EMERGENCIA", font=("Arial", 16, "bold"))
    title.pack(pady=20)

    status = ctk.CTkLabel(root, text="✅ La aplicación básica funciona\n❌ Pero hay problemas con la versión completa",
                         font=("Arial", 11))
    status.pack(pady=10)

    # Área de texto para URLs
    text_label = ctk.CTkLabel(root, text="Pega tus URLs aquí:")
    text_label.pack(pady=(20, 5))

    text_area = ctk.CTkTextbox(root, height=80)
    text_area.pack(pady=(0, 20), padx=20, fill="x")
    text_area.insert("0.0", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    # Botón básico
    def test_download():
        urls = text_area.get("0.0", "end").strip()
        if urls:
            status.configure(text=f"🎵 URL detectada:\n{urls[:50]}...")
        else:
            status.configure(text="❌ Pega una URL primero")

    btn = ctk.CTkButton(root, text="🧪 PROBAR URL", command=test_download)
    btn.pack(pady=10)

    # Información de ayuda
    help_text = ctk.CTkLabel(root,
                           text="💡 Si ves esta ventana, significa que:\n" +
                                "   • Python funciona\n" +
                                "   • La interfaz gráfica funciona\n" +
                                "   • Hay un problema específico en la app completa\n\n" +
                                "📧 Reporta el error para solucionarlo",
                           font=("Arial", 9))
    help_text.pack(pady=(20, 10))

    close_btn = ctk.CTkButton(root, text="❌ CERRAR", command=root.quit, fg_color="red")
    close_btn.pack(pady=10)

    print("✅ Modo emergencia iniciado")
    print("🎯 Si ves esta ventana, el problema está en la app principal")
    root.mainloop()

except Exception as e:
    print(f"❌ ERROR CRÍTICO: {e}")
    print("\n🔍 Información del sistema:")
    print(f"Python: {sys.version}")
    print(f"Plataforma: {sys.platform}")
    print(f"Directorio: {os.getcwd()}")

    import traceback
    traceback.print_exc()

    input("\nPresiona Enter para salir...")
