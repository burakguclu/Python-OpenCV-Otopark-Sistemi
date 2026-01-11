import cv2
import pickle
import numpy as np

video_path = 'otoparkVideo.mp4'
pickle_path = 'park_koordinatlari'
window_name = "Otopark Analizi"

cap = cv2.VideoCapture(video_path)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 1280, 720)

with open(pickle_path, 'rb') as f:
    posList = pickle.load(f)

def checkParkingSpace(imgPro, imgOriginal):
    spaceCounter = 0
    for line in posList:
        pt1, pt2 = line
        
        mask = np.zeros(imgPro.shape, np.uint8)
        cv2.line(mask, pt1, pt2, 255, 1)
        masked_image = cv2.bitwise_and(imgPro, imgPro, mask=mask)
        count = cv2.countNonZero(masked_image)

        if count < 50:
            color = (0, 255, 0)
            spaceCounter += 1
        else:
            color = (0, 0, 255)
        
        cv2.line(imgOriginal, pt1, pt2, color, 2)

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

    checkParkingSpace(imgThreshold, img)
    cv2.imshow(window_name, img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break