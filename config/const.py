from os.path import dirname
# from config.secret_const import GENIUS_TOKEN as __GENIUS_TOKEN
from config.secret_const import YANDEX_TOKEN

__MAIN_DIR = f'{dirname(__file__)}/..'
__CONFIG_DIR = f'{dirname(__file__)}'
TEMP_DIR = __MAIN_DIR + '/temp'
ASSETS_DIR = __MAIN_DIR + '/assets'
__DB_DIR = __MAIN_DIR + '/DB'

ARTISTS_DIR = __DB_DIR + '/artists'
RAW_ARTISTS_FILE = __DB_DIR + '/raw_artists.json'
FEAT_ARTISTS_FILE = __DB_DIR + '/feat_artists.json'
ERR_ARTISTS_FILE = __DB_DIR + '/err_artists.json'
DAY_SONG_FILE = __DB_DIR + '/day_song.json'

SONG_INFO_DB = __DB_DIR + '/song_info.db'
NODES_DB = __DB_DIR + '/nodes.db'
VECTORS_DB = __DB_DIR + '/vectors.vdb'
USERS_DB = __DB_DIR + '/users.db'
QUERY_DB = __DB_DIR + '/query.db'
EMOTIONS_DB = __DB_DIR + '/emotions.db'

PHRASES_FILE = __CONFIG_DIR + '/phrases.json'
IMG_NULL_FILE = ASSETS_DIR + '/null.png'
IMG_LOGOS_FILE = ASSETS_DIR + '/logos.png'
IMG_EMOTION_TEMPLATE_FILE = ASSETS_DIR + '/emotion_template.png'

FONT_NOAH_LIGHT = ASSETS_DIR + '/Noah Light.ttf'
DRAW_MAX_RADIUS = 5

# GENIUS_HEADERS = {'Authorization': f'Bearer {__GENIUS_TOKEN}'}
# GENIUS_API_MAIN_URL = "http://api.genius.com"
# GENIUS_MAIN_URL = "http://genius.com"
# GENIUS_SEARCH_URL = GENIUS_API_MAIN_URL + "/search"
# GENIUS_LYRICS_CONTAINER = "Lyrics__Container-sc-1ynbvzw-1 kUgSbL"

YNISON_DEVICE_INFO = {'app_name': 'Chrome', 'type': 1}
YNISON_GRY_MAIN_URL = 'wss://ynison.music.yandex.ru/redirector.YnisonRedirectService/GetRedirectToYnison'
YNISON_PYS_MAIN_URL = 'wss://%%/ynison_state.YnisonStateService/PutYnisonState'

MONTH_NAMES = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
               'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря')

EMOTIONS_COLOR = {
    'Спокойствие': '#fdec85',
    'Радость': '#fce65f',
    'Экстаз': '#f9d706',
    'Признание': '#c7e17f',
    'Доверие': '#b5d856',
    'Восхищение': '#aacc4c',
    'Опасение': '#70c780',
    'Страх': '#43b658',
    'Ужас': '#43a655',
    'Отвлечение': '#80d6b7',
    'Удивление': '#58c9a0',
    'Изумление': '#4bae8b',
    'Задумчивость': '#85b6ff',
    'Печаль': '#5f9fff',
    'Горе': '#5e91de',
    'Скука': '#a7b5f4',
    'Брезгливость': '#8b9ef1',
    'Отвращение': '#7d8fdd',
    'Досада': '#f8828b',
    'Гнев': '#f65a67',
    'Ярость': '#d2545f',
    'Интерес': '#f7be8b',
    'Ожидание': '#f5a967',
    'Бдительность': '#e39653'
}

EMOTIONS_RANG1 = ('Экстаз', 'Восхищение', 'Ужас', 'Изумление', 'Горе', 'Отвращение', 'Ярость', 'Бдительность')
EMOTIONS_RANG2 = ('Радость', 'Доверие', 'Страх', 'Удивление', 'Печаль', 'Брезгливость', 'Гнев', 'Ожидание')
EMOTIONS_RANG3 = ('Спокойствие', 'Признание', 'Опасение', 'Отвлечение', 'Задумчивость', 'Скука', 'Досада', 'Интерес')

EMOTION_RANG1_MULTIPLIER = 900
EMOTION_RANG2_MULTIPLIER = 600
EMOTION_RANG3_MULTIPLIER = 300

ARTISTS_PAGE_SIZE = 10
ARTIST_PAGE_SIZE = 10
ALBUM_PAGE_SIZE = 10
USERS_PAGE_SIZE = 20
QUERY_PAGE_SIZE = 10

MAX_SEARCH_NUMBER = 10

EMBEDDING_MODEL = "ai-forever/ru-en-RoSBERTa"

BASE62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

YANDEX_LINK_PATTERN = r'https://music\.yandex\.ru/album/\d+/track/\d+'
YANDEX_SONG_ID_PATTERN = r'https://music\.yandex\.ru/album/\d+/track/(\d+)'
LINK_PATTERN = r'https://'

# Настоящий -1001914815060
# Тестовый -1002070355602
CHANNEL_ID = -1002070355602
MAIN_ADMIN_ID = 735273809
