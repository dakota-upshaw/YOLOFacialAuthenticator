from cvzone.FaceDetectionModule import FaceDetector
import cv2
import cvzone
from time import time

########################
classID = 0# 0 is fake, 1 is real
outputFolderPath = 'Dataset/DataCollect'

confidence = 0.8
save = True
blurThreshold = 35 # larger is more focused

debug = False
offsetPercentageW = 10
offsetPercentageH = 20
camWidth, camHeight = 640, 480
floatingPoint = 6
#######################

# Initialize the webcam
# '2' means the third camera connected to the computer, usually 0 refers to the built-in webcam
cap = cv2.VideoCapture(1)
cap.set(3, camWidth)
cap.set(4, camHeight)
# Initialize the FaceDetector object
# minDetectionCon: Minimum detection confidence threshold
# modelSelection: 0 for short-range detection (2 meters), 1 for long-range detection (5 meters)
detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)


# Run the loop to continually get frames from the webcam
while True:
    # Read the current frame from the webcam
    # success: Boolean, whether the frame was successfully grabbed
    # img: the captured frame
    success, img = cap.read()
    imgOut = img.copy()

    # Detect faces in the image
    # img: Updated image
    # bboxs: List of bounding boxes around detected faces
    img, bboxs = detector.findFaces(img, draw=False)

    #Should reset after every iteration
    listBlur = [] # True False vals indicating if faces are blur or not. Value for each face.
    listInfo = [] # Normalized vals and class name for the label text file. All info to send to text file. For each face.

    # Check if any face is detected
    if bboxs:
        # Loop through each bounding box
        for bbox in bboxs:
            # bbox contains 'id', 'bbox', 'score', 'center'

            # ---- Get Data  ---- #
            #center = bbox["center"]
            x, y, w, h = bbox['bbox']
            score = bbox["score"][0]
            #score = int(bbox['score'][0] * 100)

            # -- Check Score -- #
            if score > confidence:

                # --- Add offset to the face detected -- #
                offsetW = (offsetPercentageW / 100) * w
                x = int(x - offsetW)
                w = int(w + offsetW * 2)

                offsetH = (offsetPercentageH / 100) * h
                y = int(y - offsetH * 3)
                h = int(h + offsetH * 3.5)

                # -- Avoid Vals Below 0 -- #
                if x < 0: x = 0
                if y < 0: y = 0
                if w < 0: w = 0
                if h < 0: h = 0

                # -- Find Blurriness -- #
                imgFace = img[y:y + h, x:x + w]  # crop face
                cv2.imshow("Face", imgFace)
                blurValue = int(cv2.Laplacian(imgFace, cv2.CV_64F).var())
                if blurValue > blurThreshold:
                    listBlur.append(True) # if not blurry/little blurry
                else:
                    listBlur.append(False) # if blurry

                # -- Normalize Vals -- #
                # normalizing is putting values between 0 and 1
                ih, iw, _ = img.shape
                xc, yc = x + w/2, y + h/2
                xcn, ycn = round(xc/iw, floatingPoint), round(yc/ih, floatingPoint)
                wn, hn = round(w/iw, floatingPoint), round(h/ih, floatingPoint)

                # -- Avoid Vals Above 1 -- #
                if xcn > 1:
                    xcn = 1
                if ycn > 1:
                    ycn = 1
                if wn > 1:
                    wn = 1
                if hn > 1:
                    hn = 1

                listInfo.append(f"{classID} {xcn} {ycn} {wn} {hn}\n")
                # ---- Draw Data  ---- #
                cv2.rectangle(imgOut, (x, y, w, h), (255, 0, 0), 3)
                cvzone.putTextRect(imgOut, f'Score: {int(score*100)}% Blur: {blurValue}', (x, y-20),
                                    scale=2, thickness=3)
                if debug:
                    cv2.rectangle(img, (x, y, w, h), (255, 0, 0), 3)
                    cvzone.putTextRect(img, f'Score: {int(score * 100)}% Blur: {blurValue}', (x, y - 20),
                                       scale=2, thickness=3)

        # ------ To Save -------- #
        if save:
            if all(listBlur) and listBlur != []: # if its not empty, and if the image is clear then save
                # ------- Save image ---- #
                timeNow = time()
                timeNow = str(timeNow).split('.') # split the seconds at the decimal point
                timeNow = timeNow[0] + timeNow[1]
                cv2.imwrite(f"{outputFolderPath}/{timeNow}.jpg", img) # use time instead of count bc count would reset, we want unique val
                # ------- Save Label Text File ---- #
                for info in listInfo: # store in the same txt file, multiple lines
                    f = open(f"{outputFolderPath}/{timeNow}.txt", 'a')  # f for file. a is the flag for append. if file isn't present then create it. If present then add the data to it
                    f.write(info)
                    f.close()

    # Display the image in a window named 'Image'
    cv2.imshow("Image", imgOut)
    # Wait for 1 millisecond, and keep the window open
    cv2.waitKey(1)
