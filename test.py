import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
from sklearn.neighbors import KNeighborsClassifier

def speak(message):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(message)

# Constants
CASCADE_PATH = 'haarcascade_frontalface_default.xml'
BACKGROUND_IMAGE_PATH = 'bg1.jpg'
FACES_FILE = 'data/faces_data.pkl'
NAMES_FILE = 'data/names.pkl'
COL_NAMES = ['NAME', 'TIME']
ATTENDANCE_DIR = 'Attendance'
N_NEIGHBORS = 5

# Load the Haar Cascade classifier
facedetect = cv2.CascadeClassifier(CASCADE_PATH)
if facedetect.empty():
    raise IOError(f"Failed to load cascade classifier from {CASCADE_PATH}")

# Load background image
imgBackground = cv2.imread(BACKGROUND_IMAGE_PATH)
if imgBackground is None:
    print("Error: Could not load background image.")
    imgBackground = np.zeros((720, 1280, 3), np.uint8)  # Create a black background as fallback

# Load face data and names
with open(FACES_FILE, 'rb') as f:
    faces_data = pickle.load(f)

with open(NAMES_FILE, 'rb') as f:
    names = pickle.load(f)

# Train KNN classifier
knn = KNeighborsClassifier(n_neighbors=N_NEIGHBORS)
knn.fit(faces_data, names)

# Initialize video capture
video = cv2.VideoCapture(0)

def write_attendance(name, timestamp, date):
    attendance_file = os.path.join(ATTENDANCE_DIR, f"Attendance_{date}.csv")
    exist = os.path.isfile(attendance_file)
    with open(attendance_file, 'a' if exist else 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not exist:
            writer.writerow(COL_NAMES)
        writer.writerow([name, timestamp])

while True:
    ret, frame = video.read()
    if not ret:
        print("Error: Failed to capture image from video.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        if cv2.waitKey(1) == ord('o'):
            speak("Attendance Taken..")
            time.sleep(2)  # Adjust the sleep time as needed
            write_attendance(str(output[0]), str(timestamp), date)

    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)

    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
video.release()
cv2.destroyAllWindows()
