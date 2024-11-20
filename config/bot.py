from os.path  import dirname, isfile
from os       import listdir, remove, makedirs, getenv
from re       import findall, DOTALL
from math     import sqrt
from typing   import Union, List, Tuple
from datetime import datetime


import asyncio
import aiogram
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.types import Message, CallbackQuery

from config.secret_const import TELEGRAM_BOT_TOKEN as __TELEGRAM_BOT_TOKEN

try:
    bot: Bot = Bot(token=__TELEGRAM_BOT_TOKEN, parse_mode='HTML')
except Exception:
    from aiogram.client.default import DefaultBotProperties
    bot: Bot = Bot(token=__TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

