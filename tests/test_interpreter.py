import os
import sys
import pytest
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from interpreter import Interpreter


@pytest.fixture
def temp_result_file():
    """Создаем временный файл для сохранения результата интерпретации"""
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
        f.write("<Result>Success</Result>\n")  # Пример файла результата
        yield f.name


def test_byte_code_read(temp_result_file):
    filename = 'test_file.bin'

    # Создаем файл
    with open(filename, 'wb') as f:
        f.write(b"\x36\x12\x00\x00\x00\x65\x1a\x83\x10\x36\x12\x00\x00\x00\x01\x01")

    interpreter = Interpreter(filename, 0, 1024, temp_result_file)
    interpreter.interpret()

    assert interpreter.accumulator_register == 582
    assert interpreter.registers[844] == 582

    os.remove(filename)


def test_byte_code_error(temp_result_file):
    filename = 'test_file.bin'

    # Создаем файл
    with open(filename, 'wb') as f:
        f.write(b"\x01\x02\x03\x04\x05")

    with pytest.raises(ValueError, match="В бинарном файле содержатся невалидные данные: неверный байт-код"):
        interpreter = Interpreter(filename, 0, 1024, temp_result_file)
        interpreter.interpret()

    os.remove(filename)


def test_byte_code_write_ouf_of_bounds(temp_result_file):
    filename = 'test_file.bin'

    # Создаем файл
    with open(filename, 'wb') as f:
        f.write(b"\xf5\xff")

    with pytest.raises(ValueError,
                       match="В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона"):
        interpreter = Interpreter(filename, 0, 1024, temp_result_file)
        interpreter.interpret()

    os.remove(filename)


def test_byte_code_read_ouf_of_bounds(temp_result_file):
    filename = 'test_file.bin'

    # Создаем файл
    with open(filename, 'wb') as f:
        f.write(b"\xf3\xff")

    with pytest.raises(ValueError,
                       match="В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона"):
        interpreter = Interpreter(filename, 0, 1024, temp_result_file)
        interpreter.interpret()

    os.remove(filename)
