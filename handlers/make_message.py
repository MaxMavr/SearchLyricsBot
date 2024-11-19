

def make_artist_song_lyrics_message(
        lines: str,
        artist: str,
        song: str,
        link: str):

    msg = f'<i>«{lines}»</i>\n\n<a href="{link}">{artist} — {song}</a>'

    return msg


def make_song_lyrics_message(
        lines: str):

    msg = f'<i>«{lines}»</i>'

    return msg


def make_artist_message(
        artist: str,
        albums: list[str]):

    msg = f'<b>{artist}</b>\nАльбомы\n\n'

    for s in albums:
        msg += f'{s}\n'

    return msg


def make_album_message(
        artist: str,
        album: str,
        songs: list[str]):

    msg = f'<b>{artist} — {album}</b>\n\n'

    for s in songs:
        msg += f'{s}\n'

    return msg


def make_artists_message(
        artists: list[str]):

    msg = f'<b>Исполнители</b>\n\n'

    for s in artists:
        msg += f'{s}\n'

    return msg


if __name__ == "__main__":
    pass
