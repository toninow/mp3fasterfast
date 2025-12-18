#!/usr/bin/env python3
"""
Script para quitar emojis de los mensajes de log
"""

import re

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazar emojis en log_message
replacements = {
    '✅': '[OK]',
    '❌': '[ERROR]',
    '🎯': '[INFO]',
    '📋': '[LOG]',
    '🎵': '[MUSIC]',
    '🎬': '[VIDEO]',
    '⚙️': '[CONFIG]',
    '📊': '[STATUS]',
    '🚀': '[START]',
    '🔍': '[SEARCH]',
    '📡': '[CONNECT]',
    '🖼️': '[IMAGE]',
    '👤': '[USER]',
    '💥': '[CRASH]',
    '🗑️': '[CLEAR]',
    '🔄': '[UPDATE]',
    '⏳': '[WAIT]',
    '📥': '[DOWNLOAD]',
    '💾': '[SAVE]',
    '🎨': '[THEME]',
    '🏗️': '[BUILD]',
    '🔒': '[LOCK]',
    '📺': '[TITLE]',
    '🎵': '[AUDIO]',
    '❌': '[CANCEL]',
    '🔴': '[RED]',
    '🟡': '[YELLOW]',
    '🔵': '[BLUE]',
    '🟢': '[GREEN]'
}

for old, new in replacements.items():
    # Solo reemplazar en líneas que contienen log_message
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'log_message(' in line and old in line:
            lines[i] = line.replace(old, new)
    content = '\n'.join(lines)

# Guardar el archivo
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Emojis reemplazados en mensajes de log')
