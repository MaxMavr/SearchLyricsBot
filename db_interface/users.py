from config.db import *
from config.const import USERS_DB
from db_interface.settings import add as settings_add


def __create():
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY NOT NULL,
                username TEXT NOT NULL DEFAULT 'username',
                status INTEGER CHECK (status IN (-2, -1, 0, 1)) NOT NULL DEFAULT -2
            )
        ''')  # status Не зарегистрирован, Забанен, Обычный, Админ
        cursor.close()


def add(user_id: int, username: str) -> bool:
    with sqlite3.connect(USERS_DB) as conn:
        if is_exists(user_id):
            return False

        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()
        settings_add(user_id)
        return True


def delete(user_id: int):
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()


def get_by_page(page_number: int, page_size: int):
    offset = (page_number - 1) * page_size
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users '
                       'ORDER BY CASE '
                       'WHEN status = 1 THEN 1 '
                       'WHEN status = 0 THEN 2 '
                       'WHEN status = -1 THEN 3 '
                       'WHEN status = -2 THEN 4 '
                       'END LIMIT ? OFFSET ?',
                       (page_size, offset))
        return cursor.fetchall()


def get_username(user_id: int) -> str:
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()[0]


def count() -> int:
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        return cursor.fetchone()[0]


def admit(user_id: int):
    __upd_status(user_id, 0)


def promote(user_id: int):
    __upd_status(user_id, 1)


demote = admit


def ban(user_id: int):
    __upd_status(user_id, -1)


unban = admit


def __upd_status(user_id: int, status: int):
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET status = ? WHERE id = ?",
            (status, user_id)
        )
        conn.commit()


def is_exists(user_id: int) -> bool:
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()[0] > 0


def is_admitted(user_id: int) -> bool:
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM users WHERE id = ?", (user_id,))
        status = cursor.fetchone()
        if not status:
            return False
        return status[0] == 0


def is_admin(user_id: int) -> bool:
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()[0] == 1


def is_baned(user_id: int) -> bool:
    with sqlite3.connect(USERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()[0] == -1


__create()
