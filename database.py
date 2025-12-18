import sqlite3
from datetime import datetime
from utils import DB_FILE, DATA_DIR

class Database:
    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(DB_FILE))
        self.create_tables()

    def create_tables(self):
        """Crear tablas necesarias"""
        cursor = self.connection.cursor()

        # Tabla de descargas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                title TEXT,
                artist TEXT,
                type TEXT CHECK(type IN ('mp3', 'video')) NOT NULL,
                source TEXT CHECK(source IN ('canal', 'playlist', 'url')) NOT NULL,
                file_path TEXT,
                download_date TEXT NOT NULL
            )
        ''')

        # Tabla de descargas programadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                download_type TEXT CHECK(download_type IN ('mp3', 'video', 'playlist_mp3', 'playlist_mp4')) NOT NULL,
                scheduled_time TEXT NOT NULL,
                created_date TEXT NOT NULL
            )
        ''')

        self.connection.commit()

    def add_download(self, url, title, artist, download_type, source, file_path):
        """Agregar registro de descarga"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO downloads (url, title, artist, type, source, file_path, download_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (url, title, artist, download_type, source, file_path, datetime.now().isoformat()))
        self.connection.commit()
        return cursor.lastrowid

    def get_all_downloads(self):
        """Obtener todas las descargas"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM downloads ORDER BY download_date DESC')
        return cursor.fetchall()

    def remove_download(self, download_id):
        """Eliminar registro de descarga"""
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM downloads WHERE id = ?', (download_id,))
        self.connection.commit()

    def add_scheduled_download(self, url, download_type, scheduled_time):
        """Agregar descarga programada"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO scheduled_downloads (url, download_type, scheduled_time, created_date)
            VALUES (?, ?, ?, ?)
        ''', (url, download_type, scheduled_time, datetime.now().isoformat()))
        self.connection.commit()
        return cursor.lastrowid

    def get_scheduled_downloads(self):
        """Obtener descargas programadas pendientes"""
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM scheduled_downloads WHERE scheduled_time > ? ORDER BY scheduled_time',
                      (datetime.now().isoformat(),))
        return cursor.fetchall()

    def remove_scheduled_download(self, download_id):
        """Eliminar descarga programada"""
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM scheduled_downloads WHERE id = ?', (download_id,))
        self.connection.commit()

    def close(self):
        """Cerrar conexión"""
        if self.connection:
            self.connection.close()
