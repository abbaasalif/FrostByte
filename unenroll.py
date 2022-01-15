# USAGE
# python unenroll.py --id S1901 --conf config/config.json

# import the necessary packages
from pyimagesearch.utils import Conf
from tinydb import TinyDB
from tinydb import where
import argparse
import shutil
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--id", required=True, 
	help="Unique student ID of the student")
ap.add_argument("-c", "--conf", required=True, 
	help="Path to the input configuration file")
args = vars(ap.parse_args())

# load the configuration file
conf = Conf(args["conf"])

# initialize the database and student table objects
db = TinyDB(conf["db_path"])
studentTable = db.table("student")

# retrieve the student document from the database, mark the student 
# as unenrolled, and write back the document to the database
student = studentTable.get(where(args["id"]))
# studentTable.write_back(student)
#to remove the record from the database
val = list(student.keys())
val = val[0]
print(val)
# delete the student's data from the dataset
shutil.rmtree(os.path.join(conf["dataset_path"], conf["class"],
	args["id"]))
print("[INFO] Please extract the embeddings and re-train the face" \
	" recognition model...")

# close the database
db.close()