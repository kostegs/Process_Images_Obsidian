import re
import shutil

file_path = './Test to WP.md'
storage_path = 'E:/Obsidian_Storage/Storage'

def find_all_image_names():
    file_contents = ''
    try:
        with open(file_path, 'r', encoding = 'utf-8') as f:
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

def copy_old_images(image_names):
    for image in image_names:
        source_path = f'{storage_path}/Images/{image["Name"]}'
        dest_path = f'./img_old/{image["Name"]}'
        try :
            shutil.copy(source_path, dest_path)
        except FileNotFoundError:
            print(f'File not found: {source_path}')
        except Exception:
            print(f'Error while copying image file: {Exception}')

if __name__ == '__main__':
    images = find_all_image_names()
    copy_old_images(images)


