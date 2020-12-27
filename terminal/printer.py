import serial
from typing import List


class Printer:
    def __init__(self, port, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS):
        self.serial = serial.Serial(port=port,
                                    baudrate=baudrate,
                                    parity=parity,
                                    stopbits=stopbits,
                                    bytesize=bytesize)

    def write(self, values: List[int]):
        self.serial.write(bytearray([byte.to_bytes(1, 'little')[0] for byte in values ]))

    def print(self, dataString):
        self.write([ord(c) for c in dataString])

    def println(self, dataString):
        self.write([ord(c) for c in dataString] + [0x0a])

    def get_status(self):
        self.write([0x10, 0x04, 0x01])
        return self.serial.read(1)

    def feed(self, n: int):
        self.write([0x1B, 0x64, n])

    def line_spacing(self, n):
        self.write([0x1B, 0x32, n])

    def default_line_spacing(self, n):
        self.write([0x1B, 0x32])

    def character_set(self, n):
        self.write([0x1B, 0x52, n])

    def double_height_on(self):
        self.write([0x1B, 0x21, 16])

    def double_height_off(self):
        self.write([0x1B, 0x21, 0])

    def bold_on(self):
        self.write([0x1B, 0x21, 8])

    def bold_off(self):
        self.write([0x1B, 0x21, 0])

    def underline_on(self):
        self.write([0x1B, 0x21, 128])

    def underline_off(self):
        self.write([0x1B, 0x21, 0])

    def reversed_on(self):
        self.write([0x1D, 0x42, 1])

    def reversed_off(self):
        self.write([0x1D, 0x42, 0])

    def justify_left(self):
        self.write([0x1B, 0x61, 0])

    def justify_center(self):
        self.write([0x1B, 0x61, 1])

    def justify_right(self):
        self.write([0x1B, 0x61, 2])

    def barcode_height(self, n):
        self.write([0x1D, 0x68, n])

    def barcode_width(self, n):
        self.write([0x1D, 0x77, n])

    def barcode_number_position(self, n):
        self.write([0x1D, 0x48, n])

    def print_barcode(self, code_type: int, digit_length: int):
        self.write([0x1D, 0x6B, code_type, digit_length])

    # 0x31 or 0x32 or 0x33
    def qrcode_model(self, n=0x32):
        self.write([0x1D, 0x28, 0x6B, 0x04, 0x00, 0x31, 0x41, n, 0x0])

    def qrcode_size(self, n=0x08):
        self.write([0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x43, n])

    # 0x30: 7%, 0x31: 15%, 0x32: 25%, 0x33: 33%
    def qrcode_error_correction(self, n=0x30):
        self.write([0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x45, n])

    def store_qrcode_data(self, data):
        data_size = len(data) + 3
        data_array = [ord(d) for d in data]
        self.write([0x1D, 0x28, 0x6B, data_size % 256, int(data_size / 256), 0x31, 0x50, 0x30] + data_array)

    def print_qrcode(self):
        self.write([0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x51, 0x30])

    def cut(self):
        self.write([0x1D, 0x56, 0x42, 0xA])

