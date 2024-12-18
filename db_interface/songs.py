from config.db import *
from config.const import SONG_INFO_DB


def __create():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                number_in_album INTEGER NOT NULL,
                have_text BOOLEAN NOT NULL,
                embedded BOOLEAN NOT NULL DEFAULT False
            )
        ''')
        conn.commit()


def add(song_id: str, title: str, number_in_album: int, have_text: bool):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO songs (id, title, number_in_album, have_text) VALUES (?, ?, ?, ?)',
                       (song_id, title, number_in_album, have_text))
        conn.commit()


def delete(song_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM songs WHERE id = ?', (song_id,))
        conn.commit()


def get(song_id: str) -> tuple:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM songs WHERE id = ?', (song_id,))
        return cursor.fetchone()


def get_title(song_id: str) -> str:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM songs WHERE id = ?', (song_id,))
        return cursor.fetchone()[0]


def get_by_title(song_title: str) -> tuple:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM songs WHERE title = ?', (song_title,))
        return cursor.fetchone()


def is_exists(songs_id: str) -> bool:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM songs WHERE id = ?', (songs_id,))
        return cursor.fetchone()[0] > 0


def count() -> int:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM songs')
        return cursor.fetchone()[0]


def count_with_text() -> int:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM songs WHERE have_text = 1')
        return cursor.fetchone()[0]


def upd_text_status(song_id: str, have_text: bool):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE songs SET have_text = ? WHERE id = ?', (have_text, song_id))
        conn.commit()


def upd_embed_status(song_id: str, embedded: bool):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE songs SET embedded = ? WHERE id = ?', (embedded, song_id))
        conn.commit()


def get_for_embedded(start_page_number: int = 0, page_size: int = 20):
    max_page_number = ceil(count_with_text() / page_size)

    with sqlite3.connect(SONG_INFO_DB) as conn:
        for page_number in range(start_page_number, max_page_number + 1):
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM songs WHERE have_text = 1 LIMIT ? OFFSET ?',
                           (page_size, page_number * page_size))
            for song in cursor.fetchall():
                yield song


__create()
