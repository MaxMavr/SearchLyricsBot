from config import ALL_CHAR_SRT


def __cleared_word(word: str) -> str:
    clear_word = ''

    for c in word.lower():
        if c in ALL_CHAR_SRT:
            clear_word += c

    return clear_word


def split_line(line: str) -> tuple:
    clear_line = []

    for w in line.split():
        word = __cleared_word(w)
        if len(word) != 0 and word not in clear_line:
            clear_line.append(word)

    return tuple(clear_line)


def split_lyrics(lyrics: str):
    clear_lyrics_lines = []

    for r in lyrics.split('\n'):
        cr = r.strip()
        if len(cr) != 0 and cr not in clear_lyrics_lines:
            clear_lyrics_lines.append(cr)

    return clear_lyrics_lines


if __name__ == '__main__':
    pass
