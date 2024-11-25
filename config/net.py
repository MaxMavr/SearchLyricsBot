import asyncio
import aiohttp
import requests
import re
import random
import string

from json import dumps, loads
from bs4 import BeautifulSoup as bs
from yandex_music import ClientAsync
from typing import Union, Tuple, Generator, Optional


