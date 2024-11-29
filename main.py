from config.bot import *

from bot_item.handlers.default import rt as default
from bot_item.handlers.settings import rt as setting
from bot_item.handlers.admin import rt as admin
from bot_item.handlers.search import rt as search
from bot_item.handlers.channel import rt as channel


async def main():
    dp: Dispatcher = Dispatcher()
    dp.include_router(default)
    dp.include_router(setting)
    dp.include_router(admin)
    dp.include_router(search)
    dp.include_router(channel)
    # dp.include_router(fill_preset)
    # dp.include_router(default_answers)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print("Тексты, тексты и их тексты")
    asyncio.run(main())
