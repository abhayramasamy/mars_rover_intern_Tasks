import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import zmq, cv2, numpy as np

HSV_RANGES = {
    "red1":  ((0,120,70),(10,255,255)),
    "red2":  ((170,120,70),(180,255,255)),
    "orange":((5,100,100),(25,255,255)),
    "yellow":((20,80,80),(35,255,255)),
    "green": ((40,70,70),(80,255,255)),
    "blue":  ((90,70,70),(130,255,255)),
    "purple":((130,70,70),(160,255,255)),
    "pink":  ((160,70,70),(170,255,255)),
}

class YoloClient(Node):
    def __init__(self):
        super().__init__('yolo_client')
        self.bridge = CvBridge()
        ctx = zmq.Context()
        self.socket = ctx.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")
        self.sub = self.create_subscription(Image,'/camera/image_raw',self.cb,10)

    def color_ratio(self, roi):
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        best = 0
        for lo, hi in HSV_RANGES.values():
            mask = cv2.inRange(hsv, np.array(lo), np.array(hi))
            r = mask.sum() / (mask.size * 255)
            if r > best: best = r
        return best

    def cb(self, msg):
        f = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        _, buf = cv2.imencode('.jpg', f)
        self.socket.send(buf.tobytes())
        dets = self.socket.recv_json()

        for d in dets:
            x1,y1,x2,y2 = map(int, d['bbox'])
            conf = d['conf']
            if conf < 0.20: continue   #try 0.3 try distance aware low confidence thresholding 

            roi = f[y1:y2, x1:x2]
            if roi.size == 0: continue

            if self.color_ratio(roi) < 0.15: continue

            col = tuple(map(int, roi.mean(axis=(0,1))))
            label = f"{conf:.2f}"

            cv2.rectangle(f,(x1,y1),(x2,y2),col,2)
            (w,h),_ = cv2.getTextSize(label,0,0.4,1)
            cv2.rectangle(f,(x1,y1-h-4),(x1+w,y1),col,-1) #need to try and apply BB box merging too
            cv2.putText(f,label,(x1,y1-2),0,0.4,(0,0,0),1)

        cv2.imshow("YOLO", f)
        cv2.waitKey(1)

def main():
    rclpy.init()
    n = YoloClient()
    rclpy.spin(n)
    n.destroy_node()
    rclpy.shutdown()
