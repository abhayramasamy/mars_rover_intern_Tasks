import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R
import tf2_ros
from geometry_msgs.msg import TransformStamped

class ArucoTfNode(Node):
	def __init__(self):
		super().__init__('aruco_tf_node')
		self.bridge = CvBridge()
		self.sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
		self.br = tf2_ros.TransformBroadcaster(self)
		self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
		self.params = cv2.aruco.DetectorParameters()
		self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.params)
		self.camera_matrix = np.array([[554.38,0.0,320.0],[0.0,554.38,240.0],[0.0,0.0,1.0]])
		self.dist_coeffs = np.zeros((5,1))
		self.marker_length = 0.5
		self.R_fix = np.array([[0,0,1],[-1,0,0],[0,-1,0]]) #correction to convert opencv to ros frames

	def image_callback(self, msg):
		frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
		corners, ids, _ = self.detector.detectMarkers(frame)

		if ids is not None:
			rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, self.marker_length, self.camera_matrix, self.dist_coeffs)

			for i, marker_id in enumerate(ids.flatten()):
				rvec = rvecs[i][0]
				tvec = tvecs[i][0]

				cv2.drawFrameAxes(frame, self.camera_matrix, self.dist_coeffs, rvec, tvec, 0.03)

				R_cv, _ = cv2.Rodrigues(rvec)
				R_ros = self.R_fix @ R_cv
				quat = R.from_matrix(R_ros).as_quat()

				tvec_ros = self.R_fix @ tvec.reshape(3)

				t = TransformStamped()
				t.header.stamp = self.get_clock().now().to_msg()
				t.header.frame_id = "camera_link"
				t.child_frame_id = f"aruco_{marker_id}"

				t.transform.translation.x = float(tvec_ros[0])
				t.transform.translation.y = float(tvec_ros[1])
				t.transform.translation.z = float(tvec_ros[2])

				t.transform.rotation.x = float(quat[0])
				t.transform.rotation.y = float(quat[1])
				t.transform.rotation.z = float(quat[2])
				t.transform.rotation.w = float(quat[3])

				self.br.sendTransform(t)

		if ids is not None:
			cv2.aruco.drawDetectedMarkers(frame, corners, ids)

		cv2.imshow("debug window", frame)
		cv2.waitKey(1)

def main():
	rclpy.init()
	aruco_node = ArucoTfNode()
	rclpy.spin(aruco_node)
	aruco_node.destroy_node()
	rclpy.shutdown()
