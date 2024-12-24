from config.const import (
    EMOTIONS_COLOR,
    EMOTIONS_RANG1,
    EMOTIONS_RANG2,
    EMOTIONS_RANG3,
    EMOTION_RANG1_MULTIPLIER,
    EMOTION_RANG2_MULTIPLIER,
    EMOTION_RANG3_MULTIPLIER,
    IMG_EMOTION_TEMPLATE_FILE,
    TEMP_DIR,
    FONT_NOAH_LIGHT,
    DRAW_MAX_RADIUS
)

from math import sqrt, sin, cos, pi
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from time import time

font = ImageFont.truetype(FONT_NOAH_LIGHT, 18)


# def create_book(path: str,
#                 author: str,
#                 title: str,
#                 descriptor: str,
#                 annotation_location: str,
#                 annotation: list,
#                 author_backing_color: str,
#                 title_backing_color: str,
#                 logo_backing_color: str,
#                 size: int,
#                 distance: int) -> str:
#     save_path = f'{path[:-4]}-mem-book.png'
#     basic_color = "#faef9f"
#     relation = 930 / 600
#     illustration_height = int(size * relation * 370 / 930)
#
#     small_distance = distance // 8
#     descriptor_line_width = 2 * distance // 3
#
#     img_past = Image.open(path).convert('RGB')
#     img_logo = Image.open(f'{os.path.dirname(__file__)}/assets/logo.png').convert('RGBA')
#
#     myriad_pro_bold = f'{os.path.dirname(__file__)}/assets/Myriad Pro Bold.OTF'
#     myriad_pro_cond_bold = f'{os.path.dirname(__file__)}/assets/Myriad Pro Cond Bold.OTF'
#     myriad_pro_cond_italic = f'{os.path.dirname(__file__)}/assets/Myriad Pro Cond Italic.OTF'
#
#     img = Image.new('RGB', (size, int(size * relation)), color=basic_color)
#     img_cnv = ImageDraw.Draw(img)
#
#     # Верхний черный прямоугольник
#     img_cnv.rectangle((distance,
#                        distance - 2 * small_distance,
#                        size - distance,
#                        distance - small_distance),
#                       fill="#000000")
#
#     # Нижний черный прямоугольник для надписи "русская классика"
#     img_cnv.rectangle((distance,
#                        img.height - (distance - 2 * small_distance) - descriptor_line_width,
#                        img.width - distance,
#                        img.height - (distance - 2 * small_distance)),
#                       fill="#000000")
#
#     font_descriptor = ImageFont.truetype(myriad_pro_bold, 18)
#     for i in range(len(descriptor) + 1):
#         img_cnv.text((distance + int((size - (distance * 2)) * (i / (len(descriptor) + 1))),
#                       img.height - (distance - 2 * small_distance) - descriptor_line_width // 2),
#                      f' {descriptor}'[i],
#                      font=font_descriptor,
#                      fill=basic_color,
#                      anchor="mm"
#                      )
#
#     annotation_size = random.randint(90, 140)
#     font_annotation = ImageFont.truetype(myriad_pro_cond_italic, 19)
#
#     if annotation_location == 'l':
#         position_annotation = int(1.5 * distance)
#         position_l_title = int(2 * distance) + 153
#         position_r_title = img.width - distance
#     else:
#         position_annotation = img.width - int(1.5 * distance) - 153
#         position_l_title = distance
#         position_r_title = img.width - int(2 * distance) - 153
#
#     # Прямоугольник для названия (около "Книги, изменившие мир.")
#     img_cnv.rectangle((position_l_title,
#                        img.height - (distance - small_distance) - descriptor_line_width - annotation_size,
#                        position_r_title,
#                        img.height - (distance - small_distance) - descriptor_line_width),
#                       fill=author_backing_color)
#
#     img_cnv.text((position_annotation,
#                   img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) - 22),
#                  annotation[0],
#                  font=font_annotation,
#                  fill='#000000',
#                  anchor="lm"
#                  )
#     img_cnv.text((position_annotation,
#                   img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2)),
#                  annotation[1],
#                  font=font_annotation,
#                  fill='#000000',
#                  anchor="lm"
#                  )
#     img_cnv.text((position_annotation,
#                   img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) + 22),
#                  annotation[2],
#                  font=font_annotation,
#                  fill='#000000',
#                  anchor="lm"
#                  )
#
#     if len(title) < 6:
#         title_name_font = myriad_pro_bold
#     else:
#         title_name_font = myriad_pro_cond_italic
#
#     if len(title.split()) >= 2 and len(title) > 16:
#         bottom_title = " ".join(title.split()[(len(title.split()) // 2 + len(title.split()) % 2):])
#         upper_title = " ".join(title.split()[:(len(title.split()) - len(title.split()) // 2)])
#
#         if len(upper_title) >= len(bottom_title):
#             max_title = upper_title
#         else:
#             max_title = bottom_title
#
#         title_size = calc_font_size(max_title, int(img.width - 3.5 * distance - 153), title_name_font)
#         title_font = ImageFont.truetype(title_name_font, title_size)
#
#         img_cnv.text((position_l_title + distance // 4,
#                       img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) - 5),
#                      upper_title,
#                      font=title_font,
#                      fill='#000000',
#                      anchor="lb"
#                      )
#
#         img_cnv.text((position_l_title + distance // 4,
#                       img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) + 5),
#                      bottom_title,
#                      font=title_font,
#                      fill='#000000',
#                      anchor="lt"
#                      )
#
#     else:
#         title_size = calc_font_size(title, int(img.width - 3.5 * distance - 153), title_name_font)
#
#         if title_size > annotation_size:
#             title_size = annotation_size
#
#         title_font = ImageFont.truetype(title_name_font, title_size)
#
#         if len(title) < 6:
#             position = img.height - (distance - small_distance) - descriptor_line_width - int(0.82 * annotation_size // 2)
#         else:
#             position = img.height - (distance - small_distance) - descriptor_line_width - int(0.92 * annotation_size // 2)
#
#         img_cnv.text((position_l_title + distance // 4,
#                       position),
#                      title,
#                      font=title_font,
#                      fill='#000000',
#                      anchor="lm"
#                      )
#
#     if len(author.split()) <= 1:
#         bottom_author = author if author != '' else "Иванов"
#         upper_author = "Иван Иванович"
#     else:
#         bottom_author = author.split()[-1]
#         upper_author = " ".join(author.split()[:-1])
#
#     if len(upper_author.split()) == 2:
#         upper_author_name_font = myriad_pro_cond_bold
#     else:
#         upper_author_name_font = myriad_pro_bold
#
#     upper_author_size = size // 2
#     upper_author_font = ImageFont.truetype(upper_author_name_font, upper_author_size)
#     upper_author_width = img_cnv.textlength(upper_author, font=upper_author_font)
#
#     while (upper_author_width >= (img.width - 2.5 * distance) - upper_author_size) and \
#             (upper_author_size != 1):
#         upper_author_size = upper_author_size - 1 if upper_author_size - 1 > 0 else 1
#         upper_author_font = ImageFont.truetype(upper_author_name_font, upper_author_size)
#         upper_author_width = img_cnv.textlength(upper_author, font=upper_author_font)
#
#     bottom_author_size = calc_font_size(bottom_author, int(img.width - 2.5 * distance), myriad_pro_cond_bold)
#     bottom_author_font = ImageFont.truetype(myriad_pro_cond_bold, bottom_author_size)
#
#     # Тут сложная логика через левую коленку, но если в двух словах
#     # скрипт вычислил сверху абсолютные значения для картинки, верхнего и нижнего имени автора.
#     # код ниже растягивает эти значения на оставшуюся часть картинки
#     #
#     #                    Срезаем место сверху
#     #                    |          Срезаем место снизу
#     #                    |          |                                                    Срезаем расстояния меж блоками
#     #                    L_______   L_________________________________________________   L___________________
#     place = img.height - distance - distance - descriptor_line_width - annotation_size - (4 * small_distance)
#
#     relation4place = place / (illustration_height + upper_author_size + bottom_author_size)
#
#     illustration_height = int(illustration_height * relation4place)
#     upper_author_size = int(upper_author_size * relation4place)
#     bottom_author_size = int(bottom_author_size * relation4place)
#
#     img_past = img_past.resize((size - (distance * 2), illustration_height))
#     img.paste(img_past, (distance, distance))
#
#     img_cnv.rectangle((distance,
#                        distance + img_past.height + small_distance,
#                        size - distance,
#                        distance + img_past.height + 2 * small_distance),
#                       fill="#000000")
#
#     # Чтобы было удобно считать, определяем новый «нуль» (Относительно низа картинки)
#     zero_below_img = distance + img_past.height + 3 * small_distance
#
#     img_cnv.rectangle((distance,
#                        zero_below_img,
#                        size - distance,
#                        zero_below_img + upper_author_size),
#                       fill=author_backing_color)
#
#     img_cnv.rectangle((distance,
#                        zero_below_img,
#                        distance + upper_author_size,
#                        zero_below_img + upper_author_size),
#                       fill=logo_backing_color)
#
#     img_logo = img_logo.resize((upper_author_size, upper_author_size))
#     img.paste(img_logo,
#               (distance,
#                zero_below_img),
#               mask=img_logo)
#
#     img_cnv.text(((img.width + upper_author_size) // 2,
#                   int(zero_below_img + 0.62 * upper_author_size)),
#                  upper_author,
#                  font=upper_author_font,
#                  fill='#000000',
#                  anchor="mm"
#                  )
#
#     img_cnv.rectangle((distance,
#                        zero_below_img + small_distance + upper_author_size,
#                        size - distance,
#                        int(zero_below_img + small_distance + upper_author_size + bottom_author_size)),
#                       fill=title_backing_color)
#
#     img_cnv.text((img.width // 2,
#                   int(zero_below_img + small_distance + upper_author_size + 0.62 * bottom_author_size)),
#                  bottom_author,
#                  font=bottom_author_font,
#                  fill=basic_color,
#                  anchor="mm"
#                  )
#
#     img.save(save_path)
#     return save_path

def make_map(emo_dict: dict) -> str:
    save_path = TEMP_DIR + f'/{time()}.png'
    img = Image.open(IMG_EMOTION_TEMPLATE_FILE)
    size = img.size
    img_cnv = ImageDraw.Draw(img)

    def draw_ellipse(centre_xy: Tuple[int, int], color: str):
        img_cnv.ellipse((
            centre_xy[0] - DRAW_MAX_RADIUS,
            centre_xy[1] - DRAW_MAX_RADIUS,
            centre_xy[0] + DRAW_MAX_RADIUS,
            centre_xy[1] + DRAW_MAX_RADIUS),
            color)

    coord_rang1, coord_rang2, coord_rang3 = [], [], []
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

        if emo in EMOTIONS_RANG2:
            radius = value * EMOTION_RANG2_MULTIPLIER // 2
            coord = (radius * sin(angle) + size[0] // 2, radius * cos(angle) + size[1] // 2)
            coord_rang2.append(coord)
            coord_emo[emo] = coord

        if emo in EMOTIONS_RANG3:
            radius = value * EMOTION_RANG3_MULTIPLIER // 2
            coord = (radius * sin(angle) + size[0] // 2, radius * cos(angle) + size[1] // 2)
            coord_rang3.append(coord)
            coord_emo[emo] = coord

        print(round(angle, 3))
        print(round(sin(angle), 3))
        print(round(cos(angle), 3))
        print()

    img_cnv.polygon(xy=coord_rang1, fill='blue', outline=(0, 0, 0))
    img_cnv.polygon(xy=coord_rang2, fill='blue', outline=(0, 0, 0))
    img_cnv.polygon(xy=coord_rang3, fill='blue', outline=(0, 0, 0))

    for emo in emo_dict.keys():
        draw_ellipse(coord_emo[emo], EMOTIONS_COLOR[emo])

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
