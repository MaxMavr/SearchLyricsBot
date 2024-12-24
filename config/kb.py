from config.phrases import phrases

from aiogram.utils.keyboard import ReplyKeyboardMarkup as KMarkup
from aiogram.utils.keyboard import KeyboardButton as KButton
from aiogram.utils.keyboard import InlineKeyboardMarkup as IMarkup
from aiogram.utils.keyboard import InlineKeyboardButton as IButton
from aiogram.utils.keyboard import InlineKeyboardBuilder as IBuilder

from typing import List, Tuple


suffixes2suffixes_text = {
    'A': 'artist',
    'a': 'album',
    'l': 'song',
    's': 'text'
}
suffixes_direction = ['A', 'a', 'l', 's']
NULL_BUTTON = IButton(text=phrases['icon_empty'], callback_data='pass')


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


def __make_button(text: str = None, data: str = None):
    if not text and not data:
        return NULL_BUTTON
    return IButton(text=text, callback_data=data)


def __make_page_callback_data(suffix: str, select_vector: List[int]):
    return f'pageSI_{suffix}_{select_vector[0]}_{select_vector[1]}_{select_vector[2]}_{select_vector[3]}'


def decoding_page_callback(callback_data: str) -> list:
    callback_data_list = callback_data.split('_')
    type_data = callback_data_list[1]
    select_artist = int(callback_data_list[2])
    select_album = int(callback_data_list[3])
    select_song = int(callback_data_list[4])
    select_lyrics = int(callback_data_list[5])
    return [type_data, [select_artist, select_album, select_song, select_lyrics]]


def __make_past_item_button(select_vector: List[int], suffix: Suffix, icons: dict):
    if select_vector[suffix.index] > 1:
        modify_select_vector = select_vector.copy()
        modify_select_vector[suffix.index] -= 1
        if suffix.index >= len(select_vector):
            modify_select_vector[suffix.index + 1] = 1
        return __make_button(icons['icon_up'] + phrases['button'][suffix.text]['past'],
                             __make_page_callback_data(suffix.current, modify_select_vector))
    return NULL_BUTTON


def __make_next_item_button(select_vector: List[int], suffix: Suffix, icons: dict, max_select: int):
    if select_vector[suffix.index] < max_select:
        modify_select_vector = select_vector.copy()
        modify_select_vector[suffix.index] += 1
        if suffix.index >= len(select_vector):
            modify_select_vector[suffix.index + 1] = 1
        return __make_button(icons['icon_down'] + phrases['button'][suffix.text]['next'],
                             __make_page_callback_data(suffix.current, modify_select_vector))
    return NULL_BUTTON


def __make_past_page_button(select_vector: List[int], suffix: Suffix, icons: dict,
                            page_number: int, relative_select_number: int, page_size: int):
    if page_number > 1:
        modify_select_vector = select_vector.copy()
        modify_select_vector[suffix.index] -= (relative_select_number + page_size)
        if suffix.index >= len(select_vector):
            modify_select_vector[suffix.index + 1] = 1
        return __make_button(icons['icon_past_page'] + phrases['button']['past_page'],
                             __make_page_callback_data(suffix.current, modify_select_vector))
    return NULL_BUTTON


def __make_next_page_button(select_vector: List[int], suffix: Suffix, icons: dict,
                            page_number: int, relative_select_number: int, page_size: int, max_page: int):
    if page_number < max_page:
        modify_select_vector = select_vector.copy()
        modify_select_vector[suffix.index] -= (relative_select_number - page_size)
        if suffix.index >= len(select_vector):
            modify_select_vector[suffix.index + 1] = 1
        return __make_button(phrases['button']['next_page'] + icons['icon_next_page'],
                             __make_page_callback_data(suffix.current, modify_select_vector))
    return NULL_BUTTON


def __make_child_button(select_vector: List[int], suffix: Suffix, icons: dict):
    if suffix.child != '':
        return __make_button(phrases['button'][suffix.text]['child'] + icons['icon_child'],
                             __make_page_callback_data(suffix.child, select_vector))
    return NULL_BUTTON


def __make_parent_button(select_vector: List[int], suffix: Suffix, icons: dict):
    if suffix.parent != '':
        return __make_button(icons['icon_parent'] + phrases['button'][suffix.text]['parent'],
                             __make_page_callback_data(suffix.parent, select_vector))
    return NULL_BUTTON


def __make_analytics_button(song_id: str, icons: dict):
    return IMarkup(inline_keyboard=[[IButton(text=icons['icon_parent'] + phrases['button']['show_analytics'],
                                             callback_data=f'anal_{song_id}')]])
