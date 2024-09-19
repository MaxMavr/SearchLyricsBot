from config import SONGS_INFO_DIR, listdir, time
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


def the_fucking_terrible_sorting_algorithm():
    start_time = time()
    vecs = read_wrd_vecs_file()
    search_vecs = []
    nodes = [node.make(vec=i) for i in range(len(vecs))]
    active_nodes = [i for i in range(len(nodes))]
    len_active_nodes = len(active_nodes)

    sim_between_nodes = [[-1] * (len(nodes) - i - 1) for i in range(len(nodes))]

    print(f'Нашёл {len_active_nodes} векторов\n')

    while len_active_nodes > 1:
        print(f'Осталось {len_active_nodes} векторов', end=' ')

        max_sim_vecs = 0
        right_node = 0
        left_node = 0

        for i in active_nodes:
            if i >= len(vecs):
                vec_i = search_vecs[node.get_vec(nodes[i - len(vecs)])]
            else:
                vec_i = vecs[node.get_vec(nodes[i])]

            for j in active_nodes:
                if j <= i:
                    continue

                if j >= len(vecs):
                    vec_j = search_vecs[node.get_vec(nodes[j - len(vecs)])]
                else:
                    vec_j = vecs[node.get_vec(nodes[j])]

                if sim_between_nodes[i][j - i - 1] == -1:
                    sim_vecs = calc_sim_vecs(vec_i, vec_j, 'c')
                    sim_between_nodes[i][j - i - 1] = sim_vecs
                else:
                    sim_vecs = sim_between_nodes[i][j - i - 1]

                if max_sim_vecs < sim_vecs:
                    max_sim_vecs = sim_vecs
                    right_node = i
                    left_node = j

        print(active_nodes)
        print(max_sim_vecs, right_node, left_node)
        active_nodes.append(len(vecs) + len(search_vecs))
        active_nodes.remove(right_node)
        active_nodes.remove(left_node)

        if right_node >= len(vecs):
            right_vec = search_vecs[node.get_vec(nodes[right_node - len(vecs)])]
        else:
            right_vec = vecs[node.get_vec(nodes[right_node])]

        if left_node >= len(vecs):
            left_vec = search_vecs[node.get_vec(nodes[left_node - len(vecs)])]
        else:
            left_vec = vecs[node.get_vec(nodes[left_node])]

        print(f'Объединил "{vec2word(right_vec)}" -{round(max_sim_vecs, 5)}- "{vec2word(left_vec)}"')

        center_vec = calc_cent_vec(right_vec, left_vec)

        search_vecs.append(center_vec)

        center_node = node.make(right=right_node,
                                left=left_node,
                                vec=len(search_vecs) - 1)

        nodes.append(center_node)

        nodes[right_node] = node.set_parent(nodes[right_node], len(nodes) - 1)
        nodes[left_node] = node.set_parent(nodes[left_node], len(nodes) - 1)

        for i in sim_between_nodes:
            i.append(-1)
        sim_between_nodes.append([])

        len_active_nodes -= 1

    print(f'\nСортировал {round(time() - start_time, 3)}c')
    make_node_file(nodes)
    make_src_vecs_file(search_vecs)


def search_in_tree(find_vec: tuple):
    nodes = read_node_file()
    current_node = len(nodes) - 1
    search_vecs = read_src_vecs_file()

    right_node, left_node = node.get_next(nodes[current_node])

    while left_node is not None or \
            right_node is not None:

        right_vec = search_vecs[node.get_vec(nodes[right_node])]
        left_vec = search_vecs[node.get_vec(nodes[left_node])]

        right_sim = calc_sim_vecs(right_vec, find_vec)
        left_sim = calc_sim_vecs(left_vec, find_vec)

        if right_sim > left_sim:
            current_node = right_node
        else:
            current_node = left_node

        right_node, left_node = node.get_next(nodes[current_node])

    found_vec = node.get_vec(nodes[current_node])
    wrd_vecs = read_wrd_vecs_file()

    return wrd_vecs[found_vec]


def check_paths_vec2line():
    vecs = read_wrd_vecs_file()

    for i in range(len(vecs)):
        print()
        word = vec2word(vecs[i])
        print(word)

        for line in take_line_by_vec_index(i, take_all=True):
            print(line.replace(word, f'\033[31m{word}\033[0m'))


if __name__ == "__main__":
    # make_new_vecs_from_songs_file()
    # the_fucking_terrible_sorting_algorithm()
    # make_tree_img()
    # check_paths_vec2line()

    fvec = search_in_tree(word2vec('клоун'))
    print(fvec)
    print(vec2word(fvec))
