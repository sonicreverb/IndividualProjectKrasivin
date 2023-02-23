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

    # если сслыка относительная, то к ней добавляется хост
    index = 0
    while index < (len(links_li)):
        curr_link = links_li[index]
        if curr_link[0] == '/':
            links_li[index] = host + curr_link
    # если ссылка невалидна на самом сайте, удаляем её из нашего массива
        elif curr_link[0] == '#':
            links_li.pop(index)
            index -= 1
        index += 1

    # тот же самый алгоритм для ссылок на изображения
    index = 0
    while index < (len(img_li)):
        curr_link = img_li[index]
        if curr_link[0] == '/':
            img_li[index] = host + curr_link
            if curr_link[0] == '#':
                links_li.pop(index)
                index -= 1
        index += 1

    data = {"Links": links_li, "ImgLinks": img_li}
    return data


print(get_data('File'))
