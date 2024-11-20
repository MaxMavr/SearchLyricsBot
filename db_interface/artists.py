from config.db import *
from config.const import SONG_INFO_DB


def __create():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS artists (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                take_songs BOOLEAN DEFAULT False
            )
        ''')
        conn.commit()


def add(artist_id: str, title: str, take_songs: bool = False):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO artists (id, title, take_songs) VALUES (?, ?, ?)', (artist_id, title, take_songs))
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


def get_by_page(page_number: int, page_size: int = 20):
    offset = (page_number - 1) * page_size
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bonds LIMIT ? OFFSET ? WHERE take_songs = 1', (page_size, offset))
        return cursor.fetchall()


def is_exists(artist_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM artists WHERE id = ?', (artist_id,))
        return cursor.fetchone()[0] > 0


def upd_take_status(artist_id: str, take_songs: bool):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE artists SET take_songs = ? WHERE id = ?', (take_songs, artist_id))
        conn.commit()


def count():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM artists')
        return cursor.fetchone()[0]


def count_take_song():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM artists WHERE take_songs = 1')
        return cursor.fetchone()[0]


__create()
