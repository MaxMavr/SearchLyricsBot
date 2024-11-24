from config.kb import *
from config.const import (ARTISTS_PAGE_SIZE,
                          ARTIST_PAGE_SIZE,
                          ALBUM_PAGE_SIZE,
                          SONG_PAGE_SIZE,
                          USERS_PAGE_SIZE)

suffixes2suffixes_text = {
    'A': 'artist',
    'a': 'album',
    'l': 'song',
    's': ''
}
suffixes_direction = ['A', 'a', 'l', 's']
suffixes_index_coordinate = ['A', 'a', 'l']


class Suffix:
    def __init__(self, suffix_current: str):
        self.__current_index = suffixes_direction.index(suffix_current)
        self.current = suffix_current

        if self.__current_index == len(suffixes_direction) - 1:
            self.child = ''
        else:
            self.child = suffixes_direction[self.__current_index + 1]

        if self.__current_index == 0:
            self.parent = ''
        else:
            self.parent = suffixes_direction[self.__current_index - 1]

        self.text = suffixes2suffixes_text[suffixes_direction[self.__current_index]]

        if suffix_current != 's':
            self.coord_in = suffixes_direction.index(suffix_current)


suffix_artists = Suffix('A')
suffix_artist = Suffix('a')
suffix_album = Suffix('l')
suffix_song = Suffix('s')


main = KMarkup(keyboard=[[KButton(text=phrases['button_main_artists'])]],
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


def __make_page_callback_data(suffix: str, show_ids: bool,
                              select_vector: Tuple[int, int, int]):
    show_ids_data = 'T' if show_ids else 'F'
    return f'pageSI_{suffix}{show_ids_data}_{select_vector[0]}_{select_vector[1]}_{select_vector[2]}'


def decoding_page_callback(callback_data: str) -> Tuple[str, bool, Tuple[int, int, int]]:
    callback_data_list = callback_data.split('_')
    type_data = callback_data_list[1]
    suffix = type_data[0]
    show_ids = type_data[1] == 'T'
    select_artist = int(callback_data_list[2])
    select_album = int(callback_data_list[3])
    select_song = int(callback_data_list[4])
    return suffix, show_ids, (select_artist, select_album, select_song)


def __modify_select_vector(select_vector: Tuple[int, int, int], main_select_index: int, offset: int) -> Tuple[int, int, int]:
    new_select_vector = tuple(
        (select_vector[i] + offset) if i == main_select_index else select_vector[i] for i in range(3))
    return new_select_vector


def __make_artists_artist_page(select_vector: Tuple[int, int, int],
                               main_select_index: int,
                               relative_main_select_number: int,
                               max_main_select: int,
                               page_number: int, page_size: int, max_page: int,
                               show_ids: bool,
                               suffix: Suffix):

    msi = main_select_index
    del main_select_index

    past_item = None
    if select_vector[msi] > 1:
        past_item = (phrases[f'button_past_{suffix.text}'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector, msi, -1)))

    next_item = None
    if select_vector[msi] < max_main_select:
        next_item = (phrases[f'button_next_{suffix.text}'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector, msi, +1)))

    ids = (phrases[f'button_show_ids_{not show_ids}'],
           __make_page_callback_data(suffix.current, not show_ids, select_vector))

    child = None
    if suffix.child != '':
        if msi == len(select_vector) - 1:
            child = (phrases[f'button_child_{suffix.text}'],
                     __make_page_callback_data(suffix.child, show_ids, select_vector))
        else:
            child = (phrases[f'button_child_{suffix.text}'],
                     __make_page_callback_data(suffix.child, show_ids,
                                               __modify_select_vector(select_vector, msi + 1, - select_vector[msi + 1] + 1)))

    parent = None
    if suffix.parent != '':
        parent = (phrases[f'button_parent_{suffix.text}'],
                  __make_page_callback_data(suffix.parent, show_ids, select_vector))

    if max_page <= 1:
        return IMarkup(inline_keyboard=[
            [__make_page_button(past_item)],
            [__make_page_button(parent), __make_page_button(ids), __make_page_button(child)],
            [__make_page_button(next_item)]
        ])

    past_page = None
    if page_number > 1:
        offset = -relative_main_select_number - page_size
        past_page = (phrases['button_past_page'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector, msi, offset)))

    next_page = None
    if page_number < max_page:
        offset = -relative_main_select_number + page_size
        next_page = (phrases['button_next_page'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector, msi, offset)))

    return IMarkup(inline_keyboard=[
        [__make_page_button(past_item)],
        [__make_page_button(past_page), __make_page_button(next_page)],
        [__make_page_button(parent), __make_page_button(ids), __make_page_button(child)],
        [__make_page_button(next_item)]
    ])


def make_artists(select_vector: Tuple[int, int, int],
                 relative_main_select_number: int,
                 max_main_select: int,
                 page_number: int,
                 max_page: int,
                 show_ids: bool):

    return __make_artists_artist_page(
        select_vector=select_vector,
        main_select_index=0,
        relative_main_select_number=relative_main_select_number,
        max_main_select=max_main_select,
        page_number=page_number,
        page_size=ARTISTS_PAGE_SIZE,
        max_page=max_page,
        show_ids=show_ids,
        suffix=suffix_artists,
    )


def make_artist(select_vector: Tuple[int, int, int],
                relative_main_select_number: int,
                max_main_select: int,
                page_number: int,
                max_page: int,
                show_ids: bool):

    return __make_artists_artist_page(
        select_vector=select_vector,
        main_select_index=1,
        relative_main_select_number=relative_main_select_number,
        max_main_select=max_main_select,
        page_number=page_number,
        page_size=ARTIST_PAGE_SIZE,
        max_page=max_page,
        show_ids=show_ids,
        suffix=suffix_artist,
    )


def make_album(select_vector: Tuple[int, int, int],
               relative_main_select_number: int,
               max_main_select: int,
               page_number: int,
               max_page: int,
               show_ids: bool,
               album_number: int):

    msi = 2
    suffix = suffix_album

    past_item = None
    if select_vector[msi] > 1:
        past_item = (phrases[f'button_past_song'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector, msi, -1)))

    next_item = None
    if select_vector[msi] < max_main_select:
        next_item = (phrases[f'button_next_song'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector, msi, +1)))

    ids = (phrases[f'button_show_ids_{not show_ids}'],
           __make_page_callback_data(suffix.current, not show_ids, select_vector))

    child = None
    if suffix.child != '':
        if msi == len(select_vector) - 1:
            child = (phrases[f'button_child_{suffix.text}'],
                     __make_page_callback_data(suffix.child, show_ids, select_vector))
        else:
            child = (phrases[f'button_child_{suffix.text}'],
                     __make_page_callback_data(suffix.child, show_ids,
                                               __modify_select_vector(select_vector, msi + 1, - select_vector[msi + 1] + 1)))

    parent = None
    if suffix.parent != '':
        parent = (phrases[f'button_parent_{suffix.text}'],
                  __make_page_callback_data(suffix.parent, show_ids, select_vector))

    if max_page <= 1:
        return IMarkup(inline_keyboard=[
            [__make_page_button(past_item)],
            [__make_page_button(parent), __make_page_button(ids), __make_page_button(child)],
            [__make_page_button(next_item)]
        ])

    past_page = None
    if page_number > 1:
        offset = -relative_main_select_number - page_size
        past_page = (phrases['button_past_page'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector, msi, offset)))

    next_page = None
    if page_number < max_page:
        offset = -relative_main_select_number + page_size
        next_page = (phrases['button_next_page'],
                     __make_page_callback_data(suffix.current, show_ids,
                                               __modify_select_vector(select_vector, msi, offset)))

    return IMarkup(inline_keyboard=[
        [__make_page_button(past_item)],
        [__make_page_button(past_page), __make_page_button(next_page)],
        [__make_page_button(parent), __make_page_button(ids), __make_page_button(child)],
        [__make_page_button(next_item)]
    ])


def make_song(select_vector: Tuple[int, int, int],
              relative_main_select_number: int,
              max_main_select: int,
              page_number: int,
              max_page: int,
              show_ids: bool):

    return __make_song_info_page(
        select_vector=select_vector,
        main_select_index=None,
        relative_main_select_number=relative_main_select_number,
        max_main_select=max_main_select,
        page_number=page_number,
        page_size=SONG_PAGE_SIZE,
        max_page=max_page,
        show_ids=show_ids,
        suffix=suffix_song,
    )
