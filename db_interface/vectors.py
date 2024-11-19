from config.db import *
from config.const import VECTORS_DB
__client = chromadb.PersistentClient(path=VECTORS_DB)


def make_vector_id(song_id: str, line_id: int) -> str:
    return f'{song_id}/{line_id}'


def split_vector_id(vector_id: str) -> Tuple[str, int]:
    song_id, line_id = vector_id.split('/')
    line_id = int(line_id)
    return song_id, line_id


try:
    collection = __client.get_collection(
        name="embeddings",
    )
except InvalidCollectionException:
    collection = __client.create_collection(
        name="embeddings",
        metadata={"hnsw:space": "cosine"}
    )
