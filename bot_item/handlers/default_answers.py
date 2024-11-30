from config.bot import *
rt: Router = Router()


@rt.message(F.content_type.in_({ContentType.TEXT,
                                ContentType.PHOTO,
                                ContentType.AUDIO,
                                ContentType.VOICE,
                                ContentType.VIDEO,
                                ContentType.DOCUMENT,
                                ContentType.VIDEO_NOTE}))
async def cmd_start(message: Message):
    await sent_from_list(message, 'default_answers', kb.main)
