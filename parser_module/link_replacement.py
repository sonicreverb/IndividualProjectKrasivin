from main import BASE_DIR
import os


def validator(data):
    validatorspath = os.path.join(BASE_DIR, 'parser_module', 'prohibited_sites.txt')

    if os.path.exists(validatorspath):
        with open(validatorspath, 'r', encoding='UTF-8') as r:
            # todo добавить бан всех сайта, имеющихся в data по хосту
            for link in r.read().split():
                if link in data['Links']:
                    while data['Links'][link]:
                        if '[запрещённая ссылка]' in data['Links']:
                            data['Links']['[запрещённая ссылка]'] += 1
                        else:
                            data['Links']['[запрещённая ссылка]'] = 1

                        data['Links'][link] -= 1

                    data['Links'].pop(link)

                if link in data['ImgLinks']:
                    while data['ImgLinks'][link] > 0:
                        if '[запрещённая ссылка]' in data['ImgLinks']:
                            data['ImgLinks']['[запрещённая ссылка]'] += 1
                        else:
                            data['ImgLinks']['[запрещённая ссылка]'] = 1

                        data['ImgLinks'][link] -= 1
                    data['ImgLinks'].pop(link)
    else:
        with open(validatorspath, 'w'):
            pass


def links_replacement():
    pass
