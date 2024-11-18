# Описание
Этот проект включает в себя два компонента: **Ассемблер** и **Интерпретатор** для учебной виртуальной машины (УВМ). Целью разработки является создание системы, которая позволяет преобразовывать текстовые программы в машинный байт-код (с помощью ассемблера) и затем выполнять их на виртуальной машине (с помощью интерпретатора). Проект реализует несколько полезных инструментов для работы с бинарными программами и логами в формате XML.

## Ассемблер
Ассемблер принимает на вход текстовую программу, написанную с использованием команд УВМ, и генерирует бинарный файл, который можно выполнить на виртуальной машине. Помимо бинарного файла, ассемблер также генерирует лог-файл в формате XML, в котором каждая ассемблированная команда представлена в виде списка "ключ=значение".

## Интерпретатор
Интерпретатор принимает бинарный файл, созданный ассемблером, и выполняет программу на виртуальной машине. В процессе выполнения интерпретатор сохраняет значения из заданного диапазона памяти УВМ в выходной файл, который также записывается в формате XML.


# Запуск ассемблера и интерпретатора

Проект содержит файл ```script.py```, который позволяет запускать либо ассемблер, либо интерпретатор.

## Запуск ассемблера:
```bash
py [path]/script.py assemble [code_path] [binary_file_path] [log_file_path]
```

Где:

- **path** -- Путь до директории со скриптом,
- **code_path** -- Путь до файла с кодом для ассемблера,
- **binary_file_path** -- Путь до бинарного файла,
- **log_file_path** -- Путь до лог-файла.

## Запуск интерпретатора:
```bash
py [path]/script.py interpret [binary_file_path] [left_bound] [right_bound] [result_file_path]
```

Где:

- **path** -- Путь до директории со скриптом,
- **binary_file_path** -- Путь до бинарного файла,
- **left_bound** и **right_bound** -- Диапазон адрессов памяти УВМ, целые числа,
- **result_file_path** -- Опциональный аргумент, путь до файла с результатом.

# Команды ассемблера

## Загрузка константы
Размер команды: 5 байт.

Номер команды: 6

Операнд: целочисленное поле в формате ```#значение``` от $0$ до $2^{30} - 1$. 

Результат: регистр-аккумулятор.
```bash
LOAD_CONSTANT #582
```
Байт-код для примера выше:
```0x36, 0x12, 0x00, 0x00, 0x00 ```
## Чтение из памяти
Размер команды: 2 байта.

Номер команды: 3.

Операнд: ячейка памяти по адресу в формате ```Rадрес``` от $0$ до $2^{12} - 1$. 

Результат: регистр-аккумулятор.
```bash
READ_MEMORY R528
```
Байт-код для примера выше:
```0x83, 0x10```

## Запись в память
Размер команды: 2 байта.

Номер команды: 5.

Операнд: регистр-аккумулятор.

Результат: ячейка памяти по адресу в формате ```Rадрес``` от $0$ до $2^{12} - 1$.
```bash
WRITE_MEMORY R844
```
Байт-код для примера выше:
```0x65, 0x1A```
## Унарная операция: побитовое "не"
Размер команды: 1 байт.

Номер команды: 1.

Операнд: регистр-аккумулятор.

Результат: регистр-аккумулятор.
```bash
BITWISE_NOT
```
Байт-код для примера выше:
```0x01```
# Тестовая программа

В папке ```test_programm``` написана тестовая программа, в которой выполнено поэлементно операцию побитовое "не" над вектором длины 6. Результат записан в исходный вектор.

# Тесты

Для всех методов были написаны тесты, в результате удалось добиться покрытия в 86%.
Также нужно убедиться, что на устройстве установлена библиотеки ```pytest``` и ```coverage```

### Для генерации отчета о покрытии тестами необходимо выполнить команду:

```shell
coverage run --branch -m pytest tests/
```

### Просмотр результатов покрытия:

```shell
coverage report
```

## Процент покрытия:
![image](https://github.com/user-attachments/assets/dd1fa3ea-f8a0-4187-8b34-0c2b790fcf24)

