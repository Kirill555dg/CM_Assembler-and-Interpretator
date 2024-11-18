from sys import argv
from os.path import exists
from assembler import Assembler
from interpreter import Interpreter


def assemble(args):
    if len(args) < 3:
        raise ValueError('Введены не все аргументы для корректной работы ассемблера')

    if len(args) > 3:
        raise ValueError('Введено неожиданное количество аргументов')

    path_to_code = args[0]
    path_to_binary_file = args[1]
    path_to_log = args[2]

    if not exists(path_to_code):
        raise FileNotFoundError('Файл с текстом исходной программы не найден')

    if not exists(path_to_binary_file):
        raise FileNotFoundError('Бинарный файл не найден')

    if not exists(path_to_log):
        raise FileNotFoundError('Лог-файл не найден')

    assembler = Assembler(path_to_code, path_to_binary_file, path_to_log)
    try:
        assembler.assemble()
    except SyntaxError as e:
        print("Ошибка синтаксиса кода")
        print(e)
        exit(1)
    except ValueError as e:
        print("Недопустимое значение в программе")
        print(e)
        exit(1)


def interpret(args):
    if len(args) < 3:
        raise ValueError('Введены не все аргументы для корректной работы интерпретатора')

    if len(args) > 4:
        raise ValueError('Введено неожиданное количество аргументов')

    path_to_binary_file = args[0]
    left_boundary = args[1]
    right_boundary = args[2]
    path_to_result_file = args[3] if len(args) == 4 else "files/result.xml"

    if not exists(path_to_binary_file):
        raise FileNotFoundError('Бинарный файл не найден')

    try:
        left_boundary, right_boundary = int(left_boundary), int(right_boundary)
    except ValueError:
        print('Границы диапазона памяти УВМ должны быть заданы целыми числами')
        exit(1)

    interpreter = Interpreter(path_to_binary_file, left_boundary, right_boundary, path_to_result_file)

    try:
        interpreter.interpret()
    except ValueError as e:
        print("Ошибка при чтении файла")
        print(e)
        exit(1)


if __name__ == '__main__':
    if len(argv) < 2:
        print('Для запуска скрипта необходимо ввести assemble или interpret с соответствующими аргументами')
    try:
        match argv[1]:
            case 'assemble':
                assemble(argv[2:])
            case 'interpret':
                interpret(argv[2:])
            case wrong:
                print('Для запуска скрипта необходимо ввести assemble или interpret с соответствующими аргументами')
                exit(1)
    except FileNotFoundError as e:
        print(e)
        exit(1)
    except ValueError as e:
        print(e)
        exit(1)
