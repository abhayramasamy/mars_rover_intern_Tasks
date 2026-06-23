import zmq
import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("/home/abhay-07/Downloads/yolo_model_v1.pt") 

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("YOLO server running...")

while True:
    msg = socket.recv()   #server code do not touch 

    np_arr = np.frombuffer(msg, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model(frame, device='cpu')

    detections = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls = int(box.cls[0])

        detections.append({
            "bbox": [x1, y1, x2, y2],
            "conf": conf,
            "class": cls
        })

    socket.send_json(detections)
