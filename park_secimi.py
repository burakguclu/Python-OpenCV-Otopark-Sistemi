import cv2
import pickle

width, height = 107, 48
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

def mouseClick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
    with open(file_path, 'wb') as f:
        pickle.dump(posList, f)

cv2.setMouseCallback(window_name, mouseClick)

while True:
    img = img_first_frame.copy()
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow(window_name, img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break