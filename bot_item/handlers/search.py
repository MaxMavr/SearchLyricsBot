from config.bot import *
from bot_item.pages import make_artists_page, make_artist_page
rt: Router = Router()

# TODO:
#  Команда /artists — показывать список исполнителей, которые есть в базах данных
#  Команда  {id/название} — показывать альбомы исполнителя (Со стрелочками)
#  Команда  {id/название} — показывать песни из альбома (Со стрелочками) (Обложка)
#  Команда  {id/название} — показывать текст песни если есть (В целом всю информацию о треке, которая есть)
#  Команда /format {текст \n ссылка} — форматировать сообщение под формата ППТПИ (Для Админов ППТПИ нужна кнопка «опубликовать»)
#  Команда /search


@rt.message(F.text.lower() == 'исполнители')
async def catch_artists(message: Message):
    await make_artists_page(message, select_number=1)


@rt.message(Command(commands='artists'))  # /artists
async def cmd_artists(message: Message):
    await make_artists_page(message, select_number=1)


@rt.message(Command(commands='artist'))  # /artist
async def cmd_artist(message: Message):
    artist_id = await get_cmd_artist_id(message)
    if artist_id == '':
        return

    await make_artist_page(message, artist_id, select_number=1)


# @rt.message(Command(commands='album'))  # /album
# async def cmd_album(message: Message):
#     album_id = await get_cmd_artist_id(message)
#     if album_id == '':
#         return
#
#     await make_album_page(message, album_id, select_number=1)
#
#
# @rt.message(Command(commands='song'))  # /song
# async def cmd_song(message: Message):
#     song_id = await get_cmd_artist_id(message)
#     if song_id == '':
#         return
#
#     await make_song_page(message, song_id, select_number=1)


@rt.callback_query(F.data.startswith('pg_'))
async def catch_goto_page(callback: CallbackQuery):
    _, type_of_page, id_of_page, select_number, show_ids = callback.data.split('_')

    print(f'pg_ {type_of_page = }')
    print(f'pg_ {id_of_page = }')
    print(f'pg_ {select_number = }')
    print(f'pg_ {show_ids = }')

    if type_of_page == 'arts':
        await make_artists_page(callback, select_number=int(select_number),
                                show_ids=show_ids == 'True')
    elif type_of_page == 'art':
        await make_artist_page(callback, artist_id=id_of_page, select_number=int(select_number),
                               show_ids=show_ids == 'True')
    # elif type_of_page == 'al':
    #     await make_album_page(callback, album_id=id_of_page, select_number=int(select_number),
    #                           show_ids=show_ids == 'True')
    # elif type_of_page == 'sng':
    #     await make_song_page(callback, song_id=id_of_page, select_number=int(select_number),
    #                          show_ids=show_ids == 'True')
