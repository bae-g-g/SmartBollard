import cv2
import numpy as np
from ultralytics import YOLO
import time
import requests  # HTTP 요청을 위한 라이브러리

# YOLO 모델 로드
model = YOLO('yolov8n.pt') 
model.classes = [0, 1, 2, 3]  # 특정 클래스만

# 비디오 스트림 열기
video_url = "http://172.20.10.3:5000/video_feed"
cap = cv2.VideoCapture(video_url)

if not cap.isOpened():
    print("비디오 스트림을 열 수 없습니다.")
    exit()

cv2.setUseOptimized(True)
cv2.setNumThreads(4)

frame_skip = 10  # 프레임 건너뛰기
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("프레임을 가져올 수 없습니다.")
        break

    if frame_count % frame_skip == 0:
        results = model(frame)

        detected = False
        for result in results:
            for cls in result.boxes.cls:
                class_name = model.names[int(cls)]
                if class_name.lower() in ["car", "truck", "bus", "person"]:
                    print("---------------차량 인식----------------")
                    detected = True
                    break
            if detected:
                break
        
        # 차량 인식 여부에 따른 HTTP 요청
        if detected:
            pass
            response = requests.get("http://172.20.10.3:5000/signal/on")
            print("차량 인식됨. 요청 보냄:", response.status_code)
        else:
            pass
            response = requests.get("http://172.20.10.3:5000/signal/off")
            print("차량 미인식. 요청 보냄:", response.status_code)

    
    frame_count += 1

cap.release()
cv2.destroyAllWindows()



@app.route('/')
def index():
    return "TEAM-GTQ Server"

def generate():
    while True:
        frame = picam2.capture_array()
        ret, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 전역 변수로 상태 관리
current_state = "off"

@app.route('/signal', methods=['GET'])
def signal():
    global current_state
    return current_state

@app.route('/signal/<state>', methods=['GET'])
def set_signal(state):
    global current_state
    if state in ["on", "off"]:
        current_state = state
        return f"{state}", 200
    else:
        return "Invalid state", 400
