from os.path   import dirname, isfile
from os        import listdir, remove
from re        import search, findall
from re        import compile as comp
from math      import ceil
from typing    import Union, List, Tuple, Callable, Coroutine
from random    import randint
from itertools import groupby

import asyncio
import aiogram
from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaAudio, FSInputFile
from aiogram.fsm.context import FSMContext


from config.secret_const import TELEGRAM_BOT_TOKEN as __TELEGRAM_BOT_TOKEN
from config.const import (MAIN_ADMIN_ID,
                          CHANNEL_ID,
                          YANDEX_LINK_PATTERN,
                          YANDEX_SONG_ID_PATTERN,
                          LINK_PATTERN,
                          IMG_LOGOS_FILE,
                          TEMP_DIR,
                          MAX_SEARCH_NUMBER)

import db_interface.users as users
import db_interface.settings as settings

import db_interface.artists as artists
import db_interface.albums as albums
import db_interface.songs as songs
import db_interface.bonds as bonds

import bot_item.keyboards as kb
import config.ids as ids

from bot_item.keyboards import decoding_page_callback
from api.lyrics_search import get_line_by_id
from api.music_yandex import (get_day_song,
                              get_song_artist_title_by_song_id,
                              get_artist_title_by_album_id,
                              get_artist_title_by_song_id,
                              download_song,
                              get_song_lyrics)
from bot_item.make_message import *
from config.phrases import phrases


try:
    bot: Bot = Bot(token=__TELEGRAM_BOT_TOKEN, parse_mode='HTML')
except Exception:
    from aiogram.client.default import DefaultBotProperties
    bot: Bot = Bot(token=__TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))


class Settings(StatesGroup):
    icon = State()
    allicon = State()


async def get_editors():
    return [editor.user.id
            for editor in
            (await bot.get_chat_administrators(chat_id=CHANNEL_ID))
            if not editor.user.is_bot]


class IsEditor(BaseFilter):
    @staticmethod
    async def check(user_id) -> bool:
        return user_id in (await get_editors())

    async def __call__(self, message: Message) -> bool:
        return await self.check(message.from_user.id)


class IsNotAdmitted(BaseFilter):
    @staticmethod
    async def check(user_id: int) -> bool:
        return not users.is_admitted(user_id)

    async def __call__(self, message: Message) -> bool:
        return await self.check(message.from_user.id)


class IsBaned(BaseFilter):
    @staticmethod
    async def check(user_id: int) -> bool:
        return users.is_baned(user_id)

    async def __call__(self, message: Message) -> bool:
        return await self.check(message.from_user.id)


class IsAdmin(BaseFilter):
    @staticmethod
    async def check(user_id: int) -> bool:
        return users.is_admin(user_id) or await IsSuperAdmin.check(user_id)

    async def __call__(self, message: Message) -> bool:
        if message.chat.type != 'private':
            return False
        return await self.check(message.from_user.id)


class IsSuperAdmin(BaseFilter):
    @staticmethod
    async def check(user_id) -> bool:
        return user_id == MAIN_ADMIN_ID

    async def __call__(self, message: Message) -> bool:
        if message.chat.type != 'private':
            return False
        return await self.check(message.from_user.id)


async def sent_from_list(message: Message, keyword: str, keyboard=None):
    if keyboard:
        await message.answer(phrases[keyword][randint(0, len(phrases[keyword]) - 1)], reply_markup=keyboard)
        return
    await message.answer(phrases[keyword][randint(0, len(phrases[keyword]) - 1)], reply_markup=kb.main)


def command_with_arguments(func):
    async def wrapper(message: Message):
        args = message.text.split()[1:]
        if len(args) == 0:
            await message.answer(phrases['error']['empty_argument'], reply_markup=kb.main)
            return
        await func(message, args)
    return wrapper


def command_with_arguments_by_newline(func):
    async def wrapper(message: Message):
        args = message.text.split('\n')[1:]
        if len(args) == 0:
            await message.answer(phrases['error']['empty_newline_argument'], reply_markup=kb.main)
            return
        await func(message, args)
    return wrapper


def command_with_digit_argument(func):
    @command_with_arguments
    async def wrapper(message: Message, args):
        digit = args[0]
        if not digit.isdigit():
            await message.answer(phrases['error']['not_digit'], reply_markup=kb.main)
            return
        await func(message, digit)
    return wrapper


def command_with_user_id_argument(func):
    @command_with_digit_argument
    async def wrapper(message: Message, user_id):
        if not users.is_exists(user_id):
            await message.answer(phrases['error']['user_not_exist'], reply_markup=kb.main)
            return
        await func(message, user_id)
    return wrapper


def command_with_artist_id_argument(func):
    @command_with_arguments
    async def wrapper(message: Message, args):
        artist_id = args[0]
        if len(artist_id) > 3:
            await message.answer(phrases['error']['long_argument_3'], reply_markup=kb.main)
            return
        artist_id = ids.decoding(artist_id)
        if len(artist_id) < 1:
            await message.answer(phrases['error']['artist_not_exist'], reply_markup=kb.main)
            return
        if artist_id[0] > artists.count():
            await message.answer(phrases['error']['artist_not_exist'], reply_markup=kb.main)
            return
        await func(message, artist_id[:1])
    return wrapper


def command_with_album_id_argument(func):
    @command_with_arguments
    async def wrapper(message: Message, args):
        album_id = args[0]
        if len(album_id) > 6:
            await message.answer(phrases['error']['long_argument_6'], reply_markup=kb.main)
            return
        album_id = ids.decoding(album_id)
        if len(album_id) < 2:
            await message.answer(phrases['error']['album_not_exist'], reply_markup=kb.main)
            return
        if album_id[0] > artists.count() or album_id[1] > albums.count():
            await message.answer(phrases['error']['album_not_exist'], reply_markup=kb.main)
            return
        await func(message, album_id[:2])
    return wrapper


def command_with_song_id_argument(func):
    @command_with_arguments
    async def wrapper(message: Message, args):
        song_id = args[0]
        if len(song_id) > 9:
            await message.answer(phrases['error']['long_argument_9'], reply_markup=kb.main)
            return
        song_id = ids.decoding(song_id)
        if len(song_id) < 3:
            await message.answer(phrases['error']['song_not_exist'], reply_markup=kb.main)
            return
        if song_id[0] > artists.count() or song_id[1] > albums.count() or song_id[2] > songs.count():
            await message.answer(phrases['error']['song_not_exist'], reply_markup=kb.main)
            return
        await func(message, song_id[:3])
    return wrapper


async def is_yandex_link(link: str) -> bool:
    return bool(search(YANDEX_LINK_PATTERN, link))


async def is_link(link: str) -> bool:
    return link.startswith(LINK_PATTERN)
