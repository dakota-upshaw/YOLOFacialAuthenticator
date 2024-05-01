from ultralytics import YOLO
import cv2
import cvzone
import math
import time
import serial

ser = serial.Serial('COM3', 115200, timeout=1) #listening serial at the same baud rate as the separate arduino code

 #TO DO:
confidence = 0.8
cap = cv2.VideoCapture(0)  # For Webcam
cap.set(3, 640)
cap.set(4, 480)
# cap = cv2.VideoCapture("../Videos/motorbikes.mp4")  # For Video
model = YOLO("C:/Users/Master/Desktop/378FacialRecog/runs/detect/train6/weights/best.pt") # change to the best weight made from running train.py
classNames = ["fake", "real"]
#model = YOLO("../models/yolov8l.pt")
 
prev_frame_time = 0
new_frame_time = 0
 
while True:
    new_frame_time = time.time()
    success, img = cap.read()
    results = model(img, stream=True)
    
    is_real_detected = False
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            color = (128, 128, 128)
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
                color = (0, 0, 255) if classNames[cls] == 'fake' else (0, 255, 0)
                if classNames[cls] == 'real':
                    is_real_detected = True
                    if is_real_detected is None:
                        real_face_time = time.time()
                        
            cvzone.cornerRect(img, (x1, y1, w, h),colorC=color, colorR= color)
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1, colorR= color, colorB=color)
            
    if is_real_detected:
        if time.time() - real_face_time >= 3 and not prompt_shown:
            ser.write(b'scan_rfid\n')
            prompt_shown = True
    else:
        real_face_time = None
        prompt_shown = False

    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print(fps)
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)