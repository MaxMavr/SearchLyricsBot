from config.db import *
from config.const import USERS_DB
from config.phrases import phrases


def __create():
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY NOT NULL,
                icon_select TEXT,
                icon_songs TEXT,
                icon_not_songs TEXT,
                icon_embedded TEXT,
                icon_text TEXT,
                icon_not_text TEXT,
                bool_show_ids BOOLEAN NOT NULL DEFAULT FALSE,
                bool_show_date BOOLEAN NOT NULL DEFAULT TRUE,
                bool_show_feat BOOLEAN NOT NULL DEFAULT TRUE,
                FOREIGN KEY (id) REFERENCES users(id)
            )''')
        cursor.close()


def add(user_id: int):
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO settings (id) VALUES (?)', (user_id,))
        conn.commit()


def delete(user_id: int):
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM settings WHERE id = ?', (user_id,))
        conn.commit()


def get_icon(user_id: int, suffix: str):
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT {suffix} FROM settings WHERE id = ?', (user_id,))
        icon_select = cursor.fetchone()

        if not icon_select:
            return phrases[f'default_{suffix}']
        if icon_select == 'None':
            return phrases[f'default_{suffix}']
        return icon_select[0]


def __preprocessing(settings_items: dict):
    for name, value in settings_items.items():
        if name.startswith('icon_'):
            if not value:
                settings_items[name] = phrases[f'default_{name}']

        if name.startswith('bool_'):
            settings_items[name] = bool(value)

    return settings_items


def get(user_id: int):
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT
               icon_select, icon_songs, icon_not_songs,
               icon_embedded, icon_text, icon_not_text,
               bool_show_ids, bool_show_date, bool_show_feat
               FROM settings WHERE id = ?''', (user_id,))
        values = cursor.fetchone()
        names = [description[0] for description in cursor.description]
        return __preprocessing(dict(zip(names, values)))


def get_for_artists(user_id: int):
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT icon_select, icon_songs, icon_not_songs, bool_show_ids
               FROM settings WHERE id = ?''', (user_id,))
        values = cursor.fetchone()
        names = [description[0] for description in cursor.description]
        return __preprocessing(dict(zip(names, values)))


def get_for_artist(user_id: int):
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT icon_select, bool_show_ids FROM settings WHERE id = ?', (user_id,))
        values = cursor.fetchone()
        names = [description[0] for description in cursor.description]
        return __preprocessing(dict(zip(names, values)))


def get_for_album(user_id: int):
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT icon_select, icon_embedded, icon_text, icon_not_text, bool_show_ids, bool_show_date, bool_show_feat FROM settings WHERE id = ?', (user_id,))
        values = cursor.fetchone()
        names = [description[0] for description in cursor.description]
        return __preprocessing(dict(zip(names, values)))


def upd_bool(user_id: int, suffix: str):
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT {suffix} FROM settings WHERE id = ?', (user_id,))
        bool_value = cursor.fetchone()[0]
        cursor.execute(f'UPDATE settings SET {suffix} = ? WHERE id = ?', (1 - bool_value, user_id))


def set_icon(user_id: int, suffix: str, icon: str):
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(f'UPDATE settings SET {suffix} = ? WHERE id = ?', (icon, user_id))


__create()
