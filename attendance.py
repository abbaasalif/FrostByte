# USAGE
# python attendance.py --conf config/config.json

# import the necessary packages
from pyimagesearch.utils import Conf
from imutils.video import VideoStream
from datetime import datetime
from datetime import date
from tinydb import TinyDB
from tinydb import where
import face_recognition
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import RPi.GPIO as GPIO

driver_port_1 = 11
driver_port_2 = 13
button_port = 10

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(driver_port_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(driver_port_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(button_port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



def forward():
    GPIO.output(driver_port_1, GPIO.HIGH)
    GPIO.output(driver_port_2, GPIO.LOW)
    time.sleep(.8)
    GPIO.output(driver_port_1, GPIO.LOW)
    GPIO.output(driver_port_2, GPIO.LOW)


def backward():
    GPIO.output(driver_port_1, GPIO.LOW)
    GPIO.output(driver_port_2, GPIO.HIGH)
    time.sleep(.65)
    GPIO.output(driver_port_1, GPIO.LOW)
    GPIO.output(driver_port_2, GPIO.LOW)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, 
	help="Path to the input configuration file")
args = vars(ap.parse_args())

# load the configuration file
conf = Conf(args["conf"])

# initialize the database, student table, and attendance table
# objects
db = TinyDB(conf["db_path"])
studentTable = db.table("student")
attendanceTable = db.table("attendance")

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(conf["recognizer_path"], "rb").read())
le = pickle.loads(open(conf["le_path"], "rb").read())

def recognize():
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        prevPerson = None
        curPerson = None
        consecCount = 0
        print("[INFO] taking attendance...")
        studentDict = {}
        currentTime = datetime.now()
        timeout = time.time() + 22
        while True:
                print("[INFO] warming up camera...")
                frame = vs.read()
                frame = imutils.resize(frame, width=400)
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(rgb,
                    model=conf["detection_method"])
                if len(boxes) > 0:
                        encodings = face_recognition.face_encodings(rgb, boxes)
                        preds = recognizer.predict_proba(encodings)[0]
                        if max(preds)>0.7:
                                j = np.argmax(preds)
                                curPerson = le.classes_[j]
                        else:
                                curPerson = '000'
                        if curPerson != '000':		
                                print('found'+"_"+str(curPerson))
                                forward()
                                time.sleep(5)
                                backward()
                elif len(boxes) == 0:
                    print('Stand in front dumb person!!!')
                
                if (curPerson != '000' and curPerson) or  time.time() > timeout:
                        break
        print("[INFO] cleaning up...")
        time.sleep(3.0)
        vs.stop()
        db.close()

def button_callback(channel):
    if GPIO.input(button_port) == GPIO.HIGH:
        print("Button is pressed!!")
        recognize()
        time.sleep(5)

GPIO.add_event_detect(button_port, GPIO.RISING, callback=button_callback)

while True:
        time.sleep(1)
