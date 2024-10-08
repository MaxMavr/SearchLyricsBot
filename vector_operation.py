from config import (ZERO_VEC,
                    END_VEC,

                    DIM,
                    DIM_SPACE,
                    DIM_CHAR,

                    SERV_NUM_INDEXES,
                    LENGTH_INDEX,
                    LENGTH_CHAR_INDEX,
                    MAX_LENGTH_VEC,

                    INDEXED_ALL_CHAR_MTRX,
                    INDEXED_ALL_CHAR_RVS_MTRX,

                    sqrt, Union
                    )


def word2vec(word: str) -> tuple:
    vec = list(ZERO_VEC)

    if len(word) >= DIM_SPACE:
        print(f'\n\nword2vec:\nЧасть информации потерялась!\n{word} -> {word[:DIM_SPACE - 1]}\n\n')

    for i in range(min(len(word), DIM_SPACE - 1)):
        char = INDEXED_ALL_CHAR_MTRX[word[i]]

        for c in range(len(char)):
            vec[i * DIM_CHAR + c + SERV_NUM_INDEXES] = char[c]

    vec[LENGTH_INDEX] = __calc_length_vec(vec)
    vec[LENGTH_CHAR_INDEX] = DIM_SPACE if len(word) >= DIM_SPACE else len(word) + 1

    return tuple(vec)


def vec2word(vec: Union[tuple, list]) -> str:
    word = ''

    vec_char = slice_vec2subvec(vec)

    for i in vec_char:
        if i == END_VEC:
            break
        elif i[0] == 0:
            continue
        else:
            try:
                word += INDEXED_ALL_CHAR_RVS_MTRX[i]
            except KeyError:
                word += '?'

    return word


def slice_vec2subvec(vec:  Union[tuple, list]) -> list:
    vec_char = [tuple(vec[i:i + DIM_CHAR]) for i in range(SERV_NUM_INDEXES, vec[LENGTH_CHAR_INDEX] * DIM_CHAR + SERV_NUM_INDEXES, DIM_CHAR)]
    return vec_char


def rounded_vec(vec: Union[tuple, list]) -> tuple:
    round_vec = list(ZERO_VEC)

    for i in range(DIM_SPACE + SERV_NUM_INDEXES):
        round_vec[i] = int(vec[i])

    return tuple(round_vec)


def is_zero_dist(vec1: Union[tuple, list], vec2: Union[tuple, list]) -> bool:
    for d in range(DIM + SERV_NUM_INDEXES):
        if vec1[d] != vec2[d]:
            return False
    return True


def __calc_length_vec(vec: Union[tuple, list]) -> float:
    if vec == ZERO_VEC:
        return 0

    if vec[LENGTH_INDEX] == 0:
        amount = 0

        for d in vec[SERV_NUM_INDEXES:]:
            amount += d ** 2

        vec[LENGTH_INDEX] = sqrt(amount)

        return sqrt(amount)

    else:
        return vec[LENGTH_INDEX]


# Косинусное сходство
def __calc_cos_sim(vec1: Union[tuple, list], vec2: Union[tuple, list]) -> float:
    amount = 0

    for d in range(SERV_NUM_INDEXES, DIM + SERV_NUM_INDEXES):
        amount += vec1[d] * vec2[d]

    cos_sim = amount / (vec1[LENGTH_INDEX] * vec2[LENGTH_INDEX])

    return cos_sim


# Eвклидово расстояние
def __calc_euclid_dist(vec1: Union[tuple, list], vec2: Union[tuple, list]) -> float:
    amount = 0

    for d in range(SERV_NUM_INDEXES, DIM + SERV_NUM_INDEXES):
        amount += (vec1[d] - vec2[d]) ** 2

    euclid_dist = sqrt(amount)

    return euclid_dist


# Сходство векторов
def calc_sim_vecs(vec1: Union[tuple, list],
                  vec2: Union[tuple, list],
                  mode: str = 'c') -> float:
    sim = 0

    if mode == 'e':
        sim = __calc_euclid_dist(vec1, vec2)
    elif mode == 'c':
        sim = __calc_cos_sim(vec1, vec2)

    if '2' in mode:
        return sim ** 2

    if '3' in mode:
        return sim ** 3

    return sim


def calc_cent_vec(vec1: Union[tuple, list], vec2: Union[tuple, list]) -> tuple:
    center_vec = list(ZERO_VEC)

    for d in range(SERV_NUM_INDEXES, DIM + SERV_NUM_INDEXES):
        center_vec[d] = (vec1[d] + vec2[d]) / 2

    center_vec[LENGTH_INDEX] = __calc_length_vec(center_vec)
    center_vec[LENGTH_CHAR_INDEX] = max(vec1[LENGTH_CHAR_INDEX], vec2[LENGTH_CHAR_INDEX])

    return tuple(center_vec)


def bind_equal_vecs(vecs: list) -> tuple:
    to_remove = set()
    map_binds = []
    clear_vecs = []

    for i in range(len(vecs)):
        if i in to_remove:
            continue

        bind = [i]
        for j in range(i + 1, len(vecs)):
            if j in to_remove:
                continue

            if is_zero_dist(vecs[i], vecs[j]):
                bind.append(j)
                to_remove.add(j)

        map_binds.append(bind)
        clear_vecs.append(vecs[i])

    return clear_vecs, map_binds


def have_equal_vecs(vecs: list) -> bool:
    for x in range(len(vecs)):
        for y in range(x + 1, len(vecs)):
            if is_zero_dist(vecs[x][1], vecs[y][1]):
                return True
    return False


def calc_avg_len_char(vecs: list) -> float:
    amount = 0
    for vec in vecs:
        amount += vec[LENGTH_CHAR_INDEX]
    return amount / len(vecs)


def calc_avg_len_vec(vecs: list) -> float:
    amount = 0
    for vec in vecs:
        amount += vec[LENGTH_INDEX]
    return amount / len(vecs)


if __name__ == "__main__":
    print(word2vec('ак'))
    # fox_vec1 = word2vec('лиса')
    # fox_vec2 = word2vec('лисонька')
    #
    # c_vec = bind_equal_vecs(
    #     [
    #         word2vec('лиса'),
    #         word2vec('лиса'),
    #         word2vec('лиса'),
    #         word2vec('ли3са'),
    #         word2vec('ли3са'),
    #         word2vec('ли3са'),
    #         word2vec('ли223са'),
    #         word2vec('ли223са'),
    #         word2vec('ли22са'),
    #     ])
    #
    # print(c_vec[1])
    #
    # for i in c_vec[0]:
    #     print(vec2word(i))

    # print(f"{ZERO_VEC =                                            }")
    # print(f"{word2vec('лиса')}")
    # print(f"{word2vec('лисонька') =                                }")
    # print(f"{rounded_vec(calc_centvec(fox_vec1, fox_vec2)) =       }")
