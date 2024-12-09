from config.bot import *
import bot_item.page as pg
rt: Router = Router()


@rt.message(CommandStart())  # /start
async def cmd_start(message: Message):
    if users.add(message.from_user.id, message.from_user.username):
        await message.answer(text=phrases['cmd_start'], reply_markup=kb.start)


@rt.callback_query(F.data == 'read_agreement')
async def call_cancel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(phrases['agreement'], reply_markup=kb.agreement)
    await callback.message.edit_reply_markup(reply_markup=None)


@rt.callback_query(F.data == 'agree')
async def call_cancel(callback: CallbackQuery):
    await callback.answer()
    users.admit(callback.from_user.id)
    await callback.message.answer(text=phrases['admitted'], reply_markup=kb.main)
    await callback.message.edit_reply_markup(reply_markup=None)


@rt.message(IsNotAdmitted())
async def catch_admit(message: Message):
    await sent_from_list(message, 'stat_not_admit')


@rt.message(IsBaned())
async def catch_ban(message: Message):
    await sent_from_list(message, 'stat_ban')

# - - - - - - - - Сверху стандартные функции, снизу приколы - - - - - - - -


@rt.message(F.text.lower() == 'настройки')
async def catch_settings(message: Message):
    await pg.make_settings(message)


@rt.message(Command(commands='settings'))  # /settings
async def cmd_settings(message: Message):
    await catch_settings(message)


@rt.message(Command(commands='about'))  # /about
async def cmd_about(message: Message):
    await message.answer_photo(caption=phrases["cmd_about"], reply_markup=kb.main, photo=FSInputFile(IMG_LOGOS_FILE))


@rt.message(Command(commands='help'))  # /help
async def cmd_help(message: Message):
    await message.answer(phrases["cmd_help"], reply_markup=kb.main)


@rt.message(Command(commands='agreement'))  # /agreement
async def cmd_agreement(message: Message):
    await message.answer(phrases["agreement"], reply_markup=kb.main)


@rt.message(Command(commands='day_song'))  # /day_song
async def cmd_day_song(message: Message):
    song_title, song_id, artists_title, album_id = await get_day_song()

    msg_txt = make_song_lyrics_message(song=song_title, artist=artists_title,
                                       link=make_yandex_song_link(song_id, album_id))
    await message.answer(text=msg_txt, disable_web_page_preview=True, reply_markup=kb.main)


@rt.message(Command(commands='format'))  # /format
@command_with_arguments_by_newline
async def cmd_format(message: Message, args):
    groups = ['\n'.join(group) for key, group in groupby(args, lambda x: x == '') if not key]
    del args

    if len(groups) > 3:
        await message.answer(text=phrases['error']['lot_of_arguments_3'], reply_markup=kb.main)
        return

    if len(groups) == 3:
        if await is_yandex_link(groups[2]):
            song_id = search(YANDEX_SONG_ID_PATTERN, groups[2]).group(1)
            song_title, artist_title = await get_song_artist_title_by_song_id(song_id)
            msg_text = make_song_lyrics_message(lines=groups[0],
                                                song=song_title,
                                                artist=artist_title,
                                                link=groups[2])

        elif await is_link(groups[2]):
            msg_text = make_song_lyrics_message(lines=groups[0],
                                                artist_song=groups[1],
                                                link=groups[2])
        else:
            msg_text = make_song_lyrics_message(lines=groups[0],
                                                artist_song=groups[1])

    elif len(groups) == 2:
        if await is_yandex_link(groups[1]):
            song_id = search(YANDEX_SONG_ID_PATTERN, groups[1]).group(1)
            song_title, artist_title = await get_song_artist_title_by_song_id(song_id)
            msg_text = make_song_lyrics_message(lines=groups[0],
                                                song=song_title,
                                                artist=artist_title,
                                                link=groups[1])
        else:
            msg_text = make_song_lyrics_message(lines=groups[0],
                                                artist_song=groups[1])

    else:
        msg_text = make_song_lyrics_message(lines=groups[0])

    if settings.is_suggested(message.from_user.id):
        if await IsEditor.check(message.from_user.id):
            await message.answer(text=msg_text, reply_markup=kb.publish_post, disable_web_page_preview=True)
        else:
            await message.answer(text=msg_text, reply_markup=kb.suggest_post, disable_web_page_preview=True)
    else:
        await message.answer(text=msg_text, disable_web_page_preview=True)


@rt.callback_query(F.data == 'pass')
async def call_cancel(callback: CallbackQuery):
    await callback.answer(reply_markup=kb.main)


# - - - - - - - - Псевдоним команд - - - - - - - -


@rt.message(Command(commands='sr'))  # /sr (start)
async def alias_cmd_artists(message: Message):
    await cmd_start(message)


@rt.message(Command(commands='st'))  # /st (settings)
async def alias_cmd_settings(message: Message):
    await catch_settings(message)


@rt.message(Command(commands='ab'))  # /ab (about)
async def alias_cmd_about(message: Message):
    await cmd_about(message)


@rt.message(Command(commands='h'))  # /h (help)
async def alias_cmd_help(message: Message):
    await cmd_help(message)


@rt.message(Command(commands='ag'))  # /ag (agreement)
async def alias_cmd_agreement(message: Message):
    await cmd_agreement(message)


@rt.message(Command(commands='ds'))  # /ds (day_song)
async def alias_cmd_day_song(message: Message):
    await cmd_day_song(message)


@rt.message(Command(commands='f'))  # /f (format)
async def alias_cmd_format(message: Message):
    await cmd_format(message)
