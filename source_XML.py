import random
from datetime import datetime
import time
import sched
from xml.etree.ElementTree import Element, SubElement, tostring
import os

class Article:
    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.datetime = datetime.now().strftime("%A %d-%b-%Y %H:%M:%S") 
        self.likes = random.randint(10, 100)

_I = 5
_TIME_SEC = 3
_THIS_DIR = os.getcwd()
_LOG_FILE = f'{_THIS_DIR}/Системная интеграция программных приложений(Тимченко В.И.)/Log/serialize-{datetime.now().strftime("%Y.%m.%d")}.log'

os.makedirs(f'{_THIS_DIR}/Системная интеграция программных приложений(Тимченко В.И.)/Log/', exist_ok=True)
os.makedirs(f'{_THIS_DIR}/Системная интеграция программных приложений(Тимченко В.И.)/Download/', exist_ok=True)

def log(s):
    with open(_LOG_FILE, "a") as f:
        f.writelines(f'{datetime.now().strftime("%H:%M:%S")} | {s} \n')

def to_xml(article):
    root = Element("Article")
    SubElement(root, "title").text = article.title
    SubElement(root, "body").text = article.body
    SubElement(root, "datetime").text = article.datetime
    SubElement(root, "likes").text = str(article.likes)
    return tostring(root, encoding="unicode", method="xml")

def send_xml_data(i):
    try:
        title = f'Заголовок - {random.randint(1, 9999)}'
        body = f'Некоторый текст - {random.randint(1000, 9999999)}'
        art = Article(title, body)
        fd = f'{_THIS_DIR}/Системная интеграция программных приложений(Тимченко В.И.)/Download/{i}-{datetime.now().strftime("%Y.%m.%d %H:%M:%S")}-data.xml'
        with open(fd, "w") as f:
            f.write(to_xml(art))
        log(f'отправка {i} выполнена')
    except Exception as err:
        log(f'ошибка отправки {i} - {err}')

_J = 0
def do_work(sc): 
    global _J
    _J += 1
    print(f'--- {_J} ---')
    send_xml_data(_J)
    if _J < _I:
        s.enter(_TIME_SEC, 1, do_work, (sc,))

log("-= START =-")
s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, do_work, (s,))
s.run()
log("-= STOP =-")