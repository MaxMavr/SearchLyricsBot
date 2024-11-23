from config.net import *
from config.const import YANDEX_TOKEN
from db_interface.files import (read_day_song,
                                upd_day_song)


__client = Client(YANDEX_TOKEN).init()


def get_song_lyrics(song_id) -> Union[str, None]:
    song = __client.tracks(song_id)[0]
    if song.lyrics_info.has_available_text_lyrics:
        return song.get_lyrics().fetch_lyrics()
    else:
        return None


def get_album_songs(album_id):
    response = __client.albums_with_tracks(album_id)

    for volume in response.volumes:
        for song in volume:
            song_id = str(song.id)
            title = song.title
            artists_id = [(str(artist.id), artist.name) for artist in song.artists]

            have_lyrics = song.lyrics_info.has_available_text_lyrics

            yield song_id, title, artists_id, have_lyrics


def get_artist_albums(artist_id):
    page = 0
    response = __client.artists_direct_albums(artist_id, page=page)

    while len(response.albums) != 0:
        for album in response.albums:
            yield str(album.id), album.title, album.cover_uri, str(album.release_date)

        page += 1
        response = __client.artists_direct_albums(artist_id, page=page)


def get_song_artist_title(song_id: str) -> Tuple[str, str]:
    song = __client.tracks(song_id)[0]
    return song.title, ', '.join([artist.name for artist in song.artists])


def search_artist_id(artist_title: str) -> Tuple[str, str]:
    search_result = __client.search(artist_title)

    if search_result.best.type == 'artist':
        if search_result.best.result.name.lower() == artist_title.lower():
            return str(search_result.best.result.id), search_result.best.result.name
    return '', ''


def get_day_song() -> Optional[Tuple[str, str, str, str]]:
    # queue_id = __client.queues_list()[0].id
    # queue = __client.queue(queue_id)

    # if len(queue.tracks) <= 0:
    #     return read_day_song()
    return read_day_song()

    # song_id = queue.get_current_track()
    # song = song_id.fetch_track()
    #
    # artists_title = ', '.join(artist.name for artist in song.artists)
    #
    # upd_day_song([song.title, str(song.id), artists_title, str(song.albums[0].id)])
    # return song.title, str(song.id), artists_title, str(song.albums[0].id)


def set_day_song(album_id: str, song_id: str):
    song = __client.tracks(song_id)[0]
    artists_title = ', '.join(artist.name for artist in song.artists)

    upd_day_song([song.title, song_id, artists_title, album_id])

