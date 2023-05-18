from PIL import Image
import os
from keras_facenet import FaceNet
import numpy as np
from numpy import asarray
from numpy import expand_dims
from django.conf import settings
import pickle
import cv2
import datetime
import time
import asyncio
from person_detector.models import DetectedFace

HaarCascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))
MyFaceNet = FaceNet()

def make_720p(cap):
        cap.set(3, 1280)
        cap.set(4, 720)

def open_camera():
    cap = cv2.VideoCapture(0)
    last_print_time = time.time()

    # make_720p(cap)
    while True:        
        file_path = os.path.join(settings.BASE_DIR, 'person_detector','ml_models', 'data.pkl')
        with open(file_path, 'rb') as f:
            database = pickle.load(f)

        _, gbr1 = cap.read()
        
        wajah = HaarCascade.detectMultiScale(gbr1,1.1,4)
        
        if len(wajah)>0:
            x1, y1, width, height = wajah[0]        
        else:
            x1, y1, width, height = 1, 1, 10, 10
        
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        
        
        gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
        gbr = Image.fromarray(gbr)                  # konversi dari OpenCV ke PIL
        gbr_array = asarray(gbr)
        
        face = gbr_array[y1:y2, x1:x2]                        
        
        face = Image.fromarray(face)                       
        face = face.resize((160,160))
        face = asarray(face)
        
    #     face = face.astype('float32')
    #     mean, std = face.mean(), face.std()
    #     face = (face - mean) / std
        
        face = expand_dims(face, axis=0)
    #     signature = MyFaceNet.predict(face)
        signature = MyFaceNet.embeddings(face)

        
        min_dist=100
        identity=' '
        for key, value in database.items() :
            dist = np.linalg.norm(value-signature)
            if dist < min_dist:
                min_dist = dist
                identity = key
        if identity:
            current_time = datetime.datetime.now()
            if time.time() - last_print_time >= 4:
                detected_face = DetectedFace.objects.create(name=identity, detected_time=current_time)
                detected_face.save()
                last_print_time = time.time()  # Memperbarui waktu terakhir pesan dicetak dan data disimpan
                
                print(f"Nama wajah terdeteksi: {identity}; Waktu: {current_time}")
                
        cv2.putText(gbr1,identity, (100,100),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        cv2.rectangle(gbr1,(x1,y1),(x2,y2), (0,255,0), 2)
            
        cv2.imshow('res',gbr1)
        
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
            
    cv2.destroyAllWindows()
    cap.release()

