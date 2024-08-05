import re
import shutil
import os.path
from pathlib import Path
from PIL import Image

file_path = 'E:/Kostegs/Obsidian_Storage/Storage/Data/Визуализация данных.md'
storage_path = Path(file_path).parents[1]
file_name = Path(file_path).name
print(file_name)
processed_data_path = os.path.join(storage_path, 'ProcessedData')
compressed_images_path = os.path.join(processed_data_path, 'img_new', '')


def parse_image_names(source_file):
    file_contents = ''
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            file_contents = f.read()
    except Exception as e:
        print(f'Can\'t read the file, because: {e}')
        return []

    # find all items like ![[Pasted image 20240711090319.png|Timeline_AutoPlay]]
    # or ![[Pasted image 20240711090319.png|Timeline_AutoPlay|400]]
    # than split them for original name: Pasted image 20240711090319.png
    # and new name: Timeline_AutoPlay
    pattern = r'pasted image \d+.\w+\|.[^]|]+'
    picture_names = re.findall(pattern, file_contents, re.IGNORECASE)
    picture_names = [x.split(r'|') for x in picture_names]
    temp_list = ['Name', 'NewName']

    finish_list = []

    # list of dictionaries: {Name : Original name, NewName : new name}
    for pict_name in picture_names:
        finish_list.append(dict(zip(temp_list, pict_name)))

    return finish_list, file_contents


def check_folders_exist():
    if not os.path.exists(processed_data_path):
        os.makedirs(processed_data_path)
    if not os.path.exists(compressed_images_path):
        os.makedirs(compressed_images_path)
    if not os.path.exists(compressed_images_path):
        os.makedirs(compressed_images_path)

def copy_source_file():
    dest_path = os.path.join(processed_data_path, file_name)
    shutil.copy(file_path, dest_path)
    return dest_path


def compress_img(image_name, new_image_name, quality):
    with Image.open(image_name, 'r') as img:
        # new extension is JPEG
        new_filename = f"{new_image_name}.jpg"

        try:
            img.save(new_filename, quality=quality, optimize=True)
        except OSError:
            # convert the image to RGB mode first
            img = img.convert("RGB")
            # save the image
            img.save(new_filename, quality=quality, optimize=True)

        print("[+] New file saved:", new_filename)


if __name__ == '__main__':
    check_folders_exist()
    source_file = copy_source_file()
    images, content = parse_image_names(source_file)

    origin_img_path = os.path.join(storage_path, 'Images', '')

    for image in images:
        source_image = f'{origin_img_path}{image['Name']}'
        dest_image = f'{compressed_images_path}{image['NewName']}'
        compress_img(source_image, dest_image, 80)

#TODO:
# -add images unique name in the beginning
# -skip using folder for old_files
# -change image links in source database-file
# -backup database file before changing
# -get all paths from json with settings
# -translate new image name from russian to english (if we need)
# Копируем исходный файл, в папку /wp_post/filename
# туда же в images кладем картинки, сжатые
# меняем в исходном файле названия, открываем его в Wordpress, постим
# отдельно скрипт, который чистит файл вместе с картинками


