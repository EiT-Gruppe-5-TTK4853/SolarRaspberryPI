#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-


# Read info with ModbusClient

import time


# import the server implementation
from pymodbus.client import ModbusSerialClient as ModbusClient
from pyepsolartracer.client import EPsolarTracerClient
from pymodbus.mei_message import *
import serial.rs485

from flask import jsonify
import sqlite3

# configure the client logging
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="main.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

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
    "solar_voltage",
    "solar_current",
    "solar_power",
    "battery_temp",
    "battery_voltage",
    "battery_current",
    "load_voltage",
    "load_current",
]


def get_db_connection():
    try:
        conn = sqlite3.connect("solar.sqlite")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return None


def insert_data(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                INSERT INTO solar (solar_power, solar_voltage, solar_current, battery_voltage, battery_current, battery_temp, load_current, load_voltage)
                VALUES (:solar_power, :solar_voltage, :solar_current, :battery_voltage, :battery_current, :battery_temp, :load_current, :load_voltage)
                """,
            data,
        )
        conn.commit()
        conn.close()
        return {"message": "Data inserted"}, 201
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        return {"message": str(e)}, 500


def fetch_registers():
    data = {}
    for register in registers:
        response = client.read_input(register)
        data[register] = float(response.value)
        logger.info(f"{register}: {float(response.value)}")
    return data


def run():
    while True:
        retry_attempts = 3  # Number of total attempts including the first one
        interval = 900  # 15 minutes
        for attempt in range(retry_attempts):
            try:
                logger.info("Insterting data from solar panel...")
                data = fetch_registers()
                insert_data(data)
                break  # If fetch_registers succeeds, break out of the retry loop
            except Exception as e:
                print(e)
                if attempt < retry_attempts - 1:
                    time.sleep(5)
                    logger.info("Attempting to retry...")
                    continue  # Try again
                else:
                    logger.info("Max retries reached. Waiting for the next cycle.")
                    break  # Exit the retry loop after the last attempt
        time.sleep(interval)  # Wait for {interval} minutes before the next cycle


if __name__ == "__main__":
    run()  # Run script for fetching values from solar panel
