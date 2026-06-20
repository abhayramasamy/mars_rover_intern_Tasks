import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np

from geometry_msgs.msg import TransformStamped
import tf2_ros

from scipy.spatial.transform import Rotation as R


class ArucoTFNode(Node):

    def __init__(self):
        super().__init__('aruco_tf_node')

        self.bridge = CvBridge()

        self.sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.br = tf2_ros.TransformBroadcaster(self)

        # ArUco setup
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50
        )
        self.params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(
            self.aruco_dict,
            self.params
        )

        # Camera calibration (replace later)
        self.camera_matrix = np.array([
            [554.38, 0.0, 320.0],
            [0.0, 554.38, 240.0],
            [0.0, 0.0, 1.0]
        ])

        self.dist_coeffs = np.zeros((5, 1))

        self.marker_length = 0.5  # meters

        # 🔥 OpenCV → ROS conversion matrix
        self.R_fix = np.array([
            [0, 0, 1],
            [-1, 0, 0],
            [0, -1, 0]
        ])

    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        corners, ids, _ = self.detector.detectMarkers(frame)

        if ids is not None:

            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners,
                self.marker_length,
                self.camera_matrix,
                self.dist_coeffs
            )

            for i, marker_id in enumerate(ids.flatten()):

                rvec = rvecs[i][0]
                tvec = tvecs[i][0]

                # Draw axes (OpenCV view)
                cv2.drawFrameAxes(
                    frame,
                    self.camera_matrix,
                    self.dist_coeffs,
                    rvec,
                    tvec,
                    0.03
                )

                # 🔥 Convert rotation
                R_cv, _ = cv2.Rodrigues(rvec)
                R_ros = self.R_fix @ R_cv

                quat = R.from_matrix(R_ros).as_quat()

                # 🔥 Convert translation
                tvec_ros = self.R_fix @ tvec.reshape(3)

                # TF message
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

        # Draw marker borders
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        cv2.imshow("Aruco TF Debug", frame)
        cv2.waitKey(1)


def main():
    rclpy.init()
    node = ArucoTFNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
