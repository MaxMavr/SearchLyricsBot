from config.net import asyncio

from db_interface.files import (read_raw_artists,
                                clear_raw_artists,
                                upd_feat_artists,
                                upd_err_artists)

from api.music_yandex import (get_album_songs,
                              get_artist_albums,
                              search_artist_id,
                              get_song_lyrics)

import db_interface.artists as artists
import db_interface.albums as albums
import db_interface.songs as songs
import db_interface.bonds as bonds


def process_raw_artists():
    raw_artists = read_raw_artists()
    err_artists = []
    feat_artists = []

    for raw_artist in raw_artists:
        artist_id, artist_title = search_artist_id(raw_artist)

        if not artists.is_exists(artist_id):
            artists.add(artist_id, artist_title, True)
        else:
            artists.upd_take_status(artist_id, True)
        print(artist_id, artist_title)

        for album_id, album_title, album_cover, album_data in get_artist_albums(artist_id):
            if albums.is_exists(album_id):
                continue
            print('\t', album_id, album_title)

            for i, (song_id, song_title, song_artists, have_text) in enumerate(get_album_songs(album_id)):
                if songs.is_exists(song_id):
                    continue
                songs.add(song_id, song_title, i, have_text)
                print('\t\t', song_id, song_title, song_artists, have_text)

                for song_artist_id, song_artist_title in song_artists:
                    if not artists.is_exists(song_artist_id):
                        artists.add(song_artist_id, song_artist_title)
                        feat_artists.append(song_artist_title)

                    bonds.add(song_artist_id, album_id, song_id)

            albums.add(album_id, album_title, album_cover, album_data)

    # clear_raw_artists()
    upd_feat_artists(feat_artists)
    upd_err_artists(err_artists)


def compress_lines(lines: list) -> list:
    compressed_lines = list(dict.fromkeys(lines))

    two_lines = []
    for ln in range(0, len(compressed_lines), 2):
        two_lines.append(' '.join(compressed_lines[ln:ln + 2]))

    return two_lines


def get_song_lines(song_id: str):
    lyrics = get_song_lyrics(song_id)
    lines = compress_lines(lyrics.split('\n'))
    for line in lines:
        clear_line = line.strip()
        if clear_line != '':
            yield clear_line


def get_line_by_id(song_id: str, line_id: int) -> str:
    lyrics = get_song_lyrics(song_id)
    lines = compress_lines(lyrics.split('\n'))
    return lines[line_id]


if __name__ == "__main__":
    process_raw_artists()

