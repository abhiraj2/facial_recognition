import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
from os.path import join, dirname


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)
args  = vars(ap.parse_args())


protPath = join(dirname(__file__), "deploy.prototxt")
modPath = join(dirname(__file__),"res10_300x300_ssd_iter_140000.caffemodel")

detector = cv2.dnn.readNetFromCaffe(protPath, modPath)

embedder = cv2.dnn.readNetFromTorch("nn4.small2.v1.t7")


recognizer = pickle.loads(open("recognizer", "rb").read())
le = pickle.loads(open("le.pickle", "rb").read())

img = cv2.imread(args["image"])
img = imutils.resize(img, width=600)
(h,w)= img.shape[:2]

imgblob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)),
                                    1.0, (300, 300), (104.0, 177.0, 123.0),
                                    swapRB=False, crop=False)
                                    
detector.setInput(imgblob)
detections = detector.forward()


for i in range(0, detections.shape[2]):
        confidence = detections[0,0,i,2]
        
        if confidence > 0.5:
            box = detections[0,0,i,3:7]*np.array([w,h,w,h])
            (startX, startY, endX, endY) = box.astype("int")
            
            
            face = img[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]
            
            if fW < 20 or fH < 20:
                continue
            
            faceBlob = cv2.dnn.blobFromImage(face, 1.0/255, (96,96),
                                            (0,0,0), swapRB=True, crop=False)
                                            
            embedder.setInput(faceBlob)
            vec = embedder.forward()
            
            
            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]
            
            text = f"{name}: {proba*100}"
            y = startY-10 if startY-10 > 10 else startY+10
            cv2.rectangle(img, (startX, startY), (endX, endY), (0,0,255), 2)
            cv2.putText(img, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0,0,255),2)
            
            
          
cv2.imwrite("image.jpg", img)
