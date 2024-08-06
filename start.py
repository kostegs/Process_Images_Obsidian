import re
import shutil
import sys
from pathlib import Path
from PIL import Image


def parse_image_names(source_file):
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


def check_folder_exist(folder):
    if not Path(folder).exists():
        Path(folder).mkdir()


def copy_source_file(original_file_path, processed_data_path, file_name):
    dest_path = Path(processed_data_path).joinpath(file_name)
    shutil.copy(original_file_path, dest_path)
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


def process_file(file_path, storage_for_site):
    storage_path = Path(file_path).parents[1]
    file_name = Path(file_path).name
    processed_data_path = Path(storage_for_site).joinpath('Data')
    compressed_images_path = Path(storage_for_site).joinpath('Images')

    check_folder_exist(processed_data_path)
    check_folder_exist(compressed_images_path)

    dest_file = copy_source_file(file_path, processed_data_path, file_name)
    images, content = parse_image_names(dest_file)

    origin_img_path = Path(storage_path).joinpath('Images\\')
    pattern = r'!\[+img_name.+\]'

    for image in images:
        source_image = Path(origin_img_path).joinpath(image['Name'])
        dest_image = Path(compressed_images_path).joinpath(image['NewName'])
        compress_img(source_image, dest_image, 80)
        current_pattern = pattern.replace('img_name', image['Name'])
        content = re.sub(current_pattern, f'![[{image['NewName']}.jpg]]', content)

    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    # 2 arguments:
    # -path to source file
    # -path to storage for site
    if len(sys.argv) > 2:
        file_path = sys.argv[1]
        storage_for_site = sys.argv[2]
        process_file(file_path, storage_for_site)
