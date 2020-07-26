import os
from bs4 import BeautifulSoup


# Creating directory for .zip
def create_main_directory():
    basedir = os.getcwd()
    try:
        os.makedirs(os.path.join(basedir, 'task_result'))
        return 'Success'
    except FileExistsError:
        return 'Directory already exists'


# We start to find all hrefs on page
def parse_text(text):
    soup = BeautifulSoup(text, 'lxml')
    return str(soup.head)


# Record data in files
