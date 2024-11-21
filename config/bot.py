from os.path  import dirname, isfile
from os       import listdir, remove, makedirs, getenv
from re       import findall, DOTALL
from math     import ceil
from typing   import Union, List, Tuple
from datetime import datetime
from random import randint

import asyncio
import aiogram
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.types import Message, CallbackQuery

from config.secret_const import TELEGRAM_BOT_TOKEN as __TELEGRAM_BOT_TOKEN
from config.secret_const import MAIN_ADMIN_ID

import db_interface.users as users
import db_interface.artists as artists
import db_interface.albums as albums
import db_interface.songs as songs
import db_interface.bonds as bonds

import bot_item.keyboards as kb
from config.phrases import phrases

try:
    bot: Bot = Bot(token=__TELEGRAM_BOT_TOKEN, parse_mode='HTML')
except Exception:
    from aiogram.client.default import DefaultBotProperties
    bot: Bot = Bot(token=__TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))


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


async def sent_to_banned(message: Message):
    await message.answer(
        phrases["ban"][randint(0, len(phrases["ban"]) - 1)])


async def get_cmd_args(message: Message) -> list:
    return message.text.split()[1:] or [None]


async def get_cmd_digit(message: Message) -> int:
    digit = await get_cmd_args(message)

    digit = digit[0]

    if digit is None:
        await message.answer(phrases['err_empty_argument'])
        return -1

    if not digit.isdigit():
        await message.answer(phrases['err_not_digit'])
        return -1

    return int(digit)


async def get_cmd_user_id(message: Message) -> int:
    user_id = await get_cmd_digit(message)

    if user_id == -1:
        return -1

    if not users.is_exists(user_id):
        await message.answer(phrases['err_user_not_exist'])
        return -1

    return user_id


async def get_cmd_artist_id(message: Message) -> str:
    artist_id = await get_cmd_args(message)
    artist_id = artist_id[0]

    if artist_id is None:
        await message.answer(phrases['err_empty_argument'])
        return ''

    if not artists.is_exists(artist_id):
        await message.answer(phrases['err_artist_not_exist'])
        return ''

    return artist_id


async def get_cmd_album_id(message: Message) -> str:
    album_id = await get_cmd_args(message)
    album_id = album_id[0]

    if album_id is None:
        await message.answer(phrases['err_empty_argument'])
        return ''

    if not albums.is_exists(album_id):
        await message.answer(phrases['err_album_not_exist'])
        return ''

    return album_id


async def get_cmd_song_id(message: Message) -> str:
    song_id = await get_cmd_args(message)
    song_id = song_id[0]

    if song_id is None:
        await message.answer(phrases['err_empty_argument'])
        return ''

    if not songs.is_exists(song_id):
        await message.answer(phrases['err_song_not_exist'])
        return ''

    return song_id




