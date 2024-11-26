from config.bot import *
from bot_item.pages import make_users_page
rt: Router = Router()

# TODO:
#  Команда /addraw {имя} — добавить необработанного исполнителя
#  Команда /raw — посмотреть не обработанных исполнителей
#  Команда /err — посмотреть не обработанных исполнителей, которых не нашёл алгоритм
#  Команда /banana — для бана пользователя
#  Команда /clear_temp — очистить временные файлы (песенки)
#  Команда /... — Забрать song_info.db
#  Команда /... — обновить song_info.db
#


@rt.message(Command(commands='users'), IsAdmin())  # /users
async def cmd_artists(message: Message):
    await make_users_page(message, 1)


@rt.callback_query(F.data.startswith('pageUSERS_'), IsAdmin())
async def catch_goto_page_song_info(callback: CallbackQuery):
    page_number = int(callback.data.replace('pageUSERS_', ''))
    await make_users_page(callback, page_number)
