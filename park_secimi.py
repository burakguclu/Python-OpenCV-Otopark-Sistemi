import cv2
import pickle

video_path = 'otoparkVideo.mp4'
file_path = 'park_koordinatlari'
window_name = "Park Yeri Secimi"

cap = cv2.VideoCapture(video_path)
success, img_first_frame = cap.read()
cap.release()

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 1280, 720)

try:
    with open(file_path, 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

temp_point = None

def mouseClick(event, x, y, flags, param):
    global temp_point, posList

    if event == cv2.EVENT_LBUTTONDOWN:
        if temp_point is None:
            temp_point = (x, y)
        else:
            posList.append((temp_point, (x, y)))
            temp_point = None
            with open(file_path, 'wb') as f:
                pickle.dump(posList, f)

    if event == cv2.EVENT_RBUTTONDOWN:
        if len(posList) > 0:
            posList.pop()
            with open(file_path, 'wb') as f:
                pickle.dump(posList, f)

cv2.setMouseCallback(window_name, mouseClick)

while True:
    img = img_first_frame.copy()
    
    for line in posList:
        cv2.line(img, line[0], line[1], (255, 0, 255), 2)
        
    if temp_point:
        cv2.circle(img, temp_point, 5, (0,0,255), -1)

    cv2.imshow(window_name, img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()