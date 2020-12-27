import socket
import time
import requests
from datetime import datetime

import RPi.GPIO as GPIO

from printer import Printer

APP_VERSION = "1.0"


class App:
    def __init__(self, endpoint_url, token, terminal_id="Terminal 01", terminal_location="Schule", pin=4):

        self.endpoint_url = endpoint_url
        self.token = token
        self.terminal_id = terminal_id
        self.terminal_location = terminal_location
        self.pin = pin
        self.close_requested = False
        self.is_pressing_button = False
        self.printer = Printer(port='/dev/serial0')

    def init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def init_printer(self):
        self.printer.character_set(0x02)
        self.printer.justify_center()
        self.printer.println('-= UniFi Voucher Terminal Version ' + APP_VERSION + ' =-')
        self.printer.println('-= Developed by Oliver Enes  =-')
        self.printer.justify_left()
        self.printer.println('')
        self.printer.println('Terminal ID: ' + self.terminal_id)
        self.printer.println('Terminal Standort: ' + self.terminal_location)
        self.printer.println('Host:' + socket.gethostname())
        self.printer.println('Endpoint: ' + self.endpoint_url)
        if self.is_site_up():
            self.printer.println("Endpoint reachable.")
        else:
            self.printer.println("! Endpoint not available !")
        self.printer.println('ready.')
        self.printer.cut()

    def init(self):
        self.init_gpio()
        self.init_printer()

    def print_voucher(self, voucher, qrcode_data, prependix, appendix):
        self.printer.justify_center()
        self.printer.println(prependix)
        if qrcode_data:
            self.printer.println('')
            self.printer.qrcode_size(0x9)
            self.printer.store_qrcode_data(qrcode_data)
            self.printer.print_qrcode()
        self.printer.println('')
        self.printer.bold_on()
        self.printer.println('Code')
        self.printer.bold_on()
        self.printer.double_height_on()
        self.printer.println(voucher)
        self.printer.double_height_off()
        self.printer.println('')
        self.printer.println("Zeitpunkt der Erstellung:")
        self.printer.println(datetime.today().strftime('%d.%m.%Y %H:%M'))
        self.printer.character_set(1)
        self.printer.println(appendix)
        self.printer.cut()

    def print_error(self, error):
        self.printer.bold_on()
        self.printer.double_height_on()
        self.printer.println("ERROR: " + error)
        self.printer.cut()
        self.printer.bold_off()
        self.printer.double_height_off()

    def is_site_up(self):
        tries = 0
        while tries < 12:
            try:
                conn = requests.get(self.endpoint_url)
                return True
            except:
                pass
            finally:
                time.sleep(5)  # wait for network
                tries = tries + 1
        return True

    def on_voucher_request(self):
        try:
            result = requests.post(self.endpoint_url, {'token': self.token})
            if result.status_code == 200:
                json = result.json()
                self.print_voucher(json['voucher'], json['qrcodeData'], json['prependix'], json['appendix'])
            else:
                self.print_error(result.json()['error'])
        except Exception as e:
            self.print_error('Voucher Anfrage fehlgeschlagen: ' + str(e))

    def run(self):
        self.init()
        while not self.close_requested:
            try:
                if GPIO.input(self.pin):
                    self.is_pressing_button = True
                else:
                    if self.is_pressing_button:
                        self.is_pressing_button = False
                        self.on_voucher_request()
            except Exception as e:  # catch all exceptions
                print(e)
            time.sleep(0.25)  # cooldown
