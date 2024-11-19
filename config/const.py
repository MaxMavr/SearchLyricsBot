from os.path import dirname
from config.secret_const import GENIUS_TOKEN as __GENIUS_TOKEN
from config.secret_const import YANDEX_TOKEN

__MAIN_DIR = f'{dirname(__file__)}/../'
__CONFIG_DIR = f'{dirname(__file__)}/'
__DB_DIR = __MAIN_DIR + '/DB'
ARTISTS_DIR = __DB_DIR + '/artists'
RAW_ARTISTS_FILE = __DB_DIR + '/raw_artists.json'
ERR_ARTISTS_FILE = __DB_DIR + '/err_artists.json'

SONG_INFO_DB = __DB_DIR + '/song_info.db'
NODES_DB = __DB_DIR + '/nodes.db'
USERS_DB = __DB_DIR + '/users.db'

PHRASES_FILE = __CONFIG_DIR + '/phrases.json'

# GENIUS_HEADERS = {'Authorization': f'Bearer {__GENIUS_TOKEN}'}
# GENIUS_API_MAIN_URL = "http://api.genius.com"
# GENIUS_MAIN_URL = "http://genius.com"
# GENIUS_SEARCH_URL = GENIUS_API_MAIN_URL + "/search"
# GENIUS_LYRICS_CONTAINER = "Lyrics__Container-sc-1ynbvzw-1 kUgSbL"

MONTH_NAMES = ["января", "февраля", "марта", "апреля", "мая", "июня",
               "июля", "августа", "сентября", "октября", "ноября", "декабря"]

CHANNEL_ID = -1001914815060
