from config.kb import *
from config.kb import (__make_past_item_button,
                       __make_next_item_button,
                       __make_past_page_button,
                       __make_next_page_button,
                       __make_child_button,
                       __make_parent_button,

                       __make_button,
                       __make_page_callback_data)

from config.const import (ARTISTS_PAGE_SIZE,
                          ARTIST_PAGE_SIZE,
                          ALBUM_PAGE_SIZE)

start = IMarkup(inline_keyboard=[[IButton(text=phrases['button']['read_agreement'], callback_data='read_agreement'),
                                  IButton(text=phrases['button']['admitted'], callback_data='agree')]])


agreement = IMarkup(inline_keyboard=[[IButton(text=phrases['button']['admitted'], callback_data='agree')]])


main = KMarkup(keyboard=[[KButton(text=phrases['button']['main_settings']),
                          KButton(text=phrases['button']['main_artists'])]],
               resize_keyboard=True,
               input_field_placeholder=phrases['placeholder_appeal'])


publish_post = IMarkup(inline_keyboard=[[IButton(text=phrases['button']['publish_post'],
                                                 callback_data='publish_post')]])

suggest_post = IMarkup(inline_keyboard=[[IButton(text=phrases['button']['suggest_post'],
                                                 callback_data='suggest_post')]])


def __make_artists_artist_page(select_vector: List[int],
                               relative_select_number: int,
                               max_select: int,
                               page_number: int, page_size: int, max_page: int,
                               suffix: Suffix,
                               icons: dict):

    past_item = __make_past_item_button(select_vector, suffix, icons)
    next_item = __make_next_item_button(select_vector, suffix, icons, max_select)

    child = __make_child_button(select_vector, suffix, icons)
    parent = __make_parent_button(select_vector, suffix, icons)

    if max_page <= 1:
        return IMarkup(inline_keyboard=[
            [past_item],
            [parent, child],
            [next_item]
        ])

    past_page = __make_past_page_button(select_vector, suffix, icons, page_number,
                                        relative_select_number, page_size)

    next_page = __make_next_page_button(select_vector, suffix, icons, page_number,
                                        relative_select_number, page_size, max_page)

    return IMarkup(inline_keyboard=[
        [past_item],
        [past_page, next_page],
        [parent,  child],
        [next_item]
    ])


def make_artists(select_vector: List[int],
                 relative_select_number: int,
                 max_select: int,
                 page_number: int,
                 max_page: int,
                 icons: dict):

    return __make_artists_artist_page(
        select_vector=select_vector,
        relative_select_number=relative_select_number,
        max_select=max_select,
        page_number=page_number,
        page_size=ARTISTS_PAGE_SIZE,
        max_page=max_page,
        suffix=suffix_artists,
        icons=icons
    )


def make_artist(select_vector: List[int],
                relative_select_number: int,
                max_select: int,
                page_number: int,
                max_page: int,
                icons: dict):

    return __make_artists_artist_page(
        select_vector=select_vector,
        relative_select_number=relative_select_number,
        max_select=max_select,
        page_number=page_number,
        page_size=ARTIST_PAGE_SIZE,
        max_page=max_page,
        suffix=suffix_artist,
        icons=icons
    )


def make_album(select_vector: List[int],
               relative_select_number: int,
               max_select: int,
               page_number: int,
               max_page: int,
               max_album: int,
               icons: dict):

    suffix = suffix_album

    past_item = __make_past_item_button(select_vector, suffix, icons)
    next_item = __make_next_item_button(select_vector, suffix, icons, max_select)

    if select_vector[1] > 1 and past_item == NULL_BUTTON:
        modify_select_vector = select_vector.copy()
        modify_select_vector[suffix.index - 1] -= 1
        modify_select_vector[suffix.index] = -2
        past_item = __make_button(icons['icon_up'] + phrases['button']['song']['past'],
                                  __make_page_callback_data(suffix.current, modify_select_vector))

    if select_vector[1] < max_album and next_item == NULL_BUTTON:
        modify_select_vector = select_vector.copy()
        modify_select_vector[suffix.index - 1] += 1
        modify_select_vector[suffix.index] = 1
        next_item = __make_button(icons['icon_down'] + phrases['button']['song']['next'],
                                  __make_page_callback_data(suffix.current, modify_select_vector))

    child = __make_child_button(select_vector, suffix, icons)
    parent = __make_parent_button(select_vector, suffix, icons)

    if max_page <= 1 and select_vector[1] >= max_album:
        return IMarkup(inline_keyboard=[
            [past_item],
            [parent, child],
            [next_item]
        ])

    past_page = __make_past_page_button(select_vector, suffix, icons, page_number,
                                        relative_select_number, ALBUM_PAGE_SIZE)

    next_page = __make_next_page_button(select_vector, suffix, icons, page_number,
                                        relative_select_number, ALBUM_PAGE_SIZE, max_page)

    if select_vector[1] > 1 and past_page == NULL_BUTTON:
        modify_select_vector = select_vector.copy()
        modify_select_vector[suffix.index - 1] -= 1
        modify_select_vector[suffix.index] = -1
        past_page = __make_button(icons['icon_past_page'] + phrases['button']['song']['past_album'],
                                  __make_page_callback_data(suffix.current, modify_select_vector))

    if select_vector[1] < max_album and next_page == NULL_BUTTON:
        modify_select_vector = select_vector.copy()
        modify_select_vector[suffix.index - 1] += 1
        modify_select_vector[suffix.index] = 1
        next_page = __make_button(phrases['button']['song']['next_album'] + icons['icon_next_page'],
                                  __make_page_callback_data(suffix.current, modify_select_vector))

    return IMarkup(inline_keyboard=[
        [past_item],
        [past_page, next_page],
        [parent, child],
        [next_item]
    ])


def make_song(select_vector: List[int],
              max_page: int,
              icons: dict):

    suffix = suffix_song

    parent = __make_parent_button(select_vector, suffix, icons)

    if max_page <= 1:
        return IMarkup(inline_keyboard=[
            [parent, NULL_BUTTON],
        ])

    past_page = __make_past_page_button(select_vector, suffix, icons, select_vector[3],
                                        0, 1)

    next_page = __make_next_page_button(select_vector, suffix, icons, select_vector[3],
                                        0, 1, max_page)

    show_emos = 
    return IMarkup(inline_keyboard=[
        [past_page, next_page],
        [parent, NULL_BUTTON],
    ])


def make_users(page_number: int, max_page: int, icons):
    kb = IBuilder()

    if page_number != 1:
        kb.button(text=icons['icon_past_page'] + phrases['button']['past_page'], callback_data=f'pageUSERS_{page_number - 1}')
    if page_number < max_page:
        kb.button(text=phrases['button']['next_page'] + icons['icon_next_page'], callback_data=f'pageUSERS_{page_number + 1}')
    return kb.adjust(2).as_markup(resize_keyboard=True)


def make_query(page_number: int, max_page: int, icons):
    kb = IBuilder()

    if page_number != 1:
        kb.button(text=icons['icon_past_page'] + phrases['button']['past_page'], callback_data=f'pageQUERY_{page_number - 1}')
    if page_number < max_page:
        kb.button(text=phrases['button']['next_page'] + icons['icon_next_page'], callback_data=f'pageQUERY_{page_number + 1}')
    return kb.adjust(2).as_markup(resize_keyboard=True)


def make_settings(settings_items: dict, page_mode: str):
    icon_kb = []
    if page_mode == 'icon':
        for name, value in settings_items.items():
            if name.startswith('icon_'):
                icon_kb.append(IButton(text=value.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&'),
                                       callback_data=f'settings_{name}'))
        icon_kb = [icon_kb[i:i + 3] for i in range(0, len(icon_kb), 3)]
        icon_kb += [[IButton(text=phrases['button']['settings']['allicon'], callback_data=f'settings_allicon')]]

    bool_kb = []
    set_kb = []
    if page_mode == 'bool':
        for name, value in settings_items.items():
            if name.startswith('bool_'):
                bool_kb.append(IButton(text=phrases['button']['settings'][f'{name}_{not value}'],
                                       callback_data=f'settings_{name}_{not value}'))
        bool_kb = [bool_kb[i:i + 2] for i in range(0, len(bool_kb), 2)]

        for name, set_set in phrases['settings']['presets'].items():
            set_kb.append(IButton(text=set_set['title'],
                                  callback_data=f'settings_preset_{name}'))

        set_kb = [set_kb[i:i + 3] for i in range(0, len(set_kb), 3)]

    kb = icon_kb
    kb += bool_kb
    kb += set_kb

    if page_mode == 'icon':
        kb += [[IButton(text=settings_items['icon_past_page'] + phrases['button']['past_page'], callback_data='pageSET_bool')]]
    if page_mode == 'bool':
        kb += [[IButton(text=phrases['button']['next_page'] + settings_items['icon_next_page'], callback_data='pageSET_icon')]]

    return IMarkup(inline_keyboard=kb)


def make_clear(user_id: int):
    return IMarkup(inline_keyboard=[[IButton(text=phrases['button']['clear'], callback_data=f'clear_{user_id}')]])
