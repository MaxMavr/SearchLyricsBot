from config import (ZERO_VEC,
                    END_VEC,

                    DIM,
                    DIM_SPACE,
                    DIM_CHAR,

                    NUM_SERV_VEC,
                    LONG_INDEX,

                    INDEXED_ALL_CHAR_MTRX,
                    INDEXED_ALL_CHAR_RVS_MTRX,

                    sqrt,
                    Union
                    )

from file_interface import take_unp_vecs_from_file, add_unp_vec


def word2vec(word: str) -> tuple:
    vec = list(ZERO_VEC)

    if len(word) >= DIM_SPACE:
        print(f'\n\nword2vec:\nЧасть информации потерялась!\n{word} -> {word[:DIM_SPACE - 1]}\n\n')

    for i in range(min(len(word), DIM_SPACE - 1)):
        char = INDEXED_ALL_CHAR_MTRX[word[i]]

        for c in range(len(char)):
            vec[i * DIM_CHAR + c + NUM_SERV_VEC] = char[c]

    vec[LONG_INDEX] = calc_long(vec)

    return tuple(vec)


def vec2word(vec: tuple) -> str:
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
    vec_char = [vec[i:i + DIM_CHAR] for i in range(NUM_SERV_VEC, DIM + NUM_SERV_VEC, DIM_CHAR)]
    return vec_char


def rounded_vec(vec: tuple) -> tuple:
    round_vec = list(ZERO_VEC)

    for i in range(DIM_SPACE + NUM_SERV_VEC):
        round_vec[i] = int(vec[i])

    return tuple(round_vec)


def calc_long(vec: list) -> float:
    if vec == ZERO_VEC:
        return 0

    if vec[LONG_INDEX] == 0:
        amount = 0

        for d in vec[NUM_SERV_VEC:]:
            amount += d ** 2

        vec[LONG_INDEX] = sqrt(amount)

        return sqrt(amount)

    else:
        return vec[LONG_INDEX]


# Косинусное сходство
def calc_cos_dist(vec1: tuple, vec2: tuple) -> float:
    amount = 0

    for d in range(NUM_SERV_VEC, DIM + NUM_SERV_VEC):
        amount += vec1[d] * vec2[d]

    cos_dist = amount / (vec1[LONG_INDEX] * vec2[LONG_INDEX])

    return cos_dist


def is_zero_dist(vec1: tuple, vec2: tuple) -> bool:
    for d in range(DIM + NUM_SERV_VEC):
        if vec1[d] != vec2[d]:
            return False

    return True


def calc_centvec(vec1: tuple, vec2: tuple) -> tuple:
    center_vec = list(ZERO_VEC)

    for d in range(NUM_SERV_VEC, DIM + NUM_SERV_VEC):
        center_vec[d] = (vec1[d] + vec2[d]) / 2

    center_vec[LONG_INDEX] = calc_long(center_vec)

    return tuple(center_vec)


def calc_delta_sqr_err(vec1: tuple, vec2: tuple) -> float:
    '''
    В общем случае нужно считать:
    ((n1 * n2) / (n1 + n2)) * d(C1, C2) ** 2,

    где n — количество элементов кластера, С — центр кластера
    '''

    delta_square_error = calc_cos_dist(vec1, vec2) ** 2

    return delta_square_error


def bind_similar_vecs_from_unp():
    vecs = take_unp_vecs_from_file()

    clear_vecs = []

    print("Начальное количество", len(vecs))

    to_remove = set()

    for x in range(len(vecs)):
        for y in range(x + 1, len(vecs)):
            if is_zero_dist(vecs[x][1], vecs[y][1]):
                vecs[x][0].append(vecs[y][0][0])
                to_remove.add(y)

    vecs = [vec for i, vec in enumerate(vecs) if i not in to_remove]

    print("Конечное количество", len(vecs))
    add_unp_vec(vecs)


def have_similar_vecs_from_vecs(vecs):
    for x in range(len(vecs)):
        for y in range(x + 1, len(vecs)):
            if is_zero_dist(vecs[x][1], vecs[y][1]):
                print("ЕСТЬ СОВПАДЕНИЯ")

    print("нет совпадений")


def calc_average_len_char(vecs):
    amount = 0

    for vec in vecs:
        char_vec = slice_vec2subvec(vec)

        for c in range(len(char_vec)):
            if char_vec[c] == list(END_VEC):
                amount += c
                break

    return amount / len(vecs)


def calc_average_len_vec(vecs):
    amount = 0

    for vec in vecs:
        amount += vec[LONG_INDEX]

    return amount / len(vecs)


if __name__ == "__main__":
    fox_vec1 = word2vec('лиса')
    fox_vec2 = word2vec('лисонька')

    print(f"{ZERO_VEC =                                            }")
    print(f"{word2vec('лиса') =                                    }")
    print(f"{word2vec('лисонька') =                                }")
    print(f"{rounded_vec(calc_centvec(fox_vec1, fox_vec2)) =       }")



