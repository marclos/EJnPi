import csv
import os
import time
from datetime import datetime

import serial
from collections import OrderedDict

class Sensor:
    def __init__(self, tty='/dev/ttyS0'):
        self.tty = tty

    def open(self):
        self.serial = serial.Serial(self.tty, baudrate=9600)

    def close(self):
        self.serial.close()

    def read_bytes(self, data, idx, size=2):
        return int("".join(data[idx:idx + size]), 16)

    def read(self):
        data = self.serial.read(32)
        data = ["{:02X}".format(d) for d in data]

        if data[0] != '42' or data[1] != '4D':
            return None

        res = OrderedDict()
        res['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res['pm1_cf'] = self.read_bytes(data, 4)
        res['pm25_cf'] = self.read_bytes(data, 6)
        res['pm10_cf'] = self.read_bytes(data, 8)
        res['pm1'] = self.read_bytes(data, 10)
        res['pm25'] = self.read_bytes(data, 12)
        res['pm10'] = self.read_bytes(data, 14)
        res['temperature'] = self.read_bytes(data, 24) / 10
        res['humidity'] = self.read_bytes(data, 26) / 10
        return res

def write_to_csv(file_path, fieldnames, data):
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

if __name__ == '__main__':
    sensor = Sensor()
    file_path = 'sensor_data.csv'
    fieldnames = ['timestamp', 'pm1_cf', 'pm25_cf', 'pm10_cf', 'pm1', 'pm25', 'pm10', 'temperature', 'humidity']

    while True:
        sensor.open()
        data = sensor.read()
        sensor.close()
        if data:
            write_to_csv(file_path, fieldnames, data)
            print(f"Data written to {file_path} at {data['timestamp']}")
        time.sleep(60)  # wait for 10 minutes (600 seconds)
