#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi


echo -e "enable_uart=1" >> /boot/config.txt

systemctl stop serial-getty@ttyS0.service
systemctl disable serial-getty@ttyS0.service

systemctl stop serial-getty@serial0.service
systemctl disable serial-getty@serial0.service

systemctl stop serial-getty@ttyAMA0.service
systemctl disable serial-getty@ttyAMA0.service

apt-get install python3
apt-get install python3-pip
pip3 install -r requirements.txt

mkdir -p /var/log/unifi_voucher_printer/
touch /var/log/unifi_voucher_printer/log.log
chmod 777 /var/log/unifi_voucher_printer/log.log

DIR=$(pwd)
crontab -l | { cat; echo "@reboot sleep 60 && $DIR/run.sh >> /var/log/unifi_voucher_printer/log.log 2>&1"; } | crontab -

echo -e "!! Please edit /boot/cmdline.txt and remove 'console=serial0,115200', 'console=ttyAMA0,115200'. Reboot after that !!"
echo -e "Done."