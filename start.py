import re
import shutil
import os.path
from PIL import Image

file_path = './Timeline.md'
storage_path = 'E:/Obsidian_Storage/Storage'
old_images_path = './img_old/'
compressed_images_path = './img_new/'


def find_all_image_names():
    file_contents = ''
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
    except Exception as e:
        print(f'Can\'t read the file, because: {e}')
        return []

    pattern = r'pasted image \d+.\w+\|.[^]]+'
    picture_names = re.findall(pattern, file_contents, re.IGNORECASE)
    picture_names = [x.split(r'|') for x in picture_names]
    temp_list = ['Name', 'NewName']

    finish_list = []

    for pict_name in picture_names:
        finish_list.append(dict(zip(temp_list, pict_name)))

    return finish_list


def check_image_path():
    if not os.path.exists(old_images_path):
        os.makedirs(old_images_path)
    if not os.path.exists(compressed_images_path):
        os.makedirs(compressed_images_path)


def copy_old_images(image_names):
    for image in image_names:
        source_path = f'{storage_path}/Images/{image["Name"]}'
        dest_path = f'{old_images_path}{image["Name"]}'

        try :
            shutil.copy(source_path, dest_path)
        except FileNotFoundError:
            print(f'File not found: {source_path}')
        except Exception:
            print(f'Error while copying image file: {Exception}')


def compress_img(image_name, new_image_name, quality):
    # load the image to memory
    with Image.open(image_name, 'r') as img:
        # change the extension to JPEG
        new_filename = f"{new_image_name}.jpg"

        try:
            # save the image with the corresponding quality and optimize set to True
            img.save(new_filename, quality=quality, optimize=True)
        except OSError:
            # convert the image to RGB mode first
            img = img.convert("RGB")
            # save the image with the corresponding quality and optimize set to True
            img.save(new_filename, quality=quality, optimize=True)

        print("[+] New file saved:", new_filename)


if __name__ == '__main__':
    images = find_all_image_names()
    check_image_path()
    copy_old_images(images)

    for image in images:
        source_image = f'{old_images_path}{image['Name']}'
        dest_image = f'{compressed_images_path}{image['NewName']}'
        compress_img(source_image, dest_image, 80)


