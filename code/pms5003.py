# PMS5003 Sensor 
# Python Code 
# Simple Read

import serial
from collections import OrderedDict
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
    
    if data[0] != '42' or data[1] !='4D':
      return None
      
      res = OrderedDict()
      res['pm1_cf'] = self.read_bytes(data, 4)
      res['pm25_cf'] = self.read_bytes(data, 6)
      res['pm10_cf'] = self.read_bytes(data, 8)
      res['pm1'] = self.read_bytes(data, 10)
      res['pm25'] = self.read_bytes(data, 12)
      res['pm10'] = self.read_bytes(data, 14)
      res['temperature'] = self.read_bytes(data, 24)/10
      res['humidity'] = self.read_bytes(data, 26)/10
      return res
      
if __name__ == '__main__':
  '''
  Test code
  '''
  sensor = Sensor()
  sensor.open()
  data = sensor.read()
  sensor.close()
  print(data)
