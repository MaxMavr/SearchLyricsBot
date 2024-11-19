from config.db import *
from config.const import SONG_INFO_DB


def __create():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS artists (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL
            )
        ''')
        conn.commit()


def add(artist_id: str, title: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO artists (id, title) VALUES (?, ?)', (artist_id, title))
        conn.commit()


def delete(artist_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM artists WHERE id = ?', (artist_id,))
        conn.commit()


def get(artist_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM artists WHERE id = ?', (artist_id,))
        return cursor.fetchone()


def is_exists(artist_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM artists WHERE id = ?', (artist_id,))
        return cursor.fetchone()[0] > 0


def count():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM artists')
        return cursor.fetchone()[0]


__create()
