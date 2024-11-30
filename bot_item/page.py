from config.const import (MONTH_NAMES,
                          ARTISTS_PAGE_SIZE,
                          ALBUM_PAGE_SIZE,
                          ARTIST_PAGE_SIZE,
                          USERS_PAGE_SIZE,
                          IMG_NULL_FILE)
from config.bot import *
import time


async def __init_page(event: Union[Message, CallbackQuery]):
    if isinstance(event, CallbackQuery):
        await event.answer()


def __split_lyrics_into_page(lyrics: str, max_length: int = 900):
    fragments = ['\n'.join(group) for key, group in groupby(lyrics.split('\n'), lambda x: x == '') if not key]

    current_page = ''
    pages = []

    for fragment in fragments:
        if len(current_page) + len(fragment) + 2 > max_length:
            if current_page:
                pages.append(current_page)
            current_page = fragment
        else:
            if current_page:
                current_page += '\n\n' + fragment
            else:
                current_page = fragment

    if current_page:
        pages.append(current_page)

    return pages


def __format_date(date_str: str) -> str:
    if not date_str:
        return ''
    if date_str == 'None':
        return ''
    date = datetime.fromisoformat(date_str)
    return f"<i>Вышел {date.day} {MONTH_NAMES[date.month - 1]} {date.year} года</i>"


def __format_img_link(img_link: str, caption: str):
    if not img_link:
        return InputMediaPhoto(media=FSInputFile(IMG_LOGOS_FILE), caption=caption)
    else:
        return InputMediaPhoto(media='https://' + img_link.replace('%%', '800x800'), caption=caption)


def __make_page_counter(page_number: int, max_page_number: int) -> str:
    return f'\n<i>Страница {page_number} из {max_page_number}</i>'


def __calculate_page_number(quantity_items: int, page_size: int) -> int:
    return ceil(quantity_items / page_size)


def __calculate_relative_select_number(select_number: int, page_size: int) -> int:
    return (select_number - 1) % page_size


async def make_artists(event: Union[Message, CallbackQuery], select_vector: Tuple[int, int, int, int]):
    await __init_page(event)
    settings_items = settings.get_for_artists(event.from_user.id)

    relative_select_number = __calculate_relative_select_number(select_vector[0], ARTISTS_PAGE_SIZE)
    page_number = __calculate_page_number(select_vector[0], ARTISTS_PAGE_SIZE)
    page = artists.get_by_page(page_number, ARTISTS_PAGE_SIZE)

    quantity = artists.count()
    max_page_number = __calculate_page_number(quantity, ARTISTS_PAGE_SIZE)

    page_text = phrases['title']['artists']

    for i in range(ARTISTS_PAGE_SIZE):
        if i < len(page):
            artist_id, artist_title, take_song = page[i]
            if i == relative_select_number:
                page_text += settings_items['icon_select']
                page_text += ' '

            if take_song:
                page_text += settings_items['icon_songs']
            else:
                page_text += settings_items['icon_not_songs']
            page_text += ' '

            if settings_items['bool_show_ids']:
                page_text += f'<code>{artist_id.ljust(9)}</code>'

            if settings_items['bool_show_link']:
                page_text += f'<a href = "{make_yandex_artist_link(artist_id)}">'
            if i == relative_select_number:
                page_text += '<b>'
            page_text += artist_title
            if i == relative_select_number:
                page_text += '</b>'
            if settings_items['bool_show_link']:
                page_text += '</a>'
        page_text += '\n'

    if settings_items['bool_show_footnote']:
        page_text += '\n' + settings_items['icon_songs']
        page_text += phrases['footnote_songs']
        if settings_items['bool_show_ids']:
            page_text += phrases['footnote_ids_artists']
    page_text += __make_page_counter(page_number, max_page_number)

    page_kb = kb.make_artists(select_vector,
                              relative_select_number,
                              quantity,
                              page_number,
                              max_page_number,
                              settings.get_for_kb(event.from_user.id))

    if isinstance(event, Message):
        await event.answer(text=page_text, disable_web_page_preview=True, reply_markup=page_kb)
        return
    await event.message.edit_text(text=page_text, disable_web_page_preview=True, reply_markup=page_kb)


async def make_artist(event: Union[Message, CallbackQuery], select_vector: Tuple[int, int, int, int]):
    await __init_page(event)
    settings_items = settings.get_for_artist(event.from_user.id)

    artist_id, artist_title, _ = artists.get_by_select_number(select_vector[0] - 1)
    relative_select_number = __calculate_relative_select_number(select_vector[1], ARTIST_PAGE_SIZE)
    page_number = __calculate_page_number(select_vector[1], ARTIST_PAGE_SIZE)
    page = bonds.get_albums_by_artist_by_page(artist_id, page_number, ARTIST_PAGE_SIZE)

    quantity = bonds.count_albums_by_artist(artist_id)
    max_page_number = __calculate_page_number(quantity, ARTIST_PAGE_SIZE)

    page_text = phrases['title']['artist']
    if settings_items['bool_show_link']:
        page_text += f'<a href = "{make_yandex_artist_link(artist_id)}">'
    page_text += f'{artist_title}\n\n'
    if settings_items['bool_show_link']:
        page_text += '</a>'

    for i in range(ARTIST_PAGE_SIZE):
        if i < len(page):
            album_id, album_title, _, _ = page[i]

            if i == relative_select_number:
                page_text += settings_items['icon_select']
                page_text += ' '

            if settings_items['bool_show_ids']:
                page_text += f'<code>{album_id.ljust(9)}</code>'

            if settings_items['bool_show_link']:
                page_text += f'<a href = "{make_yandex_album_link(album_id)}">'
            if i == relative_select_number:
                page_text += f'<b>{album_title}</b>'
            else:
                page_text += f'{album_title}'
            if settings_items['bool_show_link']:
                page_text += '</a>'
        page_text += '\n'

    if settings_items['bool_show_ids'] and settings_items['bool_show_footnote']:
        page_text += phrases['footnote_ids_albums']

    page_text += __make_page_counter(page_number, max_page_number)

    page_kb = kb.make_artist(select_vector,
                             relative_select_number,
                             quantity,
                             page_number,
                             max_page_number,
                             settings.get_for_kb(event.from_user.id))

    if isinstance(event, Message):
        await event.answer(text=page_text, disable_web_page_preview=True, reply_markup=page_kb)
        return

    if event.message.photo:
        await event.message.answer(text=page_text, disable_web_page_preview=True, reply_markup=page_kb)
        await event.message.delete()
        return

    await event.message.edit_text(text=page_text, disable_web_page_preview=True, reply_markup=page_kb)


async def make_album(event: Union[Message, CallbackQuery], select_vector: Tuple[int, int, int, int]):
    await __init_page(event)
    settings_items = settings.get_for_album(event.from_user.id)

    artist_id, _, _ = artists.get_by_select_number(select_vector[0] - 1)
    album_id, album_title, album_img, album_date = bonds.get_albums_by_artist_select_number(artist_id, select_vector[1] - 1)
    album_artists_title = ', '.join(await get_artist_title_by_album_id(album_id))

    quantity = bonds.count_songs_by_album(album_id)
    max_page_number = __calculate_page_number(quantity, ALBUM_PAGE_SIZE)

    if select_vector[2] == -2:
        select_vector = [select_vector[0], select_vector[1], quantity, 1]

    if select_vector[2] == -1:
        select_vector = [select_vector[0], select_vector[1], ((max_page_number - 1) * ALBUM_PAGE_SIZE) + 1, 1]

    relative_select_number = __calculate_relative_select_number(select_vector[2], ALBUM_PAGE_SIZE)
    page_number = __calculate_page_number(select_vector[2], ALBUM_PAGE_SIZE)
    page = bonds.get_songs_by_album_by_page(album_id, page_number, ALBUM_PAGE_SIZE)

    page_text = ''
    if settings_items['bool_show_link']:
        page_text += f'<a href = "{make_yandex_album_link(album_id)}">'
    page_text += f'<b>{album_title}</b>\n'
    if settings_items['bool_show_link']:
        page_text += '</a>'
    page_text += f'{album_artists_title}\n'

    if settings_items['bool_show_date']:
        page_text += f'{__format_date(album_date)}\n'
    page_text += '\n'

    for i in range(ALBUM_PAGE_SIZE):
        if i < len(page):
            song_id, song_title, _, have_text, embedded = page[i]

            song_artists_title = ''
            if settings_items['bool_show_feat']:
                song_artists_title = ', '.join([artist for artist in await get_artist_title_by_song_id(song_id) if artist not in album_artists_title])

            if i == relative_select_number:
                page_text += settings_items['icon_select']
                page_text += ' '

            if have_text:
                if embedded:
                    page_text += settings_items['icon_embedded']
                else:
                    page_text += settings_items['icon_text']
            else:
                page_text += settings_items['icon_not_text']
            page_text += ' '

            if settings_items['bool_show_ids']:
                page_text += f'<code>{song_id.ljust(11)}</code>'

            if settings_items['bool_show_link']:
                page_text += f'<a href = "{make_yandex_song_link(song_id, album_id)}">'
            if i == relative_select_number:
                page_text += '<b>'

            page_text += song_title

            if settings_items['bool_show_feat'] and song_artists_title != '':
                page_text += f' — {song_artists_title}'

            if i == relative_select_number:
                page_text += '</b>'
            if settings_items['bool_show_link']:
                page_text += '</a>'
            page_text += '\n'

    if settings_items['bool_show_footnote']:
        page_text += '\n' + settings_items['icon_text']
        page_text += phrases['footnote_text']
        page_text += '\n' + settings_items['icon_embedded']
        page_text += phrases['footnote_embedded']
        if settings_items['bool_show_ids']:
            page_text += phrases['footnote_ids_songs']
    page_text += __make_page_counter(page_number, max_page_number)

    page_kb = kb.make_album(select_vector,
                            relative_select_number,
                            quantity,
                            page_number,
                            max_page_number,
                            bonds.count_albums_by_artist(artist_id),
                            settings.get_for_kb(event.from_user.id))

    if isinstance(event, Message):
        if settings_items['bool_show_img']:
            await event.answer_media(media=__format_img_link(album_img, page_text), reply_markup=page_kb)
            return
        await event.answer(text=page_text, reply_markup=page_kb)
        return

    if settings_items['bool_show_img']:
        await event.message.edit_media(media=__format_img_link(album_img, page_text), reply_markup=page_kb)
        return

    if event.message.photo or event.message.audio:
        await event.message.answer(text=page_text, disable_web_page_preview=True, reply_markup=page_kb)
        await event.message.delete()
        return

    await event.message.edit_text(text=page_text, disable_web_page_preview=True, reply_markup=page_kb)


async def make_song(event: Union[Message, CallbackQuery], select_vector: Tuple[int, int, int, int]):
    await __init_page(event)
    settings_items = settings.get_for_song(event.from_user.id)

    artist_id, _, _ = artists.get_by_select_number(select_vector[0] - 1)
    album_id, _, _, _ = bonds.get_albums_by_artist_select_number(artist_id, select_vector[1] - 1)
    song_id, song_title, _, have_text, embedded = bonds.get_songs_by_album_select_number(album_id, select_vector[2] - 1)
    artists_title = ', '.join(await get_artist_title_by_song_id(song_id))
    song = await download_song(artist_id, album_id, song_id, time.time())

    lyrics = phrases['error']['empty_lyrics']
    if have_text:
        lyrics = await get_song_lyrics(song_id)

    pages = __split_lyrics_into_page(lyrics)
    page = pages[select_vector[3] - 1]
    max_page_number = len(pages)

    page_text = ''
    if embedded:
        page_text += settings_items['icon_embedded'] + ' '

    if settings_items['bool_show_link']:
        page_text += f'<a href = "{make_yandex_song_link(song_id, album_id)}">'
    page_text += f'<b>{song_title}</b>\n'
    if settings_items['bool_show_link']:
        page_text += '</a>'
    page_text += f'{artists_title}\n\n'

    page_text += page
    page_text += '\n'

    if embedded and settings_items['bool_show_footnote']:
        page_text += phrases['footnote_embedded']
    page_text += __make_page_counter(select_vector[3], max_page_number)

    page_kb = kb.make_song(select_vector,
                           max_page_number,
                           settings.get_for_kb(event.from_user.id))

    if isinstance(event, Message):
        if settings_items['bool_show_song']:
            await event.answer_media(
                media=InputMediaAudio(media=FSInputFile(song, filename=f'{artists_title} - {song_title}'),
                                      caption=page_text), reply_markup=page_kb)
            return
        await event.answer(text=page_text, reply_markup=page_kb)
        return

    if settings_items['bool_show_song']:
        await event.message.edit_media(
            media=InputMediaAudio(media=FSInputFile(song, filename=f'{artists_title} - {song_title}'),
                                  caption=page_text), reply_markup=page_kb)
        return

    if event.message.photo or event.message.audio:
        await event.message.answer(text=page_text, disable_web_page_preview=True, reply_markup=page_kb)
        await event.message.delete()
        return

    await event.message.edit_text(text=page_text, disable_web_page_preview=True, reply_markup=page_kb)


async def make_users(event: Union[Message, CallbackQuery], select_number: int):
    await __init_page(event)

    page = users.get_by_page(select_number, USERS_PAGE_SIZE)
    max_page_number = __calculate_page_number(users.count(), USERS_PAGE_SIZE)
    page_text = phrases['title']['users']

    for i in range(USERS_PAGE_SIZE):
        if i < len(page):
            user_id, username, status = page[i]
            page_text += f'<code>{str(user_id).ljust(12)}</code>'

            if status == 1:
                page_text += f'{phrases["icon_admin"]}<b>@{username}</b>'
            elif status == -1:
                page_text += f'<s>@{username}</s>'
            elif status == -2:
                page_text += f'<tg-spoiler>@{username}</tg-spoiler>'
            else:
                page_text += f'@{username}'
        page_text += '\n'

    page_text += __make_page_counter(select_number, max_page_number)

    page_kb = kb.make_users(select_number,
                            max_page_number,
                            settings.get_for_kb(event.from_user.id))

    if isinstance(event, Message):
        await event.answer(
            text=page_text,
            reply_markup=page_kb)
    else:
        await event.message.edit_text(
            text=page_text,
            reply_markup=page_kb)


async def make_settings(event: Union[Message, CallbackQuery]):
    await __init_page(event)
    settings_items = settings.get(event.from_user.id)

    page_text = phrases['title']['settings']
    page_text += phrases['title']['settings_icon']
    for name, value in settings_items.items():
        if str(name).startswith('icon_'):
            page_text += f'{value} '
            page_text += phrases['settings']['description'][name]

    page_text += phrases['title']['settings_bool']
    for name, value in settings_items.items():
        if str(name).startswith('bool_'):
            if value:
                page_text += phrases['icon_choice']
            else:
                page_text += phrases['icon_not_choice']
            page_text += phrases['settings']['description'][name]

    page_text += phrases['title']['settings_presets']
    for i, preset in enumerate(phrases['settings']['presets']):
        page_text += f'{i + 1}. ' + phrases['settings']['presets'][preset]['title'] + '\n'

    page_kb = kb.make_settings(settings_items)

    if isinstance(event, Message):
        await event.answer(text=page_text, reply_markup=page_kb)
        return
    await event.message.edit_text(text=page_text, reply_markup=page_kb)
