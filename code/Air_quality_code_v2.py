# New Version -- PMS and Air Quality Tempate 
# Import packages (which sensor uses which package is noted)

# Datetime
import datetime
#import spidev # MiCS-2714
#import os # MiCS-2714
import serial # PMS5003
from collections import OrderedDict # PMS5003
#import board # BME280
#import busio # BME280
#import adafruit_bme280 # BME280
import csv # All
import time # All
import RPi.GPIO as GPIO # For LED

GPIO.setmode(GPIO.BCM) # For LED
GPIO.setwarnings(False) # For LED
GPIO.setup(24,GPIO.OUT,initial=GPIO.LOW) # For LED


# MiCS-2714 Code
#spi = spidev.SpiDev()
#spi.open(0,0)
#spi.max_speed_hz=1000000
 
#def ReadChannel(channel):
#  adc = spi.xfer2([1,(8+channel)<<4,0])
#  data = ((adc[1]&3) << 8) + adc[2]
#  return data
 
#def ConvertVolts(data,places):
#  volts = (data * 3.3) / float(1023)
#  volts = round(volts,places)
#  return volts
 
#def ConvertNO2(data,places):
#  NO2 = ((data * 10.05)/float(1023))+0.05
#  NO2 = round(NO2,places)
#  return NO2
 
#NO2_channel = 0

# MQ-131 Code

#def ConvertO3(data,places):
#  O3 = ((data * 1001)/float(1023))+1
#  O3 = round(O3,places)
#  return O3
  
#O3_channel = 1

# PMS5003 Code
class Sensor():
  def __init__(self, tty = '/dev/ttyS0'): 
    self.tty = tty
  
  def open(self): 
    self.serial = serial.Serial(self.tty, baudrate = 9600)
  
  def close(self):
    self.serial.close()
    
  def read_bytes(self, data, idx, size = 2):
    return int("".join(data[idx : idx + size]), 16)
    
  def read(self):
    data = self.serial.read(32)
    data = ["{:02X}".format(d) for d in data]
    
    if data[0] != '42' or data[1] != '4D':
      return None
      
    res = OrderedDict()
    res['DateTime'] = datetime.datetime.now()
    res['pm1_cf'] = self.read_bytes(data, 4)
    res['pm25_cf'] = self.read_bytes(data, 6)
    res['pm10_cf'] = self.read_bytes(data, 8)
    res['pm1'] = self.read_bytes(data, 10)
    res['pm25'] = self.read_bytes(data, 12)
    res['pm10'] = self.read_bytes(data, 14)
    return res

# BME280 Code
#i2c = busio.I2C(board.SCL, board.SDA)
#bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
#bme280.sea_level_pressure = 1013.25

# CSV Code
def  write_to_csv():
        if __name__ == "__main__":
                with open('/home/pi/airquality_data.csv', mode='a') as csv_file: 
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow([data])
                with open('/home/pi/airquality_data.csv', mode='r') as csv_file: 
                        csv_reader = csv.reader(csv_file)
                        for row in csv_reader:
                                print(row)


# Command
if __name__ == "__main__":
  while True:
    GPIO.output(24,GPIO.HIGH)
    # MiCS-2714 output
    #NO2_level = ReadChannel(NO2_channel)
    #NO2_volts = ConvertVolts(NO2_level,2)
    #NO2       = ConvertNO2(NO2_level,2)
    # MQ-131 output
    #O3_level = ReadChannel(O3_channel)
    #O3_volts = ConvertVolts(O3_level,2)
    #O3       = ConvertO3(O3_level,2)
    # PMS5003 output
    sensor = Sensor()
    sensor.open()
    data = sensor.read()
    sensor.close()
    # Write to csv, sleep for 60 seconds
    write_to_csv()
    time.sleep(2)
    GPIO.output(24,GPIO.LOW)
    time.sleep(58)
