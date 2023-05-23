import cv2
import os
from django.conf import settings

settings.configure()

cam =cv2.VideoCapture(0)
photo_counter = 1

# Membuat folder jika belum ada
save_folder = os.path.join(settings.BASE_DIR, 'static', 'images', 'memory_tray_detector')
os.makedirs(save_folder, exist_ok=True)

# os.makedirs(save_folder, exist_ok=True)

cam = cv2.VideoCapture(0)
photo_counter = 1  # Variable to keep track of the photo counter

while True:
    check, frame = cam.read()

    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    
    # Check if spacebar is pressed
    if key == 32:
        photo_name = f'photo{photo_counter}.jpg'  # Generate a unique photo name
        photo_path = os.path.join(save_folder, photo_name)  # Construct the full path to save the photo
        cv2.imwrite(photo_path, frame)  # Save the current frame as a photo
        photo_counter += 1  # Increment the photo counter
        print(f'Photo {photo_name} saved!')
        
    # Check if 'Esc' key is pressed
    elif key == 27:
        break

cam.release()
cv2.destroyAllWindows()