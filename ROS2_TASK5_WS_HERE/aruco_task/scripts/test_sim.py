import cv2
import numpy as np

IMAGE_PATH = "/home/abhay-07/Pictures/Screenshots/testimg6.png"
DICT = cv2.aruco.DICT_4X4_50


aruco_dict = cv2.aruco.getPredefinedDictionary(DICT)
params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, params)

img = cv2.imread(IMAGE_PATH)

if img is None:
    raise ValueError("Image not found")

h, w = img.shape[:2]

print("\n=== Distance Simulation ===\n")

# simulate distance by scaling down
scales = [1.0, 0.75, 0.5, 0.35, 0.25, 0.15, 0.1]

for s in scales:
    resized = cv2.resize(img, (int(w*s), int(h*s)), interpolation=cv2.INTER_AREA)

    canvas_size = 800
    canvas = np.ones((canvas_size, canvas_size, 3), dtype=np.uint8) * 255

    rh, rw = resized.shape[:2]
########################
    scale_factor = min(canvas_size / rw, canvas_size / rh, 1.0)
    if scale_factor < 1.0:
        resized = cv2.resize(
            resized,
            (int(rw * scale_factor), int(rh * scale_factor)),
            interpolation=cv2.INTER_AREA
        )
        rh, rw = resized.shape[:2]

    y = (canvas_size - rh)//2
    x = (canvas_size - rw)//2
    canvas[y:y+rh, x:x+rw] = resized

    corners, ids, _ = detector.detectMarkers(canvas)

    print(f"Scale {s:.2f} | Size ~{rw}px | Detected:", ids)

    vis = canvas.copy()

    if len(vis.shape) == 2:
        vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(vis, corners, ids)

    cv2.imshow("test", vis)
    cv2.waitKey(500)

cv2.destroyAllWindows()
