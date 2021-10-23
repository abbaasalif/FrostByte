# USAGE
# python initialize_database.py --conf config/config.json

# import the necessary packages
from pyimagesearch.utils import Conf
from tinydb import TinyDB
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, 
	help="Path to the input configuration file")
args = vars(ap.parse_args())

# load the configuration file
conf = Conf(args["conf"])

# initialize the database
db = TinyDB(conf["db_path"])

# insert the details regarding the class
print("[INFO] initializing the database...")
db.insert({"class": conf["class"]})
print("[INFO] database initialized...")

# close the database
db.close()