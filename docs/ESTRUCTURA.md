# 📁 Estructura Organizada - MP3 FasterFast

## 🎯 Estructura Principal

```
MP3FasterFast/
├── 🚀 MP3FasterFast.bat           # Launcher principal
├── 📄 MP3FasterFast.pyw           # Launcher alternativo
├── 🔧 MP3FasterFast_Portable.py   # Configurador portable
│
├── 📂 bin/                        # Ejecutables
│   ├── 🎵 yt-dlp.exe
│   └── 🎬 ffmpeg.exe
│
├── 📂 data/                       # Datos de aplicación
│   └── 💾 downloads.db
│
├── 📂 docs/                       # Documentación
│   ├── 📖 README.md
│   └── 🏗️ ESTRUCTURA.md
│
├── 📂 downloads/                  # Archivos descargados
│   ├── 🎵 MP3/
│   ├── 🎬 Videos/
│   ├── 📋 Playlists/
│   └── 📺 Canales/
│
├── 📂 installers/                 # Instalación y diagnóstico
│   ├── 🔍 diagnostic_MP3FasterFast.py
│   ├── ⚙️ instalar_MP3FasterFast.py
│   └── 📋 requirements.txt
│
├── 📂 launchers/                  # Launchers alternativos
│   ├── 🤖 MP3FasterFast_Auto.py
│   ├── 🪟 MP3FasterFast_Portable.bat
│   └── 🚀 INICIAR_MP3FasterFast.bat
│
├── 🎨 logo-fasterfast.png         # Logo de la aplicación
│
└── 💻 Código fuente:
    ├── 🖥️ app.py                  # Aplicación principal (GUI)
    ├── 💾 database.py             # Gestión de base de datos
    ├── ⬇️ downloader.py           # Lógica de descarga
    └── 🛠️ utils.py                # Utilidades y configuración
```

## 📋 Descripción de Carpetas

### 🖥️ **Raíz del Proyecto**
- **`MP3FasterFast.bat`** - **Launcher principal** (haz doble clic aquí)
- **`app.py`** - Código principal de la aplicación
- **`database.py`** - Gestión de SQLite
- **`downloader.py`** - Lógica de descarga de YouTube
- **`utils.py`** - Funciones de utilidad y configuración

### 📂 **bin/**
Contiene los ejecutables necesarios:
- **`yt-dlp.exe`** - Descargador de YouTube
- **`ffmpeg.exe`** - Convertidor de audio/video

### 📂 **data/**
Datos persistentes:
- **`downloads.db`** - Base de datos SQLite con historial

### 📂 **docs/**
Documentación del proyecto:
- **`README.md`** - Manual de usuario completo
- **`ESTRUCTURA.md`** - Este archivo

### 📂 **downloads/**
Archivos descargados organizados por tipo:
- **`MP3/`** - Música en formato MP3
- **`Videos/`** - Videos en MP4
- **`Playlists/`** - Listas de reproducción completas
- **`Canales/`** - Contenido de canales específicos

### 📂 **installers/**
Herramientas de instalación y diagnóstico:
- **`diagnostic_MP3FasterFast.py`** - Verifica compatibilidad del sistema
- **`instalar_MP3FasterFast.py`** - Instalador automático
- **`requirements.txt`** - Lista de dependencias Python

### 📂 **launchers/**
Diferentes formas de iniciar la aplicación:
- **`MP3FasterFast_Portable.bat`** - Funciona en cualquier PC
- **`MP3FasterFast_Auto.py`** - Detector automático de Python
- **`INICIAR_MP3FasterFast.bat`** - Launcher alternativo

## 🎯 Inicio Rápido

### 🚀 Opción Recomendada:
```bash
# Doble clic en:
MP3FasterFast.bat
```

### 🔧 Para Desarrollo:
```bash
python app.py
```

### 🌍 Para Otro PC:
```bash
python installers/diagnostic_MP3FasterFast.py
# Luego:
MP3FasterFast.bat
```

## 📦 Distribución

Para compartir con otros usuarios:
1. **Comprime toda la carpeta** `MP3FasterFast/`
2. **Envía el ZIP** completo
3. **El receptor ejecuta:** `python installers/diagnostic_MP3FasterFast.py`

## 🔄 Actualizaciones

Para actualizar:
1. **Descarga nueva versión**
2. **Copia:** `bin/`, `data/`, `downloads/`
3. **Reemplaza:** archivos de código
4. **Mantén:** configuraciones personalizadas

## 💡 Consejos de Organización

- ✅ **Nunca borres** `data/` o `downloads/`
- ✅ **Copia completa** al mover a otro PC
- ✅ **Usa el diagnóstico** antes de reportar problemas
- ✅ **Lee el README** para uso avanzado

---

**¡Estructura clara y organizada para un desarrollo fácil!** 🏗️✨
