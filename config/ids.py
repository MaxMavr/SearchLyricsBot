from config.const import BASE62


def encoding(*ids: int) -> str:
    encoded_ids = [''] * len(ids)

    for i, sub_id in enumerate(ids):
        while sub_id > 0:
            sub_id, remainder = divmod(sub_id, 62)
            encoded_ids[i] = BASE62[remainder] + encoded_ids[i]
        encoded_ids[i] = encoded_ids[i].zfill(3)

    return ''.join(encoded_ids)


def decoding(ids: str) -> list:
    encoded_ids = [ids[i:i + 3] for i in range(0, len(ids), 3)]
    decoding_ids = [0] * len(encoded_ids)

    for i, sub_id in enumerate(encoded_ids):
        for char in sub_id:
            if char not in BASE62:
                return []
            decoding_ids[i] = decoding_ids[i] * 62 + BASE62.index(char)

    return decoding_ids
