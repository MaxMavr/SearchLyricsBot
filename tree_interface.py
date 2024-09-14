from config import UNP_DIR, listdir
from db_interface import add_song2db
from vector_operation import *
from preparing_words import *
from file_interface import *


def make_new_unp_vecs():
    for song_file in listdir(UNP_DIR):
        song_info = read_song_file(song_file)

        song_code = add_song2db(song_info['artist'],
                                song_info['album'],
                                song_info['song'])

        lyrics = song_info['lyrics']

        make_lyrics_file(song_code, lyrics)

        for line in range(len(lyrics)):
            line_code = song_code + (line,)

            for word in split_line(lyrics[line]):
                vec = word2vec(word)

                add_unp_vec(line_code, vec)


def soft_add_new_vecs2tree():
    pass






