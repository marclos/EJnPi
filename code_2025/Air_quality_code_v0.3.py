## PMS5005
# Untested
# Code to Read PMS5003
# Need Code to read BME280
# Flash LED after each reading (0.5 s)
# Save to CSV
# Version 0.3


import RPi.GPIO as GPIO
import serial
import time
import csv
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24,GPIO.OUT, initial=GPIO.LOW)

# Set the serial port and baud rate
serial_port = '/dev/ttyS0'  # Adjust the port as needed
baud_rate = 9600

# Create a serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=2.0)

def read_sensor_data():
    # Read 32 bytes of data from the sensor
    data = ser.read(32)

    # Check if the data is valid
    if data[0] == 0x42 and data[1] == 0x4d:
        pm1_0 = (data[10] << 8) | data[11]
        pm2_5 = (data[12] << 8) | data[13]
        pm10 = (data[14] << 8) | data[15]
        return pm1_0, pm2_5, pm10
    else:
        print("Invalid data")
        return None, None

def record_data(filename, pm1_0, pm2_5, pm10):
    # Append data to a CSV file
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        csv_writer.writerow([timestamp, pm1_0, pm2_5, pm10])

def main():
    # Set the filename for recording data
    filename = 'sensor_data_v3.csv'

    try:
        while True:
            #
            GPIO.output(24,GPIO.LOW)            
            # Read data from the sensor
            pm1_0, pm2_5, pm10 = read_sensor_data()

            if pm2_5 is not None and pm10 is not None:
                # Record data to CSV file
                record_data(filename, pm1_0, pm2_5, pm10)
                print(f"{datetime.now().strftime('%m/%d %H:%M:%S')}: PM1.0 = {pm1_0} µg/m³, PM2.5 = {pm2_5} µg/m³, PM10 = {pm10} µg/m³")

            # Wait for 30 seconds
            GPIO.output(24,GPIO.HIGH)
            time.sleep(5)

    except KeyboardInterrupt:
        print("Script terminated by user.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()

# Set GPIO pin 7 to HIGH
