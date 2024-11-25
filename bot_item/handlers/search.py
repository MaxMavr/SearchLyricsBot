from config.bot import *
from bot_item.pages import make_artists_page, make_artist_page, make_album_page, make_song_page
rt: Router = Router()

# TODO:
#  Команда /artists — показывать список исполнителей, которые есть в базах данных
#  Команда  {id/название} — показывать альбомы исполнителя (Со стрелочками)
#  Команда  {id/название} — показывать песни из альбома (Со стрелочками) (Обложка)
#  Команда  {id/название} — показывать текст песни если есть (В целом всю информацию о треке, которая есть)
#  Команда /search


@rt.message(F.text.lower() == 'исполнители')
async def catch_artists(message: Message):
    await make_artists_page(event=message, select_vector=(1, 1, 1, 1))


@rt.message(Command(commands='artists'))  # /artists
async def cmd_artists(message: Message):
    await catch_artists(message)


@rt.message(Command(commands='artist'))  # /artist
async def cmd_artist(message: Message):
    artist_id = await get_cmd_artist_id(message)
    if artist_id == '':
        return

    await make_artist_page(message, artist_id, select_number=1)


@rt.message(Command(commands='album'))  # /album
async def cmd_album(message: Message):
    album_id = await get_cmd_artist_id(message)
    if album_id == '':
        return

    await make_album_page(message, album_id, select_number=1)


@rt.message(Command(commands='song'))  # /song
async def cmd_song(message: Message):
    song_id = await get_cmd_artist_id(message)
    if song_id == '':
        return

    await make_song_page(message, song_id, select_number=1)


@rt.callback_query(F.data.startswith('pageSI_'))
async def catch_goto_page_song_info(callback: CallbackQuery):
    type_of_page, show_ids, select_vector = decoding_page_callback(callback.data)

    print(callback.data, type_of_page, show_ids, select_vector)

    if type_of_page == 'A':
        await make_artists_page(callback, select_vector, show_ids)
    elif type_of_page == 'a':
        await make_artist_page(callback, select_vector, show_ids)
    elif type_of_page == 'l':
        await make_album_page(callback, select_vector, show_ids)
    elif type_of_page == 's':
        await make_song_page(callback, select_vector, show_ids)
