from config.db import *
from config.const import VECTORS_DB
# __client = await chromadb.AsyncHttpClient(path=VECTORS_DB)
# __client = await chromadb.AsyncHttpClient()


def make_vector_id(song_id: str, line_id: int) -> str:
    return f'{song_id}/{line_id}'


def split_vector_id(vector_id: str) -> Tuple[str, int]:
    song_id, line_id = vector_id.split('/')
    line_id = int(line_id)
    return song_id, line_id


# try:
#     client = await chromadb.AsyncHttpClient()
#     collection = await __client.get_collection(
#         name="embeddings",
#     )
# except InvalidCollectionException:
#     collection = await __client.create_collection(
#         name="embeddings",
#         metadata={"hnsw:space": "cosine"}
#     )
