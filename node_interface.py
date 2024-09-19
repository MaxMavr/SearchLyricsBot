def make(
        right: int = None,
        left: int = None,
        parent: int = None,
        vec: int = None) -> list:
    return [right, left, parent, vec]


def get_right(node: list) -> int:
    return node[0]


def get_left(node: list) -> int:
    return node[1]


def get_next(node: list) -> tuple:
    return get_right(node), get_left(node)


def get_parent(node: list) -> int:
    return node[2]


def set_parent(node: list, parent) -> list:
    new_node = make(node[0], node[1], parent, node[3])
    return new_node


def get_vec(node: list) -> int:
    return node[3]


def node2dict(node: list) -> dict:
    return {'right': node[0], 'left': node[1], 'parent': node[2], 'vec': node[3]}
