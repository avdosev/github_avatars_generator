from PIL import ImageDraw, Image
import numpy as np
import hashlib
from itertools import chain

size = (480,480)
block_size = size[0] // 12 # размер квадрата
background_color = '#f2f1f2'
s = 'test1'
path = f'{s}.png'

# Варианты генерации
## 12x12 - 144бит - 18байт
## 6*12 - 72бит - 9байт <- мне больше нравится
## Изображения получатся симметричными
## 6*6 - 36бит - 4.5байт

img = Image.new('RGB', size, background_color)
draw = ImageDraw.Draw(img)

bytes = hashlib.md5(s.encode('utf-8')).digest()

## Получаем цвет из хеша

main_color = bytes[:3]
# rgb
main_color = tuple(channel // 2 + 128 for channel in main_color)

## Генерируем матрицу заполнения блоков

# массив 6 на 12
need_color = np.array([bit == '1' for byte in bytes[3:3+9] for bit in bin(byte)[2:].zfill(8)]).reshape(6, 12)
# получаем матрицу 12 на 12
need_color = np.concatenate((need_color, need_color[::-1]), axis=0)

for i in range(12):
    need_color[0, i] = 0
    need_color[11, i] = 0
    need_color[i, 0] = 0
    need_color[i, 11] = 0

## Рисуем изображения по матрице заполнения

for x in range(size[0]):
    for y in range(size[1]):
        need_to_paint = need_color[x // block_size, y // block_size]
        if need_to_paint:
            draw.point((x, y), main_color)

img.save(path, 'png')