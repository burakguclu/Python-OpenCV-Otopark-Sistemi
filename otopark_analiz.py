import cv2
import pickle
import numpy as np

video_path = 'otoparkVideo.mp4'
pickle_path = 'park_koordinatlari'
width, height = 107, 48
window_name = "Otopark Analizi"

cap = cv2.VideoCapture(video_path)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 1280, 720)

with open(pickle_path, 'rb') as f:
    posList = pickle.load(f)

def checkParkingSpace(imgPro, imgOriginal):
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

        cv2.rectangle(imgOriginal, pos, (pos[0] + width, pos[1] + height), color, 2)
    
    cv2.putText(imgOriginal, f'Bos: {spaceCounter}/{len(posList)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)

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
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate, img)
    cv2.imshow(window_name, img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break