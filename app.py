# app.py
from flask import Flask, render_template, request, jsonify, url_for, Response
import joblib
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import numpy as np


app = Flask(__name__, template_folder="templates")

### Codigo para escaneo de la camara

def generate_frames(camera_index=0):
    camera = cv2.VideoCapture(camera_index)
    if not camera.isOpened():
        raise RuntimeError(f"Could not start camera with index {camera_index}")

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            for barcode in decode(frame):
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type
                print(f"Found {barcode_type} barcode: {barcode_data}")

                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
                cv2.putText(frame, barcode_data, (barcode.rect[0], barcode.rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True)