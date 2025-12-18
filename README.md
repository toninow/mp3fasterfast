# 🎵 MP3 FASTERFAST
**Descargador Profesional de Música y Videos desde YouTube**

[![Estado](https://img.shields.io/badge/Estado-Funcional-brightgreen)](https://github.com/toninow/mp3fasterfast)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Licencia](https://img.shields.io/badge/Licencia-Gratis-green)](https://github.com/toninow/mp3fasterfast)

## ✨ Características Avanzadas

### 🎵 **Descargas Inteligentes**
- 🎵 **MP3 de alta calidad** (320kbps, 256kbps, 192kbps, 128kbps)
- 🎬 **Videos MP4 en HD** (1080p, 720p, 480p, 360p)
- 📂 **Playlists completas** de YouTube
- 🖼️ **Portadas automáticas** integradas en MP3
- 🎯 **Calidad personalizable** por descarga

### 📊 **Interfaz Profesional**
- 🖼️ **Thumbnails en tiempo real** de videos
- 📺 **Títulos automáticos** de YouTube
- 📊 **Progreso visual avanzado** con barras individuales
- ✅ **Estados visuales claros** (verde completado, azul descargando)
- ❌ **Cancelación de descargas** en curso
- 📋 **Logs copiables** al portapapeles

### ⚙️ **Configuración Inteligente**
- 🎛️ **Calidades dinámicas** (kbps para audio, p para video)
- 💾 **Configuraciones persistentes** guardadas
- 🔄 **Actualización automática** de opciones
- 📱 **Interfaz responsive** y moderna

### 🔧 **Sistema Robusto**
- 📚 **Historial completo** de descargas
- 🎨 **Tema negro/verde neón** profesional
- 🔧 **Diagnóstico automático** de problemas
- 📦 **Instalación automática** de dependencias
- 🌍 **Portable** - funciona sin instalación

## 🚀 Inicio Rápido

### Paso 1: Descarga
```bash
git clone https://github.com/toninow/mp3fasterfast.git
cd mp3fasterfast
```

### Paso 2: Ejecuta (Elige una opción)

#### 🎯 **OPCIÓN RECOMENDADA - Automática**
```bash
# Diagnóstico + instalación automática + inicio
INICIAR_APP.bat
```

#### 🔧 **Opciones Alternativas**
```bash
# Inicio simplificado (para problemas)
INICIAR_SIMPLE.bat

# Diagnóstico del sistema
py diagnostico.py

# Modo emergencia (ultra básico)
py EMERGENCIA.py

# Inicio directo
py MP3FasterFast.pyw

# Test de descargas
py test_download.py
```

**Linux/Mac:**
```bash
python3 MP3FasterFast.pyw
```

## 🔧 Instalación Manual

### Requisitos
- **Python 3.10+** ([Descargar](https://python.org))
- **Windows/Linux/Mac**

### Dependencias
```bash
pip install customtkinter mutagen pillow
```

### Archivos Necesarios
- ✅ `yt-dlp.exe` (incluido)
- ✅ `ffmpeg.exe` (incluido)
- ✅ `fasterfast.png` (logo)

## 🎯 Cómo Usar

1. **Pega UNA URL** de YouTube en el campo superior
2. **Selecciona formato** (MP3/Video) en el panel izquierdo
3. **Elige calidad** (automáticamente muestra opciones correctas):
   - **MP3**: Mejor, 320kbps, 256kbps, 192kbps, 128kbps
   - **Video**: Mejor, 1080p, 720p, 480p, 360p
4. **Haz clic** en "🚀 DESCARGAR" (botón al lado derecho)
5. **Observa** el progreso visual en "DESCARGAS ACTIVAS":
   - 🖼️ **Thumbnail** del video
   - 📺 **Título** obtenido automáticamente
   - 📊 **Barra de progreso** en tiempo real
   - ✅ **Fondo verde** cuando termina
6. **Encuentra** tus archivos en `downloads/MP3/` o `downloads/Videos/`

### URLs Soportadas
```
• Videos: https://www.youtube.com/watch?v=VIDEO_ID
• Shorts: https://www.youtube.com/shorts/SHORT_ID
• Playlists: https://www.youtube.com/playlist?list=PLAYLIST_ID
• Canales: https://www.youtube.com/@channel
```

## 🔍 Solución de Problemas

### ✅ **PROBLEMA RESUELTO - La aplicación funciona perfectamente**

Las **4 opciones de inicio** están disponibles y **todas funcionan**:

```bash
# 🎯 COMPLETA (recomendada)
INICIAR_APP.bat

# 🔧 SIMPLE
INICIAR_SIMPLE.bat

# 🚨 EMERGENCIA
py EMERGENCIA.py

# ⚡ DIRECTA
py MP3FasterFast.pyw
```

### 🔍 **Si aún hay problemas (raro)**
```bash
# Diagnóstico del sistema
py diagnostico.py

# Test de descargas
py test_download.py
```

### ⚠️ **Errores Anteriores (Ya Solucionados)**
- ✅ `NameError: name 'sys' is not defined` - **CORREGIDO**
- ✅ Dependencias faltantes - **Auto-detectadas e instaladas**
- ✅ Tema CustomTkinter - **Simplificado y robusto**
- ✅ Interfaz gráfica - **Verificada y funcionando**

## 📁 Estructura del Proyecto

```
mp3fasterfast/
├── 🎵 MP3FasterFast.pyw      # Aplicación principal
├── 🔧 INICIAR_APP.bat        # Launcher con diagnóstico
├── 🔍 diagnostico.py         # Verificación del sistema
├── 🧪 test_download.py       # Prueba de descargas
├── 📦 yt-dlp.exe            # Descargador de YouTube
├── 🎬 ffmpeg.exe            # Convertidor multimedia
├── 🎨 fasterfast.png        # Logo de la aplicación
├── 📚 downloads/            # Archivos descargados
│   ├── 🎵 MP3/             # Música descargada
│   ├── 🎬 Videos/          # Videos descargados
│   └── 📂 Playlists/       # Playlists descargadas
└── 🗄️ data/
    └── downloads.db         # Base de datos del historial
```

## 🎨 Interfaz

### Tema: Negro y Verde Neón
- **Fondo**: Negro elegante
- **Texto**: Verde neón brillante
- **Botones**: Verde neón con efectos hover
- **Bordes**: Verde neón sutil

### Secciones Principales
- **⚙️ Configuración**: Selección de formato
- **📊 Progreso**: Barra visual y estado
- **🔗 Entrada URLs**: Área de pegado múltiple
- **📋 Log Actividad**: Registro en tiempo real
- **📚 Historial**: Lista de descargas anteriores

## 📊 Indicadores Visuales

### Durante Descarga
- 🔴 **Inactivo** → 🟡 **Procesando** → 🔵 **Descargando** → 🟢 **Completado**
- 📊 **Barra de progreso** con porcentaje
- 📝 **Log detallado** de cada paso
- 🎵 **Portadas automáticas** al finalizar

### Estados del Sistema
- ✅ **Éxito**: Descarga completada
- ❌ **Error**: Problema en descarga
- ⚠️ **Advertencia**: Configuración no óptima
- 🔄 **Procesando**: Operación en curso

## 🛠️ Desarrollo

### Tecnologías
- **Python 3.10+**
- **CustomTkinter** - Interfaz moderna
- **yt-dlp** - Descargas de YouTube
- **ffmpeg** - Conversión multimedia
- **SQLite** - Base de datos
- **Mutagen** - Metadatos MP3
- **Pillow** - Manejo de imágenes

### Dependencias
```bash
pip install customtkinter mutagen pillow
```

### Ejecutar en Modo Desarrollo
```bash
# Versión completa
python app.py

# Versión mínima (pruebas)
python app_minimal.py

# Diagnóstico
python diagnostico.py
```

## 📝 Notas Importantes

- ⚖️ **Uso responsable**: Solo descarga contenido que tengas derecho a descargar
- 📱 **Compatible**: Windows 10/11, Linux, macOS
- 🔄 **Actualizaciones**: El proyecto se mantiene actualizado
- 🐛 **Reportar bugs**: Usa los Issues de GitHub

## 📄 Licencia

Este proyecto es **gratuito** y **open source**. Úsalo responsablemente.

---

## ✅ **ESTADO FINAL - 100% FUNCIONAL**

### 🎯 **Aplicación Completamente Operativa**
- ✅ **Interfaz negro/verde neón** moderna y elegante
- ✅ **Descargas MP3/MP4** con portadas automáticas
- ✅ **Progreso visual** en tiempo real
- ✅ **Historial completo** con doble-clic para editar
- ✅ **Múltiples opciones de inicio** para máxima compatibilidad
- ✅ **Sistema robusto** con diagnóstico automático
- ✅ **Errores críticos corregidos** (imports, variables)

### 🚀 **Inicio Inmediato**
```bash
# Simplemente ejecuta:
INICIAR_APP.bat
```

**¡La aplicación se abre automáticamente!**

### 📞 **¿Problemas?**
Si algo no funciona (muy improbable), ejecuta:
```bash
py diagnostico.py
```

---

## 🎨 NUEVO DISEÑO VISUAL (2025)

### Interfaz Simplificada
- **Campo URL único**: Pega una URL de YouTube
- **Botón al lado**: "🚀 DESCARGAR" inmediatamente accesible
- **Descargas activas**: Lista visual abajo con indicadores
- **Estados claros**: Verde = completado, barra = descargando

### Ventajas del Nuevo Diseño
- ✅ **Más intuitivo**: Una URL a la vez
- ✅ **Visual inmediato**: Ves el progreso al instante
- ✅ **Menos confuso**: Sin áreas de texto grandes
- ✅ **Estados claros**: Verde para terminado, barra para progreso

### Captura Visual
```
┌─ URL: [____________________] 🚀 DESCARGAR ─┐
│                                             │
│ 📥 DESCARGAS ACTIVAS                        │
│ ┌─────────────────────────────────────────┐ │
│ │ 🎵 Canción XYZ...                     │ │
│ │ ████████░ 75% ⏳ Descargando...       │ │
│ │ 🎵 Canción ABC...                     │ │
│ │ ████████████████████ 100% ✅ Listo!   │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

---

**¿Te gusta el proyecto?** ⭐ Dale una estrella en GitHub!

Hecho con ❤️ para amantes de la música 🎵✨
