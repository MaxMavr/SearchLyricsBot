from config.bot import *
rt: Router = Router()


@rt.message(CommandStart())  # /start
async def cmd_start(message: Message):
    if users.add(message.from_user.id, message.from_user.username):
        await message.answer(text=phrases["cmd_start"], reply_markup=kb.main)


@rt.message(IsBaned())
async def catch_ban(message: Message):
    await sent_to_banned(message)


@rt.message(Command(commands='about'))  # /about
async def cmd_about(message: Message):
    await message.answer(phrases["cmd_about"], reply_markup=kb.main)


@rt.message(Command(commands='help'))  # /help
async def cmd_help(message: Message):
    await message.answer(phrases["cmd_help"], reply_markup=kb.main)


@rt.callback_query(F.data == 'pass')
async def call_cancel(callback: CallbackQuery):
    await callback.answer(reply_markup=kb.main)
