from config.db import *
from config.const import VECTORS_DB
client = chromadb.PersistentClient(path=VECTORS_DB)


def make_vector_id(song_id: str, line_id: int) -> str:
    return f'{song_id}/{line_id}'


def split_vector_id(vector_id: str) -> Tuple[str, int]:
    song_id, line_id = vector_id.split('/')
    line_id = int(line_id)
    return song_id, line_id


try:
    collection = client.get_collection(
        name="collection_name",
    )

except InvalidCollectionException:
    collection = client.create_collection(
        name="collection_name",
        metadata={"hnsw:space": "cosine"}
    )

collection.add(
    embeddings=vectors,
    ids=["id1", "id2", "id3", ...]
)


# https://docs.trychroma.com/guides#filtering-by-metadata:~:text=You%20can%20query%20by%20a%20set%20of

collection.query(
    query_embeddings=vectors,
    n_results=10,
    where={"metadata_field": "is_equal_to_this"},
    where_document={"$contains":"search_string"}
)