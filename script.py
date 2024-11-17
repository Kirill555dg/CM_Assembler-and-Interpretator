from sys import argv
from os.path import exists
from assembler import Assembler
from interpreter import Interpreter


def assemble():
    if len(argv) < 5:
        print('Введены не все аргументы для корректной работы ассемблера')
        exit(1)

    path_to_code = argv[2]
    path_to_binary_file = argv[3]
    path_to_log = argv[4]

    if not exists(path_to_code):
        print('Файл с текстом исходной программы не найден')
        exit(1)

    if not exists(path_to_binary_file):
        print('Бинарный файл не найден')
        exit(1)

    if not exists(path_to_log):
        print('Лог-файл не найден')
        exit(1)

    assembler = Assembler(path_to_code, path_to_binary_file, path_to_log)
    try:
        assembler.assemble()
    except ValueError as e:
        print(e)
        exit(1)

    assembler.to_binary_file()


def interpret():
    if len(argv) < 4:
        print('Введены не все аргументы для корректной работы интерпретатора')
        exit(1)

    path_to_binary_file = argv[2]
    left_boundary = argv[3]
    right_boundary = argv[4]

    if not exists(path_to_binary_file):
        print('Бинарный файл не найден')
        exit(1)

    try:
        left_boundary, right_boundary = int(left_boundary), int(right_boundary)
    except ValueError:
        print('Границы диапазона памяти УВМ должны быть заданы целыми числами')
        exit(1)

    interpreter = Interpreter(path_to_binary_file, left_boundary, right_boundary)


    try:
        interpreter.interpret()
    except ValueError as e:
        print(e)
        exit(1)


if __name__ == '__main__':
    if len(argv) < 2:
        print('Для запуска скрипта необходимо ввести assemble или interpret с соответствующими аргументами')
    match argv[1]:
        case 'assemble':
            assemble()
        case 'interpret':
            interpret()
