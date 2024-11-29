from config.bot import *
import bot_item.page as pg
rt: Router = Router()


@rt.message(Command(commands='cancel'))  # /cancel
async def cmd_artists(message: Message, state: FSMContext):
    await message.answer(phrases['cancel'])
    await state.clear()


@rt.callback_query(F.data.startswith('settings_'))
async def catch_goto_page_song_info(callback: CallbackQuery, state: FSMContext = None):
    type_setting = callback.data.split('_')

    if type_setting[1] == 'bool':
        settings.upd_bool(callback.from_user.id, '_'.join(type_setting[1:-1]))
        await callback.answer(phrases[f"popup_{'_'.join(type_setting[1:])}"])
        await pg.make_settings(callback)

    if type_setting[1] == 'icon':
        await callback.answer()
        await state.set_state(Settings.icon)
        await state.update_data(edit_message=callback.message)
        await state.update_data(edit_icon='_'.join(type_setting[1:]))
        await callback.message.answer(text=phrases['settings_icon'] + phrases['footnote_cancel'])


@rt.message(Settings.icon)
async def set_icon(message: Message, state: FSMContext):
    if len(message.text) > 3:
        await message.answer(phrases['err_long_argument_icon'])
        return

    data = await state.get_data()
    edit_message: Message = data.get('edit_message')
    edit_icon = data.get('edit_icon')
    settings.set_icon(message.from_user.id, edit_icon, message.text)
    await edit_message.delete()
    await pg.make_settings(message)
    await state.clear()
