from config import (DIM,
                    DIM_SPACE,
                    DIM_CHAR,

                    IN_MARK,
                    OUT_MARK,
                    )

from vector_operation import slice_vec2subvec


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


def vec2str(vec: tuple, word: str = None):
    if word is not None:
        vec_line = ''
        for i in range(len(word)):
            if i % 2 == 0:
                vec_line += f'{IN_MARK}{word[i]}{OUT_MARK}'
            else:
                vec_line += f'{word[i]}'
        vec_line += '\n('
    else:
        vec_line = '('

    vec_char = slice_vec2subvec(vec)

    for i in range(DIM_SPACE):
        if vec_char[i][0] == 0:
            vec_line += f'0, ...{DIM - i * DIM_CHAR - 2}..., 0)'  # 2 — это нули
            break

        if i % 2 == 0:
            vec_line += f'{IN_MARK}{str(vec_char[i])[1:-1]}{OUT_MARK}, '
        else:
            vec_line += f'{str(vec_char[i])[1:-1]}, '

    return vec_line


if __name__ == "__main__":
    print(vec2str(
        (30, 2, 0, 30, 0, 4, 30, 3, 2, 30, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        word='лиса'
    ))




