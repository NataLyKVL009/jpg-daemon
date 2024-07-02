import os
import time
from datetime import datetime
from PIL import Image


# Проверяем есть ли в папке jpg-файлы
def get_jpg_files(folder_path):
    # Получение списка файлов в папке
    files = os.listdir(folder_path)
    formats = ('jpg', 'jpeg', 'JPG')

    # Фильтрация файлов по формату JPG
    jpg_files = [f for f in files if f.endswith(formats)]

    return jpg_files


# Проверяем размер изображения.
# Если размер бОльшей из сторон превышает 150, то меняем размер этой стороны на 150.
# При этом размер изображения должен уменьшится прапорционально.
def correct_size(image):
    # Получение информации об изображении
    width, height = image.size  # Размер изображения (ширина, высота)
    orientation = ""

    # проверяем размеры изображения (бОльшая сторона > 512)
    if width > height and width > 512:
        # находим новую размерность высоты
        new_height = (512 / width) * height
        image.thumbnail((512, new_height), Image.Resampling.LANCZOS)

        # определяем ориентацию изображения (альбомная)
        orientation = 'альбомная'
    elif height > width and height > 512:
        # находим новую размерность ширины
        new_width = (512 / height) * width
        image.thumbnail((new_width, 512), Image.Resampling.LANCZOS)

        # определяем ориентацию изображения (портретная)
        orientation = 'портретная'

    return orientation


# Изменить размер изображения на (512Х512)
# Создать белый квадрат 512Х512 и поместить изображение в центр квадрата
def change_size(width, height):
    # Создание белого квадрата 512x512
    new_image = Image.new("RGB", (512, 512), (255, 255, 255))

    # Вычисление координат для центровки изображения
    offset_x = (512 - width) // 2
    offset_y = (512 - height) // 2

    # Наложение исходного изображения на белую подложку
    new_image.paste(image, (offset_x, offset_y))

    return new_image


# генерируем имя файла в цифровом порядке
def get_next_file_number(folder_path):
    files = os.listdir(folder_path)
    numbers = []

    for f in files:
        try:
            numbers.append(int(os.path.splitext(f)[0]))
        except ValueError:
            continue

    return str(max(numbers) + 1)


if __name__ == "__main__":
    # директория, в которой хранятся .jpg-файлы
    source_directory = 'upload'

    # директория с .png-файлами
    target_directory = 'ready'

    while True:
        # получаем список jpg-файлов
        files_list = get_jpg_files(source_directory)
        if files_list:
            for i in files_list:
                # Открытие изображения
                file_path = os.path.join(source_directory, i)
                with Image.open(os.path.abspath(file_path)) as image:
                    # Корректируем пропорции изображения, если нужно
                    orientation = correct_size(image)

                    # Меняем размер изображения на 512х512
                    new_image = change_size(*image.size)

                # Генерируем имя файла и сохраняем новое изображение
                new_name = get_next_file_number(target_directory)
                new_path = os.path.join(target_directory, new_name)
                new_image.save(f'{os.path.abspath(new_path)}.png')
                print(
                    f'[{datetime.now()}] Изображение {i}, ориентация: {orientation}, обработано и сохранено в {new_name}.png')

                # Удаляем изображение в исходной папке
                os.remove(file_path)
        else:
            time.sleep(5)
