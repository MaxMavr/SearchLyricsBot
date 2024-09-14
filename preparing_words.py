from config import ALL_CHAR_SRT


def cleared_word(word: str) -> str:
    clear_word = ''

    for c in word.lower():
        if c in ALL_CHAR_SRT:
            clear_word += c

    return clear_word


def split_line(line: str) -> tuple:
    clear_line = []

    for w in line.split():
        word = cleared_word(w)
        if len(word) != 0:
            clear_line.append(word)

    return tuple(clear_line)


def split_lyrics(lyrics: str):
    clear_lyrics_line = []

    for r in lyrics.split('\n'):
        cr = r.strip()
        if len(cr) != 0:
            clear_lyrics_line.append(cr)

    return clear_lyrics_line


if __name__ == '__main__':
    pass
