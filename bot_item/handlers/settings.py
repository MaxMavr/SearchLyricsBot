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
        await callback.answer(phrases['settings']['popup']['_'.join(type_setting[1:])])
        await pg.make_settings(callback)
        return

    if type_setting[1] == 'icon':
        await callback.answer()
        await state.set_state(Settings.icon)
        await state.update_data(edit_message=callback.message)
        await state.update_data(edit_icon='_'.join(type_setting[1:]))
        await callback.message.answer(text=phrases['settings_icon'] + phrases['footnote_cancel'])
        return

    if type_setting[1] == 'allicon':
        await callback.answer()
        await state.set_state(Settings.allicon)
        await state.update_data(edit_message=callback.message)
        await callback.message.answer(text=phrases['settings_allicon'] + phrases['footnote_cancel'])
        return

    if type_setting[1] == 'preset':
        await callback.answer(
            phrases['settings']['popup']['set']
            + phrases['settings']['presets'][type_setting[2]]['title'] +
            phrases['settings']['popup']['preset'])
        settings.set_preset(callback.from_user.id, type_setting[2])
        await pg.make_settings(callback)
        return


@rt.callback_query(F.data.startswith('pageSET_'))
async def catch_goto_page_song_info(callback: CallbackQuery):
    page_mode = callback.data.replace('pageSET_', '')
    await pg.make_settings(callback, page_mode)


@rt.message(Settings.allicon)
async def set_allicon(message: Message, state: FSMContext):
    icon_list = message.text.split('\n')

    if len(icon_list) < phrases['settings']['count_icon']:
        await message.answer(text=phrases['error']['is_not_all_icon'], reply_markup=kb.main)
        return

    icon_list = icon_list[:phrases['settings']['count_icon']]

    for i, icon in enumerate(icon_list):
        if len(icon) > 3:
            await message.answer(text=phrases['error']['long_argument_all_icon'] + f'{i}. <i>{icon}</i>',
                                 reply_markup=kb.main)
            return

    i = 0
    for name in phrases['settings']['presets']['default']:
        if name.startswith('icon_'):
            settings.set_icon(message.from_user.id, name,
                              icon_list[i].replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;'))
            i += 1

    data = await state.get_data()
    edit_message: Message = data.get('edit_message')
    await edit_message.delete()
    await pg.make_settings(message, 'icon')
    await state.clear()

    await state.clear()


@rt.message(Settings.icon)
async def set_icon(message: Message, state: FSMContext):
    if len(message.text) > 3:
        await message.answer(text=phrases['error']['long_argument_icon'], reply_markup=kb.main)
        return

    data = await state.get_data()
    edit_message: Message = data.get('edit_message')
    edit_icon = data.get('edit_icon')
    settings.set_icon(message.from_user.id, edit_icon, message.text.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;'))
    await edit_message.delete()
    await pg.make_settings(message, 'icon')
    await state.clear()
