def make_yandex_song_link(song_id: str, album_id: str) -> str:
    return f'https://music.yandex.ru/album/{album_id}/track/{song_id}'


def make_yandex_album_link(album_id: str) -> str:
    return f'https://music.yandex.ru/album/{album_id}'


def make_yandex_artist_link(artist_id: str) -> str:
    return f'https://music.yandex.ru/artist/{artist_id}'


def make_song_lyrics_message(
        artist_song: str = None,
        song: str = None,
        artist: str = None,
        link: str = None,
        lines: str = None) -> str:

    msg = ''
    if lines:
        msg += f'<i>«{lines}»</i>\n\n'

    if link:
        msg += f'<a href="{link}">'

    if artist_song:
        msg += artist_song

    else:
        if artist:
            msg += f'{artist} — '

        if song:
            msg += song

    if link:
        msg += '</a>'

    return msg
