# Raspberry Pi lighting timer
# 8 STDP relay channels
# 2 PWM channels
# Using realtime new() to use as hours of the day

# import GPIO module
import RPi.GPIO as GPIO


# import GPIO module
import RPi.GPIO as GPIO


# set up GPIO pins as outputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button
GPIO.setup(21, GPIO.OUT) # Appliance 5/25 volt relay
##GPIO.setup(24, GPIO.OUT)# LED
state = 0 # Do you need this variable???
button = GPIO.input(25)


# import date and time modules
import datetime
import time

# 0 = off, 1 = on
# Create a 10 column x 24 row matrix to track lighting times
matrix = [[0 for x in range(10)] for y in range(24)]

matrix[0][0] = 1

timeprog = [['0', 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            ['1', 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            ['2', 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            ['3', 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            ['4', 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            ['5', 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            ['6', 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
            ['7', 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
            ['8', 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
            ['9', 0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
            ['10', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            ['11', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ['12', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ['13', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            ['14', 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            ['15', 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            ['16', 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            ['17', 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            ['18', 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            ['19', 1, 1, 1, 0, 1, 1, 1, 1, 0, 0],
            ['20', 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            ['21', 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            ['22', 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            ['23', 0, 1, 1, 0, 1, 1, 0, 1, 1, 0]]
            

print(timeprog)
# Enter the times you want the appliance to turn on and off for
# each day of the week.  The times are in 24 hour format.

# Use system time to determine the time of day
# and day of the week
# get the current time in hours, minutes and seconds
from datetime import datetime
from datetime import timedelta

now = datetime.now()

current_time = now.strftime("%H")

print("Current Houe =", current_time)


i =20

print(timeprog[i][0])
current_time == timeprog[i][0]
[row[0] for row in timeprog]
[col[1] for col in timeprog]

# Extract 2 column in the timeprog matrix
[row[1] for row in timeprog]
[row[2] for row in timeprog]
timeprog[1][0] #hour
timeprog[1][1] # relay 1
timeprog[1][2] # relay 2
timeprog[1][3] # relay 3
timeprog[1][4] # relay 4

timings = [row[0] for row in timeprog]


# loop matrix to find matching row in timeprog
for i in range(24):
    print(timeprog[i][1])
    print(timeprog[i][2])
    print(timeprog[i][3])
    print(timeprog[i][4])
    print(timeprog[i][5])
    print(timeprog[i][6])
    print(timeprog[i][7])
    print(timeprog[i][8])
    print(timeprog[i][9])
    print(timeprog[i][10])
    print("")
        

# loop matrix to find matching row in timeprog

            




