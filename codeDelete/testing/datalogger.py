import RPi.GPIO as GPIO
import datetime
from datetime import timedelta, datetime
import time
from time import sleep
import csv
from csv import writer
import signal


datestring = datetime.strftime(datetime.now(), '%Y_%m_%d-%H_%M_%S')

def my_callback(channel):
     data_writer.writerow([GPIO.input(26), datetime.now()])      # writes the detected
     # edge event to a CSV file with columns of rise/fall and the date & time of detection


if __name__ == '__main__':

    GPIO.setmode(GPIO.BOARD)       # set up GPIO numbering (BOARD = physical pins on Pi)
    GPIO.setup(26, GPIO.IN)         # set physical pin 26 as input


# create CSV file to write edge detection data to called Datalogger, with data on new line
    with open('/media/pi/KINGSTON/Datalogger_' + datestring + '.csv', 'w', newline='') as Datalogger:
        data_writer = writer(Datalogger)

        data_writer.writerow(["Edge type (0 = Falling)", "Date & Time"])       # create headers in CSV file


        GPIO.add_event_detect(26, GPIO.BOTH, callback=my_callback, bouncetime=20)     # edge detection function
        # detects both rise and fall in signal on pin 26, then runs my callback

        signal.pause()

        except KeyboardInterrupt:
          print("Program stopped")
          exit(0)
          
        while True:
# main program loop here - loops detection of edges then runs my callback

          time.sleep(0.01)
          
