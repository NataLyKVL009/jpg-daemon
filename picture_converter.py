import os
import time
from datetime import datetime
from PIL import Image

#Проверяем есть ли в папке jpg-файлы
def check_folder(folder_path):
    # Получение списка файлов в папке
    files = os.listdir(folder_path)

    # Фильтрация файлов по формату JPG
    jpg_files = [f for f in files if f.lower().endswith('.jpg')]

    return jpg_files


def correct_size(image):

    # Получение информации об изображении
    width, height = image.size  # Размер изображения (ширина, высота)

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


def change_size(width, height):
    # Создание белого квадрата 512x512
    new_image = Image.new("RGB", (512, 512), (255, 255, 255))

    # Вычисление координат для центровки изображения
    offset_x = (512 - width) // 2
    offset_y = (512 - height) // 2

    # Наложение исходного изображения на белую подложку
    new_image.paste(image, (offset_x, offset_y))

    return new_image


#генерируем имя файла в цифровом порядке
def get_next_file_number(folder_path):
    files = os.listdir(folder_path)
    numbers = [int(os.path.splitext(f)[0]) for f in files]
    print(numbers)
    return max(numbers) + 1



if __name__ == "__main__":

    while True:

        files_list = check_folder('upload')
        if files_list:
            for i in range(len(files_list)):
                # Открытие изображения
                with Image.open(f'upload\{files_list[i]}') as image:

                    # Корректируем пропорции изображения, если нужно
                    orientation = correct_size(image)

                    # Меняем размер изображения на 512х512
                    new_image = change_size(*image.size)

                # Генерируем имя файла и сохраняем новое изображение
                new_name = get_next_file_number('ready')
                new_image.save(f'ready\{new_name}.png')
                print(f'[{datetime.now()}] Изображение {files_list[i]}, ориентация: {orientation}, обработано и сохранено в {new_name}.png')

                # Удаляем изображение в исходной папке
                os.remove(f'upload\{files_list[i]}')
        else:
            time.sleep(5)


        #break
