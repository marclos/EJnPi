import RPi.GPIO as GPIO
import time
import subprocess, os
import signal

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO_switch = 24 # select pin to connect button
GPIO.setup(GPIO_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:

    run = 0
    while True:
        if GPIO.input(GPIO_switch)==0 and run == 0:
            rpistr = "python3 /home/pi/Documents/DataloggerV2.py"
            p=subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid)
            run=1
            while GPIO.input(GPIO_switch)==0:
                time.sleep(0.01)
        if GPIO.input(GPIO_switch)==0 and run == 1:
            run = 0
            os.killpg(p.pid, signal.SIGTERM)
            while GPIO.input(GPIO_switch)==0:
                time.sleep(0.01)


except KeyboardInterrupt:

    GPIO.cleanup()
