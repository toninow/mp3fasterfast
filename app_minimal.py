#!/usr/bin/env python3
"""
Versión mínima de MP3 FasterFast para pruebas
"""

import sys
import os

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

print("Starting minimal MP3 FasterFast...")

try:
    import tkinter as tk
    print("Tkinter OK")
except ImportError as e:
    print(f"Tkinter error: {e}")
    sys.exit(1)

try:
    import customtkinter as ctk
    print("CustomTkinter OK")
except ImportError as e:
    print(f"CustomTkinter error: {e}")
    sys.exit(1)

try:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    print("Theme OK")
except Exception as e:
    print(f"Theme error: {e}")

try:
    root = ctk.CTk()
    root.title("MP3 FasterFast - Minimal")
    root.geometry("500x300")
    print("Window created")
except Exception as e:
    print(f"Window error: {e}")
    sys.exit(1)

# Simple UI
try:
    title = ctk.CTkLabel(root, text="MP3 FASTERFAST", font=("Arial", 18, "bold"))
    title.pack(pady=20)

    status = ctk.CTkLabel(root, text="Aplicación funcionando!", font=("Arial", 12))
    status.pack(pady=10)

    # Simple text area
    text_area = ctk.CTkTextbox(root, height=80)
    text_area.pack(pady=10, padx=20, fill="x")
    text_area.insert("0.0", "Pega tus URLs aquí...")

    # Button
    btn = ctk.CTkButton(root, text="🚀 INICIAR", command=lambda: print("Button clicked"))
    btn.pack(pady=10)

    print("UI created successfully")
except Exception as e:
    print(f"UI error: {e}")

print("Starting mainloop... (will close in 5 seconds)")
root.after(5000, root.quit)
root.mainloop()
print("Mainloop finished successfully!")