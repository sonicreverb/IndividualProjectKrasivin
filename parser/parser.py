import os
import re
import requests
from bs4 import BeautifulSoup
from main import BASE_DIR


# получаем html заданному url
def get_html_from_url(url):
    try:
        return requests.get(url)
    except Exception as exc:
        print(exc)
        return None


# получаем html из файла
def get_html_from_file():
    html_file_path = os.path.join(BASE_DIR, 'parser', 'input.html')

    # проверка на то существует ли файл
    if os.path.exists(html_file_path):
        with open(html_file_path, encoding='UTF-8') as r:
            return r.read()
    # если не существует, то создаём пустой файл
    else:
        print("Ошибка, отсутствует файл с HTML кодом.")
        with open(html_file_path, 'w', encoding='UTF-8'):
            pass
        return None


def get_data(input_type):
    if input_type == "URL":
        url = input('Введите адресс:')
        html = get_html_from_url(url)

        # находим вхождение / в ссылке, для того чтобы получить хост сайта
        try:
            url_cut_to_index = [_.start() for _ in re.finditer('/', url)][2]
            host = url[:url_cut_to_index]
        except Exception as exc:
            print(exc, '(parser.py get_data line 42).')
            host = ""

        print(host)

        if html and html.status_code == 200:
            soup = BeautifulSoup(html.text, "html.parser")
        else:
            print('Ошибка, не удалось получить доступ к сайту (parser.py get_data line 48).')
            return None

    elif input_type == "File":
        html = get_html_from_file()
        soup = BeautifulSoup(html, "html.parser")
        host = ''

    else:
        return None

    links_li = [link.get('href') for link in soup.find_all('a')]
    img_li = [img.get('src') for img in soup.find_all('img')]

    links_dict = {}
    img_dict = {}

    for link in links_li:
        if len(link) > 0:
            # если ссылка относительная - добавляем к ней хост
            if link[0] == "/":
                link = host + link
            # если сслыка невалидна на самом сайте - пропускаем её
            elif link[0] == "#":
                continue

            # добавление ссылок и контролирование их кол-ва
            if link not in links_dict:
                links_dict[link] = 1
            else:
                links_dict[link] += 1

    for img in img_li:
        if len(img) > 0:
            if img[0] == "#":
                continue

            if img not in img_dict:
                img_dict[img] = 1
            else:
                img_dict[img] += 1

    data = {"Links": links_dict, "ImgLinks": img_dict}
    return data
