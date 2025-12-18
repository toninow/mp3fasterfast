#!/usr/bin/env python3

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Probando imports...")

try:
    import customtkinter as ctk
    print("✓ customtkinter importado correctamente")
except ImportError as e:
    print(f"✗ Error importando customtkinter: {e}")
    sys.exit(1)

try:
    import mutagen
    print("✓ mutagen importado correctamente")
except ImportError as e:
    print(f"✗ Error importando mutagen: {e}")
    sys.exit(1)

try:
    from utils import validate_dependencies, ensure_directories
    print("✓ utils importado correctamente")
except ImportError as e:
    print(f"✗ Error importando utils: {e}")
    sys.exit(1)

try:
    from database import Database
    print("✓ database importado correctamente")
except ImportError as e:
    print(f"✗ Error importando database: {e}")
    sys.exit(1)

# Verificar dependencias
print("\nVerificando dependencias...")
missing = validate_dependencies()
if missing:
    print(f"✗ Faltan dependencias: {missing}")
    sys.exit(1)
else:
    print("✓ Todas las dependencias están presentes")

# Crear directorios
print("\nCreando directorios...")
ensure_directories()
print("✓ Directorios creados")

# Probar base de datos
print("\nProbando base de datos...")
try:
    db = Database()
    downloads = db.get_all_downloads()
    print(f"✓ Base de datos funcionando. {len(downloads)} descargas encontradas")
    db.close()
except Exception as e:
    print(f"✗ Error con base de datos: {e}")
    sys.exit(1)

print("\n🎉 Todos los tests pasaron correctamente!")
print("La aplicación debería funcionar. Si no ves la ventana, verifica que tengas un entorno gráfico disponible.")
