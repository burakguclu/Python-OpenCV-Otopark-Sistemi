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

drawing = False
ix, iy = -1, -1
img_temp = img_first_frame.copy()

def mouseClick(event, x, y, flags, param):
    global ix, iy, drawing, posList, img_temp

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_temp = img_first_frame.copy()
            for line in posList:
                cv2.line(img_temp, line[0], line[1], (255, 0, 255), 2)
            cv2.line(img_temp, (ix, iy), (x, y), (255, 0, 0), 2)
            cv2.imshow(window_name, img_temp)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        posList.append(((ix, iy), (x, y)))
        with open(file_path, 'wb') as f:
             pickle.dump(posList, f)
        img_temp = img_first_frame.copy()

    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(posList) > 0:
            posList.pop()
            with open(file_path, 'wb') as f:
                pickle.dump(posList, f)

cv2.setMouseCallback(window_name, mouseClick)
cv2.imshow(window_name, img_first_frame)

while True:
    if not drawing:
        img_display = img_first_frame.copy()
        for line in posList:
            cv2.line(img_display, line[0], line[1], (255, 0, 255), 2)
        cv2.imshow(window_name, img_display)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()