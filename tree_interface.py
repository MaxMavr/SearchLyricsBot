from config import SONGS_INFO_DIR, listdir
from db_interface import *
from vector_operation import *
from preparing_words import *
from file_interface import *
import node_interface as node
from make_message import vec2str


def make_new_vecs_from_songs_file():
    for song_file in listdir(SONGS_INFO_DIR):
        song_info = read_song_file(f'{SONGS_INFO_DIR}/{song_file}')

        song_code = add_songs_info_db(song_info['artist'],
                                      song_info['album'],
                                      song_info['song'],
                                      song_info['link'])

        lyrics = song_info['lyrics']

        make_lyrics_file(song_code, lyrics)

        vecs = []
        vec2line_code = []

        for line in range(len(lyrics)):
            line_code = (song_code, line)

            for word in split_line(lyrics[line]):
                vec = word2vec(word)
                vec2line_code.append(line_code)
                vecs.append(vec)

        map_bind = add2wrd_vecs_file(vecs)

        add2vec_to_song_code_file(map_bind, vec2line_code)


def THE_GREAT_SORTING_ALGORITHM():
    vecs = read_wrd_vecs_file()
    search_vecs = []

    nodes = [node.make(vec=i) for i in range(len(vecs))]
    active_nodes = [i for i in range(len(nodes))]

    len_active_nodes = len(active_nodes)
    print(f'Нашёл {len_active_nodes} векторов')

    sim_between_nodes = []

    for i in range(len(nodes)):
        vec_i = vecs[node.get_vec(nodes[i])]
        tmp_sim_between_nodes = []
        for j in range(i + 1, len(nodes)):
            vec_j = vecs[node.get_vec(nodes[j])]

            tmp_sim_between_nodes.append(calc_sim_vecs(vec_i, vec_j))
        sim_between_nodes.append(tmp_sim_between_nodes)

    for i in sim_between_nodes:
        print(i)


    # while len_active_nodes > 1:
    #     print(f'Осталось {len_active_nodes} векторов')
    #     len_active_nodes -= 1


def search_in_tree(find_vec: tuple):
    nodes = read_node_file()
    current_node = len(nodes) - 1
    search_vecs = read_node_file()


def chech_paths_vec2line():
    vecs = read_wrd_vecs_file()

    for i in range(len(vecs)):
        print()
        word = vec2word(vecs[i])
        print(word)

        for line in take_line_by_vec_index(i, take_all=True):
            print(line.replace(word, f'\033[31m{word}\033[0m'))





if __name__ == "__main__":
    make_new_vecs_from_songs_file()
    # chech_paths_vec2line()


