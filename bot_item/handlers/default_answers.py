from config.bot import *
rt: Router = Router()


@rt.message()
async def cmd_start(message: Message):
    await sent_from_list(message, 'default_answers', kb.main)
