# Unifi Voucher Terminal

Unifi Voucher Terminal is an inofficial app for voucher code printing by pressing a button using a raspberry pi and an Epson TM88-IV (other serial printers may be supported)

## Installation

Copy the code under "terminal" into the home directory of the pi user. Run setup.sh. Configure app settings under "main.py"

Copy the code under "web" to your unifi controller web server or any other web server. Edit settings under "unifi_terminal.php"


## Usage
Press the button (5V on the "PIN" GPIO) and the printer should print a voucher.