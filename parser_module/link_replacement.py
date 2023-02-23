import re
import os
from main import BASE_DIR


def validator(data):
    validatorspath = os.path.join(BASE_DIR, 'parser_module', 'prohibited_sites.txt')

    if os.path.exists(validatorspath):
        with open(validatorspath, 'r', encoding='UTF-8') as r:
            # todo добавить бан всех сайта, имеющихся в data по хосту
            for link in r.read().split():
                for full_link in list(data['Links']):
                    if link in full_link:
                        while data['Links'][full_link]:
                            if '[запрещённая ссылка]' in data['Links']:
                                data['Links']['[запрещённая ссылка]'] += 1
                            else:
                                data['Links']['[запрещённая ссылка]'] = 1

                            data['Links'][full_link] -= 1

                        data['Links'].pop(full_link)

                for full_img_link in list(data["ImgLinks"]):
                    if link in full_img_link:
                        while data['ImgLinks'][full_img_link]:
                            if '[запрещённая ссылка]' in data['ImgLinks']:
                                data['ImgLinks']['[запрещённая ссылка]'] += 1
                            else:
                                data['ImgLinks']['[запрещённая ссылка]'] = 1

                            data['ImgLinks'][full_img_link] -= 1
                        data['ImgLinks'].pop(full_img_link)
    else:
        with open(validatorspath, 'w'):
            pass


def links_replacement(origin_link, new_link):
    html_file_path = os.path.join(BASE_DIR, 'parser_module', 'input.html')
    if os.path.exists(html_file_path):
        html = open(html_file_path, 'wr', encoding='utf-8')
        if origin_link in html.read():
            html.write(re.sub(origin_link, new_link, origin_link))
        else:
            print("Ошибка, невозможно произвести замену, так как исходной ссылку нет в HTML, (link_replacement.py"
                  "links_replacement line 42).")

    else:
        print("Ошибка, невозможно произвести замену, так как файла с HTML не существует, (link_replacement.py"
              "links replacement line 40).")
        with open(html_file_path, 'w'):
            pass
        return None
