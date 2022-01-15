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
import pyttsx3
import pickle
import time
import cv2
import RPi.GPIO as GPIO

# stepper_1 = 11
# stepper_2 = 13
# stepper_3 = 15
# stepper_4 = 16

# t_delay = .01

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(stepper_1, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(stepper_2, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(stepper_3, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(stepper_4, GPIO.OUT, initial=GPIO.LOW)


# def forward(steps):
# 	for i in range (0,steps):
# 		GPIO.output(stepper_1, GPIO.LOW)
# 		GPIO.output(stepper_4, GPIO.HIGH)
# 		time.sleep(t_delay)
# 		GPIO.output(stepper_4, GPIO.LOW)
# 		GPIO.output(stepper_3, GPIO.HIGH)
# 		time.sleep(t_delay)
# 		GPIO.output(stepper_3, GPIO.LOW)
# 		GPIO.output(stepper_2, GPIO.HIGH)
# 		time.sleep(t_delay)
# 		GPIO.output(stepper_2, GPIO.LOW)
# 		GPIO.output(stepper_1, GPIO.HIGH)
# 		time.sleep(t_delay)
# 	GPIO.output(stepper_1, GPIO.LOW)
# 	GPIO.output(stepper_2, GPIO.LOW)
# 	GPIO.output(stepper_3, GPIO.LOW)
# 	GPIO.output(stepper_4, GPIO.LOW)

# def backward(steps):
# 	for i in range (0,steps):
# 		GPIO.output(stepper_4, GPIO.LOW)
# 		GPIO.output(stepper_1, GPIO.HIGH)
# 		time.sleep(t_delay)
# 		GPIO.output(stepper_1, GPIO.LOW)
# 		GPIO.output(stepper_2, GPIO.HIGH)
# 		time.sleep(t_delay)
# 		GPIO.output(stepper_2, GPIO.LOW)
# 		GPIO.output(stepper_3, GPIO.HIGH)
# 		time.sleep(t_delay)
# 		GPIO.output(stepper_3, GPIO.LOW)
# 		GPIO.output(stepper_4, GPIO.HIGH)
# 		time.sleep(t_delay)
# 	GPIO.output(stepper_1, GPIO.LOW)
# 	GPIO.output(stepper_2, GPIO.LOW)
# 	GPIO.output(stepper_3, GPIO.LOW)
# 	GPIO.output(stepper_4, GPIO.LOW)

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

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# initialize previous and current person to None
prevPerson = None
curPerson = None

# initialize consecutive recognition count to 0
consecCount = 0

# initialize the text-to-speech engine, set the speech language, and
# the speech rate
print("[INFO] taking attendance...")
#ttsEngine = pyttsx3.init()
#ttsEngine.setProperty("voice", conf["language"])
#ttsEngine.setProperty("rate", conf["rate"])

# initialize a dictionary to store the student ID and the time at
# which their attendance was taken
studentDict = {}
# loop over the frames from the video stream	
while True:
	# store the current time and calculate the time difference
	# between the current time and the time for the 
	currentTime = datetime.now()
	# grab the next frame from the stream, resize it and flip it
	# horizontally
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	frame = cv2.flip(frame, 1)

	# if the maximum time limit to record attendance has been crossed
	# then skip the attendance taking procedure
	#if timeDiff > conf["max_time_limit"]:
		# check if the student dictionary is not empty
		#if len(studentDict) != 0:
		# insert the attendance into the database and reset the
		# student dictionary
			#attendanceTable.insert({str(date.today()): studentDict})
			#studentDict = {}

			# draw info such as class, class timing, and current time on
			# the frame
	cv2.putText(frame, "Class: {}".format(conf["class"]),
		(10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
	cv2.putText(frame, "Current time: {}".format(
	currentTime.strftime("%H:%M:%S")), (10, 40),
	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

	#show the frame
	cv2.imshow("Attendance System", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord('q'):
		break
	

		# convert the frame from RGB (OpenCV ordering) to dlib 
	# ordering (RGB)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
				
	boxes = face_recognition.face_locations(rgb,
		model=conf["detection_method"])

		# loop over the face detections
	# for (top, right, bottom, left) in boxes:
	# 		# draw the face detections on the frame
	# 	cv2.rectangle(frame, (left, top), (right, bottom),
	# 				(0, 255, 0), 2)

			# calculate the time remaining for attendance to be taken

			# draw info such as class, class timing, current time, and
			# remaining attendance time on the frame
	# cv2.putText(frame, "Current time: {}".format(
	# currentTime.strftime("%H:%M:%S")), (10, 40),
	# cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
	
	# check if atleast one face has been detected	
	if len(boxes) > 0:
			# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes)
				
		# perform classification to recognize the face
		preds = recognizer.predict_proba(encodings)[0]
		if max(preds)>0.5:
			j = np.argmax(preds)
			curPerson = le.classes_[j]
		else:
			curPerson = '000' #unknown
		if curPerson != None or curPerson != '000':		
			print('found'+"_"+str(curPerson))
			forward()
			time.sleep(5)
			backward()
		# if a particular person is recognized for a given
		# number of consecutive frames, we have reached a 
		# positive recognition and alert/greet the person accordingly
	
		
	elif len(boxes) == 0:
		
				# construct a label asking the student to stand in fron
				# to the camera and draw it on to the frame
		label = "Please stand in front of the camera"
		cv2.putText(frame, label, (5, 175),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
		curPerson = None
	
		

		# show the frame
	cv2.imshow("Attendance System", frame)
	key = cv2.waitKey(1) & 0xFF

# check if the `q` key was pressed
	if key == ord("q"):
		# check if the student dictionary is not empty, and if so,
		# insert the attendance into the database
		#if len(studentDict) != 0:
			#attendanceTable.insert({str(date.today()): studentDict})
			
		# break from the loop
		break

# clean up
print("[INFO] cleaning up...")
time.sleep(3.0)
vs.stop()
db.close()
