import cv2
import numpy as np
import os 
import imutils
import sys
from winsound import Beep
from time import sleep

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

id = 0

names = ['None', 'Nanda','rohit','sri','tej','Kannan','sri','Kannan','Kg'] 


cam = cv2.VideoCapture(1)
cam.set(3, 640) 
cam.set(4, 480) 

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

unknown = []

while True:

    ret, img =cam.read()
    # img=imutils.resize(img,width=300)
    # print("resizing")
   
     # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    print(faces)
    # print("to gray")

    for(x,y,w,h) in faces:
        print("face loop")

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        if ((100-confidence)>30):
            print(id)
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "Unknown"
            unknown.append(True)
            # if len(unknown) > 20:
            #     cv2.imwrite("screenshot.jpg", img)
                # os.system("python ./alert.py")
                # break

            
            confidence = "  {0}%".format(round(100 - confidence))

        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (0,0,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    img = imutils.resize(img, width=400)
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff 
    if k == 27:
        break

print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()

# os.system("python ./alert.py")
# count = 0
# while True:
#     Beep(3000, 1000)
#     sleep(0.2)
#     if count >= 5:
#         break

