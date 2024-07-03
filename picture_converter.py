import time
from utils import get_jpg_files, JpegImage


if __name__ == "__main__":

    while True:
        # получаем список jpg-файлов
        files_list = get_jpg_files('upload')

        for file_path in files_list:
            JpegImage(file_path=file_path, output_dir='ready').process()

        if not files_list:
            time.sleep(5)
