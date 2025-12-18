#!/usr/bin/env python3
"""
Script de prueba para verificar que las descargas funcionan
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from downloader import Downloader

def test_download():
    print("🔍 Probando sistema de descargas...")
    print("📡 Verificando conexión a internet...")

    # Verificar conexión a internet
    import urllib.request
    try:
        urllib.request.urlopen('http://www.google.com', timeout=5)
        print("✅ Conexión a internet OK")
    except:
        print("❌ Sin conexión a internet")
        return False

    # Crear downloader
    d = Downloader(lambda msg: print(f"📝 {msg}"))

    # URL de prueba
    url = 'https://www.youtube.com/watch?v=kXYiU_JCYtU'
    print(f"🎵 Intentando descargar: {url}")

    try:
        result = d.download_video(url, 'mp3', 'url')
        if result:
            print("✅ ¡DESCARGA EXITOSA!")
            print("📁 Revisa la carpeta 'downloads/MP3/'")
            return True
        else:
            print("❌ DESCARGA FALLÓ")
            return False
    except Exception as e:
        print(f"💥 ERROR: {str(e)}")
        return False
    finally:
        d.close()

if __name__ == "__main__":
    success = test_download()
    print(f"\n📊 RESULTADO FINAL: {'✅ FUNCIONA' if success else '❌ PROBLEMAS'}")
