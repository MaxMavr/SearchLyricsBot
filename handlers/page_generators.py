# TODO:
#  Файл для создания стрелочек

from config.const import MONTH_NAMES
from config.bot import datetime


def __format_date(date_str: str) -> str:
    if not date_str:
        return ''
    date_object = datetime.fromisoformat(date_str)
    return f"<i>вышел {date_object.day} {MONTH_NAMES[date_object.month - 1]} {date_object.year} года</i>"
