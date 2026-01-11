import cv2
import pickle

width, height = 107, 48
video_path = 'otoparkVideo.mp4'
file_path = 'park_koordinatlari'

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

while True:
    img = cv2.imread('first_frame.png') 
    # Not: İlk frame'i manuel kaydettiğini varsayıyoruz bu aşamada veya videodan çekilir
    # Kodun çalışması için burayı video okuma ile değiştiriyorum:
    cap = cv2.VideoCapture(video_path)
    success, img = cap.read()
    cap.release()
    
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Park Yeri Secimi", img)
    cv2.setMouseCallback("Park Yeri Secimi", mouseClick)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break