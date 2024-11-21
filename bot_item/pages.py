# TODO:
#  Файл для создания стрелочек

from config.const import (MONTH_NAMES,
                          ARTISTS_PAGE_SIZE,
                          SONGS_PAGE_SIZE,
                          ALBUMS_PAGE_SIZE,
                          USERS_PAGE_SIZE)
from config.bot import *


def __format_date(date_str: str) -> str:
    if not date_str:
        return ''
    date = datetime.fromisoformat(date_str)
    return f"<i>Вышел {date.day} {MONTH_NAMES[date.month - 1]} {date.year} года</i>"


def __make_page_counter(page_number: int, max_page_number: int) -> str:
    if max_page_number <= 1:
        return ''
    return f'\n<i>Страница {page_number} из {max_page_number}</i>'


def __calculate_page(quantity_items: int, page_size: int) -> int:
    return ceil(quantity_items / page_size)


async def __init_page(event: Union[Message, CallbackQuery]):
    if isinstance(event, CallbackQuery):
        await event.answer()


async def __update_page(event: Union[Message, CallbackQuery],
                        page_text: str, page_keyboard):
    if isinstance(event, CallbackQuery):
        await bot.edit_message_text(
            chat_id=event.message.chat.id,
            message_id=event.message.message_id,
            text=page_text,
            reply_markup=page_keyboard)
    else:
        await event.answer(page_text, reply_markup=page_keyboard)


async def make_artists_page(event: Union[Message, CallbackQuery],
                            select_number: int,
                            show_ids: bool = False):
    await __init_page(event)

    relative_select_number = (select_number - 1) % ARTISTS_PAGE_SIZE

    page_number = __calculate_page(select_number, ARTISTS_PAGE_SIZE)
    page = artists.get_by_page(page_number, ARTISTS_PAGE_SIZE)

    quantity_artists = artists.count()
    max_page_number = __calculate_page(quantity_artists, ARTISTS_PAGE_SIZE)

    page_text = phrases['title_artists']

    for i in range(ARTISTS_PAGE_SIZE):
        if i < len(page):
            artist_id, artist_title, take_song = page[i]
            if i == relative_select_number:
                page_text += phrases['icon_select']
            if take_song:
                page_text += phrases['icon_text']
            if show_ids:
                page_text += f'<code>{artist_id.ljust(9)}</code>'

            if i == relative_select_number:
                page_text += f'<b>{artist_title}</b>'
            else:
                page_text += f'{artist_title}'
        page_text += '\n'

    if show_ids:
        page_text += phrases['footnote_ids_artists']

    page_text += phrases['footnote_text']
    page_text += __make_page_counter(page_number, max_page_number)

    page_kb = kb.make_artists(select_number,
                              quantity_artists,
                              page_number,
                              max_page_number,
                              show_ids,
                              page[relative_select_number][0],
                              page[relative_select_number][2])

    await __update_page(event, page_text, page_kb)


async def make_artist_page(event: Union[Message, CallbackQuery],
                           artist_id: str,
                           select_number: int,
                           show_ids: bool = False):
    await __init_page(event)

    relative_select_number = (select_number - 1) % ALBUMS_PAGE_SIZE

    page_number = __calculate_page(select_number, ALBUMS_PAGE_SIZE)
    page = bonds.get_albums_by_artist_by_page(artist_id, page_number, ALBUMS_PAGE_SIZE)

    quantity_album = bonds.count_albums_by_artist(artist_id)
    max_page_number = __calculate_page(quantity_album, ALBUMS_PAGE_SIZE)

    page_text = phrases['title_album']
    page_text += f'{artists.get_title(artist_id)}\n\n'

    for i in range(ALBUMS_PAGE_SIZE):
        if i < len(page):
            album_id, album_title, _, _ = page[i]
            if i == relative_select_number:
                page_text += phrases['icon_select']
            if show_ids:
                page_text += f'<code>{album_id.ljust(9)}</code>'
            if i == relative_select_number:
                page_text += f'<b>{album_title}</b>'
            else:
                page_text += f'{album_title}'
        page_text += '\n'

    if show_ids:
        page_text += phrases['footnote_ids_albums']

    page_text += __make_page_counter(page_number, max_page_number)

    page_kb = kb.make_artist(select_number,
                             quantity_album,
                             page_number,
                             max_page_number,
                             show_ids,
                             page[relative_select_number][0],
                             page[relative_select_number][2],
                             artist_id)

    await __update_page(event, page_text, page_kb)

