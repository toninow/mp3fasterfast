# 🎵 MP3 FasterFast - Descargador de Música Portable

> **Aplicación completamente portable** para descargar música y videos desde YouTube sin instalación. Solo copia y ejecuta.

[![Windows](https://img.shields.io/badge/Plataforma-Windows%2010%2F11-blue.svg)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-red.svg)](https://opensource.org/licenses/MIT)

## 🚀 Características Principales

### ✨ **Completamente Portable**
- **Cero instalación**: Copia la carpeta a cualquier PC Windows y funciona
- **Sin dependencias externas**: Todo incluido en el paquete
- **Sin registros del sistema**: No modifica Windows ni deja rastros
- **Ejecutable directo**: Solo necesitas Python instalado

### 🎵 **Descargas de Música**
- **MP3 de alta calidad**: Conversión automática con FFmpeg
- **Playlists completas**: Descarga todas las canciones de una playlist
- **Canales de YouTube**: Descarga contenido completo de canales
- **Metadatos automáticos**: Título, artista, álbum y portada
- **Descargas múltiples**: Pega varias URLs y descárgalas en lote

### 🎬 **Videos y Más**
- **Videos MP4**: Mejor calidad disponible hasta 720p
- **Solo audio**: MP3 limpio sin video
- **Playlists MP4**: Videos completos de playlists
- **Velocidad optimizada**: Descargas rápidas y eficientes

### 🛠️ **Características Avanzadas**
- **Historial completo**: Registro de todas las descargas con contador
- **Eliminación fácil**: Borra descargas del historial con un clic
- **Editor de metadatos**: Edita título, artista, álbum (doble clic en MP3)
- **Descargas por lotes**: Procesa múltiples URLs simultáneamente
- **Interfaz sobria**: Diseño profesional y ordenado
- **Registro de actividad**: Log detallado con opción de limpiar

## 📦 Instalación y Uso

### 🔧 Requisitos Previos
- **Windows 10/11**
- **Python 3.10+** instalado ([Descargar Python](https://python.org))

### 📥 Descarga
```bash
# Clona el repositorio
git clone https://github.com/TU_USUARIO/mp3fasterfast.git
cd mp3fasterfast
```

### ▶️ Ejecución
**Opción 1 - Archivo batch (Recomendado):**
```cmd
Ejecutar.bat
```

**Opción 2 - Línea de comandos:**
```bash
python app.py
```

## 🎯 Cómo Usar

### 1. **Descargar Música (Individual o Múltiple)**
1. Selecciona el **tipo de descarga**: `MP3 (Audio)`, `Video (MP4)`, `Playlist MP3` o `Playlist MP4`
2. **Pega las URLs** en el área de texto (una por línea)
3. El contador muestra automáticamente cuántas URLs tienes
4. Haz clic en **"🚀 Iniciar Descargas"**
5. ¡Listo! Se descargarán en orden secuencial

### 2. **Editar Metadatos MP3**
1. Ve al **historial** de descargas
2. **Doble clic** en cualquier archivo MP3
3. Edita título, artista, álbum y comentario
4. **Guardar** directamente en el archivo

### 3. **Gestionar Historial**
- **Actualizar**: Botón para recargar el historial
- **Eliminar**: Selecciona y haz clic en "Eliminar del historial"
- **Contador**: Muestra el número total de descargas

### 4. **Registro de Actividad**
- **Ver logs**: Área dedicada para seguimiento de descargas
- **Limpiar**: Botón para limpiar el registro
- **Mensajes detallados**: Información completa de cada proceso

## 📁 Estructura de Archivos

```
mp3fasterfast/
├── 📄 app.py                 # Interfaz gráfica principal
├── 📄 database.py            # Base de datos SQLite
├── 📄 downloader.py          # Motor de descargas yt-dlp
├── 📄 metadata.py            # Editor de metadatos MP3
├── 📄 scheduler.py           # Programador de descargas
├── 📄 utils.py               # Utilidades y configuración
├── 🖥️  yt-dlp.exe            # Ejecutable YouTube downloader
├── 🎵 ffmpeg.exe             # Conversor audio/video
├── 📋 Ejecutar.bat           # Script de inicio
└── 📖 README.md              # Este archivo
```

## 🔄 Carpetas Creadas Automáticamente

Al ejecutar por primera vez, se crean estas carpetas:

```
downloads/
├── MP3/           # Música MP3 descargada
├── Videos/        # Videos MP4 descargados
├── Playlists/     # Playlists MP3/MP4
└── Canales/       # Contenido de canales

data/
└── downloads.db   # Base de datos SQLite
```

## 🛡️ Seguridad y Privacidad

- **Sin telemetría**: No envía datos a servidores externos
- **Archivos locales**: Todo se guarda en tu PC
- **Sin dependencias online**: Funciona sin conexión a internet (excepto para descargar)
- **Código abierto**: Puedes revisar exactamente qué hace

## 🔧 Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje principal
- **CustomTkinter**: Interfaz moderna y atractiva
- **yt-dlp**: Motor de descarga de YouTube (actualizado)
- **FFmpeg**: Conversión audio/video profesional
- **SQLite**: Base de datos local ligera
- **Mutagen**: Edición de metadatos MP3
- **Threading**: Operaciones en segundo plano

## 📋 Requisitos de Sistema

| Componente | Requisito |
|------------|-----------|
| **SO** | Windows 10/11 |
| **Python** | 3.10 o superior |
| **RAM** | 512MB mínimo |
| **Disco** | 50MB para programa + espacio para descargas |
| **Internet** | Solo para descargar contenido |

## 🚨 Solución de Problemas

### ❌ "Python no encontrado"
- Instala Python desde [python.org](https://python.org)
- Asegúrate de marcar "Add Python to PATH"

### ❌ "yt-dlp.exe no encontrado"
- Verifica que todos los archivos estén en la misma carpeta
- No muevas archivos individuales

### ❌ "Error de descarga"
- Verifica que la URL de YouTube sea válida
- Algunos videos requieren cuenta premium o tienen restricciones

### ❌ "Ventana no aparece"
- Verifica que tengas entorno gráfico disponible
- Ejecuta desde línea de comandos para ver errores

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/nueva-funcion`)
3. Commit cambios (`git commit -am 'Agrega nueva función'`)
4. Push a la rama (`git push origin feature/nueva-funcion`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Motor de descarga
- [FFmpeg](https://ffmpeg.org/) - Conversión multimedia
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Interfaz moderna
- [Mutagen](https://github.com/quodlibet/mutagen) - Metadatos MP3

---

## 🎉 ¡Disfruta tu música!

**MP3 FasterFast** - La forma más sencilla de descargar música desde YouTube sin complicaciones. 🎵✨

*¿Te gusta el proyecto? ¡Deja una ⭐ en GitHub!*
