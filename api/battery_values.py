#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-


# Read info with ModbusClient

import time


# import the server implementation
from pymodbus.client import ModbusSerialClient as ModbusClient
from pyepsolartracer.client import EPsolarTracerClient
from pymodbus.mei_message import *
import serial.rs485

# configure the client logging
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# choose the serial client
client = ModbusClient(
    method="rtu",
    port="/dev/ttyXRUSB0",
    baudrate=115200,
    stopbits=1,
    bytesize=8,
    timeout=1,
)
client.connect()
try:
    client.socket.rs485_mode = serial.rs485.RS485Settings()
except:
    pass

client = EPsolarTracerClient(serialclient=client)

"""
Registers
Charging equipment input voltage
Charging equipment input current
Charging equipment input power
Battery Temperature
Charging equipment output voltage
Charging equipment output current
Charging equipment output power
Discharging equipment output voltage
Discharging equipment output current
Discharging equipment output power
"""

registers = [
    "Charging equipment input voltage",
    "Charging equipment input current",
    "Charging equipment input power",
    "Battery Temperature",
    "Charging equipment output voltage",
    "Charging equipment output current",
    "Charging equipment output power",
    "Discharging equipment output voltage",
    "Discharging equipment output current",
    "Discharging equipment output power",
]


def fetch_registers():
    for register in registers:
        response = client.read_input(register)
        print(register + ": " + str(response))


while True:
    retry_attempts = 3  # Number of total attempts including the first one
    for attempt in range(retry_attempts):
        try:
            fetch_registers()
            break  # If fetch_registers succeeds, break out of the retry loop
        except Exception as e:
            print(e)
            if attempt < retry_attempts - 1:
                time.sleep(5)
                print("Attempting to retry...")
                continue  # Try again
            else:
                print("Max retries reached. Waiting for the next cycle.")
                break  # Exit the retry loop after the last attempt
    time.sleep(900)  # Wait for 15 minutes before the next cycle
