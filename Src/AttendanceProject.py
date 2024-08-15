import cv2
import firestore as firestore
import numpy as np
import face_recognition
import pyttsx3 as textSpeach
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import os
from datetime import datetime


config = {
    "apiKey": "AIzaSyC_uLZz1i7hg6IAF0eFCJI9B9HHq0tbqWM",
    "authDomain": "attendance-system-b5b46.firebaseapp.com",
    "projectId": "attendance-system-b5b46",
    "databaseURL": "https://attendance-system-b5b46-default-rtdb.firebaseio.com/",
    "storageBucket": "attendance-system-b5b46.appspot.com",
    "serviceAccount": "cerificate.json",
    'messagingSenderId': "752097683746",
    'appId': "1:752097683746:web:86fb7a54c83fe8085a1d7b"
}

cred = credentials.Certificate("cerificate.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


path = 'trainingImg'
# list to get the images automatically
images = []
# to get the names
classNames = []
# to get the images to the project
theListOfNames = os.listdir(path)
# import the images one by one
classid = []
for cl in theListOfNames:
    # to Load the image ("cl" is the name of the image)
    curImg = cv2.imread(f'{path}/{cl}')
    # to add the images to the list ("images")
    images.append(curImg)
    # to add the names to the list ("classNames")
    classNames.append(os.path.splitext(cl)[0].split('_')[0])
    classid.append(os.path.splitext(cl)[0].split('_')[1])
print(classNames)
print(classid)

fixedH = 9
fixedM = 10


# Function to Get all the encodes for the file
def findEncodings(images):
    # List to have all encodes
    encodeList = []
    for img in images:
        # convert the image to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # To encode the face to num
        encode = face_recognition.face_encodings(img)[0]
        # to add to the list ("encode")
        encodeList.append(encode)
    return encodeList


def MarkAttendence(name, ids):
    with open('Attendance.csv', 'r+') as f:
        myDatalist = f.readlines()
        nameList = []
        for line in myDatalist:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.now()
            timestr = now.strftime('%c')
            lateDays(ids)
            f.writelines(f'\n{name}, {timestr}')
            textSpeach.speak("Welcome" + name, 1)


def lateDays(ids):
    timestrh = datetime.now().hour

    timestrm = datetime.now().minute
    print(ids)
    lD = db.collection('Members').document(ids).get({'LateDay'})
    print(lD.to_dict())
    thedayv = '{}'.format(lD.to_dict()['LateDay'])
    if (timestrh > fixedH):
        thedayv = int(thedayv) + 1
        db.collection('Members').document(ids).update({'theDay': firestore.SERVER_TIMESTAMP, 'LateDay': thedayv})
        print(thedayv)
    elif (timestrh == fixedH and timestrm > fixedM):
        thedayv = int(thedayv) + 1
        db.collection('Members').document(ids).update({'theDay': firestore.SERVER_TIMESTAMP, 'LateDay': thedayv})


# Call the function
encodeListKnow = findEncodings(images)
print("Encode Complete")

# To initialize the webcam
cap = cv2.VideoCapture(0)
# to get each frame one by one
while True:
    # to get the image from the webcam
    success, img = cap.read()
    # to small the size of the image
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # convert the image to RGB
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Show the location of the face
    faceCrFrame = face_recognition.face_locations(imgS)
    # To encode the face to num (will send the small image and the location of faces)
    encodesCrFrame = face_recognition.face_encodings(imgS, faceCrFrame)
    # iterate to compare the Faces in webcam with our images (use zip to be in the same loop)

    for encodeFace, faceLoc in zip(encodesCrFrame, faceCrFrame):
        # To compare the Faces (The 128 measurements by liner SVM)
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace, 0.5)
        # To see the similarity between the faces (the lower the better)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)

        # to take the lowest value
        matchIndex = np.argmin(faceDis)
        # to print name
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            ids = classid[matchIndex]
            # Show the location of the face
            y1, x2, y2, x1 = faceLoc
            # to make the size big again
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (81, 186, 0), 2)
            cv2.rectangle(img, (x1, y2 - 25), (x2, y2), (81, 186, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 7, y2 - 6), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 2)
            MarkAttendence(name, ids)

        else:
            y1, x2, y2, x1 = faceLoc
            # to make the size big again
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 25), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "Not Registered", (x1 + 7, y2 - 6), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 2)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(10) == 13:
        break
cap.release()
cv2.destroyAllWindows()
