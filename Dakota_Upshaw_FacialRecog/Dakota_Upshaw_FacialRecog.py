import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import ultralytics
import cv2
from time import time

#----------------DATA COLLECTOR---------------------
classID = 0 #0 is fake, 1 is real
outputDir = '/home/dakota/378semproject/CECS378FacialRecog/Dakota_Upshaw_FacialRecog/Dataset/Datacollect'
confidence = 0.8
save =True
debug = False

blurThres = 35 #the bigger the better focus
offsetPercentW = 10
offsetPercentH = 20
camW, camH = 640 ,480

cap = cv2.VideoCapture(2)
cap.set(3, camW)
cap.set(4, camH)

# Initialize the FaceDetector object
# minDetectionCon: Minimum detection confidence threshold
# modelSelection: 0 for short-range detection (2 meters), 1 for long-range detection (5 meters)
detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

while True:
    success, img = cap.read()
    imgOut = img.copy()

    # Detect faces in the image
    # img: Updated image
    # bboxs: List of bounding boxes around detected faces
    img, bboxs = detector.findFaces(img, draw=False)
    
    listBlur = [] # bool values indicating if faces are blurred
    listInfo  = [] # normal values and class name for label txt file
    
    # Check if any face is detected
    if bboxs:
        for bbox in bboxs:
            x, y, w, h = bbox['bbox']
            score = bbox["score"][0]
            print(x,y,w,h)
            
            # check score
            if score > confidence:
            
                #offset for new bounding box face detections
                offsetW = (offsetPercentW/100) * w
                x = int(x - offsetW)
                w = int(w + offsetW *2)
            
                offsetH = (offsetPercentH/100) * w
                y = int(y - offsetH*3)
                h = int(h + offsetH *3.5)
            
            
                #prevents errors with values below 0 (face off camera)
                if x < 0: x = 0
                if y < 0: y = 0
                if w < 0: w = 0
                if h < 0: h = 0
            
                #detect bluriness
                imgFace = img[y : y + h,x:x+w]
                cv2.imshow("Face", imgFace)
                blurVal = int(cv2.Laplacian(imgFace, cv2.CV_64F).var())
                
                if blurVal > blurThres:
                    listBlur.append(True)
                else: 
                    listBlur.append(False)
                    
                
                ####normalize vals for YOLO format
                imgW, imgH, _ = img.shape
                #need the center points
                xc, yc = x+w/2,y+h/2
                #print(xc,yc)
                #center points normalized
                xcn = round(xc/imgW, 6)
                ycn = round(yc/imgH, 6)
                wn, hn = round(w/imgW, 6), round(h/imgH, 6)
                #print(xcn,ycn, wn, hn)
                
                #prevents errors with values above 1 (face off camera for normalized values, prevents data corruption)
                if xcn > 1: xcn = 1
                if ycn > 1: ycn = 1
                if wn > 1: wn = 1
                if hn > 1: hn = 1
                
                listInfo.append(f'{classID} {xcn} {ycn} {wn} {hn}\n')
            
            
                #draw objects
                cvzone.putTextRect(imgOut,f'Score: {int(score*100)}% Blur: {blurVal}',(x,y-20),scale =2, thickness = 2)
                cv2.rectangle(imgOut,(x,y,w,h),(255,0,0),3) #new bounding box resized
                
                if debug:                   
                    cvzone.putTextRect(img,f'Score: {int(score*100)}% Blur: {blurVal}',(x,y-20),scale =2, thickness = 2)
                    cv2.rectangle(img,(x,y,w,h),(255,0,0),3) #new bounding box resized
                
        # saving imgs        
        if save:
            #print(listBlur, all(listBlur)) #debug output
            if all(listBlur) and listBlur != []:
               timeCurr = time()
               timeCurr = str(timeCurr).split('.')
               timeCurr = timeCurr[0]+timeCurr[1]
               print(timeCurr)
               cv2.imwrite(f"{outputDir}/{timeCurr}.jpg", img) 
               
               #save label txt
               for info in listInfo:

                   f = open(f"{outputDir}/{timeCurr}.txt", "a")
                   f.write(info)
                   f.close
            



    cv2.imshow("Image", imgOut)
    cv2.waitKey(1)