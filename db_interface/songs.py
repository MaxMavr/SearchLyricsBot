from config.db import *
from config.const import SONG_INFO_DB


def __create():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                link TEXT,
                have_text BOOLEAN
            )
        ''')
        conn.commit()


def add(song_id: str, title: str, link: str, have_text: bool):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO songs (id, title, link, have_text) VALUES (?, ?, ?, ?)',
                       (song_id, title, link, have_text))
        conn.commit()


def delete(song_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM songs WHERE id = ?', (song_id,))
        conn.commit()


def get(song_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM songs WHERE id = ?', (song_id,))
        return cursor.fetchone()


def is_exists(songs_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM songs WHERE id = ?', (songs_id,))
        return cursor.fetchone()[0] > 0


def count():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM songs')
        return cursor.fetchone()[0]


def count_with_text():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM songs WHERE have_text = 1')
        return cursor.fetchone()[0]


def upd_text_status(song_id: str, have_text: bool):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE songs SET have_text = ? WHERE id = ?', (have_text, song_id))
        conn.commit()


def get_with_text():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM songs WHERE have_text = 1')
        return cursor.fetchall()


__create()
