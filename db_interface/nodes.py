from config.db import *
from config.const import NODES_DB


def __create():
    with sqlite3.connect(NODES_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nodes (
                right TEXT,
                current TEXT NOT NULL PRIMARY KEY,
                left TEXT
            )
        ''')
        conn.commit()


def add(current: str, right: str = None, left: str = None):
    with sqlite3.connect(NODES_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO nodes (right, current, left) VALUES (?, ?, ?)',
                       (right, current, left))
        conn.commit()


def get(current: str):
    with sqlite3.connect(NODES_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM nodes WHERE current = ?', (current,))
        return cursor.fetchone()


def delete(current: str):
    with sqlite3.connect(NODES_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM nodes WHERE current = ?', (current,))
        conn.commit()


__create()
