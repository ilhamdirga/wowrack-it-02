import cv2
import os
import pickle
from datetime import datetime
import time

from django.conf import settings
from trash_can_detector.models import Gallery, Camera, CamCard
from django.shortcuts import get_object_or_404

def open_camera(save_folder, cam_id):
    # Mengambil instance camera sesuai Camera ID
    camera = get_object_or_404(Camera, id=cam_id)
    # address = camera.ip_camera
    cam = cv2.VideoCapture(0)
    # cam.open(address)

    # Cek apakah file counter sudah ada
    counter_file = os.path.join(settings.BASE_DIR, 'trash_can_detector', 'ml_models', 'counter.pkl')
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
            picture = os.path.join('trash_can_detector', photo_name)
            current_time = datetime.now()
            gallery = Gallery.objects.create(name = camera,
                                             picture = picture, 
                                             quantity = quantity,
                                             timestamp = current_time
                                             )
            gallery.save()

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