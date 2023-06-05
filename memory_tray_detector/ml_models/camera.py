import cv2
import os
import pickle
from datetime import datetime
import time
import paho.mqtt.client as mqtt
import json
import socket

from django.contrib import messages
from django.shortcuts import redirect

from django.conf import settings
from memory_tray_detector.models import Gallery, Camera, CamCard
from django.shortcuts import get_object_or_404

# def send_mqtt_message(message):
#     try:
#         client = mqtt.Client()
#         client.connect("localhost", 1883)

#         topic = 'mtray'
#         json_message = json.dumps(message)
#         client.publish(topic, json_message)

#         client.disconnect()
#     except Exception as e:
#         print("Error saat mengirim pesan MQTT:", str(e))

# Konfigurasi MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print("Failed to connect, return code %d" % rc)

def on_publish(client, userdata, mid):
    print("Message successfully published")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker")

def connect_mqtt():
    client = mqtt.Client()
    client.username_pw_set("f4211843-ae3c-4e5d-9f3a-87c27aec1066", "ltvxkTFHRBv8Hcg2RNHpkivLzox3z4b0XtBBLSLH3ZP9fY9w2D7l59Kcg5IRiP1qxgLD4nVsNCU2mEN2")  # Ganti dengan nama pengguna dan kata sandi yang sesuai
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # Ganti dengan alamat dan port broker MQTT yang sesuai
    broker_address = "telemetry.iotstadium.com"
    port = 1883

    try:
        client.connect(broker_address, port)
        client.loop_start()
        return client
    except Exception as e:
        print("Error connecting to MQTT Broker:", str(e))
        return None

def send_mqtt_message(client, topic, message):
    try:
        json_message = json.dumps(message)
        result, mid = client.publish(topic, json_message)
        if result == mqtt.MQTT_ERR_SUCCESS:
            print('Message successfully sent')
        else:
            print('Failed to send message, return code %d' % result)
    except Exception as e:
        print("Error sending MQTT message:", str(e))

def disconnect_mqtt(client):
    client.loop_stop()
    client.disconnect()

def send_message_to_mqtt(pesan):
    client = connect_mqtt()
    if client:
        topic = 'f4211843-ae3c-4e5d-9f3a-87c27aec1066'
        message = pesan
        send_mqtt_message(client, topic, message)
        disconnect_mqtt(client)
# Akhir Konfigurasi


def open_camera(save_folder, cam_id):
    # try:
        # Mengambil instance camera sesuai Camera ID
        camera = get_object_or_404(Camera, id=cam_id)
        address = camera.ip_camera
        cam = cv2.VideoCapture(address)
        # cam.open(address)

        # connected = cam.open(address)

        # if not connected:
        #     raise socket.error('Tidak dapat terhubung dengan alamat Ip Camera')

        # Cek apakah file counter sudah ada
        counter_file = os.path.join(settings.BASE_DIR, 'memory_tray_detector', 'ml_models', 'counter.pkl')
        if os.path.exists(counter_file):
            with open(counter_file, 'rb') as f:
                photo_counter = pickle.load(f)
        else:
            photo_counter = 1

        show_text = False
        text_timer = 0
        display_time = 0.5

        
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

                formatted_time = current_time.strftime('%d%m%Y%H%M%S')
                message = {
                        'name': camera.name,
                        'quantity': str(quantity),
                        'timestamp': formatted_time
                    }
                send_message_to_mqtt(message)


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
    # except Exception as e:
    #     error_message = f'Kamera tidak dapat terbuka, error: {str(e)}'
    #     raise Exception(error_message)