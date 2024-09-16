"""
CHAR_CYR_MTRX = [
    'ё',
    'йцукенгшщзхъ',
    'фывапролджэ',
    'ячсмитьбю'
]

CHAR_LAT_MTRX = [
    'qwertyuiop',
    'asdfghjkl',
    'zxcvbnm'
]

CHAR_NUM_MTRX = '1234567890'

ALL_CHAR_MTRX = [CHAR_NUM_MTRX, CHAR_LAT_MTRX, CHAR_CYR_MTRX]
"""


from os.path import dirname, isfile
from os      import listdir, remove, makedirs
from re      import findall, DOTALL
from math    import sqrt
from typing  import List, Tuple
from typing import Union

import sqlite3
import json
import requests


# Для работы с векторами
# 48 символов по 3 позиции для каждого (см. INDEXED_ALL_CHAR_MTRX)
DIM_SPACE = 48  # Размерность чар-векторного вектора
DIM_CHAR = 3  # Размерность чар-вектора
DIM = DIM_SPACE * DIM_CHAR  # Размерность вектора

SERV_NUM_INDEXS = 2  # Кол-во служебных векторов
LENGTH_INDEX = 0  # Индекс длины вектора
LENGTH_CHAR_INDEX = 1  # Индекс длины вектора

MAX_LENGTH_VEC = sqrt(DIM * 15 ** 2)  # 15 среднее значение координаты

ZERO_VEC = tuple(0 for _ in range(DIM + SERV_NUM_INDEXS))  # пустой вектор (Нулевой)


# Для очисти, перевода слов в вектора,
# Все символы, которые мы обрабатываем (см. INDEXED_ALL_CHAR_MTRX)
ALL_CHAR_SRT = 'abcdefghijklmnopqrstuvwxyz0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
# Индексированная матрица ALL_CHAR_MTRX и обратная к ней
INDEXED_ALL_CHAR_MTRX = {
    "1": (10, 0, 0),
    "2": (10, 0, 1),
    "3": (10, 0, 2),
    "4": (10, 0, 3),
    "5": (10, 0, 4),
    "6": (10, 0, 5),
    "7": (10, 0, 6),
    "8": (10, 0, 7),
    "9": (10, 0, 8),
    "0": (10, 0, 9),
    "q": (20, 0, 0),
    "w": (20, 0, 1),
    "e": (20, 0, 2),
    "r": (20, 0, 3),
    "t": (20, 0, 4),
    "y": (20, 0, 5),
    "u": (20, 0, 6),
    "i": (20, 0, 7),
    "o": (20, 0, 8),
    "p": (20, 0, 9),
    "a": (20, 1, 0),
    "s": (20, 1, 1),
    "d": (20, 1, 2),
    "f": (20, 1, 3),
    "g": (20, 1, 4),
    "h": (20, 1, 5),
    "j": (20, 1, 6),
    "k": (20, 1, 7),
    "l": (20, 1, 8),
    "z": (20, 2, 0),
    "x": (20, 2, 1),
    "c": (20, 2, 2),
    "v": (20, 2, 3),
    "b": (20, 2, 4),
    "n": (20, 2, 5),
    "m": (20, 2, 6),
    "ё": (30, 0, 0),
    "й": (30, 1, 0),
    "ц": (30, 1, 1),
    "у": (30, 1, 2),
    "к": (30, 1, 3),
    "е": (30, 1, 4),
    "н": (30, 1, 5),
    "г": (30, 1, 6),
    "ш": (30, 1, 7),
    "щ": (30, 1, 8),
    "з": (30, 1, 9),
    "х": (30, 1, 10),
    "ъ": (30, 1, 11),
    "ф": (30, 2, 0),
    "ы": (30, 2, 1),
    "в": (30, 2, 2),
    "а": (30, 2, 3),
    "п": (30, 2, 4),
    "р": (30, 2, 5),
    "о": (30, 2, 6),
    "л": (30, 2, 7),
    "д": (30, 2, 8),
    "ж": (30, 2, 9),
    "э": (30, 2, 10),
    "я": (30, 3, 0),
    "ч": (30, 3, 1),
    "с": (30, 3, 2),
    "м": (30, 3, 3),
    "и": (30, 3, 4),
    "т": (30, 3, 5),
    "ь": (30, 3, 6),
    "б": (30, 3, 7),
    "ю": (30, 3, 8),
}
INDEXED_ALL_CHAR_RVS_MTRX = {
    (10, 0, 0): "1",
    (10, 0, 1): "2",
    (10, 0, 2): "3",
    (10, 0, 3): "4",
    (10, 0, 4): "5",
    (10, 0, 5): "6",
    (10, 0, 6): "7",
    (10, 0, 7): "8",
    (10, 0, 8): "9",
    (10, 0, 9): "0",
    (20, 0, 0): "q",
    (20, 0, 1): "w",
    (20, 0, 2): "e",
    (20, 0, 3): "r",
    (20, 0, 4): "t",
    (20, 0, 5): "y",
    (20, 0, 6): "u",
    (20, 0, 7): "i",
    (20, 0, 8): "o",
    (20, 0, 9): "p",
    (20, 1, 0): "a",
    (20, 1, 1): "s",
    (20, 1, 2): "d",
    (20, 1, 3): "f",
    (20, 1, 4): "g",
    (20, 1, 5): "h",
    (20, 1, 6): "j",
    (20, 1, 7): "k",
    (20, 1, 8): "l",
    (20, 2, 0): "z",
    (20, 2, 1): "x",
    (20, 2, 2): "c",
    (20, 2, 3): "v",
    (20, 2, 4): "b",
    (20, 2, 5): "n",
    (20, 2, 6): "m",
    (30, 0, 0): "ё",
    (30, 1, 0): "й",
    (30, 1, 1): "ц",
    (30, 1, 2): "у",
    (30, 1, 3): "к",
    (30, 1, 4): "е",
    (30, 1, 5): "н",
    (30, 1, 6): "г",
    (30, 1, 7): "ш",
    (30, 1, 8): "щ",
    (30, 1, 9): "з",
    (30, 1, 10): "х",
    (30, 1, 11): "ъ",
    (30, 2, 0): "ф",
    (30, 2, 1): "ы",
    (30, 2, 2): "в",
    (30, 2, 3): "а",
    (30, 2, 4): "п",
    (30, 2, 5): "р",
    (30, 2, 6): "о",
    (30, 2, 7): "л",
    (30, 2, 8): "д",
    (30, 2, 9): "ж",
    (30, 2, 10): "э",
    (30, 3, 0): "я",
    (30, 3, 1): "ч",
    (30, 3, 2): "с",
    (30, 3, 3): "м",
    (30, 3, 4): "и",
    (30, 3, 5): "т",
    (30, 3, 6): "ь",
    (30, 3, 7): "б",
    (30, 3, 8): "ю",
}
# (0, n, n) — служебные чар-вектора
END_VEC = tuple(0 for _ in range(DIM_CHAR))  # пустой чар-вектор (Конец вектора)


# Для оформления сообщений (Поменять для ТГ)
IN_MARK = '\033[4m'   # <u>
OUT_MARK = '\033[0m'  # </u>
IN_SKIP = '\033[3m'   # <i>
OUT_SKIP = '\033[0m'  # </i>


# Для работы с файлами и БД
MAIN_DIR = dirname(__file__)

DB_DIR = MAIN_DIR + '/DB'
LYRICS_DIR = DB_DIR + '/lyrics'
VEC_DIR = DB_DIR + '/vectors'
SONGS_INFO_DIR = DB_DIR + '/songs_info'

SONGS_INFO_DB = DB_DIR + '/songs_info.db'

WRD_VECS_FILE = VEC_DIR + '/word_vectors.json'
SRC_VECS_FILE = VEC_DIR + '/search_vectors.json'
NODE_FILE = VEC_DIR + '/node.json'

VEC_TO_LINE_CODE_FILE = DB_DIR + '/vec_to_songs_code.json'


PARSING_XML_PATTERN = r'<(\w+)>(.*?)<\/\1>'


makedirs(DB_DIR, exist_ok=True)
makedirs(LYRICS_DIR, exist_ok=True)
makedirs(VEC_DIR, exist_ok=True)
makedirs(SONGS_INFO_DIR, exist_ok=True)


if __name__ == "__main__":
    pass
