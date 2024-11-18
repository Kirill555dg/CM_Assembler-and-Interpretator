import xml.etree.ElementTree as ET


class Interpreter:

    def __init__(self, path_to_binary_file, left_boundary, right_boundary, path_to_result_file="files/result.xml"):
        self.result_path = path_to_result_file
        self.boundaries = (left_boundary, right_boundary)
        self.registers = [0] * (right_boundary - left_boundary + 1)
        self.accumulator_register = 0

        with open(path_to_binary_file, 'rb') as binary_file:
            self.byte_code = int.from_bytes(binary_file.read(), byteorder="little")

    def interpret(self):
        while self.byte_code != 0:
            a = self.byte_code & ((1 << 3) - 1)
            self.byte_code >>= 3
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
        B = self.byte_code & ((1 << 32) - 1)
        self.byte_code >>= 37
        self.accumulator_register = B

    def read_memory(self):
        B = self.byte_code & ((1 << 12) - 1)
        self.byte_code >>= 13

        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError(
                "В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")

        self.accumulator_register = self.registers[B - self.boundaries[0]]

    def write_memory(self):
        B = self.byte_code & ((1 << 12) - 1)
        self.byte_code >>= 13

        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError(
                "В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")

        self.registers[B - self.boundaries[0]] = self.accumulator_register

    def bitwise_not(self):
        self.accumulator_register = ~self.accumulator_register
        self.byte_code >>= 5

    def make_result(self):
        log_file = ET.ElementTree(ET.Element("Result"))

        element = ET.SubElement(log_file.getroot(), "register")
        element.attrib['type'] = "accumulator"
        element.text = str(self.accumulator_register)

        for pos, register in enumerate(self.registers, self.boundaries[0]):
            element = ET.SubElement(log_file.getroot(), "register")
            element.attrib['type'] = "memory"
            element.attrib['address'] = str(pos)
            element.text = str(register)

        log_file.write(self.result_path)


if __name__ == "__main__":  # Для тестирования
    path_to_binary_file = "files/binary_data.bin"
    interpreter = Interpreter(path_to_binary_file, 0, 1023)
    try:
        interpreter.interpret()
    except ValueError as e:
        print(e)
