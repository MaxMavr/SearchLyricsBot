from db_interface.files import (read_raw_artists_file,
                                make_raw_artists_file,
                                upd_err_artists_songs)

from api.music_yandex import (get_album_songs,
                              get_artist_albums,
                              get_artist_id,
                              get_song_lyrics)

import db_interface.artists as artists
import db_interface.albums as albums
import db_interface.songs as songs
import db_interface.bonds as bonds


async def process_raw_artists():
    raw_artists = read_raw_artists_file()
    err_artists = []
    raw_feat_artists = []

    for raw_artist in raw_artists:
        artist_id, artist_title = get_artist_id(raw_artist)

        if artist_id == '':
            err_artists.append(raw_artist)
            continue

        artists.add(artist_id, artist_title)

        for album_id, album_title, album_cover, album_data in get_artist_albums(artist_id):
            albums.add(album_id, album_title, album_cover, album_data)

            for song_id, song_title, song_artists, song_link, song_text in get_album_songs(album_id):
                songs.add(song_id, song_title, song_link, song_text)

                for song_artist_id, song_artist_title in song_artists:
                    if not artists.is_exists(song_artist_id):
                        artists.add(song_artist_id, song_artist_title)
                        raw_feat_artists.append(song_artist_title)

                    bonds.add(song_artist_id, album_id, song_id)

    make_raw_artists_file(raw_feat_artists)
    upd_err_artists_songs(err_artists)


def get_song_lines(song_id):
    lyrics = get_song_lyrics(song_id)
    for line in lyrics.strip():
        clear_line = line.strip()
        if clear_line != '':
            yield clear_line
