from os.path  import dirname, isfile
from os       import listdir, remove, makedirs, getenv
from re       import search
from math     import ceil
from typing   import Union, List, Tuple, Callable, Coroutine
from datetime import datetime
from random import randint
from itertools import groupby

import asyncio
import aiogram
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaAudio


from config.secret_const import TELEGRAM_BOT_TOKEN as __TELEGRAM_BOT_TOKEN
from config.const import MAIN_ADMIN_ID, CHANNEL_ID, YANDEX_LINK_PATTERN, YANDEX_SONG_ID_PATTERN, LINK_PATTERN

import db_interface.users as users
import db_interface.artists as artists
import db_interface.albums as albums
import db_interface.songs as songs
import db_interface.bonds as bonds

import bot_item.keyboards as kb
from bot_item.keyboards import decoding_page_callback
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


async def sent_from_list(message: Message, keyword: str):
    await message.answer(
        phrases[keyword][randint(0, len(phrases[keyword]) - 1)])


async def get_cmd_args(message: Message) -> list:
    args = message.text.split()[1:]
    if len(args) == 0:
        await message.answer(phrases['err_empty_argument'], reply_markup=kb.main)
        return [None]
    return args


async def get_cmd_args_by_newline(message: Message) -> list:
    args = message.text.split('\n')[1:]
    if len(args) == 0:
        await message.answer(phrases['err_empty_newline_argument'], reply_markup=kb.main)
        return [None]
    return args


async def get_cmd_digit(message: Message) -> int:
    digit = (await get_cmd_args(message))[0]

    if not digit:
        return -1

    if not digit.isdigit():
        await message.answer(phrases['err_not_digit'], reply_markup=kb.main)
        return -1

    return int(digit)


async def get_cmd_user_id(message: Message) -> int:
    user_id = await get_cmd_digit(message)

    if user_id == -1:
        return -1

    if not users.is_exists(user_id):
        await message.answer(phrases['err_user_not_exist'], reply_markup=kb.main)
        return -1

    return user_id


async def get_cmd_artist_id(message: Message) -> str:
    artist_id = (await get_cmd_args(message))[0]

    if not artist_id:
        return ''

    if not artists.is_exists(artist_id):
        await message.answer(phrases['err_artist_not_exist'], reply_markup=kb.main)
        return ''

    return artist_id


async def get_cmd_album_id(message: Message) -> str:
    album_id = (await get_cmd_args(message))[0]

    if not album_id:
        return ''

    if not albums.is_exists(album_id):
        await message.answer(phrases['err_album_not_exist'], reply_markup=kb.main)
        return ''

    return album_id


async def get_cmd_song_id(message: Message) -> str:
    song_id = (await get_cmd_args(message))[0]

    if not song_id:
        return ''

    if not songs.is_exists(song_id):
        await message.answer(phrases['err_song_not_exist'], reply_markup=kb.main)
        return ''

    return song_id


async def get_cmd_id_from_yandex_link(message: Message) -> tuple:
    link = (await get_cmd_args(message))[0]

    if not await is_link(link):
        await message.answer(phrases['err_is_not_link'], reply_markup=kb.main)
        return None, None

    if not await is_yandex_link(link):
        await message.answer(phrases['err_is_not_yandex_link'], reply_markup=kb.main)
        return None, None

    album_id, _, song_id = link.split('/')[-3:]

    return album_id, song_id


async def is_yandex_link(link: str) -> bool:
    return bool(search(YANDEX_LINK_PATTERN, link))


async def is_link(link: str) -> bool:
    return link.startswith(LINK_PATTERN)
