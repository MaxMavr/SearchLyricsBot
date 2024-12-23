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


def get_albums_by_artist_by_page(id_artist: str, page_number: int, page_size: int) -> list:
    offset = (page_number - 1) * page_size
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM albums WHERE id IN (
                          SELECT DISTINCT id_album FROM bonds
                          WHERE id_artist = ?) ORDER BY date DESC LIMIT ? OFFSET ?''', (id_artist, page_size, offset))
        return cursor.fetchall()


def get_songs_by_album_by_page(id_album: str, page_number: int, page_size: int) -> list:
    offset = (page_number - 1) * page_size
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM songs WHERE id IN (
                          SELECT DISTINCT id_song FROM bonds
                          WHERE id_album = ?) ORDER BY number_in_album DESC LIMIT ? OFFSET ?''', (id_album, page_size, offset))
        return cursor.fetchall()


def get_albums_by_artist_select_number(id_artist: str, select_number: int) -> tuple:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM albums WHERE id IN (
                          SELECT DISTINCT id_album FROM bonds
                          WHERE id_artist = ?) ORDER BY date DESC LIMIT 1 OFFSET ?''',
                       (id_artist, select_number))
        return cursor.fetchone()


def get_songs_by_album_select_number(id_album: str, select_number: int) -> tuple:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM songs WHERE id IN (
                          SELECT DISTINCT id_song FROM bonds
                          WHERE id_album = ?) ORDER BY number_in_album DESC LIMIT 1 OFFSET ?''',
                       (id_album, select_number))
        return cursor.fetchone()


def get_album_select_number_by_album_id(artist_id: str, albums_id: str) -> int:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''WITH SortedAlbums AS (SELECT *, ROW_NUMBER() OVER (ORDER BY date DESC) AS RowNum
                          FROM albums WHERE id IN (SELECT DISTINCT id_album FROM bonds WHERE id_artist = ?))
                          SELECT RowNum FROM SortedAlbums WHERE id = ?''',
                       (artist_id, albums_id,))
        return cursor.fetchone()[0]


def get_song_select_number_by_song_id(albums_id: str, song_id: str) -> int:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''WITH SortedSongs AS (SELECT *, ROW_NUMBER() OVER (ORDER BY number_in_album DESC) AS RowNum
                          FROM songs WHERE id IN (SELECT DISTINCT id_song FROM bonds WHERE id_album = ?))
                          SELECT RowNum FROM SortedSongs WHERE id = ?''',
                       (albums_id, song_id,))
        return cursor.fetchone()[0]


def get_by_artist(id_artist: str) -> list:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bonds WHERE id_artist = ?', (id_artist,))
        return cursor.fetchall()


def get_by_album(id_album: str) -> list:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bonds WHERE id_album = ?', (id_album,))
        return cursor.fetchone()


def get_by_song(id_song: str) -> list:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bonds WHERE id_song = ?', (id_song,))
        return cursor.fetchone()


def count_albums_by_artist(id_artist: str) -> int:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM albums WHERE id IN (
                          SELECT DISTINCT id_album FROM bonds
                          WHERE id_artist = ?)''', (id_artist,))
        return cursor.fetchone()[0]


def count_songs_by_album(id_album: str) -> int:
    with sqlite3.connect(SONG_INFO_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM songs WHERE id IN (
                          SELECT DISTINCT id_song FROM bonds
                          WHERE id_album = ?)''', (id_album,))
        return cursor.fetchone()[0]


__create()
