from picamera2 import Picamera2
import cv2
from flask import Flask, Response

picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)
picam2.configure(config)
picam2.set_controls({"FrameDurationLimits": (33333, 33333)})
picam2.start()




app = Flask(__name__)

@app.route('/')
def index():
    return "TEAM-GTQ Server"



#영상전송

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



#신호전송

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





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)