import time
import sched
import random
from datetime import datetime
import shutil
import os
from os import walk
from xml.etree import ElementTree as ET


class Article:
    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.datetime = datetime.now().strftime("%A %d-%b-%Y %H:%M:%S")
        self.likes = random.randint(10, 100)


_I = 5
_THIS_DIR = os.getcwd()
_LOG_FILE = f'{_THIS_DIR}/Системная интеграция программных приложений(Тимченко В.И.)/Log/copy-{datetime.now().strftime("%Y%m%d")}.log'
_PATH_DOWN = f'{_THIS_DIR}/Системная интеграция программных приложений(Тимченко В.И.)/Download/'

os.makedirs(f'{_THIS_DIR}/Системная интеграция программных приложений(Тимченко В.И.)/Loaded/', exist_ok=True)
os.makedirs(f'{_THIS_DIR}/Системная интеграция программных приложений(Тимченко В.И.)/Error/', exist_ok=True)

def log(s):
    with open(_LOG_FILE, "a") as f:
        f.writelines(f'{datetime.now().strftime("%H:%M:%S")} | {s} \n')


def print_article(o):
    print(o.title, o.body, o.datetime, o.likes, sep='\n')
    log(f'данные обработаны {o.title}')


def read_file(path, f_name):
    with open(f'{path}{f_name}', "r") as f:
        content = f.read()
        return ET.fromstring(content)


def copy_file(f_name):
    shutil.copy(f'{_PATH_DOWN}{f_name}', f"{_THIS_DIR}/Системная интеграция программных приложений(Тимченко В.И.)/Loaded/")


def error_copy_file(f_name):
    shutil.copy(f'{_PATH_DOWN}{f_name}', f"{_THIS_DIR}/Системная интеграция программных приложений(Тимченко В.И.)/Error/")


def remove_file(f_name):
    os.remove(f'{_PATH_DOWN}{f_name}')


def from_dict(xml_element, f_name):
    try:
        title = xml_element.find("title").text
        body = xml_element.find("body").text
        datetime_str = xml_element.find("datetime").text
        likes = int(xml_element.find("likes").text)

        article = Article(title, body)
        article.datetime = datetime_str
        article.likes = likes

        copy_file(f_name)
        return article
    except Exception as err:
        log(f'ошибка - {err}')
        error_copy_file(f_name)
    finally:
        remove_file(f_name)


def watch_dir(path):
    for root, dirs, files in walk(path):
        for file in files:
            if not file.endswith(".xml"):
                continue
            log(f'обнаружен файл {file}')
    xml_data = read_file(path, file)
    article = from_dict(xml_data, file)
    if article:
        print_article(article)

def do_work(sc):
    global _I
    print(f'--- {_I} ---')
    watch_dir(_PATH_DOWN)
    _I = _I - 1
    if _I > 0:
        s.enter(3, 1, do_work, (sc,))


log("-= START =-")
s = sched.scheduler(time.time, time.sleep)
s.enter(5, 1, do_work, (s,))
s.run()
log("-= STOP =-")
