import cv2
import numpy as np
import face_recognition

# import image
imgMo = face_recognition.load_image_file('img/Moimg.jfif')
# convert the image to RGB
imgMo = cv2.cvtColor(imgMo, cv2.COLOR_BGR2RGB)

imgMoTest = face_recognition.load_image_file('img/TestMo.jfif')
imgMoTest = cv2.cvtColor(imgMoTest, cv2.COLOR_BGR2RGB)

# Find the Location Or Detect  The Face In The Image
faceLoc = face_recognition.face_locations(imgMo)[0]
# To encode the face to num
encodeMo = face_recognition.face_encodings(imgMo)[0]
# Show the location of the face
cv2.rectangle(imgMo, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 255, 0), 2)

faceLocTest = face_recognition.face_locations(imgMoTest)[0]
encodeMoTest = face_recognition.face_encodings(imgMoTest)[0]
cv2.rectangle(imgMoTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (0, 255, 0), 1)
# To compare the Faces (The 128 measurements by liner SVM)
results = face_recognition.compare_faces([encodeMo], encodeMoTest)
# To see the similarity between the faces (the lower the better)
faceDis = face_recognition.face_distance([encodeMo], encodeMoTest)

print(results, faceDis)
# to write in the show box
cv2.putText(imgMoTest, f'{results} {round(faceDis[0], 2)}', (5, 20), cv2.FONT_ITALIC, 1, (255, 255, 255), 1)

# to show the images
cv2.imshow('Mo Salah', imgMo)
cv2.imshow('Mo Salah Test', imgMoTest)

cv2.waitKey(0)
