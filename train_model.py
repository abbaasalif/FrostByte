# USAGE
# python train_model.py --conf config/config.json

# import the necessary packages
from pyimagesearch.utils import Conf
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, 
	help="Path to the input configuration file")
args = vars(ap.parse_args())

# load the configuration file
conf = Conf(args["conf"])

# load the face encodings
print("[INFO] loading face encodings...")
data = pickle.loads(open(conf["encodings_path"], "rb").read())

# encode the labels
print("[INFO] encoding labels...")
le = LabelEncoder()
labels = le.fit_transform(data["names"])

# train the model used to accept the 128-d encodings of the face and
# then produce the actual face recognition
print("[INFO] training model...")
recognizer = SVC(C=1.0, kernel="linear", probability=True)
recognizer.fit(data["encodings"], labels)

# write the actual face recognition model to disk
print("[INFO] writing the model to disk...")
f = open(conf["recognizer_path"], "wb")
f.write(pickle.dumps(recognizer))
f.close()

# write the label encoder to disk
f = open(conf["le_path"], "wb")
f.write(pickle.dumps(le))
f.close()