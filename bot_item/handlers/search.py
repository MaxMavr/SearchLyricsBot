from config.bot import *
import bot_item.page as pg
rt: Router = Router()

# TODO:
#  Команда /artist {id} — показывать альбомы исполнителя (Со стрелочками)
#  Команда /album {id} — показывать песни из альбома (Со стрелочками) (Обложка)
#  Команда /song {id} — показывать текст песни если есть (В целом всю информацию о треке, которая есть)
#  Команда /search


@rt.message(F.text.lower() == 'исполнители')
async def catch_artists(message: Message):
    await pg.make_artists(event=message, select_vector=(1, 1, 1, 1))


@rt.message(Command(commands='artists'))  # /artists
async def cmd_artists(message: Message):
    await catch_artists(message)


@rt.message(Command(commands='artist'))  # /artist
@command_with_artist_id_argument
async def cmd_artist(message: Message, artist_id):
    SN = artists.get_select_number_by_id(artist_id)
    await message.answer(text=f'{artist_id} -> {SN}')


@rt.message(Command(commands='album'))  # /album
@command_with_album_id_argument
async def cmd_album(message: Message, album_id):
    pass


@rt.message(Command(commands='song'))  # /song
@command_with_song_id_argument
async def cmd_song(message: Message, song_id):
    pass


@rt.message(Command(commands='search'))  # /search
@command_with_arguments
async def cmd_song(message: Message, args):
    query = ' '.join(args)
    await message.answer(query)


@rt.callback_query(F.data.startswith('pageSI_'))
async def catch_goto_page_song_info(callback: CallbackQuery):
    type_of_page, select_vector = decoding_page_callback(callback.data)

    print(callback.data, type_of_page, select_vector)

    if type_of_page == 'A':
        await pg.make_artists(callback, select_vector)
    elif type_of_page == 'a':
        await pg.make_artist(callback, select_vector)
    elif type_of_page == 'l':
        await pg.make_album(callback, select_vector)
    elif type_of_page == 's':
        await pg.make_song(callback, select_vector)
