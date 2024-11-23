from config.bot import *
rt: Router = Router()


@rt.callback_query(F.data == 'publish_post')
async def call_cancel(callback: CallbackQuery):
    await callback.answer()
    await bot.send_message(chat_id=CHANNEL_ID, text=callback.message.text)
    await callback.answer(text=phrases['publish_post'], reply_markup=kb.main)


@rt.callback_query(F.data == 'suggest_post')
async def call_cancel(callback: CallbackQuery):
    await callback.answer()
    await bot.send_message(chat_id=MAIN_ADMIN_ID, text=f'От @{callback.from_user.username}')
    await bot.send_message(chat_id=MAIN_ADMIN_ID, text=callback.message.text, reply_markup=kb.publish_post)
    await callback.answer(text=phrases['suggest_post'], reply_markup=kb.main)
