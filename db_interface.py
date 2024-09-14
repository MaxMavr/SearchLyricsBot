from config import (sqlite3,
                    SONG_INFO_DB)

con_song_info = sqlite3.connect(SONG_INFO_DB)
cur_song_info = con_song_info.cursor()

cur_song_info.execute('''
    PRAGMA foreign_keys=on;
    
    CREATE TABLE IF NOT EXISTS artists (
        id           INTEGER NOT NULL PRIMARY KEY,
        name         TEXT    NOT NULL DEFAULT 'artist',
        amount_album INTEGER NOT NULL DEFAULT 0
    );
    
    CREATE TABLE IF NOT EXISTS albums (
        id           INTEGER NOT NULL PRIMARY KEY,
        name         TEXT    NOT NULL DEFAULT 'album',
        amount_song  INTEGER NOT NULL DEFAULT 0,
        artist_id    INTEGER,
        FOREIGN KEY  (artist_id) REFERENCES artists(id)
    );
    
    CREATE TABLE IF NOT EXISTS songs (
        id           INTEGER NOT NULL PRIMARY KEY,
        name         TEXT    NOT NULL DEFAULT 'song',
        link_song    TEXT    NOT NULL DEFAULT 'https://music.yandex.ru/',
        album_id     INTEGER,
        FOREIGN KEY (album_id) REFERENCES albums(id)
    )
''')

cur_song_info.close()
con_song_info.close()


def add_song2db(artist: str,
                album: str,
                song: str) -> tuple:

    clear_artist = artist.lower().strip()
    clear_album = album.lower().strip()
    clear_song = song.lower().strip()

    with sqlite3.connect(SONG_INFO_DB) as db:
        cur = db.cursor()

        cur.execute('SELECT id FROM artist WHERE name = ?', (clear_artist,))
        artist_code = cur.fetchone()

        cur.execute('SELECT id FROM album WHERE name = ?', (clear_album,))
        album_code = cur.fetchone()[0]

        cur.execute('SELECT id FROM song WHERE name = ?', (clear_song,))
        song_code = cur.fetchone()[0]

    return artist_code, album_code, song_code


def get_song_by_id(song_code: str) -> tuple:
    artist_id, album_id, song_id = song_code.split()

    with sqlite3.connect(SONG_INFO_DB) as db:
        cur = db.cursor()
        cur.execute('SELECT name FROM artist WHERE id = ?', (artist_id,))
        artist = cur.fetchone()[0]

        cur.execute('SELECT name FROM album WHERE id = ?', (album_id,))
        album = cur.fetchone()[0]

        cur.execute('SELECT name FROM song WHERE id = ?', (song_id,))
        song = cur.fetchone()[0]

    return artist, album, song
