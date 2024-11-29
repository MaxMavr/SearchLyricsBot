from config.kb import *
from config.const import (ARTISTS_PAGE_SIZE,
                          ARTIST_PAGE_SIZE,
                          ALBUM_PAGE_SIZE,
                          SONG_PAGE_SIZE,
                          USERS_PAGE_SIZE)

# TODO ПЕРЕПИСАТЬ ВСЕ ЭТО

suffixes2suffixes_text = {
    'A': 'artist',
    'a': 'album',
    'l': 'song',
    's': ''
}
suffixes_direction = ['A', 'a', 'l', 's']


class Suffix:
    def __init__(self, suffix_current: str):
        self.index = suffixes_direction.index(suffix_current)
        self.current = suffix_current

        if self.index == len(suffixes_direction) - 1:
            self.child = ''
        else:
            self.child = suffixes_direction[self.index + 1]

        if self.index == 0:
            self.parent = ''
        else:
            self.parent = suffixes_direction[self.index - 1]

        self.text = suffixes2suffixes_text[suffixes_direction[self.index]]

        if suffix_current != 's':
            self.coord_in = suffixes_direction.index(suffix_current)


suffix_artists = Suffix('A')
suffix_artist = Suffix('a')
suffix_album = Suffix('l')
suffix_song = Suffix('s')


start = IMarkup(inline_keyboard=[[IButton(text=phrases['button_read_agreement'], callback_data='read_agreement'),
                                  IButton(text=phrases['button_admitted'], callback_data='agree')]])


agreement = IMarkup(inline_keyboard=[[IButton(text=phrases['button_admitted'], callback_data='agree')]])


main = KMarkup(keyboard=[[KButton(text=phrases['button_main_settings']),
                          KButton(text=phrases['button_main_artists'])]],
               resize_keyboard=True,
               input_field_placeholder=phrases['placeholder_appeal'])


publish_post = IMarkup(inline_keyboard=[[IButton(text=phrases['button_publish_post'],
                                                 callback_data='publish_post')]])

suggest_post = IMarkup(inline_keyboard=[[IButton(text=phrases['button_suggest_post'],
                                                 callback_data='suggest_post')]])


def __make_page_button(content: Tuple[str, str] = None):
    if not content:
        return IButton(text=phrases['icon_empty'], callback_data='pass')
    return IButton(text=content[0], callback_data=content[1])


def __make_page_callback_data(suffix: str, select_vector: Tuple[int, int, int, int]):
    return f'pageSI_{suffix}_{select_vector[0]}_{select_vector[1]}_{select_vector[2]}_{select_vector[3]}'


def decoding_page_callback(callback_data: str) -> Tuple[str, Tuple[int, int, int, int]]:
    callback_data_list = callback_data.split('_')
    type_data = callback_data_list[1]
    select_artist = int(callback_data_list[2])
    select_album = int(callback_data_list[3])
    select_song = int(callback_data_list[4])
    select_lyrics = int(callback_data_list[5])
    return type_data, (select_artist, select_album, select_song, select_lyrics)


def __modify_select_vector(select_vector: Tuple[int, int, int, int],
                           select_index: int,
                           offset: int) -> Tuple[int, int, int, int]:
    return tuple((select_vector[i] + offset) if i == select_index else select_vector[i] for i in range(4))


def __set_to_select_vector(select_vector: Tuple[int, int, int, int],
                           select_index: int,
                           number: int) -> Tuple[int, int, int, int]:
    return tuple(number if i == select_index else select_vector[i] for i in range(4))


def __make_artists_artist_page(select_vector: Tuple[int, int, int, int],
                               relative_select_number: int,
                               max_select: int,
                               page_number: int, page_size: int, max_page: int,
                               suffix: Suffix):

    past_item = None
    if select_vector[suffix.index] > 1:
        past_item = (phrases[f'button_past_{suffix.text}'],
                     __make_page_callback_data(suffix.current,
                                               __modify_select_vector(select_vector, suffix.index, -1)))

    next_item = None
    if select_vector[suffix.index] < max_select:
        next_item = (phrases[f'button_next_{suffix.text}'],
                     __make_page_callback_data(suffix.current,
                                               __modify_select_vector(select_vector, suffix.index, +1)))

    child = (phrases[f'button_child_{suffix.text}'],
             __make_page_callback_data(suffix.child,
                                       __set_to_select_vector(select_vector, suffix.index + 1, 1)))

    parent = None
    if suffix.parent != '':
        parent = (phrases[f'button_parent_{suffix.text}'],
                  __make_page_callback_data(suffix.parent, select_vector))

    if max_page <= 1:
        return IMarkup(inline_keyboard=[
            [__make_page_button(past_item)],
            [__make_page_button(parent), __make_page_button(child)],
            [__make_page_button(next_item)]
        ])

    past_page = None
    if page_number > 1:
        past_page = (phrases['button_past_page'],
                     __make_page_callback_data(suffix.current,
                                               __modify_select_vector(select_vector, suffix.index, -relative_select_number - page_size)))

    next_page = None
    if page_number < max_page:
        next_page = (phrases['button_next_page'],
                     __make_page_callback_data(suffix.current,
                                               __modify_select_vector(select_vector, suffix.index, -relative_select_number + page_size)))

    return IMarkup(inline_keyboard=[
        [__make_page_button(past_item)],
        [__make_page_button(past_page), __make_page_button(next_page)],
        [__make_page_button(parent),  __make_page_button(child)],
        [__make_page_button(next_item)]
    ])


def make_artists(select_vector: Tuple[int, int, int, int],
                 relative_select_number: int,
                 max_select: int,
                 page_number: int,
                 max_page: int):

    return __make_artists_artist_page(
        select_vector=select_vector,
        relative_select_number=relative_select_number,
        max_select=max_select,
        page_number=page_number,
        page_size=ARTISTS_PAGE_SIZE,
        max_page=max_page,
        suffix=suffix_artists,
    )


def make_artist(select_vector: Tuple[int, int, int, int],
                relative_select_number: int,
                max_select: int,
                page_number: int,
                max_page: int):

    return __make_artists_artist_page(
        select_vector=select_vector,
        relative_select_number=relative_select_number,
        max_select=max_select,
        page_number=page_number,
        page_size=ARTIST_PAGE_SIZE,
        max_page=max_page,
        suffix=suffix_artist,
    )


def make_album(select_vector: Tuple[int, int, int, int],
               relative_select_number: int,
               max_select: int,
               page_number: int,
               max_page: int,
               max_album: int):

    suffix = suffix_album

    past_item = None
    if select_vector[2] > 1:
        past_item = (phrases[f'button_past_song'],
                     __make_page_callback_data(suffix.current,
                                               __modify_select_vector(select_vector, 2, -1)))
    if select_vector[1] > 1:
        past_item = (phrases[f'button_past_song'],
                     __make_page_callback_data(suffix.current,
                                               __set_to_select_vector(__modify_select_vector(select_vector, 1, -1), 2, -2)))

    next_item = None
    if select_vector[2] < max_select:
        next_item = (phrases[f'button_next_song'],
                     __make_page_callback_data(suffix.current,
                                               __modify_select_vector(select_vector, 2, +1)))
    elif select_vector[1] < max_album:
        next_item = (phrases[f'button_next_song'],
                     __make_page_callback_data(suffix.current,
                                               __set_to_select_vector(__modify_select_vector(select_vector, 1, +1), 2, 1)))

    child = (phrases[f'button_child_song'],
             __make_page_callback_data(suffix.child, select_vector))

    parent = (phrases[f'button_parent_song'],
              __make_page_callback_data(suffix.parent, select_vector))

    if max_page <= 1 and select_vector[1] >= max_album:
        return IMarkup(inline_keyboard=[
            [__make_page_button(past_item)],
            [__make_page_button(parent), __make_page_button(child)],
            [__make_page_button(next_item)]
        ])

    past_page = None
    if page_number > 1:
        past_page = (phrases['button_past_page'],
                     __make_page_callback_data(suffix.current,
                                               __modify_select_vector(select_vector, 2, -relative_select_number - ALBUM_PAGE_SIZE)))
    elif select_vector[1] > 1:
        past_page = (phrases['button_past_song_album'],
                     __make_page_callback_data(suffix.current,
                                               __set_to_select_vector(__modify_select_vector(select_vector, 1, -1), 2, -1)))

    next_page = None
    if page_number < max_page:
        next_page = (phrases['button_next_page'],
                     __make_page_callback_data(suffix.current,
                                               __modify_select_vector(select_vector, 2, -relative_select_number + ALBUM_PAGE_SIZE)))
    elif select_vector[1] < max_album:
        next_page = (phrases['button_next_song_album'],
                     __make_page_callback_data(suffix.current,
                                               __set_to_select_vector(__modify_select_vector(select_vector, 1, +1), 2, 1)))

    return IMarkup(inline_keyboard=[
        [__make_page_button(past_item)],
        [__make_page_button(past_page), __make_page_button(next_page)],
        [__make_page_button(parent), __make_page_button(child)],
        [__make_page_button(next_item)]
    ])


def make_song(select_vector: Tuple[int, int, int, int],
              page_number: int,
              max_page: int,
              show_ids: bool,
              max_album: int):

    return None

    suffix = suffix_album

    past_item = None
    if select_vector[2] > 1:
        past_item = (phrases[f'button_past_song'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector,
                                                                      2,
                                                                      -1)))
    if select_vector[1] > 1:
        past_item = (phrases[f'button_past_song'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __set_to_select_vector(
                                                   __modify_select_vector(select_vector, 1, -1),
                                                   2,
                                                   -1)))

    next_item = None
    if select_vector[2] < max_select:
        next_item = (phrases[f'button_next_song'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector,
                                                                      2,
                                                                      +1)))
    elif select_vector[1] < max_album:
        next_item = (phrases[f'button_next_song'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __set_to_select_vector(
                                                   __modify_select_vector(select_vector, 1, +1),
                                                   2,
                                                   1)))

    ids = (phrases[f'button_show_ids_{not show_ids}'],
           __make_page_callback_data(suffix.current, not show_ids, select_vector))

    child = (phrases[f'button_child_song'],
             __make_page_callback_data(suffix.child, show_ids, select_vector))

    parent = (phrases[f'button_parent_song'],
              __make_page_callback_data(suffix.parent, show_ids, select_vector))

    if max_page <= 1 and select_vector[1] >= max_album:
        return IMarkup(inline_keyboard=[
            [__make_page_button(past_item)],
            [__make_page_button(parent), __make_page_button(ids), __make_page_button(child)],
            [__make_page_button(next_item)]
        ])

    past_page = None
    if page_number > 1:
        past_page = (phrases['button_past_page'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector,
                                                                      2,
                                                                      -relative_select_number - ALBUM_PAGE_SIZE)))
    elif select_vector[1] > 1:
        past_page = (phrases['button_past_song_album'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __set_to_select_vector(
                                                   __modify_select_vector(select_vector, 1, -1),
                                                   2,
                                                   -1)))

    next_page = None
    if page_number < max_page:
        next_page = (phrases['button_next_page'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector,
                                                                      2,
                                                                      -relative_select_number + ALBUM_PAGE_SIZE)))
    elif select_vector[1] < max_album:
        next_page = (phrases['button_next_song_album'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __set_to_select_vector(
                                                   __modify_select_vector(select_vector, 1, +1),
                                                   2,
                                                   1)))

    return IMarkup(inline_keyboard=[
        [__make_page_button(past_item)],
        [__make_page_button(past_page), __make_page_button(next_page)],
        [__make_page_button(parent), __make_page_button(ids), __make_page_button(child)],
        [__make_page_button(next_item)]
    ])


def make_users(page_number: int, max_page: int):
    kb = IBuilder()

    if page_number != 1:
        kb.button(text=phrases['button_past_page'], callback_data=f'pageUSERS_{page_number - 1}')
    if page_number < max_page:
        kb.button(text=phrases['button_next_page'], callback_data=f'pageUSERS_{page_number + 1}')
    return kb.adjust(2).as_markup(resize_keyboard=True)


def make_settings(settings_items: dict):
    icon_kb = []
    print()
    for name, value in settings_items.items():
        if name.startswith('icon_'):
            icon_kb.append(IButton(text=value,
                                   callback_data=f'settings_{name}'))
        print(name, ':::', value)

    bool_kb = []
    for name, value in settings_items.items():
        if name.startswith('bool_'):
            bool_kb.append(IButton(text=phrases[f'button_settings_{name}_{not value}'],
                                   callback_data=f'settings_{name}_{not value}'))

    kb = [icon_kb[i:i + 3] for i in range(0, len(icon_kb), 3)]
    kb += [[b] for b in bool_kb]

    return IMarkup(inline_keyboard=kb)


def make_clear(user_id: int):
    return IMarkup(inline_keyboard=[[IButton(text=phrases['button_clear'], callback_data=f'clear_{user_id}')]])
