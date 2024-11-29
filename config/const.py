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

PHRASES_FILE = __CONFIG_DIR + '/phrases.json'
IMG_NULL_FILE = ASSETS_DIR + '/null.png'
IMG_LOGOS_FILE = ASSETS_DIR + '/logos.png'

# GENIUS_HEADERS = {'Authorization': f'Bearer {__GENIUS_TOKEN}'}
# GENIUS_API_MAIN_URL = "http://api.genius.com"
# GENIUS_MAIN_URL = "http://genius.com"
# GENIUS_SEARCH_URL = GENIUS_API_MAIN_URL + "/search"
# GENIUS_LYRICS_CONTAINER = "Lyrics__Container-sc-1ynbvzw-1 kUgSbL"

YNISON_DEVICE_INFO = {'app_name': 'Chrome', 'type': 1}
YNISON_GRY_MAIN_URL = 'wss://ynison.music.yandex.ru/redirector.YnisonRedirectService/GetRedirectToYnison'
YNISON_PYS_MAIN_URL = 'wss://%%/ynison_state.YnisonStateService/PutYnisonState'

MONTH_NAMES = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
               'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

ARTISTS_PAGE_SIZE = 10
ARTIST_PAGE_SIZE = 20
ALBUM_PAGE_SIZE = 10
SONG_PAGE_SIZE = 20

USERS_PAGE_SIZE = 20

EMBEDDING_MODEL = "ai-forever/ru-en-RoSBERTa"

YANDEX_LINK_PATTERN = r'https://music\.yandex\.ru/album/\d+/track/\d+'
YANDEX_SONG_ID_PATTERN = r'https://music\.yandex\.ru/album/\d+/track/(\d+)'
LINK_PATTERN = r'https://'

# Настоящий -1001914815060
# Тестовый -1002070355602
CHANNEL_ID = -1002070355602
MAIN_ADMIN_ID = 735273809
