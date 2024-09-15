from config import UNP_DIR, listdir
from db_interface import add_songs_db
from vector_operation import *
from preparing_words import *
from file_interface import *


def make_new_unp_vecs():
    for song_file in listdir(UNP_DIR):
        song_info = read_song_file(f'{UNP_DIR}/{song_file}')

        song_code = add_songs_db(song_info['artist'],
                                 song_info['album'],
                                 song_info['song'],
                                 song_info['link'])

        lyrics = song_info['lyrics']

        make_lyrics_file(song_code, lyrics)

        vecs = []

        for line in range(len(lyrics)):
            line_code = (line, song_code)

            for word in split_line(lyrics[line]):
                vec = word2vec(word)

                vecs.append([[line_code], vec])

        add_unp_vec(vecs)


def THE_GREAT_SORTING_ALGORITHM():
    pass
    # vecs = take_unp_vecs_from_file()
    # sort_vecs = [i[1] for i in vecs]
    #
    # for i in range(len(sort_vecs) // 2):



    # while n > 3:
    #     pass

    # print(sort_vecs)


def soft_add_new_vecs2tree():
    pass


if __name__ == "__main__":
    make_new_unp_vecs()
    bind_similar_vecs_from_unp()
    have_similar_vecs_from_vecs(take_unp_vecs_from_file())

    print(calc_average_len_char([i[1] for i in take_unp_vecs_from_file()]))

    THE_GREAT_SORTING_ALGORITHM()


