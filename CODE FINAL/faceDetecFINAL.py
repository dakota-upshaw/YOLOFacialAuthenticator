from ultralytics import YOLO
import cv2
import cvzone
import math
import time
import serial

ser = serial.Serial('COM4', 115200, timeout=1) #listening serial at the same baud rate as the separate arduino code

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
real_face_time = None
access_granted = False
threshold = 5
rfid_checking = False
revalidation = False
 
while True:
    new_frame_time = time.time()
    success, img = cap.read()
    results = model(img, stream=True, verbose = False)
    
    is_real_detected = False
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            conf = math.ceil(box.conf[0] * 100) / 100
            cls = int(box.cls[0])
            color = (0, 0, 255) if classNames[cls] == 'fake' else (0, 255, 0)

            if conf > confidence:
                cvzone.cornerRect(img, (x1, y1, x2-x1, y2-y1), colorC=color, colorR=color)
                cvzone.putTextRect(img, f'{classNames[cls]} {conf:.2f}', (x1, max(35, y1-5)), scale=1, thickness=1, colorR=color)
                if classNames[cls] == 'real':
                    is_real_detected = True
                    if real_face_time is None:
                        real_face_time = time.time()

    if is_real_detected and not rfid_checking and not revalidation: #Step 1: Initial RGB Camera Validation
        if time.time() - real_face_time >= threshold:
            ser.write(b'scan_rfid\n')
            rfid_checking = True  # Start RFID checking process
            #print("\n------\nRFID scanning initiated.\n------\n")
    elif not is_real_detected:
        if not rfid_checking:
            real_face_time = None

    if rfid_checking and ser.in_waiting: #Step 2: Monitoring for serial from the arduino code, AKA authorized RFID
        response = ser.readline().decode().strip()
        print(response)
        if response == "IR_Activated":
            rfid_checking = False
            revalidation = True
            real_face_time = None  # Reset face timer for revalidation
            print("IR Mode activated, revalidation required")
        elif response == "Unauthorized Tag":
            rfid_checking = False
            print("Access Denied: Unauthorized RFID tag.")

    if revalidation and is_real_detected: #Step 3: IR Camera Revalidation
        if real_face_time is None:
            real_face_time = time.time()
        if time.time() - real_face_time >= threshold:
            access_granted = True
            revalidation = False
            print("Access Granted: User authenticated successfully")
    
    if access_granted:
        cvzone.putTextRect(img, "AUTHORIZED USER", (50, 50), scale=2, thickness=3, colorR=(0, 255, 0))    
        


    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    #print(f"FPS: {fps}")
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)