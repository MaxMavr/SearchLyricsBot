from config.const import (
    EMOTIONS_COLOR,
    EMOTIONS_RANG1,
    EMOTIONS_RANG2,
    EMOTIONS_RANG3,
    EMOTION_RANG1_MULTIPLIER,
    EMOTION_RANG2_MULTIPLIER,
    EMOTION_RANG3_MULTIPLIER,
    IMG_COORDINATE_GRID_FILE,
    TEMP_DIR,
    FONT_NOAH_LIGHT,
    DRAW_MAX_RADIUS,
    SCALE,
)

from math import sqrt, sin, cos, pi
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from time import time

font = ImageFont.truetype(FONT_NOAH_LIGHT, 18)


def make_map(emo_dict: dict) -> str:
    save_path = TEMP_DIR + f'/{time()}.png'
    img = Image.new('RGBA', (1000 * SCALE, 1000 * SCALE), '#001219')
    coords_img = Image.open(IMG_COORDINATE_GRID_FILE)
    size = img.size
    img_cnv = ImageDraw.Draw(img)

    max_emo_color = max(emo_dict, key=emo_dict.get)

    paste_img_ellipse = Image.new('RGBA', size, (0, 0, 0, 0))
    paste_img_ellipse_cnv = ImageDraw.Draw(paste_img_ellipse)

    def draw_ellipse(centre_xy: Tuple[int, int], color: str):
        paste_img_ellipse_cnv.ellipse((
            centre_xy[0] - DRAW_MAX_RADIUS,
            centre_xy[1] - DRAW_MAX_RADIUS,
            centre_xy[0] + DRAW_MAX_RADIUS,
            centre_xy[1] + DRAW_MAX_RADIUS),
            color)

    coord_rang1, coord_rang2, coord_rang3 = [], [], []
    max_value_rang1, max_value_rang2, max_value_rang3 = 0, 0, 0
    emo_rang1, emo_rang2, emo_rang3 = '', '', ''
    coord_emo = {}
    angle = - 3 * pi / 4

    for i, (emo, value) in enumerate(emo_dict.items()):
        if i % 3 == 0:
            angle -= pi / 4

        if emo in EMOTIONS_RANG1:
            radius = value * EMOTION_RANG1_MULTIPLIER // 2
            coord = (radius * sin(angle) + size[0] // 2, radius * cos(angle) + size[1] // 2)
            coord_rang1.append(coord)
            coord_emo[emo] = coord

            if max_value_rang1 < value:
                max_value_rang1 = value
                emo_rang1 = emo

        if emo in EMOTIONS_RANG2:
            radius = value * EMOTION_RANG2_MULTIPLIER // 2
            coord = (radius * sin(angle) + size[0] // 2, radius * cos(angle) + size[1] // 2)
            coord_rang2.append(coord)
            coord_emo[emo] = coord

            if max_value_rang2 < value:
                max_value_rang2 = value
                emo_rang2 = emo

        if emo in EMOTIONS_RANG3:
            radius = value * EMOTION_RANG3_MULTIPLIER // 2
            coord = (radius * sin(angle) + size[0] // 2, radius * cos(angle) + size[1] // 2)
            coord_rang3.append(coord)
            coord_emo[emo] = coord

            if max_value_rang3 < value:
                max_value_rang3 = value
                emo_rang3 = emo

    paste_img_rang1 = Image.new('RGBA', size, (0, 0, 0, 0))
    paste_img_rang2 = Image.new('RGBA', size, (0, 0, 0, 0))
    paste_img_rang3 = Image.new('RGBA', size, (0, 0, 0, 0))

    paste_img_rang1_cnv = ImageDraw.Draw(paste_img_rang1)
    paste_img_rang2_cnv = ImageDraw.Draw(paste_img_rang2)
    paste_img_rang3_cnv = ImageDraw.Draw(paste_img_rang3)

    paste_img_rang1_cnv.polygon(xy=coord_rang1, fill=EMOTIONS_COLOR[emo_rang1] + '1a', outline=EMOTIONS_COLOR[emo_rang1], width=2)
    paste_img_rang2_cnv.polygon(xy=coord_rang2, fill=EMOTIONS_COLOR[emo_rang2] + '33', outline=EMOTIONS_COLOR[emo_rang2], width=2)
    paste_img_rang3_cnv.polygon(xy=coord_rang3, fill=EMOTIONS_COLOR[emo_rang3] + '66', outline=EMOTIONS_COLOR[emo_rang3], width=2)

    for emo in emo_dict.keys():
        draw_ellipse(coord_emo[emo], EMOTIONS_COLOR[emo])

    img.paste(paste_img_rang1, mask=paste_img_rang1)
    img.paste(paste_img_rang2, mask=paste_img_rang2)
    img.paste(paste_img_rang3, mask=paste_img_rang3)
    img.paste(paste_img_ellipse, mask=paste_img_ellipse)
    img.paste(coords_img, mask=coords_img)
    img.save(save_path)
    return save_path


if __name__ == "__main__":
    EM1 = {
        'Спокойствие': 0.1931,
        'Радость': 0.0794,
        'Экстаз': 0.2486,

        'Признание': 0.0000,
        'Доверие': 0.0000,
        'Восхищение': 0.0000,

        'Опасение': 0.0000,
        'Страх': 0.0000,
        'Ужас': 0.1946,

        'Отвлечение': 0.0000,
        'Удивление': 0.0000,
        'Изумление': 0.0879,

        'Задумчивость': 0.8486,
        'Печаль': 1.0000,
        'Горе': 0.7445,

        'Скука': 0.0952,
        'Брезгливость': 0.0000,
        'Отвращение': 0.0937,

        'Досада': 0.0000,
        'Гнев': 0.7154,
        'Ярость': 0.1727,

        'Интерес': 0.0000,
        'Ожидание': 0.0884,
        'Бдительность': 0.2793,
    }

    EM2 = {
        'Спокойствие': 0.5,
        'Радость': 0.5,
        'Экстаз': 0.5,
        'Признание': 0.5,
        'Доверие': 0.5,
        'Восхищение': 0.5,
        'Опасение': 0.5,
        'Страх': 0.5,
        'Ужас': 0.5,
        'Отвлечение': 0.5,
        'Удивление': 0.5,
        'Изумление': 0.5,
        'Задумчивость': 0.5,
        'Печаль': 0.5,
        'Горе': 0.5,
        'Скука': 0.5,
        'Брезгливость': 0.5,
        'Отвращение': 0.5,
        'Досада': 0.5,
        'Гнев': 0.5,
        'Ярость': 0.5,
        'Интерес': 0.5,
        'Ожидание': 0.5,
        'Бдительность': 0.5,
    }

    EM3 = {
        'Спокойствие': 0.5283,
        'Радость': 0.5548,
        'Экстаз': 0.5919,
        'Признание': 0.0813,
        'Доверие': 0.0443,
        'Восхищение': 0.2938,
        'Опасение': 0.4315,
        'Страх': 0.5335,
        'Ужас': 0.5897,
        'Отвлечение': 0.0000,
        'Удивление': 0.5242,
        'Изумление': 0.4499,
        'Задумчивость': 0.8844,
        'Печаль': 1.0000,
        'Горе': 0.8491,
        'Скука': 0.6278,
        'Брезгливость': 0.3171,
        'Отвращение': 0.4648,
        'Досада': 0.5109,
        'Гнев': 0.7846,
        'Ярость': 0.4777,
        'Интерес': 0.3123,
        'Ожидание': 0.3764,
        'Бдительность': 0.5719
    }

    WOW3 = {
        'Спокойствие': 0.1083,
        'Радость': 0.1115,
        'Экстаз': 0.3693,
        'Признание': 0.0882,
        'Доверие': 0.1141,
        'Восхищение': 0.2228,
        'Опасение': 0.0766,
        'Страх': 0.0000,
        'Ужас': 0.0000,
        'Отвлечение': 0.0000,
        'Удивление': 0.2008,
        'Изумление': 0.3821,
        'Задумчивость': 1.0000,
        'Печаль': 0.6929,
        'Горе': 0.0863,
        'Скука': 0.5626,
        'Брезгливость': 0.0000,
        'Отвращение': 0.2532,
        'Досада': 0.0000,
        'Гнев': 0.1485,
        'Ярость': 0.0000,
        'Интерес': 0.1635,
        'Ожидание': 0.0771,
        'Бдительность': 0.0000,
    }

    WOW5 = {
        'Спокойствие': 0.0939,
        'Радость': 0.1029,
        'Экстаз': 0.3417,
        'Признание': 0.0932,
        'Доверие': 0.1094,
        'Восхищение': 0.2068,
        'Опасение': 0.0006,
        'Страх': 0.0061,
        'Ужас': 0.0124,
        'Отвлечение': 0.0128,
        'Удивление': 0.3848,
        'Изумление': 0.3516,
        'Задумчивость': 1.0000,
        'Печаль': 0.7357,
        'Горе': 0.0093,
        'Скука': 0.6598,
        'Брезгливость': 0.0748,
        'Отвращение': 0.1604,
        'Досада': 0.1031,
        'Гнев': 0.2290,
        'Ярость': 0.0054,
        'Интерес': 0.4784,
        'Ожидание': 0.0914,
        'Бдительность': 0.0000,
    }

    WOW = {
        'Спокойствие': 0.2502,
        'Радость': 0.3491,
        'Экстаз': 0.4819,
        'Признание': 0.1907,
        'Доверие': 0.0453,
        'Восхищение': 0.3588,
        'Опасение': 0.1909,
        'Страх': 0.2980,
        'Ужас': 0.2502,
        'Отвлечение': 0.0185,
        'Удивление': 0.6630,
        'Изумление': 0.6668,
        'Задумчивость': 1.0000,
        'Печаль': 0.8531,
        'Горе': 0.2389,
        'Скука': 0.7278,
        'Брезгливость': 0.0000,
        'Отвращение': 0.1320,
        'Досада': 0.2530,
        'Гнев': 0.5268,
        'Ярость': 0.0834,
        'Интерес': 0.6179,
        'Ожидание': 0.4471,
        'Бдительность': 0.5521,
    }

    MSC = {
        'Спокойствие': 0.3192,
        'Радость': 0.3223,
        'Экстаз': 0.3866,
        'Признание': 0.0528,
        'Доверие': 0.2504,
        'Восхищение': 0.3541,
        'Опасение': 0.2823,
        'Страх': 0.4045,
        'Ужас': 0.4449,
        'Отвлечение': 0.0000,
        'Удивление': 0.5512,
        'Изумление': 0.5426,
        'Задумчивость': 1.0000,
        'Печаль': 0.9344,
        'Горе': 0.7202,
        'Скука': 0.7539,
        'Брезгливость': 0.2271,
        'Отвращение': 0.2960,
        'Досада': 0.3607,
        'Гнев': 0.6710,
        'Ярость': 0.5291,
        'Интерес': 0.4376,
        'Ожидание': 0.5009,
        'Бдительность': 0.5462,
    }

    make_map(MSC)
