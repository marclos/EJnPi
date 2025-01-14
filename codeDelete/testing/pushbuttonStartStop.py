import RPi.GPIO as GPIO
Import time
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIOIN, pull_up_down=GPIO.PUD_UP)
set = 0
while True:
   Input_state = GPIO.input(23)
    if input_state == False and set = 0:
        subprocess.("/home/pi/securipi-rpicamtd.sh", shell=True)
        p=subprocess.Popen( "/home/pi/securipi-picamtd.sh",shell=True,preexec_fn=os.setsid) 
        time.sleep(1)
        set =1
    Input_state = GPIO.input(23)
    if input_state == False and set = 1:
         os.killpg(p.pid, signal.SIGTERM)
         time.sleep(1)
         set =0
