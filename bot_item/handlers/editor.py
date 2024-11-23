from config.bot import *
from bot_item.handlers.default import cmd_day_song
rt: Router = Router()


@rt.message(Command(commands='set_day_song'), IsEditor())  # /set_day_song
async def cmd_set_day_song(message: Message):
    album_id, song_id = await get_cmd_id_from_yandex_link(message)

    if album_id and song_id:
        set_day_song(album_id, song_id)
        await message.answer(phrases['save_day_song'])
        await cmd_day_song(message)
    return
