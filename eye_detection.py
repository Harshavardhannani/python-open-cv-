import cv2
import time
import os
from sound_module import play_alarm_sound


cascade_path = os.path.join('eye', 'haarcascade_eye.xml')
if not os.path.exists(cascade_path):
    raise FileNotFoundError(f"{cascade_path} not found")


max_retries = 3
retry_delay = 1
cap = None

for i in range(max_retries):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    if cap.isOpened():
        break
    print(f"Webcam initialization attempt {i+1} failed")
    time.sleep(retry_delay)
    
if not cap or not cap.isOpened():
    raise IOError(f"Failed to open webcam after {max_retries} attempts")

# Load cascades
face_cascade = cv2.CascadeClassifier(cascade_path)
eye_cascade = cv2.CascadeClassifier(cascade_path)

closed_eye_duration = 3
alarm_triggered = False
sleep_warning_duration = 3

while True:
    ret, img = cap.read()
    if not ret:
        print("Failed to capture frame from webcam - trying to reopen...")
        cap.release()
        time.sleep(1)
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("Failed to reopen webcam")
            break
        continue
        
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    except cv2.error as e:
        print(f"OpenCV error: {e}")
        continue

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if len(eyes) == 0:  
            closed_eye_duration += 1
            cv2.putText(img, "Warning: You may be sleeping!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (10, 10, 255), 2)
            if closed_eye_duration >= sleep_warning_duration and not alarm_triggered:
                play_alarm_sound('test_sound.wav', duration=3) 
                alarm_triggered = True
        else:
            closed_eye_duration = 0
            alarm_triggered = False

    cv2.putText(img, "Press ESC to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow('Eye Sleep Detection', img)
    
    
    key = cv2.waitKey(30) & 0xff
    if key in (27, 113):  
        print("Exiting program...")
        break

cap.release()
