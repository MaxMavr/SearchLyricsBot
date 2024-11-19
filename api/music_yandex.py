from config.net import *
from config.const import YANDEX_TOKEN


__client = Client(YANDEX_TOKEN).init()


def get_song_lyrics(song_id) -> str:
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
            link = f'https://music.yandex.ru/album/{album_id}/track/{song_id}'

            have_lyrics = song.lyrics_info.has_available_text_lyrics

            yield song_id, title, artists_id, link, have_lyrics


def get_artist_albums(artist_id):
    page = 0
    response = __client.artists_direct_albums(artist_id, page=page)

    while len(response.albums) != 0:
        for album in response.albums:
            yield str(album.id), album.title, album.cover_uri, str(album.release_date)

        page += 1
        response = __client.artists_direct_albums(artist_id, page=page)


def get_artist_id(artist_name: str) -> Tuple[str, str]:
    search_result = __client.search(artist_name)

    if search_result.best.type == 'artist':
        if search_result.best.result.name.lower() == artist_name.lower():
            return str(search_result.best.result.id), search_result.best.result.name
    return '', ''
