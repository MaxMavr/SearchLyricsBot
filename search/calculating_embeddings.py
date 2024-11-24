from config.embedding import *
from config.const import EMBEDDING_MODEL

from api.lyrics_search import get_song_lines
from db_interface.songs import get_for_embedded, upd_embed_status
from db_interface.vectors import make_vector_id


__model = SentenceTransformer(EMBEDDING_MODEL, device='cuda')
__pca = PCA(n_components=1)


async def line_to_embedding(line: str):
    line_embedding = __model.encode(line, device='cuda')
    reduce_embedding = __pca.fit_transform(line_embedding.reshape(32, 32))

    compressed_embedding = np.array([i[0] for i in reduce_embedding])

    return compressed_embedding


async def song_lines_to_embeddings(song_id: str, song_title: str, collection):
    start_time = time.time()

    for i, song_line in enumerate(get_song_lines(song_id)):
        embedding = await line_to_embedding(song_line)
        await collection.add(
            embeddings=embedding,
            ids=make_vector_id(song_id, i),
        )
    print(f"{song_title.ljust(40)} :: SUCCESS!   ({round(time.time() - start_time, 3)})")


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
            name="embeddings"
        )
    except InvalidCollectionException:
        collection = await __client.create_collection(
            name="embeddings",
            metadata={"hnsw:space": "cosine"}
        )

    for song_id, song_title, _, _, embedded in get_for_embedded():
        if embedded:
            continue
        await song_lines_to_embeddings(song_id, song_title, collection)
        upd_embed_status(song_id, True)


if __name__ == "__main__":
    asyncio.run(main())
