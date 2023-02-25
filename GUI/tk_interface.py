from tkinter import *
from main import BASE_DIR
from PIL import Image, ImageTk
from parser_module import parser, link_replacement
from datetime import datetime
import os

root = Tk()

# характеристики окна
root.title('HTML парсер')
root.geometry("800x600")
root.resizable(width=False, height=False)

# favicon для приложения
ico = Image.open(os.path.join(BASE_DIR, 'GUI', 'favicon.png'))
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(True, photo)

# поля ввода и его значение для передачи в функции
url_value = StringVar()
url_entry = Entry(textvariable=url_value, width=30)
url_entry.insert(0, "здесь могла быть ваша ссылка")

url_origin_link = StringVar()
url_new_link = StringVar()

url_origin_link_entry = Entry(textvariable=url_origin_link, width=30)
url_origin_link_entry.insert(0, "исходная ссылка")

url_new_link_entry = Entry(textvariable=url_new_link, width=30)
url_new_link_entry.insert(0, "новая ссылка")


# label текущего состояния программы
state_label = Label()


def pop_up_result_window():
    path = os.path.join(BASE_DIR, 'parser_module', 'text_data', 'result_data.txt')
    os.system(path)


def pop_up_prohibited_sites_window():
    path = os.path.join(BASE_DIR, 'parser_module', 'text_data', 'prohibited_sites.txt')
    os.system(path)


def pop_up_html_file_window():
    path = os.path.join(BASE_DIR, 'parser_module', 'text_data', 'html_input.txt')
    os.system(path)


def get_data_from_url():
    data = parser.get_data("URL", url_value.get())

    if data:
        link_replacement.validator(data)
        parser.write_data_to_txt(data)
        state_label.configure(text=f"Программа выполнена успешно {str(datetime.now())[:-7]}.")
        pop_up_result_window()
        return data
    else:
        state_label.configure(text="Программе не удалось выполнить парсинг, проверьте корректность введённых данных.")


def get_data_from_html():
    data = parser.get_data("File")

    if data:
        link_replacement.validator(data)
        parser.write_data_to_txt(data)
        state_label.configure(text=f"Программа выполнена успешно {str(datetime.now())[:-7]}.")
        pop_up_result_window()
        return data
    else:
        state_label.configure(text="Программе не удалось выполнить парсинг, проверьте корректность файла ввода.")


def change_blacklist():
    try:
        pop_up_prohibited_sites_window()
        state_label.configure(text=f"Список запрещённых сайтов успешно изменён {str(datetime.now())[:-7]}.")
    except Exception as exc:
        print(exc, 'tk_interface.py change_blacklist line 67')
        state_label.configure(text="Программе не удалось изменить список запрещённых сайтов.")


def change_htmlfile():
    try:
        pop_up_html_file_window()
        state_label.configure(text=f"HTML файл успешно изменён {str(datetime.now())[:-7]}.")
    except Exception as exc:
        print(exc, 'tk_interface.py change_blacklist line 67')
        state_label.configure(text="Программе не удалось изменить HTML файл.")


def change_link_in_htmlfile():
    origin_link = url_origin_link.get()
    new_link = url_new_link.get()

    try:
        if link_replacement.links_replacement(origin_link, new_link):
            state_label.configure(text=f"Ссылка в HTML файле успешно изменена {str(datetime.now())[:-7]}.")
        else:
            state_label.configure(text="Невозможно произвести замену, так как исходная ссылка не найдена в HTML.")
    except Exception as exc:
        print(exc, 'in change_link_in_htmlfile line 103')
        state_label.configure(text="Программе не удалось заменить ссылки в HTML файле.")


start_parser_by_link_button = Button(text="Начать парсинг по ссылке", command=get_data_from_url, width=30)
start_parser_by_file_button = Button(text="Начать парсинг из файла", command=get_data_from_html, width=30)
change_blacklist_button = Button(text="Изменить список запрещённых сайтов", command=change_blacklist, width=30)
change_htmlfile_button = Button(text="Изменить HTML код", command=change_htmlfile, width=30)
change_link_in_htmlfile_button = Button(text="Заменить ссылку в HTML файле", command=change_link_in_htmlfile, width=30)

# расположение элементов в окне
url_entry.pack(pady=150)
start_parser_by_link_button.pack()
start_parser_by_file_button.pack()
change_htmlfile_button.pack()
change_blacklist_button.pack()
state_label.pack(side=BOTTOM)
change_link_in_htmlfile_button.pack(side=BOTTOM, pady=20)
url_new_link_entry.pack(side=BOTTOM)
url_origin_link_entry.pack(side=BOTTOM)

