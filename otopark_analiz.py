import cv2
import pickle
import numpy as np

video_path = 'otoparkVideo.mp4'
pickle_path = 'park_koordinatlari'
window_name = "Otopark Analizi (Poligon)"

cap = cv2.VideoCapture(video_path)

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 1280, 720)

try:
    with open(pickle_path, 'rb') as f:
        posList = pickle.load(f)
except:
    exit()

def checkParkingSpace(imgPro, imgOriginal):
    spaceCounter = 0

    for points in posList:
        pts = np.array(points, np.int32)
        mask = np.zeros(imgPro.shape, np.uint8)
        cv2.drawContours(mask, [pts], -1, 255, -1)
        masked_image = cv2.bitwise_and(imgPro, imgPro, mask=mask)
        count = cv2.countNonZero(masked_image)
        area = cv2.contourArea(pts)
        
        if area < 100: area = 100 
            
        density = count / area

        if density < 0.18: 
            color = (0, 255, 0)
            thickness = 3
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.polylines(imgOriginal, [pts], True, color, thickness)

    cv2.rectangle(imgOriginal, (20, 20), (270, 70), (0,0,0), -1) 
    cv2.putText(imgOriginal, f'Bos Alan: {spaceCounter}/{len(posList)}', (30, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

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

cap.release()
cv2.destroyAllWindows()