def make(
        right: int = None,
        left: int = None,
        parent: int = None,
        vec: int = None) -> tuple:
    return right, left, parent, vec


def get_right(node: tuple) -> int:
    return node[0]


def get_left(node: tuple) -> int:
    return node[1]


def get_parent(node: tuple) -> int:
    return node[2]


def get_vec(node: tuple) -> int:
    return node[3]


def node2dict(node: tuple) -> dict:
    return {'right': node[0], 'left': node[1], 'parent': node[2], 'vec': node[3]}
