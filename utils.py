import os
from PIL import Image
from datetime import datetime


# Проверяем есть ли в папке jpg-файлы
def get_jpg_files(folder_path):
    # Получение списка файлов в папке
    files = os.listdir(folder_path)
    formats = ('jpg', 'jpeg', 'JPG')

    # Фильтрация файлов по формату JPG
    jpg_files = [f for f in files if f.endswith(formats)]

    return jpg_files


class JpegImage:
    def __init__(self, file_path, output_dir='ready'):
        self.file_path = file_path
        self.output_dir = output_dir

    # Проверяем размер изображения.
    # Если размер бОльшей из сторон превышает 150, то меняем размер этой стороны на 150.
    # При этом размер изображения должен уменьшится прапорционально.
    @staticmethod
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
    @staticmethod
    def change_size(image):
        width, height = image.size
        # Создание белого квадрата 512x512
        new_image = Image.new("RGB", (512, 512), (255, 255, 255))

        # Вычисление координат для центровки изображения
        offset_x = (512 - width) // 2
        offset_y = (512 - height) // 2

        # Наложение исходного изображения на белую подложку
        new_image.paste(image, (offset_x, offset_y))

        return new_image

    # генерируем имя файла в цифровом порядке
    @staticmethod
    def get_next_file_number(folder_path):
        files = os.listdir(folder_path)
        numbers = []

        for f in files:
            try:
                numbers.append(int(os.path.splitext(f)[0]))
            except ValueError:
                continue

        try:
            return str(max(numbers) + 1)
        except ValueError:
            return '0'

    def process(self):
        # Открытие изображения
        full_file_path = os.path.join('upload', self.file_path)
        print(full_file_path)
        with Image.open(os.path.abspath(full_file_path)) as image:
            # Корректируем пропорции изображения, если нужно
            orientation = self.correct_size(image)

            # Меняем размер изображения на 512х512
            new_image = self.change_size(image)

        # Генерируем имя файла и сохраняем новое изображение
        new_name = self.get_next_file_number('ready')
        new_path = os.path.join('ready', new_name)
        new_image.save(f'{os.path.abspath(new_path)}.png')
        print(
            f'[{datetime.now()}] Изображение {self.file_path}, ориентация: {orientation}, обработано и сохранено в {new_name}.png')

        # Удаляем изображение в исходной папке
        os.remove(full_file_path)