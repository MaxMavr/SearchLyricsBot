from config.net import *
from config.const import (YANDEX_TOKEN,
                          YNISON_DEVICE_INFO,
                          YNISON_GRY_MAIN_URL,
                          YNISON_PYS_MAIN_URL,
                          TEMP_DIR)

from db_interface.files import (read_day_song,
                                upd_day_song)


__client = ClientAsync(YANDEX_TOKEN)


async def get_song_lyrics(song_id) -> Union[str, None]:
    song = (await __client.tracks(song_id))[0]
    if song.lyrics_info.has_available_text_lyrics:
        return await (await song.get_lyrics_async()).fetch_lyrics_async()
    else:
        return None


async def get_album_songs(album_id):
    response = await __client.albums_with_tracks(album_id)

    for volume in response.volumes:
        for song in volume:
            song_id = str(song.id)
            title = song.title
            artists_id = [(str(artist.id), artist.name) for artist in song.artists]

            have_lyrics = song.lyrics_info.has_available_text_lyrics

            yield song_id, title, artists_id, have_lyrics


async def get_artist_albums(artist_id):
    page = 0
    response = await __client.artists_direct_albums(artist_id, page=page)

    while len(response.albums) != 0:
        for album in response.albums:
            yield str(album.id), album.title, album.cover_uri, str(album.release_date)

        page += 1
        response = await __client.artists_direct_albums(artist_id, page=page)


async def get_song_artist_title_by_song_id(song_id: str) -> Tuple[str, str]:
    song = (await __client.tracks(song_id))[0]
    return song.title, ', '.join([artist.name for artist in song.artists])


async def get_artist_title_by_song_id(song_id: str) -> list:
    song = (await __client.tracks(song_id))[0]
    return [artist.name for artist in song.artists]


async def get_artist_title_by_album_id(album_id: str) -> list:
    album = (await __client.albums(album_id))[0]
    return [artist.name for artist in album.artists]


async def search_artist_id(artist_title: str) -> Tuple[str, str]:
    search_result = await __client.search(artist_title)

    if search_result.best.type == 'artist':
        if search_result.best.result.name.lower() == artist_title.lower():
            return str(search_result.best.result.id), search_result.best.result.name
    return '', ''


async def download_song(artist_title: str, album_id: str, song_id: str, x_factor) -> str:
    song = (await __client.tracks(song_id))[0]
    save_path = TEMP_DIR + f'{artist_title}-{album_id}-{song_id}-{x_factor}.mp3'
    await song.download_async(save_path)
    return save_path


async def get_day_song() -> Optional[Tuple[str, str, str, str]]:
    song = await song_from_ynison()

    if not song[0]:
        return read_day_song()

    upd_day_song(list(song))
    return song


def __create_request_payload(web_socket_proto):
    return {
        "update_full_state": {
            "player_state": {
                "player_queue": {
                    "current_playable_index": -1,
                    "entity_id": "",
                    "entity_type": "VARIOUS",
                    "playable_list": [],
                    "options": {"repeat_mode": "NONE"},
                    "entity_context": "BASED_ON_ENTITY_BY_DEFAULT",
                    "version": {
                        "device_id": web_socket_proto["Ynison-Device-Id"],
                        "version": 9021243204784341000,
                        "timestamp_ms": 0
                    },
                    "from_optional": ""
                },
                "status": {
                    "duration_ms": 0,
                    "paused": True,
                    "playback_speed": 1,
                    "progress_ms": 0,
                    "version": {
                        "device_id": web_socket_proto["Ynison-Device-Id"],
                        "version": 8321822175199937000,
                        "timestamp_ms": 0
                    }
                }
            },
            "device": {
                "capabilities": {
                    "can_be_player": True,
                    "can_be_remote_controller": False,
                    "volume_granularity": 16
                },
                "info": {
                    "device_id": web_socket_proto["Ynison-Device-Id"],
                    "type": "WEB",
                    "title": "Chrome Browser",
                    "app_name": "Chrome"
                },
                "volume_info": {"volume": 0},
                "is_shadow": True
            },
            "is_currently_active": False
        },
        "rid": "ac281c26-a047-4419-ad00-e4fbfda1cba3",
        "player_action_timestamp_ms": 0,
        "activity_interception_type": "DO_NOT_INTERCEPT_BY_DEFAULT"}


def __create_request_headers(web_socket_proto):
    return {
        "Sec-WebSocket-Protocol": f"Bearer, v2, {dumps(web_socket_proto)}",
        "Origin": "http://music.yandex.ru",
        "Authorization": f"OAuth {YANDEX_TOKEN}",
    }


async def __get_pre_ynison(session):
    web_socket_proto = {
        "Ynison-Device-Id": "".join([random.choice(string.ascii_lowercase) for _ in range(16)]),
        "Ynison-Device-Info": dumps(YNISON_DEVICE_INFO)
    }

    async with session.ws_connect(url=YNISON_GRY_MAIN_URL,
                                  headers=__create_request_headers(web_socket_proto)) as ws:

        recv = await ws.receive()
        data = loads(recv.data)

        new_web_socket_proto = web_socket_proto.copy()
        new_web_socket_proto["Ynison-Redirect-Ticket"] = data["redirect_ticket"]

        return __create_request_payload(web_socket_proto), data['host'], new_web_socket_proto


async def __fetch_ynison(session):
    request_payload, host, proto = await __get_pre_ynison(session)
    async with session.ws_connect(
            url=YNISON_PYS_MAIN_URL.replace('%%', str(host)),
            headers=__create_request_headers(proto),
            method="GET"
    ) as ws:

        await ws.send_str(dumps(request_payload))
        recv = await ws.receive()
        return loads(recv.data)


async def song_from_ynison():
    try:
        async with aiohttp.ClientSession() as session:
            ynison = await __fetch_ynison(session)
            track = ynison['player_state']['player_queue']['playable_list'][ynison['player_state']['player_queue']['current_playable_index']]
            song = (await __client.tracks(track['playable_id']))[0]
            artists_title = ', '.join(artist.name for artist in song.artists)
            # print(artists_title, ' — ', song.title)
            return song.title, str(song.id), artists_title, str(song.albums[0].id)
    except Exception as e:
        print(e)
        return None, None, None, None
