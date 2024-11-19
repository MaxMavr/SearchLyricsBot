from config.db import *
from config.const import SONG_INFO_DB


def __create():
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bonds (
                id_artist TEXT,
                id_album TEXT,
                id_song TEXT,
                FOREIGN KEY (id_artist) REFERENCES artists(id),
                FOREIGN KEY (id_album) REFERENCES albums(id),
                FOREIGN KEY (id_song) REFERENCES songs(id)
            )
        ''')
        conn.commit()


def add(id_artist: str, id_album: str, id_song: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bonds (id_artist, id_album, id_song) VALUES (?, ?, ?)', (id_artist, id_album, id_song))
        conn.commit()


def get_album_ids_by_artist(id_artist: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT id_album FROM bonds WHERE id_artist = ?', (id_artist,))
        return cursor.fetchall()


def get_ids_by_artist(id_artist: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bonds WHERE id_artist = ?', (id_artist,))
        return cursor.fetchall()


def get_ids_by_album(id_album: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bonds WHERE id_album = ?', (id_album,))
        return cursor.fetchall()


def get_ids_by_song(id_song: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bonds WHERE id_song = ?', (id_song,))
        return cursor.fetchall()


# def get_nodes_by_page(page_number, page_size=20):
#     offset = (page_number - 1) * page_size  # Вычисляем смещение
#     with sqlite3.connect(NODES_DB) as conn:
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM nodes LIMIT ? OFFSET ?', (page_size, offset))
#         return cursor.fetchall()


def is_exists_artist(artist_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM bonds WHERE id_artist = ?', (artist_id,))
        return cursor.fetchone()[0] > 0


def is_exists_album(album_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM bonds WHERE id_album = ?', (album_id,))
        return cursor.fetchone()[0] > 0


def is_exists_song(song_id: str):
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM bonds WHERE id_song = ?', (song_id,))
        return cursor.fetchone()[0] > 0


__create()
