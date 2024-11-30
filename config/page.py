from config.bot import *
from config.const import (MONTH_NAMES, IMG_NULL_FILE)
from datetime import datetime


async def init_page(event: Union[Message, CallbackQuery]):
    if isinstance(event, CallbackQuery):
        await event.answer()


def split_lyrics_into_page(lyrics: str, max_length: int = 900):
    fragments = ['\n'.join(group) for key, group in groupby(lyrics.split('\n'), lambda x: x == '') if not key]

    current_page = ''
    pages = []

    for fragment in fragments:
        if len(current_page) + len(fragment) + 2 > max_length:
            if current_page:
                pages.append(current_page)
            current_page = fragment
        else:
            if current_page:
                current_page += '\n\n' + fragment
            else:
                current_page = fragment

    if current_page:
        pages.append(current_page)

    return pages


def format_date(date_str: str) -> str:
    if not date_str:
        return ''
    if date_str == 'None':
        return ''
    date = datetime.fromisoformat(date_str)
    return f"<i>Вышел {date.day} {MONTH_NAMES[date.month - 1]} {date.year} года</i>"


def format_img_link(img_link: str, caption: str):
    if not img_link:
        return InputMediaPhoto(media=FSInputFile(IMG_NULL_FILE), caption=caption)
    else:
        return InputMediaPhoto(media='https://' + img_link.replace('%%', '800x800'), caption=caption)


def format_song_link(song: str, artists_title: str, song_title: str):
    return FSInputFile(song, filename=f'{artists_title} - {song_title}')


def make_page_counter(page_number: int, max_page_number: int) -> str:
    return f'\n<i>Страница {page_number} из {max_page_number}</i>'


def calculate_page_number(quantity_items: int, page_size: int) -> int:
    return ceil(quantity_items / page_size)


def calculate_relative_select_number(select_number: int, page_size: int) -> int:
    return (select_number - 1) % page_size
