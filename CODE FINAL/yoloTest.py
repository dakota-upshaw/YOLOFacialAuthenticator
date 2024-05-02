from ultralytics import YOLO
import cv2
import cvzone
import math
import time

 #TO DO:
confidence = 0.8
cap = cv2.VideoCapture(0)  # For Webcam
cap.set(3, 640)
cap.set(4, 480)
# cap = cv2.VideoCapture("../Videos/motorbikes.mp4")  # For Video
model = YOLO("C:/Users/Master/Desktop/378FacialRecog/runs/detect/CHECKPOINT3/weights/best.pt") # change to the best weight made from running train.py
classNames = ["fake", "real"]
#model = YOLO("../models/yolov8l.pt")
 

 
prev_frame_time = 0
new_frame_time = 0
 
while True:
    new_frame_time = time.time()
    success, img = cap.read()
    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            #cvzone.cornerRect(img, (x1, y1, w, h))
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            if conf> confidence:
                if classNames[cls] == 'real': #TO DO: can write the authorization code for the RFID here
                    color = (0,255,0) #green
                else:
                    color = (0,0,255) #red
            cvzone.cornerRect(img, (x1, y1, w, h),colorC=color, colorR= color)
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1, colorR= color, colorB=color)
 
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print(fps)
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)