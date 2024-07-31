import cv2
import pickle
import numpy as np
import os

# Constants
DATA_DIR = 'data'
NAMES_FILE = os.path.join(DATA_DIR, 'names.pkl')
FACES_FILE = os.path.join(DATA_DIR, 'faces_data.pkl')
HAAR_CASCADE = 'haarcascade_frontalface_default.xml'
FACE_COUNT = 100

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize video capture and face detector
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(HAAR_CASCADE)

faces_data = []
i = 0

name = input("Enter Your Name: ")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50))
        if len(faces_data) < FACE_COUNT and i % 10 == 0:
            faces_data.append(resized_img)
        i += 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
    
    cv2.imshow("Frame", frame)
    
    if cv2.waitKey(1) == ord('q') or len(faces_data) == FACE_COUNT:
        break

video.release()
cv2.destroyAllWindows()

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(FACE_COUNT, -1)

# Save names
if os.path.exists(NAMES_FILE) and os.path.getsize(NAMES_FILE) > 0:
    try:
        with open(NAMES_FILE, 'rb') as f:
            names = pickle.load(f)
        names.extend([name] * FACE_COUNT)
    except (EOFError, pickle.UnpicklingError):
        names = [name] * FACE_COUNT
else:
    names = [name] * FACE_COUNT

with open(NAMES_FILE, 'wb') as f:
    pickle.dump(names, f)

# Save face data
if os.path.exists(FACES_FILE) and os.path.getsize(FACES_FILE) > 0:
    try:
        with open(FACES_FILE, 'rb') as f:
            faces = pickle.load(f)
        faces = np.append(faces, faces_data, axis=0)
    except (EOFError, pickle.UnpicklingError):
        faces = faces_data
else:
    faces = faces_data

with open(FACES_FILE, 'wb') as f:
    pickle.dump(faces, f)
