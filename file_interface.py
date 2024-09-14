from config import (findall, DOTALL,
                    PARSING_XML_PATTERN,
                    LYRICS_DIR,
                    UNP_VEC,
                    UNP_DIR,
                    json)

from preparing_words import split_lyrics


def read_song_file(path2song_file: str) -> dict:
    song_info = dict()

    with open(path2song_file, 'r', encoding="utf-8") as file:
        file_text = file.read()

        matches = findall(PARSING_XML_PATTERN, file_text, DOTALL)

        for matche in matches:
            if matche[0] != 'lyrics':
                song_info[matche[0]] = matche[1]
            else:
                song_info[matche[0]] = split_lyrics(matche[1])

        return song_info


def make_lyrics_file(song_code: tuple, lyrics: list):
    with open(f'{LYRICS_DIR}/{song_code[0]}-{song_code[1]}-{song_code[2]}.json', 'w+', encoding="utf-8") as file:
        json.dump(lyrics, file, ensure_ascii=False)


def take_line_from_lyrics_file(line_code: tuple) -> str:
    with open(f'{LYRICS_DIR}/{line_code[0]}-{line_code[1]}-{line_code[2]}.json', 'w+', encoding="utf-8") as file:
        lyrics = json.load(file)

        return lyrics[line_code[3]]


def add_unp_vec(line_code: tuple, vec: tuple):
    with open(UNP_VEC, 'a+', encoding="utf-8") as file:
        file.write(f'{line_code}, {vec}\n')



'''
def make_lyrics_file_from_links_file(path2links_file) -> list:
    with open(path2links_file, 'r', encoding="utf-8") as file:
        links = file.read().split()

        for link in links:
            response = requests.get(link)

            # Проверяем статус-код
            if response.status_code == 200:
                print(response.text)

            else:
                print(f'\n\nmake_lyrics_file_from_links_file:\nОшибка соединения!\nКод:{response.status_code}\n\n')
'''

if __name__ == '__main__':
    pass
