import time
import RPi.GPIO as GPIO

stepper_1 = 11
stepper_2 = 13
stepper_3 = 15
stepper_4 = 16
t_delay = .01

GPIO.setmode(GPIO.BOARD)
GPIO.setup(stepper_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepper_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepper_3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(stepper_4, GPIO.OUT, initial=GPIO.LOW)


def forward(steps):
	for i in range (0,steps):
		GPIO.output(stepper_1, GPIO.LOW)
		GPIO.output(stepper_4, GPIO.HIGH)
		time.sleep(t_delay)
		GPIO.output(stepper_4, GPIO.LOW)
		GPIO.output(stepper_3, GPIO.HIGH)
		time.sleep(t_delay)
		GPIO.output(stepper_3, GPIO.LOW)
		GPIO.output(stepper_2, GPIO.HIGH)
		time.sleep(t_delay)
		GPIO.output(stepper_2, GPIO.LOW)
		GPIO.output(stepper_1, GPIO.HIGH)
		time.sleep(t_delay)
	GPIO.output(stepper_1, GPIO.LOW)
	GPIO.output(stepper_2, GPIO.LOW)
	GPIO.output(stepper_3, GPIO.LOW)
	GPIO.output(stepper_4, GPIO.LOW)

def backward(steps):
	for i in range (0,steps):
		GPIO.output(stepper_4, GPIO.LOW)
		GPIO.output(stepper_1, GPIO.HIGH)
		time.sleep(t_delay)
		GPIO.output(stepper_1, GPIO.LOW)
		GPIO.output(stepper_2, GPIO.HIGH)
		time.sleep(t_delay)
		GPIO.output(stepper_2, GPIO.LOW)
		GPIO.output(stepper_3, GPIO.HIGH)
		time.sleep(t_delay)
		GPIO.output(stepper_3, GPIO.LOW)
		GPIO.output(stepper_4, GPIO.HIGH)
		time.sleep(t_delay)
	GPIO.output(stepper_1, GPIO.LOW)
	GPIO.output(stepper_2, GPIO.LOW)
	GPIO.output(stepper_3, GPIO.LOW)
	GPIO.output(stepper_4, GPIO.LOW)

forward(300)