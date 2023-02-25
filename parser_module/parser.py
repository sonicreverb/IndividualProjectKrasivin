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
    html_file_path = os.path.join(BASE_DIR, 'parser_module', 'text_data', 'html_input.txt')

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


def get_data(input_type, url=None):
    if input_type == "URL" and url:
        html = get_html_from_url(url)

        if url.count('/') != 2:
            # находим вхождение / в ссылке, для того чтобы получить хост сайта
            try:
                url_cut_to_index = [_.start() for _ in re.finditer('/', url)][2]
                host = url[:url_cut_to_index]
            except Exception as exc:
                print(exc, '(parser.py get_data line 42).')
                host = ""
        else:
            host = url

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
        if link and len(link) > 0:
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

    # тот же самый алгоритм для ссылок на изображения
    for img in img_li:
        if img and len(img) > 0:
            if img[0] == "/":
                img = host + img
            if img[0] == "#":
                continue

            if img not in img_dict:
                img_dict[img] = 1
            else:
                img_dict[img] += 1

    data = {"Links": links_dict, "ImgLinks": img_dict}
    return data


def write_data_to_txt(data):
    result_path = os.path.join(BASE_DIR, 'parser_module', 'text_data', 'result_data.txt')

    with open(result_path, 'w', encoding='UTF-8') as w:
        if len(data['Links']) != 0:
            w.write("Ссылки, встречающиеся в данном HTML коде:\n")
            for link in data['Links']:
                w.write(str(link + " - " + str(data['Links'][link]) + "\n"))
        else:
            w.write("Ссылок, встречающихся в данном HTML коде не найдено...\n")
        w.write('\n')

        if len(data['ImgLinks']) != 0:
            w.write("Ссылки на изображения, встречающиеся в данном HTML коде:\n")
            for img in data['ImgLinks']:
                w.write(str(img + " - " + str(data['ImgLinks'][img]) + "\n"))
        else:
            w.write("Ссылок на изображения, встречающихся в данном HTML коде не найдено...\n")