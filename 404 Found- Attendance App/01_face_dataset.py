import cv2
import os
from PIL import Image
import time
import json
import sys

cam = cv2.VideoCapture(0)
cam.set(3, 640) 
cam.set(4, 480) 
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") #Note the change


# face_id = input('\n Enter id: ')
# face_name = input("\n Enter name (str): ")
face_name = sys.argv[1]
with open("names.json", "r") as f:
    json_data = f.readlines()
    face_id = int(json_data[-2].split(":")[0].strip().replace("\"", ""))
    json_data[-2] = json_data[-2][:-1] + ",\n"
    json_data[-1] = f'    "{face_id+1}": "{face_name}"\n'
json_data.append("}")
print(json_data)

with open("names.json", "w") as f:
    f.writelines(json_data)

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
count = 0

while(True):

    ret, img = cam.read()
    
    cv2.imshow('image1', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        # print(count)
        # cv2.imwrite("D:\\Hackathon dumps 2k23\\OpenCV-Face-Recognition\\FacialRecognition\\dataset\\User." + str(face_id) + '.' + str(count) + ".jpg",gray[y:y+h,x:x+w])
        cv2.imwrite("C:\\Users\\ramuk\\OneDrive\\Desktop\\innovation marathon\\dataset\\User." + str(face_id) + '.' + str(count) + ".jpg",gray[y:y+h,x:x+w])
        cv2.imshow('image', img)
        

        
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 100: # CHANGE COUNT HERE
         break


print("\n [INFO] Exiting Program and cleanup stuff")
# cam.release()
# cv2.destroyAllWindows()


