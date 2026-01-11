import cv2
import pickle
import numpy as np

video_path = 'otoparkVideo.mp4'
file_path = 'park_koordinatlari'
window_name = "Park Yeri Secimi (4 Nokta)"

cap = cv2.VideoCapture(video_path)
success, img_first_frame = cap.read()
cap.release()

if not success:
    exit()

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 1280, 720)

try:
    with open(file_path, 'rb') as f:
        posList = pickle.load(f)
        if len(posList) > 0 and not isinstance(posList[0], list): 
             posList = []
except:
    posList = []

current_points = []

def mouseClick(event, x, y, flags, param):
    global current_points, posList

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(current_points) < 4:
            current_points.append((x, y))
        
        if len(current_points) == 4:
            posList.append(current_points)
            current_points = []
            with open(file_path, 'wb') as f:
                pickle.dump(posList, f)

    if event == cv2.EVENT_RBUTTONDOWN:
        if len(posList) > 0:
            posList.pop()
            with open(file_path, 'wb') as f:
                pickle.dump(posList, f)
        current_points = []

cv2.setMouseCallback(window_name, mouseClick)

while True:
    img = img_first_frame.copy()

    for points in posList:
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 0, 255), 2)

    if len(current_points) > 0:
        pts_curr = np.array(current_points, np.int32)
        pts_curr = pts_curr.reshape((-1, 1, 2))
        cv2.polylines(img, [pts_curr], False, (255, 0, 0), 2)
        for pt in current_points:
            cv2.circle(img, pt, 4, (0, 0, 255), -1)

    cv2.imshow(window_name, img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()