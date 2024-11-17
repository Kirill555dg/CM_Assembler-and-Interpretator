import xml.etree.ElementTree as ET
from datetime import datetime


class Assembler:
    def __init__(self, path_to_code, path_to_binary_file, path_to_log):
        self.binary_file_path = path_to_binary_file
        self.code_path = path_to_code
        self.log_path = path_to_log

        self.bytes = []

        try:
            self.log_file = ET.parse(path_to_log)
            self.xml = ET.SubElement(self.log_file.getroot(),
                                     "log_info_" + datetime.now().isoformat(timespec='minutes').replace(':', '.'))
        except ET.ParseError:
            self.log_file = ET.ElementTree(ET.Element("logs"))
            self.xml = ET.SubElement(self.log_file.getroot(),
                                     "log_info_" + datetime.now().isoformat(timespec='minutes').replace(':', '.'))


    def load_constant(self, B):
        """Кодирует команду LOAD_CONSTANT в байты"""
        if not (0 <= B < (1 << 30)):
            raise ValueError("Константа должна быть в пределах от 0 до 2^30-1")
        bits = (B << 3) | 6
        bits = bits.to_bytes(5, byteorder="little")
        log = ET.SubElement(self.xml, 'LOAD_CONSTANT')
        log.attrib['A'] = "6"
        log.attrib['B'] = str(B)
        log.text = bits.hex()
        return bits

    def read_memory(self, B):
        """Кодирует команду READ_MEMORY в байты"""
        if not (0 <= B < (1 << 12)):
            raise ValueError("Адрес ячейки памяти должен быть в пределах от 0 до 2^12-1")
        bits = (B << 3) | 3
        bits = bits.to_bytes(2, byteorder="little")
        log = ET.SubElement(self.xml, 'READ_MEMORY')
        log.attrib['A'] = "3"
        log.attrib['B'] = str(B)
        log.text = bits.hex()
        return bits

    def write_memory(self, B):
        """Кодирует команду WRITE_MEMORY в байты"""
        if not (0 <= B < (1 << 12)):
            raise ValueError("Адрес ячейки памяти должен быть в пределах от 0 до 2^12-1")
        bits = (B << 3) | 5
        bits = bits.to_bytes(2, byteorder="little")
        log = ET.SubElement(self.xml, 'WRITE_MEMORY')
        log.attrib['A'] = "5"
        log.attrib['B'] = str(B)
        log.text = bits.hex()
        return bits

    def bitwise_not(self):
        """Кодирует команду BITWISE_NOT в байты"""
        bits = 1
        bits = bits.to_bytes(1, byteorder="little")
        log = ET.SubElement(self.xml, 'BITWISE_NOT')
        log.attrib['A'] = "1"
        log.text = bits.hex()
        return bits

    def assemble(self):
        """Считывает входной файл с кодом и обрабатывает команды в байты"""

        with open(self.code_path, "rt") as code:

            for line in code:
                line = line.split(';')[0].strip()
                if not line: continue

                command, *args = line.split(maxsplit=1)

                match command:
                    case "LOAD_CONSTANT":
                        if len(args) != 1:
                            raise ValueError(
                                f"{line}\nУ операции загрузки константы должен быть 1 аргумент: значение константы")

                        constant = args[0]
                        if constant[0] != "#":
                            raise ValueError(
                                f"{line}\n{args[0]}: константа должна быть записана в формате \"#значение\"")

                        constant = constant[1:]

                        if not constant:
                            raise ValueError(f"{line}\n{args[0]}: пропущено значение константы")

                        self.bytes.append(self.load_constant(int(constant)))

                    case "READ_MEMORY":
                        if len(args) != 1:
                            raise ValueError(
                                f"{line}\nУ операции чтении из памяти должен быть 1 аргумент: адрес ячейки памяти")

                        address = args[0]
                        if address[0] != "R":
                            raise ValueError(
                                f"{line}\n{args[0]}: адрес ячейки памяти должен записываться в формате \"Rномер\"")

                        address = address[1:]

                        if not address:
                            raise ValueError(f"{line}\n{args[0]}: пропущен номер адреса ячейки памяти")

                        self.bytes.append(self.read_memory(int(address)))

                    case "WRITE_MEMORY":
                        if len(args) != 1:
                            raise ValueError(
                                f"{line}\nУ операции чтении из памяти должен быть 1 аргумент: адрес ячейки памяти")

                        address = args[0]
                        if address[0] != "R":
                            raise ValueError(
                                f"{line}\n{args[0]}: адрес ячейки памяти должен записываться в формате \"Rномер\"")

                        address = address[1:]

                        if not address:
                            raise ValueError(f"{line}\n{args[0]}: пропущен номер адреса ячейки памяти")

                        self.bytes.append(self.write_memory(int(address)))

                    case "BITWISE_NOT":
                        if args:
                            raise ValueError(f"{line}\nУ операции побитового \"не\" не должно быть аргументов")

                        self.bytes.append(self.bitwise_not())

                    case _:
                        raise ValueError(f"{line}\nНеизвестная команда")

        self.log_file.write(self.log_path)

    def to_binary_file(self):

        with open(self.binary_file_path, "wb") as binary:
            for byte in self.bytes:
                binary.write(byte)


if __name__ == "__main__": # Для тестирования
    path_to_code = "files/code.asm"
    path_to_binary_file = "files/binary_data.bin"
    path_to_log = "files/log.xml"

    assembler = Assembler(path_to_code, path_to_binary_file, path_to_log)
    try:
        assembler.assemble()
    except ValueError as e:
        print(e)
    assembler.to_binary_file()
