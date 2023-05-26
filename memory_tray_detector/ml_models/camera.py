import cv2
import os
import pickle
from datetime import datetime
import time
import paho.mqtt.client as mqtt
import json

from django.contrib import messages
from django.shortcuts import redirect

from django.conf import settings
from memory_tray_detector.models import Gallery, Camera, CamCard
from django.shortcuts import get_object_or_404

def send_mqtt_message(message):
    try:
        client = mqtt.Client()
        client.connect("localhost", 1883)

        topic = 'mtray'
        json_message = json.dumps(message)
        client.publish(topic, json_message)

        client.disconnect()
    except Exception as e:
        print("Error saat mengirim pesan MQTT:", str(e))


def open_camera(save_folder, cam_id):
    # Mengambil instance camera sesuai Camera ID
    camera = get_object_or_404(Camera, id=cam_id)
    # address = camera.ip_camera
    cam = cv2.VideoCapture(0)
    # cam.open(address)

    # Cek apakah file counter sudah ada
    counter_file = os.path.join(settings.BASE_DIR, 'memory_tray_detector', 'ml_models', 'counter.pkl')
    if os.path.exists(counter_file):
        with open(counter_file, 'rb') as f:
            photo_counter = pickle.load(f)
    else:
        photo_counter = 1

    show_text = False
    text_timer = 0
    display_time = 2

    
    while True:
        check, frame = cam.read()

         # Menambahkan teks ke frame
        if show_text:
            text = f'Photo {camera.name} saved!'
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if time.time() - text_timer > display_time:
                show_text = False

        cv2.imshow(f'{camera.name}', frame)
        key = cv2.waitKey(1)

        if key == 32:           

            # Generate photo name
            photo_name = f'{camera.name}-{photo_counter}.jpg'

            # Save photo ke direktory
            photo_path = os.path.join(save_folder, photo_name)
            cv2.imwrite(photo_path, frame)

            # Simpan photo ke models Gallery
            quantity = 1
            picture = os.path.join('memory_tray_detector', photo_name)
            current_time = datetime.now()
            gallery = Gallery.objects.create(name = camera,
                                             picture = picture, 
                                             quantity = quantity,
                                             timestamp = current_time
                                             )
            gallery.save()

            formatted_time = current_time.strftime('%d%m%Y')
            message = {
                    'name': camera.name,
                    'quantity': str(quantity),
                    'timestamp': formatted_time
                }
            send_mqtt_message(message)


            # Mengambil objek CamCard yang terkait dengan objek Gallery yang baru dibuat
            camcard = CamCard.objects.get(name=camera)
            camcard.quantity = gallery.quantity
            camcard.timestamp = gallery.timestamp
            camcard.save()

            photo_counter += 1
            print(f'Photo {photo_name} saved!')

            # Menampilkan teks selama 3 detik
            show_text = True
            text_timer = time.time()

        elif key == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    # Simpan nilai counter ke dalam file
    with open(counter_file, 'wb') as f:
        pickle.dump(photo_counter, f)