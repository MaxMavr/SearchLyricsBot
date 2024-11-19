from config.db import *
from config.const import SONG_INFO_DB


def __create():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS albums (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                img TEXT,
                data TEXT
            )
        ''')
        conn.commit()


def add(album_id: str, title: str, img: str, data: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO albums (id, title, img, data) VALUES (?, ?, ?, ?)', (album_id, title, img, data))
        conn.commit()


def delete(album_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM albums WHERE id = ?', (album_id,))
        conn.commit()


def get(album_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM albums WHERE id = ?', (album_id,))
        return cursor.fetchone()


def is_exists(albums_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM albums WHERE id = ?', (albums_id,))
        return cursor.fetchone()[0] > 0


def count():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM albums')
        return cursor.fetchone()[0]


__create()
