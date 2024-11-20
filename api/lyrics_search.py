from config.net import asyncio

from db_interface.files import (read_raw_artists_file,
                                clear_raw_artists_file,
                                upd_feat_artists_songs,
                                upd_err_artists_songs)

from api.music_yandex import (get_album_songs,
                              get_artist_albums,
                              get_artist_id,
                              get_song_lyrics)

import db_interface.artists as artists
import db_interface.albums as albums
import db_interface.songs as songs
import db_interface.bonds as bonds


def process_raw_artists():
    raw_artists = read_raw_artists_file()
    err_artists = []
    feat_artists = []

    for raw_artist in raw_artists:
        artist_id, artist_title = get_artist_id(raw_artist)

        if not artists.is_exists(artist_id):
            artists.add(artist_id, artist_title, True)
        print(artist_id, artist_title)

        for album_id, album_title, album_cover, album_data in get_artist_albums(artist_id):
            if albums.is_exists(album_id):
                continue
            print('\t', album_id, album_title)

            for song_id, song_title, song_artists, song_link, have_text in get_album_songs(album_id):
                if songs.is_exists(song_id):
                    continue
                songs.add(song_id, song_title, song_link, have_text)
                print('\t\t', song_id, song_title, song_artists, have_text)

                for song_artist_id, song_artist_title in song_artists:
                    if not artists.is_exists(song_artist_id):
                        artists.add(song_artist_id, song_artist_title)
                        feat_artists.append(song_artist_title)

                    bonds.add(song_artist_id, album_id, song_id)

            albums.add(album_id, album_title, album_cover, album_data)

    clear_raw_artists_file()
    upd_feat_artists_songs(feat_artists)
    upd_err_artists_songs(err_artists)


# def clear_repeats():
#     for song_id, song_title, _, have_text, _ in songs.get_with_text():
#         repeats = songs.get_by_title(song_title)


def get_song_lines(song_id):
    lyrics = get_song_lyrics(song_id)

    lines = lyrics.split('\n')
    lines = list(dict.fromkeys(lines))

    two_lines = [lines[j:j + 2] for j in range(0, len(lines), 2)]

    for line in two_lines:
        clear_line = " ".join(line).strip()
        if clear_line != '':
            yield clear_line


if __name__ == "__main__":
    process_raw_artists()
