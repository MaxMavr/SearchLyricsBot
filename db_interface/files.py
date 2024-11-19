from config.db import *
from config.const import RAW_ARTISTS_FILE, ERR_ARTISTS_FILE, FEAT_ARTISTS_FILE


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


def clear_raw_artists_file():
    if not isfile(RAW_ARTISTS_FILE):
        return
    remove(RAW_ARTISTS_FILE)


def upd_feat_artists_songs(feat_artists: list):
    if not __is_file_exist(FEAT_ARTISTS_FILE):
        __make_json(FEAT_ARTISTS_FILE, [])
    content = __read_json(FEAT_ARTISTS_FILE)
    for feat_artist in feat_artists:
        content.append(feat_artist)
    __make_json(FEAT_ARTISTS_FILE, content)


def upd_err_artists_songs(err_artists: list):
    if not __is_file_exist(ERR_ARTISTS_FILE):
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
