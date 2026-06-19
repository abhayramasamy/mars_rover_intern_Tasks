# Source - https://stackoverflow.com/q/78941537
# Posted by Bobipuegi, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-19, License - CC BY-SA 4.0

import cv2

aruco_dict= cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

params = cv2.aruco.DetectorParameters()

##create aruco

marker_size = 500 #mm

for i in range(6):

    marker_image = cv2.aruco.generateImageMarker(aruco_dict, i, marker_size)
    # Source - https://stackoverflow.com/a/78941685
# Posted by Christoph Rackwitz, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-19, License - CC BY-SA 4.0
    border_width = int(500 / 7)
    marker_image = cv2.copyMakeBorder(
    	marker_image,
    	border_width, border_width, border_width, border_width,
    	borderType=cv2.BORDER_CONSTANT, value=255)
    cv2.imwrite(f"marker_{i}.png", marker_image)


##load aruco image

img = cv2.imread("marker_5.png")

#detect markers

aruco_detector = cv2.aruco.ArucoDetector(aruco_dict,params)

corners, ids, _ = aruco_detector.detectMarkers(img) 

print(corners)

print(ids)

