from config.db import *
from config.const import RAW_ARTISTS_FILE, ERR_ARTISTS_FILE, FEAT_ARTISTS_FILE, DAY_SONG_FILE


def __is_file_exist(path2file: str) -> bool:
    if isfile(path2file):
        return getsize(path2file) != 0
    return False


def __make_json(path2file: str, content: Union[list, dict]):
    with open(path2file, 'w', encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False)


def __read_json(path2file: str) -> Union[list, dict]:
    with open(path2file, 'r', encoding='utf-8') as file:
        return json.load(file)


def __upd_list_json(path2file: str, new_content: list):
    if not __is_file_exist(path2file):
        __make_json(path2file, [])
    content = __read_json(path2file)
    content += new_content
    __make_json(path2file, content)


def read_raw_artists() -> list:
    if not __is_file_exist(RAW_ARTISTS_FILE):
        return []
    return __read_json(RAW_ARTISTS_FILE)


def clear_raw_artists():
    __make_json(RAW_ARTISTS_FILE, [])


def upd_feat_artists(feat_artists: list):
    __upd_list_json(FEAT_ARTISTS_FILE, feat_artists)


def upd_err_artists(err_artists: list):
    __upd_list_json(ERR_ARTISTS_FILE, err_artists)


def read_day_song() -> list:
    if not __is_file_exist(DAY_SONG_FILE):
        return [' ', ' ', ' ', ' ']
    return __read_json(DAY_SONG_FILE)


def upd_day_song(day_song: list):
    __make_json(DAY_SONG_FILE, day_song)
