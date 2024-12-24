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


def get(artist_id: str) -> tuple:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM artists WHERE id = ?', (artist_id,))
        return cursor.fetchone()


def get_title(artist_id: str) -> str:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM artists WHERE id = ?', (artist_id,))
        return cursor.fetchone()[0]


def get_by_page(page_number: int, page_size: int) -> list:
    offset = (page_number - 1) * page_size
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM artists ORDER BY (take_songs = 0), title ASC LIMIT ? OFFSET ?',
                       (page_size, offset))
        return cursor.fetchall()


def get_by_select_number(select_number: int) -> tuple:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM artists ORDER BY (take_songs = 0), title ASC LIMIT 1 OFFSET ?',
                       (select_number,))
        return cursor.fetchone()


def get_select_number_by_id(artist_id: str) -> int:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''WITH SortedArtists AS (SELECT *, ROW_NUMBER() OVER (ORDER BY (take_songs = 0), title ASC) AS RowNum
                          FROM artists)
                          SELECT RowNum FROM SortedArtists WHERE id = ?''',
                       (artist_id,))
        return cursor.fetchone()[0]


def is_exists(artist_id: str) -> bool:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM artists WHERE id = ?', (artist_id,))
        return cursor.fetchone()[0] > 0


def upd_take_status(artist_id: str, take_songs: bool):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE artists SET take_songs = ? WHERE id = ?', (take_songs, artist_id))
        conn.commit()


def count() -> int:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM artists')
        return cursor.fetchone()[0]


def count_take_song() -> int:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM artists WHERE take_songs = 1')
        return cursor.fetchone()[0]


__create()
