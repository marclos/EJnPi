import RPi.GPIO as GPIO                     # Imports the Raspberry Pi GPIO library
from time import sleep                      # Imports the sleep function from the time module

GPIO.setmode(GPIO.BCM)                      # Tells Pi what naming convention to use for GPIO pins
GPIO.setwarnings(False)                     # Ignoring warnings for now
GPIO.setup(24,GPIO.OUT, initial=GPIO.LOW)   # Set GPIO pin 24 for output and set initial value to logic low (off)

print("Press Ctrl + C to exit")             # Outputs this info to terminal

while True:                                 # A while loop, meaning have it run forever
  print("LED on")                           # Outputs this info to terminal
  GPIO.output(24,GPIO.HIGH)                 # Turns 'on' the GPIO pin, meaning it supplies power (3.3V) enough to turn hte LED on
  sleep(1)                                  # Pauses the Python program for 1 second
  print("LED off")                          # Outputs this info to terminal
  GPIO.output(24,GPIO.LOW)                  # Turns 'off' the GPIO pin, meaning it no longer supplies power
  sleep(1)                                  # Pauses the Python program for 1 second
