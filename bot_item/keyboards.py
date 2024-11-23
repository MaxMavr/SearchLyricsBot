from config.kb import *
from config.const import (ARTISTS_PAGE_SIZE,
                          ARTIST_PAGE_SIZE,
                          ALBUM_PAGE_SIZE,
                          SONG_PAGE_SIZE,
                          USERS_PAGE_SIZE)


main = KMarkup(keyboard=[[KButton(text=phrases['button_main_artists'])]],
               resize_keyboard=True,
               input_field_placeholder=phrases['placeholder_appeal'])


publish_post = IMarkup(inline_keyboard=[[IButton(text=phrases['button_publish_post'], callback_data='publish_post')]])

suggest_post = IMarkup(inline_keyboard=[[IButton(text=phrases['button_suggest_post'], callback_data='suggest_post')]])


def __make_page_button(content: Tuple[str, str] = None):
    if not content:
        return IButton(text=phrases['icon_empty'], callback_data='pass')
    return IButton(text=content[0], callback_data=content[1])


def __make_past_next_page(page_number: int, max_page_number: int, suffix_call: str, parent_id, select_number):
    if page_number <= 1:
        past_page = None
    else:
        number = select_number - ARTISTS_PAGE_SIZE - (select_number % ARTISTS_PAGE_SIZE) + 1
        past_page = (phrases['button_past_page'], f'pg_{suffix_call}_{parent_id}_{number}_{show_ids}')

    if page_number >= max_page_number:
        next_page = None
    else:
        number = select_number + ARTISTS_PAGE_SIZE - (select_number % ARTISTS_PAGE_SIZE) + 1
        next_page = (phrases['button_next_page'], f'pg_{suffix_call}_{parent_id}_{number}_{show_ids}')


def make_artists_and_artist(select_number: int, max_select: int,
                            page_number: int, max_page: int,
                            show_ids: bool,
                            select_id: str, select_have_child: bool,
                            suffix_text: str, suffix_call: str,
                            parent_id: str, suffix_child: str):
    if select_number <= 1:
        past_item = None
    else:
        number = select_number - 1
        past_item = (phrases[f'button_past_{suffix_text}'], f'pg_{suffix_call}_{parent_id}_{number}_{show_ids}')

    if select_number >= max_select:
        next_item = None
    else:
        number = select_number + 1
        next_item = (phrases[f'button_next_{suffix_text}'], f'pg_{suffix_call}_{parent_id}_{number}_{show_ids}')

    child = None
    if select_have_child:
        child = (phrases[f'button_child_{suffix_text}'], f'pg_{suffix_child}_{select_id}_1_{show_ids}')

    detail_show_ids = (phrases[f'button_show_ids_{not show_ids}'], f'pg_{suffix_call}_{parent_id}_{select_number}_{not show_ids}')

    if max_page <= 1:
        return IMarkup(inline_keyboard=[
            [__make_page_button(past_item)],
            [__make_page_button(detail_show_ids), __make_page_button(child)],
            [__make_page_button(next_item)]
        ])

    return IMarkup(inline_keyboard=[
        [__make_page_button(past_item)],
        [__make_page_button(past_page), __make_page_button(next_page)],
        [__make_page_button(None), __make_page_button(detail_show_ids), __make_page_button(child)],
        [__make_page_button(next_item)]
    ])


def make_artists(select_number: int, max_select: int,
                 page_number: int, max_page: int,
                 show_ids: bool,
                 select_artist_id: str, select_artist_have_child: bool):

    return make_artists_and_artist(select_number, max_select,
                                   page_number, max_page,
                                   show_ids,
                                   select_artist_id, select_artist_have_child,
                                   'artist', 'arts', '', 'art')


def make_artist(select_number: int, max_select: int,
                page_number: int, max_page: int,
                show_ids: bool,
                select_album_id: str, select_album_have_child: bool,
                artist_id):

    return make_artists_and_artist(select_number, max_select,
                                   page_number, max_page,
                                   show_ids,
                                   select_album_id, select_album_have_child,
                                   'album', 'art', artist_id, 'al')
