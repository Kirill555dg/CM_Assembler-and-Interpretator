import xml.etree.ElementTree as ET


class Interpreter:

    def __init__(self, path_to_binary_file, left_boundary, right_boundary):

        self.boundaries = (left_boundary, right_boundary)
        self.registers = [0] * (right_boundary - left_boundary + 1)
        self.accumulator_register = 0

        with open(path_to_binary_file, 'rb') as binary_file:
            self.byte_code = int.from_bytes(binary_file.read(), byteorder="little")
            print(self.byte_code)

    def interpret(self):
        while self.byte_code != 0:
            a = self.byte_code & ((1 << 3) - 1)
            match a:
                case 6:
                    self.load_constant()
                case 3:
                    self.read_memory()
                case 5:
                    self.write_memory()
                case 1:
                    self.bitwise_not()
                case _:
                    raise ValueError("В бинарном файле содержатся невалидные данные: неверный байт-код")

        self.make_result()

    def load_constant(self):
        B = (self.byte_code & ((1 << 32) - 1)) >> 3
        self.byte_code >>= 40
        self.accumulator_register = B
        print("load_constant")


    def read_memory(self):
        B = (self.byte_code & ((1 << 14) - 1)) >> 3
        self.byte_code >>= 16

        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")

        self.accumulator_register = self.registers[B-self.boundaries[0]]
        print("read_memory")


    def write_memory(self):
        B = (self.byte_code & ((1 << 14) - 1)) >> 3
        self.byte_code >>= 16

        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")

        self.registers[B - self.boundaries[0]] = self.accumulator_register
        print("write_memory")


    def bitwise_not(self):
        self.accumulator_register = ~self.accumulator_register
        self.byte_code >>= 8
        print("bitwise_not")


    def make_result(self):
        pass
