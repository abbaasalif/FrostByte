import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
while True:
    if GPIO.input(18) == GPIO.HIGH:
        print(1)
    else:
        print(0)
    time.sleep(.1)
















