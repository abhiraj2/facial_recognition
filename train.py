from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

import argparse
import pickle

data = pickle.loads(open("embeddings.pickle", "rb").read())

le = LabelEncoder()
labels = le.fit_transform(data["names"])


recognizer = SVC(C=1.0, kernel="linear", probability=True)
recognizer.fit(data["embeddings"], labels)


f = open("recognizer", "wb")
f.write(pickle.dumps(recognizer))
f.close()


f = open("le.pickle", "wb")
f.write(pickle.dumps(le))
f.close()