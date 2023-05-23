import cv2
import os
import pickle
from datetime import datetime

from django.conf import settings
from memory_tray_detector.models import Gallery, Camera

def open_camera(save_folder):
    cam = cv2.VideoCapture(0)

    # Cek apakah file counter sudah ada
    counter_file = os.path.join(settings.BASE_DIR, 'memory_tray_detector', 'ml_models', 'counter.pkl')
    if os.path.exists(counter_file):
        with open(counter_file, 'rb') as f:
            photo_counter = pickle.load(f)
    else:
        photo_counter = 1

    while True:
        check, frame = cam.read()
        cv2.imshow('video', frame)
        key = cv2.waitKey(1)

        if key == 32:
            # Ambil instance Camera pertama
            camera = Camera.objects.first()

            # Generate photo name
            photo_name = f'{camera.name}-{photo_counter}.jpg'

            photo_path = os.path.join(save_folder, photo_name)
            cv2.imwrite(photo_path, frame)

            # Simpan foto ke model Gallery
            gallery = Gallery(name=camera, quantity=1)  # Menggunakan instance Camera
            gallery.picture = os.path.join('memory_tray_detector', photo_name)

            # Set timestamp
            gallery.timestamp = datetime.now()

            gallery.save()

            photo_counter += 1
            print(f'Photo {photo_name} saved!')

        elif key == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    # Simpan nilai counter ke dalam file
    with open(counter_file, 'wb') as f:
        pickle.dump(photo_counter, f)

# Panggil fungsi open_camera()
# open_camera()
