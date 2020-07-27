import os
import zipfile
from bs4 import BeautifulSoup

DIR_NAME = 'task_result'


def key_in_list(k, m):
    return bool([True for i in m if k in i.values()])


def check_task(task_id_find, task_value_dict):
    for task_list in task_value_dict:
        if key_in_list(task_id_find, task_list):
            return True
    return False


# Creating directory for .zip
def create_main_directory():
    basedir = os.getcwd()
    try:
        os.makedirs(os.path.join(basedir, DIR_NAME))
        return 'Success'
    except FileExistsError:
        return 'Directory already exists'


# We start to find unique tags on page
def parse_text(text):
    data = []
    soup = BeautifulSoup(text, 'lxml')
    for child in soup.recursiveChildGenerator():
        if child.name and child.name not in data:
            data.append(child.name)
    return data


# Record zip files
def create_zip(file_path=None, celery_id=None):
    if not file_path or not celery_id:
        return False
    with zipfile.ZipFile(os.path.join(DIR_NAME, '') + f'{celery_id}.zip', 'w') as new_zip:
        new_zip.write(file_path)
        os.remove(file_path)
    return True


# Record data in files
def create_file(data=None):
    if not data:
        return False
    import json
    recorded_data = {'tags': data}
    file_path = os.path.join(DIR_NAME, '') + 'data.json'
    with open(os.path.join(DIR_NAME, '') + 'data.json', 'w', encoding='utf-8') as f:
        json.dump(recorded_data, f, ensure_ascii=False, indent=4)
    return file_path

