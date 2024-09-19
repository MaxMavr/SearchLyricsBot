from config import (findall, DOTALL,
                    PARSING_XML_PATTERN,
                    LYRICS_DIR,
                    ZERO_VEC,

                    WRD_VECS_FILE,
                    SRC_VECS_FILE,
                    NODE_FILE,
                    VEC_TO_LINE_CODE_FILE,
                    TREE_IMG_FILE,

                    json,
                    isfile,
                    ceil,
                    log2,
                    Union)

from preparing_words import split_lyrics
from vector_operation import bind_equal_vecs, vec2word, calc_sim_vecs
import node_interface as node


def read_song_file(path2song_file: str) -> dict:
    song_info = dict()

    with open(path2song_file, 'r', encoding="utf-8") as file:
        file_text = file.read()

        matches = findall(PARSING_XML_PATTERN, file_text, DOTALL)

        for match in matches:
            if match[0] != 'lyrics':
                song_info[match[0]] = match[1]
            else:
                song_info[match[0]] = split_lyrics(match[1])

        return song_info


def make_lyrics_file(song_code: int, lyrics: list):
    with open(f'{LYRICS_DIR}/{song_code}.json', 'w+', encoding="utf-8") as file:
        json.dump(lyrics, file, ensure_ascii=False)


def make_tree_img():
    radius = 30
    text_shift = 10
    size = radius * 2

    vecs = read_wrd_vecs_file()
    search_vecs = read_src_vecs_file()
    nodes = read_node_file()

    print(len(vecs))
    print(len(search_vecs))
    print(len(nodes))
    print()

    current_node = len(nodes) - 1

    with open(TREE_IMG_FILE, 'w+', encoding="utf-8") as canvas:
        def draw_node(current_node: int, px, py, x, y) -> tuple:
            right_node, left_node, parent_node, current_vec = nodes[current_node]

            canvas.write(f'<polyline points="{x - radius},{y} {px},{y} {px},{py}"/>\n')

            if left_node is None or right_node is None:
                cur_word = vec2word(vecs[current_vec])

                canvas.write(f'<circle cx="{x}" cy="{y}" r="{radius}"/>\n')
                canvas.write(f'<text class="word" x="{x}" y="{y + text_shift}">{cur_word}</text>\n')

                return x + size, y + size
            else:
                cur_word = vec2word(search_vecs[current_vec])

                if parent_node is not None:
                    sim_vecs = calc_sim_vecs(search_vecs[current_vec],
                                             search_vecs[node.get_vec(nodes[parent_node])], 'c')
                else:
                    sim_vecs = 0

                canvas.write(f'<circle cx="{x}" cy="{y}" r="{radius}"/>\n')
                canvas.write(f'<text class="word" x="{x}" y="{y + text_shift}">{cur_word}</text>\n')
                canvas.write(f'<text class="sim" x="{px}" y="{y}">{round(sim_vecs, 5)}</text>\n')

                _, shift_y = draw_node(right_node, x, y, x + size, y + size)

                shift_x, shift_y = draw_node(left_node, x, y, x + size, y + shift_y)

                return x + shift_x, y + shift_y

        canvas.write('''<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
viewBox="0 0 4000 2000">
<style type="text/css">
  circle{
    stroke: #000;
    stroke-width: 2;
    fill: #fff;
  }
  polyline {
    stroke: #000;
    stroke-width: 2;
    fill: #fff0;
  }
  text{
    font-size: 15px;
  }
  .word{
    text-anchor: middle;
  }
  .sim{
    text-anchor: left;
  }
</style>
        ''')

        draw_node(current_node, 0, 0, size, size)

        canvas.write('</svg>')


def __read_line_from_lyrics_file(song_code: int, line: int) -> str:
    with open(f'{LYRICS_DIR}/{song_code}.json', 'r', encoding="utf-8") as file:
        lyrics = json.load(file)
        return lyrics[line]


def __make_list_file(path2file: str, __list: list):
    with open(path2file, 'w+', encoding="utf-8") as file:
        json.dump(__list, file, ensure_ascii=False)


def __read_list_file(path2file: str) -> list:
    with open(path2file, 'r', encoding='utf-8') as file:
        return json.load(file)


def __make_dict_file(path2file: str, __dict: dict):
    with open(path2file, 'w+', encoding="utf-8") as file:
        json.dump(__dict, file, ensure_ascii=False)


def __read_dict_file(path2file: str) -> dict:
    with open(path2file, 'r', encoding='utf-8') as file:
        return json.load(file)


def add2list_file(path2file: str, list_: list):
    if isfile(path2file):
        old_list_ = __read_list_file(path2file)
    else:
        old_list_ = []

    new_list_ = old_list_ + list_

    __make_list_file(path2file, new_list_)


def make_node_file(nodes: list):
    __make_list_file(NODE_FILE, nodes)


def make_src_vecs_file(vecs: list):
    __make_list_file(SRC_VECS_FILE, vecs)


def add2wrd_vecs_file(vecs: list) -> list:
    if isfile(WRD_VECS_FILE):
        old_vecs = __read_list_file(WRD_VECS_FILE)
    else:
        old_vecs = []

    new_vecs, map_bind = bind_equal_vecs(old_vecs + vecs)

    __make_list_file(WRD_VECS_FILE, new_vecs)
    return map_bind


def add2vec_to_song_code_file(map_bind: list, new_vec2line_code: list):
    if isfile(VEC_TO_LINE_CODE_FILE):
        old_vec2line_code = __read_dict_file(VEC_TO_LINE_CODE_FILE)
    else:
        old_vec2line_code = []

    index_shift = len(old_vec2line_code)

    for i in range(len(map_bind) - len(old_vec2line_code)):
        old_vec2line_code.append([])

    for i in range(len(map_bind)):
        for lc in map_bind[i]:
            line_code = new_vec2line_code[lc - index_shift]

            is_new = True

            for j in range(len(old_vec2line_code[i])):
                if line_code[0] == old_vec2line_code[i][j][0] and \
                   line_code[1] == old_vec2line_code[i][j][1]:
                    is_new = False
                    break

            if is_new:
                old_vec2line_code[i].append(line_code)

    __make_dict_file(VEC_TO_LINE_CODE_FILE, old_vec2line_code)


def read_node_file() -> list:
    return __read_list_file(NODE_FILE)


def read_wrd_vecs_file() -> list:
    return __read_list_file(WRD_VECS_FILE)


def read_src_vecs_file() -> list:
    return __read_list_file(SRC_VECS_FILE)


def take_line_by_vec_index(vec_index: int, take_all: bool = False) -> Union[str, list]:
    vecs2line_codes = __read_list_file(VEC_TO_LINE_CODE_FILE)
    line_codes = vecs2line_codes[vec_index]

    if take_all:
        lines = []
        for line_code in line_codes:
            song_code, line = line_code
            lines.append(__read_line_from_lyrics_file(song_code, line))

        return lines

    first_line_code = line_codes.pop(0)
    line_codes.append(first_line_code)

    song_code, line = first_line_code

    __make_list_file(VEC_TO_LINE_CODE_FILE, vecs2line_codes)

    return __read_line_from_lyrics_file(song_code, line)


def take_word_by_vec_index(vec_index: int) -> str:
    vecs = __read_list_file(WRD_VECS_FILE)
    return vecs[vec_index]


if __name__ == '__main__':
    make_tree_img()
    # print(take_word_by_vec_index(185))
    # print(__read_line_from_lyrics_file(1, 54))
