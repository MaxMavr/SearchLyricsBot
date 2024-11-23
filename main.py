# TODO: Переписать "сlustering_vectors" и "encoding_lyrics" на C++
#  Команды:
#  Отправка шаблона "pattern.xml"
#  Команда для добавления файла в неотсортированное (/DB/Unprocessed) (Проверка, что файл — json)
#  Команда для запуска сортировки и составления таблиц из неотсортированного clear_unprocessed()
#  Команда для запуска пересчёта кластеров ///
#  Команда вывода количества слов во всей базе данных (вводишь "я" -> ответ 173)
#  Команда вывода количества слов в альбоме или песне (вводишь "я" -> ответ 173)

from config.bot import *

from bot_item.handlers.default import rt as default
from bot_item.handlers.admin import rt as admin
from bot_item.handlers.search import rt as search
from bot_item.handlers.channel import rt as channel


async def main():
    dp: Dispatcher = Dispatcher()
    dp.include_router(default)
    dp.include_router(admin)
    dp.include_router(search)
    dp.include_router(channel)
    # dp.include_router(fill_preset)
    # dp.include_router(catch_bug)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print("Тексты, тексты и их тексты")
    asyncio.run(main())
