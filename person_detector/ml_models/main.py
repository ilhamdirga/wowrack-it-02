import cv2
import numpy as np
from tensorflow.keras.layers import Input, Lambda, Dense
from tensorflow.keras.models import load_model, Model
import os
from . import utils
from .siamese_network import buat_siamese
from . import config

import datetime
import time

from django.conf import settings
from person_detector.models import DetectedFace

haarscascade_path = os.path.join('mywebsite', 'person_detector', 'ml_models', 'haarcascade.xml')
detector = cv2.CascadeClassifier(haarscascade_path)

def model():
    inpA = Input(config.img_shape)
    inpB = Input(config.img_shape)

    embedder = buat_siamese(config.img_shape)
    vectorA = embedder(inpA)
    vectorB = embedder(inpB)

    dist = Lambda(utils.distance)([vectorA, vectorB])
    outputs = Dense(1, activation="sigmoid")(dist)
    return Model(inputs=[inpA, inpB], outputs=outputs)

def prediksi_muka(frame, model):
    hasil = []
    label = []
    for data in database:
        img = database[data]
        tes = (frame, img)
        tes = np.array([tes])
        tes = np.expand_dims(tes, axis=-1)
        tmp = model.predict([tes[:,0,:], tes[:,1,:]])
        hasil.append(tmp)
        label.append(data)
    return hasil, label

def hasil_prediksi(hasil, label):
    maks = max(hasil)
    indeks = hasil.index(maks)
    if maks > 0.4:
        teks = label[indeks]
    else:
        teks = 'Unknown'
    return teks

def buat_database():
    database_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'person_detector')
    images = os.listdir(database_path)
    database = {}
    for image in images:
        path = os.path.join(database_path, image)
        img = cv2.imread(path, 0)
        img = cv2.resize(img, (105,105), interpolation=cv2.INTER_AREA)/255.
        database[image.split('.')[0]] = img
    return database

new_model = model()
file_path = os.path.join(settings.BASE_DIR, 'person_detector', 'ml_models', 'siamese_weights.h5')
new_model.load_weights(file_path)
database = buat_database()

def open_camera():
    # address = 'http://192.168.242.101:8080/video'
    vid = cv2.VideoCapture(0)
    # vid.open(address)

    last_print_time = time.time()
    
    while(True):
        ret, frame = vid.read()

        wajah = detector.detectMultiScale(frame, scaleFactor = 1.2, minNeighbors = 5)
        
        for x1, y1, w, h in wajah:
            x2 = x1 + w
            y2 = y1 + h
            muka = frame[y1:y2, x1:x2]
            muka = cv2.cvtColor(muka, cv2.COLOR_BGR2GRAY)
            muka = cv2.resize(muka, (105,105), interpolation=cv2.INTER_AREA)/255.
            hasil, label = prediksi_muka(muka, new_model)
            teks = hasil_prediksi(hasil, label)

        if teks:
            current_time = datetime.datetime.now()
            if time.time() - last_print_time >= 2:
                detected_face = DetectedFace.objects.create(name=teks, detected_time=current_time)
                detected_face.save()
                last_print_time = time.time()  # Memperbarui waktu terakhir pesan dicetak dan data disimpan
                    
                formatted_time = current_time.strftime('%d%m%Y')

                print(f"Nama wajah terdeteksi: {teks}; Waktu: {current_time}")

        frame = cv2.rectangle(frame, (x1,y1), (x2,y2), (255,255,255), 1)
        frame = cv2.putText(frame, teks, (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        
        # print(f'terdeteksi: {teks}')
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    

    vid.release()

    cv2.destroyAllWindows()