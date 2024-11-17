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
    assembler.assemble()
    assembler.to_binary_file()


def interpret():
    if len(argv) < 4:
        print('Введены не все аргументы для корректной работы ассемблера')
        return

    path_to_bin = argv[2]
    limitation = argv[3]

    if not exists(path_to_bin):
        print('Файла с таким именем не существует')
        return

    try:
        limitation = int(limitation)
    except ValueError:
        print('Ограничение должно быть задано целым числом')
        return

    my_interpreter = Interpreter(path_to_bin, limitation)
    my_interpreter.interpret()


if __name__ == '__main__':
    if len(argv) < 2:
        print('Не введено имя подпрограммы для исполнения')
    match argv[1]:
        case 'assemble':
            assemble()
        case 'interpret':
            interpret()
