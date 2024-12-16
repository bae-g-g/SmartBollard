import cv2
from ultralytics import YOLO
import requests  # HTTP 요청을 위한 라이브러리

# YOLO 모델 로드
model = YOLO('yolov8n.pt') 
model.classes = [ 1, 2, 3, 5, 7]  # 순서대로 자전거 차 오토바이 버스 트럭

# 비디오 스트림 열기
video_url = "http://172.20.10.3:5000/video_feed"
cap = cv2.VideoCapture(video_url)

if not cap.isOpened():
    print("비디오 스트림을 열 수 없습니다.")
    exit()

cv2.setUseOptimized(True)
cv2.setNumThreads(4)

frame_skip = 5  # 프레임 건너뛰기
frame_count = 0

prev_detected = False

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("프레임을 가져올 수 없습니다.")
        break

    if frame_count % frame_skip == 0: #0.15초에 한번씩만만
        results = model(frame)

        detected = False
        
        for cls in results.boxes.cls:
            if cls in [1,2,3,5,7]:
                detected = True
                break
        

        if prev_detected != detected: #http요청을 최소화

            # 차량 인식 여부에 따른 HTTP 요청
            if detected:
                response = requests.get("http://172.20.10.3:5000/signal/on")
                print("차량 인식됨. 요청 보냄:", response.status_code)
            else:
                response = requests.get("http://172.20.10.3:5000/signal/off")
                print("차량 미인식. 요청 보냄:", response.status_code)


        prev_detected = detected

    frame_count += 1

cap.release()
cv2.destroyAllWindows()




# # 전역 변수로 상태 관리
# current_state = "off"

# @app.route('/signal', methods=['GET'])
# def signal():
#     global current_state
#     return current_state

# @app.route('/signal/<state>', methods=['GET'])
# def set_signal(state):
#     global current_state
#     if state in ["on", "off"]:
#         current_state = state
#         return f"{state}", 200
#     else:
#         return "Invalid state", 400