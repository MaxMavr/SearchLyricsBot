from config.bot import *
# from embedding.calculating_embeddings import search
import bot_item.page as pg
rt: Router = Router()


@rt.message(F.text.lower() == 'исполнители')
async def catch_artists(message: Message):
    await pg.make_artists(event=message, select_vector=[1, 1, 1, 1])


@rt.message(Command(commands='artists'))  # /artists
async def cmd_artists(message: Message):
    await catch_artists(message)


@rt.message(Command(commands='artist'))  # /artist
@command_with_artist_id_argument
async def cmd_artist(message: Message, artist_id):
    select_vector = artist_id + [1, 1, 1]
    await pg.make_artists(event=message, select_vector=select_vector)


@rt.message(Command(commands='album'))  # /album
@command_with_album_id_argument
async def cmd_album(message: Message, album_id):
    select_vector = album_id + [1, 1]
    await pg.make_artist(event=message, select_vector=select_vector)


@rt.message(Command(commands='song'))  # /song
@command_with_song_id_argument
async def cmd_song(message: Message, song_id):
    select_vector = song_id + [1]
    await pg.make_album(event=message, select_vector=select_vector)


@rt.message(Command(commands='search'))  # /search
@command_with_arguments
async def cmd_search(message: Message, args):
    query = ' '.join(args)
    # song_id, line_id = search(query)
    song_id, line_id = '86505415', 1
    line = (await get_line_by_id(song_id, line_id)) + query
    _, album_id, _ = bonds.get_ids_by_song(song_id)
    link = make_yandex_song_link(song_id, album_id)
    artists_title = ', '.join([artist for artist in await get_artist_title_by_song_id(song_id)])
    _, song_title, _, _, _ = songs.get(song_id)
    msg_text = make_song_lyrics_message(song=song_title, artist=artists_title, link=link, lines=line)

    if settings.is_suggested(message.from_user.id):
        if await IsEditor.check(message.from_user.id):
            await message.answer(text=msg_text, reply_markup=kb.publish_post, disable_web_page_preview=True)
        else:
            await message.answer(text=msg_text, reply_markup=kb.suggest_post, disable_web_page_preview=True)
    else:
        await message.answer(text=msg_text, disable_web_page_preview=True)


@rt.callback_query(F.data.startswith('pageSI_'))
async def catch_goto_page_song_info(callback: CallbackQuery):
    type_of_page, select_vector = decoding_page_callback(callback.data)

    await callback.answer(f'{type_of_page}   {select_vector}')
    # print(callback.data, type_of_page, select_vector)

    if type_of_page == 'A':
        await pg.make_artists(callback, select_vector)
    elif type_of_page == 'a':
        await pg.make_artist(callback, select_vector)
    elif type_of_page == 'l':
        await pg.make_album(callback, select_vector)
    elif type_of_page == 's':
        await pg.make_song(callback, select_vector)

# - - - - - - - - Псевдоним команд - - - - - - - -


@rt.message(Command(commands='as'))  # /as (artists)
async def alias_cmd_artists(message: Message):
    await catch_artists(message)


@rt.message(Command(commands='ar'))  # /ar (artist)
async def alias_cmd_artist(message: Message):
    await cmd_artist(message)


@rt.message(Command(commands='al'))  # /al (album)
async def alias_cmd_album(message: Message):
    await cmd_album(message)


@rt.message(Command(commands='sg'))  # /sg (song)
async def alias_cmd_song(message: Message):
    await cmd_song(message)


@rt.message(Command(commands='s'))  # /s (search)
async def alias_cmd_search(message: Message):
    await cmd_search(message)
