from config.db import *
from config.const import EMOTIONS_DB


# from pymystem3 import Mystem
#
# def process_word(word):
#     m = Mystem()
#     analysis = m.analyze(word)
#
#     if analysis and 'analysis' in analysis[0]:
#         result = analysis[0]['analysis'][0]['lex']
#         return result
#     else:
#         return None


def __create():
    with sqlite3.connect(EMOTIONS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotions (
                id TEXT PRIMARY KEY,
                calmness FLOAT NOT NULL,
                joy FLOAT NOT NULL,
                ecstasy FLOAT NOT NULL,
                recognition FLOAT NOT NULL,
                trust FLOAT NOT NULL,
                admiration FLOAT NOT NULL,
                anxiety FLOAT NOT NULL,
                fear FLOAT NOT NULL,
                horror FLOAT NOT NULL,
                distraction FLOAT NOT NULL,
                surprise FLOAT NOT NULL,
                amazement FLOAT NOT NULL,
                contemplation FLOAT NOT NULL,
                sadness FLOAT NOT NULL,
                sorrow FLOAT NOT NULL,
                boredom FLOAT NOT NULL,
                disgust FLOAT NOT NULL,
                aversion FLOAT NOT NULL,
                annoyance FLOAT NOT NULL,
                anger FLOAT NOT NULL,
                fury FLOAT NOT NULL,
                interest FLOAT NOT NULL,
                anticipation FLOAT NOT NULL,
                vigilance FLOAT NOT NULL)
        ''')
        conn.commit()


def add(song_id: str, emo_dict: dict):
    with sqlite3.connect(EMOTIONS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO emotions
        (id,
        calmness, joy, ecstasy, recognition, trust, admiration, anxiety, fear, horror, distraction, surprise, amazement,
        contemplation, sadness, sorrow, boredom, disgust, aversion, annoyance, anger, fury, interest, anticipation, vigilance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (song_id, *emo_dict.values()))
        conn.commit()


def get(song_id: str) -> dict:
    with sqlite3.connect(EMOTIONS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT (calmness, joy, ecstasy, recognition, trust, admiration, anxiety, fear, horror,
        distraction, surprise, amazement, contemplation, sadness, sorrow, boredom, disgust, aversion, annoyance,
        anger, fury, interest, anticipation, vigilance) FROM emotions WHERE id = ?''', (song_id,))

        values = cursor.fetchone()
        names = [description[0] for description in cursor.description]

        return dict(zip(names, values))


def count() -> int:
    with sqlite3.connect(EMOTIONS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM emotions')
        return cursor.fetchone()[0]


__create()
