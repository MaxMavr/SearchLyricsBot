from config.db import *
from config.const import RAW_ARTISTS_FILE, ERR_ARTISTS_FILE


def __is_file_exist(path2file: str) -> bool:
    return isfile(path2file) or getsize(path2file) == 0


def __make_json(path2file: str, content: Union[list, dict]):
    with open(path2file, 'w', encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False)


def __read_json(path2file: str) -> Union[list, dict]:
    with open(path2file, 'r', encoding='utf-8') as file:
        return json.load(file)


def read_raw_artists_file() -> list:
    if not __is_file_exist(RAW_ARTISTS_FILE):
        return []
    return __read_json(RAW_ARTISTS_FILE)


def make_raw_artists_file(raw_artists: list):
    __make_json(RAW_ARTISTS_FILE, raw_artists)


def upd_err_artists_songs(err_artists: list):
    if not isfile(ERR_ARTISTS_FILE) or getsize(ERR_ARTISTS_FILE) == 0:
        __make_json(ERR_ARTISTS_FILE, [])
    content = __read_json(ERR_ARTISTS_FILE)
    for err_artist in err_artists:
        content.append(err_artist)
    __make_json(ERR_ARTISTS_FILE, content)


def upd_artist_songs(artist_id: int, song: dict) -> str:
    path2file = f'{ARTISTS_DIR}/{artist_id}.json'

    if not isfile(path2file) or getsize(path2file) == 0:
        __make_json(path2file, [])

    content = __read_json(path2file)
    content.append(song)
    __make_json(path2file, content)

    return path2file
