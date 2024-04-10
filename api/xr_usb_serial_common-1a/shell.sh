#!/bin/sh

sudo rmmod ./xr_usb_serial_common.ko 
sudo make 
sudo rmmod cdc-acm 
sudo modprobe -r usbserial 
sudo modprobe usbserial 
sudo insmod ./xr_usb_serial_common.ko 

 
# . venv/bin/activate
# cd ..
# python main.py 