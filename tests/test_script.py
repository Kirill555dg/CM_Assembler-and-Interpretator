import os
import sys
import pytest
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from script import assemble, interpret


# Фикстуры для создания временных файлов
@pytest.fixture
def temp_code_file():
    """Создаем временный файл с кодом"""
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
        f.write("LOAD_CONSTANT #582\nWRITE_MEMORY R844\n")  # Пример кода ассемблера
        yield f.name


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


@pytest.fixture
def temp_result_file():
    """Создаем временный файл для сохранения результата интерпретации"""
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
        f.write("<Result>Success</Result>\n")  # Пример файла результата
        yield f.name


# Тесты для функции assemble

def test_assemble_valid_case(temp_code_file, temp_binary_file, temp_log_file):
    """Тест для успешной работы функции assemble с правильными файлами"""
    assemble([temp_code_file, temp_binary_file, temp_log_file])

def test_assemble_missing_code(temp_binary_file, temp_log_file):
    """Тест для несуществующего файла с кодом"""
    with pytest.raises(FileNotFoundError, match="Файл с текстом исходной программы не найден"):
        assemble(["nonexistent_code.asm", temp_binary_file, temp_log_file])


def test_assemble_missing_log(temp_code_file, temp_binary_file):
    """Тест для assemble с отсутствующим лог-файлом"""
    with pytest.raises(FileNotFoundError, match="Лог-файл не найден"):
        assemble([temp_code_file, temp_binary_file, "nonexistent_log.xml"])

def test_assemble_missing_bin(temp_code_file, temp_log_file):
    """Тест для assemble с отсутствующим бинарным файлом"""
    with pytest.raises(FileNotFoundError, match="Бинарный файл не найден"):
        assemble([temp_code_file, "nonexistent_binary_data.bin", temp_log_file])

def test_assemble_missing_args(temp_code_file, temp_binary_file):
    """Тест с недостающим количеством аргументов"""
    with pytest.raises(ValueError, match="Введены не все аргументы для корректной работы ассемблера"):
        assemble([temp_code_file, temp_binary_file])


def test_assemble_needless_args(temp_code_file, temp_binary_file, temp_log_file):
    """Тест с избыточным количеством аргументов"""
    with pytest.raises(ValueError, match="Введено неожиданное количество аргументов"):
        assemble([temp_code_file, temp_binary_file, temp_log_file, "smth"])



# Тесты для функции interpret

def test_interpret_missing_args(temp_binary_file):
    """Тест с недостающим количеством аргументов"""
    with pytest.raises(ValueError, match="Введены не все аргументы для корректной работы интерпретатора"):
        interpret([temp_binary_file])


def test_interpret_needless_args(temp_binary_file, temp_result_file):
    """Тест с избыточным количеством аргументов"""
    with pytest.raises(ValueError, match="Введено неожиданное количество аргументов"):
        interpret([temp_binary_file, "0", "10", temp_result_file, "smth"])


def test_interpret_valid_case(temp_binary_file, temp_result_file):
    """Тест для interpret с отсутствующим бинарным файлом"""
    with pytest.raises(FileNotFoundError, match="Бинарный файл не найден"):
        # Передаем правильные границы и файл результата
        interpret(["no_binary_file.bin", "0", "10", temp_result_file])


def test_interpret_invalid_boundaries(temp_binary_file, temp_result_file):
    """Тест для интерпретатора с неверными границами памяти"""
    with pytest.raises(SystemExit) as excinfo:
        interpret([temp_binary_file, "left", "10", temp_result_file])

    assert excinfo.value.code == 1

