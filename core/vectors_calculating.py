import asyncio
import time
import chromadb
from chromadb.errors import InvalidCollectionException

from config.vectors import *
from config.const import EMBADDING_MODEL
from db_interface.vectors import make_vector_id
from api.lyrics_search import get_song_lines
from db_interface.songs import get_with_text


model = SentenceTransformer(EMBADDING_MODEL, device='cuda')
__pca = PCA(n_components=1)


def line_to_vector(line):
    line_embedding = model.encode(line, device='cuda')
    reduced_line = __pca.fit_transform(line_embedding.reshape(32, 32))
    line_zip = np.array([i[0] for i in reduced_line])

    return line_zip


async def test(song_id, song_title, collection):
    a = time.time()
    for i, song_line in enumerate(get_song_lines(song_id)):
        vector = line_to_vector(song_line)
        await collection.add(
            embeddings=vector,
            ids=make_vector_id(song_id, i),
        )
    print(song_title + f":: SUCCESS!!!\t\t\t{a - time.time()}")


# collection.query(
#     query_embeddings=vectors,
#     n_results=10,
#     where={"metadata_field": "is_equal_to_this"},
#     where_document={"$contains":"search_string"}
# )


async def main():
    __client = await chromadb.AsyncHttpClient(host='localhost', port=8000)
    try:
        collection = await __client.get_collection(
            name="embeddings",
        )
    except InvalidCollectionException:
        collection = await __client.create_collection(
            name="embeddings",
            metadata={"hnsw:space": "cosine"}
        )

    for song_id, song_title, _, _ in get_with_text():
        await test(song_id, song_title, collection)


if __name__ == "__main__":
    asyncio.run(main())
