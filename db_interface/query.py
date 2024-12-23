from config.db import *
from config.const import QUERY_DB


def __create():
    with sqlite3.connect(QUERY_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS query (
                username TEXT NOT NULL DEFAULT 'username',
                prompt TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        ''')
        cursor.close()


def add(username: str, prompt: str, answer: str):
    with sqlite3.connect(QUERY_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO query (username, prompt, answer) VALUES (?, ?, ?)',
                       (username, prompt, answer))
        conn.commit()


def get_by_page(page_number: int, page_size: int):
    offset = (page_number - 1) * page_size
    with sqlite3.connect(QUERY_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM query END LIMIT ? OFFSET ?',
                       (page_size, offset))
        return cursor.fetchall()


def count() -> int:
    with sqlite3.connect(QUERY_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM query')
        return cursor.fetchone()[0]


__create()
