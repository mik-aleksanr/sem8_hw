"""
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной

Урок 8. Работа с файлами.
Дополнить справочник возможностью копирования данных из одного файла в другой.
Пользователь вводит номер строки, которую необходимо перенести из одного файла в другой.
Формат сдачи: ссылка на пулл в свой репозиторий.
"""

from os.path import exists
from csv import DictReader, DictWriter


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


class NameErrors(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_info():
    global first_name, last_name, phone_number
    is_valid_first_name = False
    while not is_valid_first_name:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameErrors("Не валидное имя")
            else:
                is_valid_first_name = True
        except NameErrors as err:
            print(err)
            continue

    is_valid_last_name = False
    while not is_valid_last_name:
        try:
            last_name = input("Введите фамилию: ")
            if len(last_name) < 2:
                raise NameErrors("Не валидное имя")
            else:
                is_valid_last_name = True
        except NameErrors as err:
            print(err)
            continue

    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера")
            else:
                is_valid_phone = True
        except ValueError:
            print("Не валидный номер!!!")
            continue
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, last_name, phone_number]


def create_file(file):
    # with - Менеджер контекста
    with open(file, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()


def read_file(file):
    with open(file, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file, lst):
    res = read_file(file)
    for el in res:
        if el["Телефон"] == str(lst[2]):
            print("Такой телефон уже есть")
            return

    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}
    res.append(obj)
    with open(file, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)


# Данная функция производит копирование файлов
def file_to_copy(f_obj, c_file, num):
    if num is None:  # если номер строки не вводится, произойдет копирование содержимого всего файла,
        # с удалением старой информации
        with open(c_file, "w", encoding='utf-8', newline='') as data:
            f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
            f_writer.writeheader()
            f_writer.writerows(f_obj)
    else:
        # в противном случае, копируем указанную строку с добавлением в файл
        with open(c_file, "a", encoding='utf-8', newline='') as data:
            f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
            f_writer.writerow(f_obj[num])
    print('Копирование завершено')


# Функция производит удаление файла или строки
def file_to_del(f_obj, d_file, num):
    if num is None:  # если номер строки не вводится, произойдет удаление содержимого всего файла,
        f_obj = []
        with open(d_file, "w", encoding='utf-8', newline='') as data:
            f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
            f_writer.writeheader()
            f_writer.writerows(f_obj)
    else:
        # в противном случае, удаляем указанную строку с добавлением в файл
        f_obj.pop(num)
        print(f_obj)
        with open(d_file, "w", encoding='utf-8', newline='') as data:
            f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
            f_writer.writeheader()
            f_writer.writerows(f_obj)
    print('Удаление завершено')


file_name = 'phone.csv'


def main():
    while True:
        command = input("Введите команду: ")
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == 'r':
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            print(*read_file(file_name))
        elif command == 'c':  # Команда для операции копирования
            file = input('Введите имя копируемого файла: ')
            if not exists(file):
                print("Файл отсутствует")
                continue
            obj_lst = read_file(file)  # открываем файл для чтения
            print(obj_lst)
            try:
                num_row = int(input('Ведите номер копируемой строки: '))
            except ValueError:
                num_row = None
            file_copy = input('Введите имя файла в который будете копировать: ')
            if not exists(file_copy):
                create_file(file_copy)
            file_to_copy(obj_lst, file_copy, num_row)
        elif command == 'd':  # Команда для операции удаления
            del_file = input('Введите имя файла для удаления: ')
            if not exists(del_file):
                print("Файл отсутствует")
                continue
            obj_lst = read_file(del_file)  # открываем файл для чтения
            print(obj_lst)
            try:
                num_row = int(input('Ведите номер удаляемой строки: '))
            except ValueError:
                num_row = None
            file_to_del(obj_lst, del_file, num_row)


main()
