from imutils import paths
import imutils
import numpy as np
import argparse
import pickle
import cv2, os
from os.path import dirname, join

protPath = join(dirname(__file__), "deploy.prototxt")
modPath = join(dirname(__file__),"res10_300x300_ssd_iter_140000.caffemodel")
detector = cv2.dnn.readNetFromCaffe(protPath, modPath)
imgPaths = list(paths.list_images('images/'))
embedder = cv2.dnn.readNetFromTorch("nn4.small2.v1.t7")
kEmbeddings = []
kNames = []

tFaces = 0



for (i, imgPath) in enumerate (imgPaths):
    name = imgPath.split(os.path.sep)[-2]
    print(name)
    image = cv2.imread(imgPath)
    image = imutils.resize(image, width=600)
    (h,w) = image.shape[:2]
    
    imgblob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)),
                                    1.0, (300, 300), (104.0, 177.0, 123.0),
                                    swapRB=False, crop=False)
                                    
    detector.setInput(imgblob)
    detections = detector.forward()
    
    if len(detections > 0):
        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0,0,i,2]
        
        if confidence > 0.5:
            box = detections[0,0,i,3:7] * np.array([w,h,w,h])
            (startX, startY, endX, endY) = box.astype("int") 
            face = image[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]
            
            if fW < 20 or fH < 20:
                continue
            
            faceBlob = cv2.dnn.blobFromImage(face, 1.0/255, (96,96),
                                            (0,0,0), swapRB=True, crop=False)
                                            
            embedder.setInput(faceBlob)
            vec = embedder.forward()
            
            
            
            kNames.append(name)
            kEmbeddings.append(vec.flatten())
            tFaces += 1
            
            
            
            
data = {"embeddings": kEmbeddings, "names": kNames}

f = open("embeddings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()