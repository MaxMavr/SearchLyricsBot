from config import (sqlite3,
                    SONGS_INFO_DB)

con_songs_info = sqlite3.connect(SONGS_INFO_DB)
cur_songs_info = con_songs_info.cursor()

cur_songs_info.execute(''' 
    CREATE TABLE IF NOT EXISTS songs_info (
    artist TEXT NOT NULL DEFAULT 'artist',
    album  TEXT NOT NULL DEFAULT 'album',
    song   TEXT NOT NULL DEFAULT 'song',
    link   TEXT NOT NULL DEFAULT 'https://music.yandex.ru/'
)
''')
cur_songs_info.close()
con_songs_info.close()


def count_songs_info_db(artist: str = None, album: str = None):
    with sqlite3.connect(SONGS_INFO_DB) as con:
        cur = con.cursor()
        if artist is not None:
            if album is not None:
                cur.execute('SELECT COUNT(*) FROM songs_info WHERE artist = ? AND album = ?', (artist, album))
                return cur.fetchone()[0]
            cur.execute('SELECT COUNT(*) FROM songs_info WHERE artist = ?', (artist,))
            return cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM songs_info')
        return cur.fetchone()[0]


def add_songs_info_db(artist: str,
                      album: str,
                      song: str,
                      link: str) -> int:

    with sqlite3.connect(SONGS_INFO_DB) as con:
        cur = con.cursor()

        cur.execute('SELECT rowid FROM songs_info WHERE artist = ? AND album = ? AND song = ?',
                    (artist, album, song))

        song_info = cur.fetchone()

        if song_info is None:
            cur.execute('INSERT INTO songs_info (artist, album, song, link) VALUES (?, ?, ?, ?)',
                        (artist, album, song, link))
            con.commit()

            cur.execute('SELECT rowid FROM songs_info WHERE artist = ? AND album = ? AND song = ?',
                        (artist, album, song))
            return cur.fetchone()[0]

        return song_info[0]


def get_song_info_by_song_code(song_code: int) -> tuple:

    with sqlite3.connect(SONGS_INFO_DB) as db:
        cur = db.cursor()
        cur.execute('SELECT artist = ?, album = ?, song = ?, link = ? FROM songs_info WHERE rowid = ?',
                    (song_code,))
        artist, album, song, link = cur.fetchone()

    return artist, album, song, link


if __name__ == "__main__":
    add_songs_info_db("Дурной Вкус", "светомузыка", "Мяу", "-")
    add_songs_info_db("Дурной Вкус", "светомузыка", "Думаешь ты", "-")
    add_songs_info_db("Дурной Вкус", "светомузыка", "with you", "-")
    add_songs_info_db("Дурной Вкус", "светомузыка", "Висели вместе", "-")
    add_songs_info_db("Дурной Вкус", "светомузыка", "Светомузыка", "-")
    add_songs_info_db("Дурной Вкус", "светомузыка", "kill me", "-")
    add_songs_info_db("Буерак", "Репост модерн", "Ладони", "-")
    add_songs_info_db("Буерак", "Репост модерн", "Репост модерн", "-")
    add_songs_info_db("Буерак", "Репост модерн", "Я танцую сам с собой", "-")
    add_songs_info_db("Буерак", "Репост модерн", "Модные ребята со взглядом в пустоту", "-")
    add_songs_info_db("Буерак", "Репост модерн", "Нет любви", "-")
    add_songs_info_db("Буерак", "Репост модерн", "Грустно", "-")
    add_songs_info_db("Буерак", "Репост модерн", "Неважно", "-")
    add_songs_info_db("Буерак", "Репост модерн", "Тупой", "-")
    add_songs_info_db("Буерак", "Репост модерн", "", "-")
    add_songs_info_db("Буерак", "Голд 2", "Голд 2", "-")
    add_songs_info_db("ТВОИ КОШМАРЫ", "Машинистам", "Машинистам", "-")
