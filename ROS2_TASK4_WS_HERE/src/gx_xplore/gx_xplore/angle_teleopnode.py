import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class ArmPositionInput(Node):
    def __init__(self):
        super().__init__('arm_position_input')

        self.publisher_ = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )

        self.get_logger().info(
            'Enter a position between -1.5 and 1.5\n'
            'Type q to quit'
        )

    def publish_position(self, position):
        msg = JointTrajectory()
        msg.joint_names = ['arm_to_extension']

        point = JointTrajectoryPoint()
        point.positions = [position]
        point.time_from_start.sec = 2

        msg.points.append(point)
        self.publisher_.publish(msg)

    def run(self):
        while True:
            user_input = input("Enter position: ")

            if user_input.lower() == 'q':
                break

            try:
                pos = float(user_input)
                pos = max(-1.5, min(1.5, pos))

                self.get_logger().info(f'Moving to: {pos:.2f}')
                self.publish_position(pos)

            except ValueError:
                self.get_logger().warn('Invalid input! Enter a number.')


def main():
    rclpy.init()
    node = ArmPositionInput()
    node.run()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
