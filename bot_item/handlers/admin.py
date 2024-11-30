from config.bot import *
import bot_item.page as pg
rt: Router = Router()

# TODO:
#  Команда /addraw {имя} — добавить необработанного исполнителя
#  Команда /raw — посмотреть не обработанных исполнителей
#  Команда /err — посмотреть не обработанных исполнителей, которых не нашёл алгоритм
#  Команда /clear_temp — очистить временные файлы (песенки)
#  Команда /... — Забрать song_info.db
#  Команда /... — обновить song_info.db
#


@rt.message(Command(commands='users'), IsAdmin())  # /users
async def cmd_users(message: Message):
    await pg.make_users(message, 1)


@rt.message(Command(commands='promote'), IsSuperAdmin())  # /promote
@command_with_user_id_argument
async def cmd_promote(message: Message, user_id):
    if IsAdmin().check(user_id):
        await message.answer(text=phrases['error']['user_admin'], reply_markup=kb.main)
        return
    users.promote(user_id)
    await message.answer(text=phrases['promote'], reply_markup=kb.make_clear(user_id))
    await bot.send_message(chat_id=user_id, text=phrases['admin'], reply_markup=kb.main)


@rt.message(Command(commands='demote'), IsSuperAdmin())  # /demote
@command_with_user_id_argument
async def cmd_demote(message: Message, user_id):
    if not IsAdmin().check(user_id):
        await message.answer(text=phrases['error']['user_not_admin'], reply_markup=kb.main)
        return
    users.demote(user_id)
    await message.answer(text=phrases['demote'], reply_markup=kb.make_clear(user_id))
    await bot.send_message(chat_id=user_id, text=phrases['not_admin'], reply_markup=kb.main)


@rt.message(Command(commands='banana'), IsAdmin())  # /banana
@command_with_user_id_argument
async def cmd_banana(message: Message, user_id):
    if IsAdmin().check(user_id):
        await message.answer(text=phrases['error']['user_admin'], reply_markup=kb.main)
        return
    users.ban(user_id)
    await message.answer(text=phrases['ban'], reply_markup=kb.make_clear(user_id))


@rt.message(Command(commands='unban'), IsAdmin())  # /unban
@command_with_user_id_argument
async def cmd_artists(message: Message, user_id):
    users.unban(user_id)
    await message.answer(text=phrases['unban'], reply_markup=kb.main)


@rt.callback_query(F.data.startswith('clear_'), IsAdmin())
async def catch_clear(callback: CallbackQuery):
    user_id = int(callback.data.replace('clear_', ''))
    settings.delete(user_id)
    users.delete(user_id)
    await callback.message.answer(text=phrases['clear'], reply_markup=kb.main)


@rt.callback_query(F.data.startswith('pageUSERS_'), IsAdmin())
async def catch_goto_page_song_info(callback: CallbackQuery):
    page_number = int(callback.data.replace('pageUSERS_', ''))
    await pg.make_users(callback, page_number)
