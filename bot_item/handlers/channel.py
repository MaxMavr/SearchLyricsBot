from config.bot import *
rt: Router = Router()


@rt.callback_query(F.data == 'publish_post')
async def call_cancel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.copy_to(chat_id=CHANNEL_ID, reply_markup=None)
    await callback.message.answer(text=phrases['publish_post'], reply_markup=kb.main)


@rt.callback_query(F.data == 'suggest_post')
async def call_cancel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await bot.send_message(chat_id=MAIN_ADMIN_ID, text=f'От @{callback.from_user.username}')
    await callback.message.copy_to(chat_id=MAIN_ADMIN_ID, disable_web_page_preview=True, reply_markup=kb.publish_post)
    await callback.message.answer(text=phrases['suggest_post'], reply_markup=kb.main)
