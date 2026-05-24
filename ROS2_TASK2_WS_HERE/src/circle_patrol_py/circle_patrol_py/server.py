import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse

from circle_patrol.action import ExecuteCircle
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import math
import time


class CirclePatrolServer(Node):

    def __init__(self):
        super().__init__('circle_patrol_server')

        self.cmd_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        self.current_pose = None
        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self._action_server = ActionServer(
            self,
            ExecuteCircle,
            'execute_circle',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        self.get_logger().info('Circle Patrol Server Started')

    def pose_callback(self, msg):
        self.current_pose = msg

    def goal_callback(self, goal_request):
        self.get_logger().info(f"Goal received: radius = {goal_request.radius}")
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info("Cancel request received")
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        #rate = self.create_rate(20)  # 20 Hz
        self.get_logger().info('Executing circle...')

        radius = goal_handle.request.radius
        linear_speed = 1.5
        angular_speed = linear_speed / radius

        twist = Twist()
        twist.linear.x = linear_speed
        twist.angular.z = angular_speed

        start_theta = None
        total_angle = 0.0

        feedback_msg = ExecuteCircle.Feedback()

        while rclpy.ok():

            if self.current_pose is None:
                time.sleep(0.05)
                continue

            if start_theta is None:
                start_theta = self.current_pose.theta

            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.stop_turtle()

                result = ExecuteCircle.Result()
                result.success = False
                result.final_report = "Mission cancelled by client"

                self.get_logger().info("Goal cancelled")
                return result

            self.cmd_pub.publish(twist)

            current_theta = self.current_pose.theta
            delta = self.angle_wrap(current_theta - start_theta)

            total_angle += abs(delta)
            start_theta = current_theta

            distance = total_angle * radius

            feedback_msg.distance_traveled = distance
            feedback_msg.current_status = f"Moving... angle={total_angle:.2f}"

            goal_handle.publish_feedback(feedback_msg)

            if total_angle >= 2 * math.pi:
                break

            time.sleep(0.05)

        self.stop_turtle()

        goal_handle.succeed()

        result = ExecuteCircle.Result()
        result.success = True
        result.final_report = "Completed full circle"

        self.get_logger().info("Circle completed successfully")

        return result

    def stop_turtle(self):
        twist = Twist()
        self.cmd_pub.publish(twist)

    def angle_wrap(self, angle):
        return math.atan2(math.sin(angle), math.cos(angle))


from rclpy.executors import MultiThreadedExecutor

def main(args=None):
    rclpy.init(args=args)

    node = CirclePatrolServer()

    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
