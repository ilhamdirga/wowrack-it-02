from django.conf import settings
from os import listdir
from PIL import Image as Img
from numpy import asarray
from numpy import expand_dims
from matplotlib import pyplot
from keras_facenet import FaceNet

import pickle
import cv2
import os
import numpy as np
import tensorflow as tf

HaarCascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))
MyFaceNet = FaceNet()

# folder='mywebsite/static/images/'
database = {}

def train(folder):
    for filename in listdir(folder):
        if filename.startswith('.'):
            continue
        path = folder + filename
        gbr1 = cv2.imread(folder + filename)
        if gbr1 is None:
            print("Failed to load image: ", folder + filename)
        else:
            gbr1 = cv2.imread(folder + filename)

            wajah = HaarCascade.detectMultiScale(gbr1,1.1,4)

            if len(wajah)>0:
                x1, y1, width, height = wajah[0]         
            else:
                x1, y1, width, height = 1, 1, 10, 10

            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height

            gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
            gbr = Img.fromarray(gbr)                  # konversi dari OpenCV ke PIL
            gbr_array = asarray(gbr)

            face = gbr_array[y1:y2, x1:x2]                        

            face = Img.fromarray(face)                       
            face = face.resize((160,160))
            face = asarray(face)

            face = expand_dims(face, axis=0)
            signature = MyFaceNet.embeddings(face)

            database[os.path.splitext(filename)[0]]=signature
            
    pickle_file = os.path.join(settings.BASE_DIR, 'person_detector', 'ml_models', 'data.pkl')
    with open(pickle_file, 'wb') as myfile:
        pickle.dump(database, myfile)
