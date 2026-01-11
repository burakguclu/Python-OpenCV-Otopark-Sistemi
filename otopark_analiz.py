import cv2
import pickle
import numpy as np

video_path = 'otoparkVideo.mp4'
pickle_path = 'park_koordinatlari'
width, height = 107, 48

cap = cv2.VideoCapture(video_path)

with open(pickle_path, 'rb') as f:
    posList = pickle.load(f)

def checkParkingSpace(imgPro):
    spaceCounter = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            spaceCounter += 1
        else:
            color = (0, 0, 255)

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2)

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    if not success:
        break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)

    checkParkingSpace(imgThreshold)
    cv2.imshow("Otopark Analizi", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break