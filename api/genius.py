from config.net import *
from config.const import GENIUS_HEADERS, GENIUS_SEARCH_URL, GENIUS_MAIN_URL, GENIUS_LYRICS_CONTAINER

'''
Мы отказались использовать Genius, так как я не могу полность текста песни при парсинге
'''


def __filter_word(word: str) -> str:
    filtered_word = word.lower()
    return re.sub(r'[^a-zа-яё]+', '', filtered_word)


async def search_song(song_name: str, artist_name: str) -> dict:
    response = requests.get(GENIUS_SEARCH_URL,
                            params={'q': song_name},
                            headers=GENIUS_HEADERS)
    data = response.json()

    if response.status_code != 200:
        err = None
        if 'meta' in data:
            err = data['meta']['message']
        if 'error_description' in data:
            err = data['error_description']
        return {
            'status': False,
            'err': err
        }
    else:
        data = data["response"]

    for hit in data['hits']:
        song = hit['result']
        artist = song['primary_artist']

        if __filter_word(song_name) in __filter_word(song['title']) \
                and __filter_word(artist_name) in __filter_word(artist['name']):
            return {
                'status': True,
                'date': tuple(song['release_date_components'].values())[::-1] if song[
                    'release_date_components'] else None,
                'song_id': song['id'],
                'artist_id': artist['id'],
                'song_path': song['path'],
                'err': None
            }

    return {
        'status': False,
        'err': 'Не нашёл песню'
    }


def get_lyrics(song_path: str) -> str:
    page_url = GENIUS_MAIN_URL + song_path
    response = requests.get(page_url)

    if response.status_code == 200:
        html = bs(response.text, "html.parser")
        lyrics_div = html.find("div", class_=GENIUS_LYRICS_CONTAINER)
        print(lyrics_div)
        lyrics = lyrics_div.get_text('\n')
        return re.sub(r'\[.*]', '', lyrics)
    return None
