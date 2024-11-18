import os
import sys
import pytest
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from assembler import Assembler


# Фикстуры для создания временных файлов


@pytest.fixture
def temp_binary_file():
    """Создаем временный бинарный файл"""
    with tempfile.NamedTemporaryFile(delete=False, mode="wb") as f:
        f.write(b"\x83\x10")  # Пример бинарных данных
        yield f.name


@pytest.fixture
def temp_log_file():
    """Создаем временный лог-файл"""
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
        f.write("<logs>smth</logs>\n")  # Пример лог-файла
        yield f.name


# Тесты команд

def test_load_constant(temp_binary_file, temp_log_file):
    filename = 'test_file.txt'

    # Создаем файл
    with open(filename, 'w') as f:
        f.write("LOAD_CONSTANT #582")

    assembler = Assembler(filename, temp_binary_file, temp_log_file)

    assembler.assemble()
    bytes = assembler.bytes[0].hex()
    assert bytes == "3612000000"
    os.remove(filename)


def test_read_memory(temp_binary_file, temp_log_file):
    filename = 'test_file.txt'

    # Создаем файл
    with open(filename, 'w') as f:
        f.write("READ_MEMORY R528")

    assembler = Assembler(filename, temp_binary_file, temp_log_file)

    assembler.assemble()
    bytes = assembler.bytes[0].hex()
    assert bytes == "8310"
    os.remove(filename)


def test_write_memory(temp_binary_file, temp_log_file):
    filename = 'test_file.txt'

    # Создаем файл
    with open(filename, 'w') as f:
        f.write("WRITE_MEMORY R844")

    assembler = Assembler(filename, temp_binary_file, temp_log_file)

    assembler.assemble()
    bytes = assembler.bytes[0].hex()
    assert bytes == "651a"
    os.remove(filename)


def test_bitwise_not(temp_binary_file, temp_log_file):
    filename = 'test_file.txt'

    # Создаем файл
    with open(filename, 'w') as f:
        f.write("BITWISE_NOT")

    assembler = Assembler(filename, temp_binary_file, temp_log_file)

    assembler.assemble()
    bytes = assembler.bytes[0].hex()
    assert bytes == "01"
    os.remove(filename)


# Тесты на ошибки

def test_command_error(temp_binary_file, temp_log_file):
    filename = 'test_file.txt'

    commands = [
        "WRITE_MEMORY R16384",
        "READ_MEMORY R16384",
        "LOAD_CONSTANT #4294967296"
    ]

    for i, command in enumerate(commands):

        with open(filename, 'w') as f:
            f.write(command)

        with pytest.raises(ValueError):
            assembler = Assembler(filename, temp_binary_file, temp_log_file)
            assembler.assemble()

    os.remove(filename)


def test_assembler_code_error(temp_binary_file, temp_log_file):
    filename = 'test_file.txt'

    # Создаем файл
    with open(filename, 'w') as f:
        f.write("COMMAND LINE")

    with pytest.raises(SyntaxError, match="COMMAND LINE\nНеизвестная команда"):
        assembler = Assembler(filename, temp_binary_file, temp_log_file)
        assembler.assemble()

    os.remove(filename)

