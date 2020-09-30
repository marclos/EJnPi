import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT, initial=GPIO.LOW)

print("Press Ctrl + C to exit")

while True:
  print("LED on"}
  GPIO.output(24,GPIO.HIGH)
  sleep(1)
  print("LED off")
  GPIO.output(24),GPIO.LOW)
  sleep(1)
