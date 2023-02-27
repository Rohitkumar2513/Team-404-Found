from flask import Flask, render_template, url_for, Response, request,redirect
import cv2
import numpy as np
import os
import imutils
import json
import threading
from PIL import Image
import time
import pymongo as mongo
from datetime import datetime, timedelta

import sys
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

client = mongo.MongoClient("mongodb://localhost:27017/")

# names = ['None', 'Someone'] 
# with open("names.json", "r") as f:
#     names_json = json.loads(f.read())
# names = ["None"] + list(names_json.values())
# print(names)
flag=1
app = Flask(__name__)



def gen_frames():
    video = cv2.VideoCapture(0)
    video.set(3, 640)
    video.set(4, 480)

    minW = 0.1*video.get(3)
    minH = 0.1*video.get(4)

    font = cv2.FONT_HERSHEY_SIMPLEX
    with open("names.json", "r") as f:
        names_json = json.loads(f.read())
    names = ["None"] + list(names_json.values())
    print(names)
    flag=1
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    while flag:
        global msg
        bg = "black"
        success, frame = video.read()
        if not success:
            msg = "Camera source not found"
            print(msg)
            break
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        if len(faces) > 1:
            print("Only one face allowed")

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            if ((100-confidence)>30):
                # print(id)
                id = names[id]
                db = client["userss"]
                collection = db["Attendance"]
                today = datetime.today().replace(microsecond=0)
                rec={   "name":id,
                        "attendence": True ,
                        "timestamp": today,
                        "location": {
                            "lat": 69,
                            "lon": 420
                        },
                        "screenshot": "upload to imgur and paste url here? OR None to mark attendance without video"
                    }
                collection.insert_one(rec)
                flag=0
                confidence = "  {0}%".format(round(100 - confidence))
                break
            else:
                id = "Unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            cv2.putText(frame, str(id), (x+5,y-5), font, 1, (0,0,255), 2)
            cv2.putText(frame, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        fps = f"FPS: {video.get(cv2.CAP_PROP_FPS)}"
        # print(fps)
        cv2.putText(
            img=frame,
            text=fps,
            org=(100, 100),
            fontScale=2.0,
            fontFace=font,
            color=(0, 0, 255)
        )
        ret, buffer = cv2.imencode('.jpg', frame)
        if cv2.waitKey(1) == ord("q"):
            break
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    video.release()
    cv2.destroyAllWindows()
def gen_frames_for_register(name):

    cam = cv2.VideoCapture(0)
    cam.set(3, 640) 
    cam.set(4, 480) 
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") #Note the change


    # face_id = input('\n Enter id: ')
    # face_name = input("\n Enter name (str): ")
    face_name = name
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
        
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            # print(count)
            # cv2.imwrite("D:\\Hackathon dumps 2k23\\OpenCV-Face-Recognition\\FacialRecognition\\dataset\\User." + str(face_id) + '.' + str(count) + ".jpg",gray[y:y+h,x:x+w])
            cv2.imwrite("dataset\\User." + str(face_id) + '.' + str(count) + ".jpg",gray[y:y+h,x:x+w])
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

            

        if count >= 50: # CHANGE COUNT HERE
            break


    print("\n [INFO] Exiting Program and cleanup stuff")

    cam.release()
    cv2.destroyAllWindows()
    os.system("py 02_face_training.py")
    

    # cam.release()
    # cv2.destroyAllWindows()


               
        
# def run_dataset_script(name):
#     gen_frames_for_register("kanan")
#     os.system(f"py 02_face_training.py") 
#     return True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register-face", methods=["GET", "POST"])
def register_face():
    flag=0
    
    return render_template("register_face.html",msg="Completed")    

msg = ""
@app.route("/mark-attendance")
def mark_attendance():
    flag=1
    global msg
    return render_template("mark_attendance.html", msg=msg)

@app.route("/video-feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/video_feed_for_register")
def video_feed_for_register():
    return Response(gen_frames_for_register("nanda01"), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)