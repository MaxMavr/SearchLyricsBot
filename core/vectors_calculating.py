from config.vectors import *
from config.const import EMBADDING_MODEL
from db_interface.vectors import collection, make_vector_id
from api.lyrics_search import get_song_lines
from db_interface.songs import get_with_text

model = SentenceTransformer(EMBADDING_MODEL)
__pca = PCA(n_components=1)


def line_to_vector(line):
    line_embedding = model.encode(line)
    reduced_line = __pca.fit_transform(line_embedding.reshape(32, 32))
    line_zip = np.array([i[0] for i in reduced_line])

    return line_zip


for song_id, song_title, _, _ in get_with_text():
    for i, song_line in enumerate(get_song_lines(song_id)):
        vector = line_to_vector(song_line)
        collection.add(
            embeddings=vector,
            ids=make_vector_id(song_id, i),
        )
    print(song_title + ":: SUCCESS!!!")



# collection.query(
#     query_embeddings=vectors,
#     n_results=10,
#     where={"metadata_field": "is_equal_to_this"},
#     where_document={"$contains":"search_string"}
# )


if __name__ == "__main__":
    pass
