# MP3 FasterFast v2.0

Descargador de música y videos desde YouTube con interfaz gráfica moderna.

## 🚀 Inicio Rápido

**¡Doble clic en `MP3FasterFast.bat` y listo!**

## 📁 Estructura del Proyecto

```
MP3FasterFast/
├── MP3FasterFast.bat           # 🚀 LAUNCHER PRINCIPAL
├── app.py                      # Código principal
├── database.py                 # Base de datos
├── downloader.py               # Lógica de descarga
├── utils.py                    # Utilidades
├── bin/                        # Ejecutables
│   ├── yt-dlp.exe
│   └── ffmpeg.exe
├── data/                       # Datos de aplicación
│   └── downloads.db
├── downloads/                  # Archivos descargados
│   ├── MP3/
│   ├── Videos/
│   ├── Playlists/
│   └── Canales/
├── docs/                       # Documentación
│   └── README.md
├── installers/                 # Instalación y diagnóstico
│   ├── diagnostic_MP3FasterFast.py
│   ├── instalar_MP3FasterFast.py
│   └── requirements.txt
└── launchers/                  # Launchers alternativos
    ├── MP3FasterFast_Auto.py
    └── MP3FasterFast_Portable.bat
```

## 🎯 Uso

### Opción 1: Launcher Principal (Recomendado)
```bash
MP3FasterFast.bat
```

### Opción 2: Desde Código Fuente
```bash
python app.py
```

### Opción 3: Launcher Portable
```bash
launchers/MP3FasterFast_Portable.bat
```

## 🔧 Requisitos del Sistema

### Mínimos:
- **Python 3.10+**
- **Windows 10+**
- **1GB espacio libre**

### Dependencias Python:
```
pip install -r installers/requirements.txt
```

O instalar manualmente:
```bash
pip install customtkinter mutagen pillow
```

## 🏗️ Instalación en Otro PC

1. **Copia toda la carpeta** `MP3FasterFast/` a otro ordenador
2. **Ejecuta diagnóstico:**
   ```bash
   python installers/diagnostic_MP3FasterFast.py
   ```
3. **Si todo está bien:**
   ```bash
   MP3FasterFast.bat
   ```

## 🔍 Diagnóstico del Sistema

Ejecuta el diagnóstico para verificar compatibilidad:
```bash
python installers/diagnostic_MP3FasterFast.py
```

El diagnóstico verifica:
- ✅ Versión de Python
- ✅ Dependencias instaladas
- ✅ Ejecutables (yt-dlp, ffmpeg)
- ✅ Espacio en disco

## 🎵 Características

- ✅ **Interfaz moderna** con CustomTkinter
- ✅ **Descarga MP3** de alta calidad (320kbps)
- ✅ **Descarga videos** MP4
- ✅ **Portadas incrustadas** automáticamente
- ✅ **Lista de reproducción** completa
- ✅ **Historial organizado** por fecha
- ✅ **Búsqueda por canales**
- ✅ **100% Portable** - funciona en cualquier PC

## 🐛 Solución de Problemas

### "Python no encontrado"
```bash
# Instalar Python desde:
https://python.org

# Marcar durante instalación:
☑ Add Python to PATH
```

### "Módulos faltantes"
```bash
pip install customtkinter mutagen pillow
```

### "Aplicación no inicia"
```bash
# Ejecutar diagnóstico:
python installers/diagnostic_MP3FasterFast.py
```

### "Archivos .pyw no funcionan"
```bash
# Usar archivos .bat en su lugar:
MP3FasterFast.bat
```

## 📋 Versiones Soportadas

- **Python:** 3.10, 3.11, 3.12
- **Windows:** 10, 11
- **macOS:** 12+ (con ajustes)
- **Linux:** Ubuntu 20.04+

## 🔄 Actualizaciones

Para actualizar:
1. Descarga nueva versión
2. Copia `bin/`, `data/` y `downloads/`
3. Reemplaza archivos antiguos

## 📞 Soporte

Si tienes problemas:
1. Ejecuta el diagnóstico
2. Revisa los logs en `data/`
3. Verifica espacio en disco

## 📜 Licencia

Proyecto personal - Uso libre.

---

**¡Disfruta descargando música con MP3 FasterFast!** 🎵🎶