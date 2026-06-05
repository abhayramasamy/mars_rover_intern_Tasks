import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import tty
import termios

class SimpleTeleop(Node):
    def __init__(self):
        super().__init__('simple_teleop')
        self.publisher_ = self.create_publisher(Twist, '/model/my_robo/cmd_vel', 10)
        self.get_logger().info('Teleop started! Use F (Forward), B (Back), S (Stop). Press Q to quit.')

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

    def run(self):
        while True:
            key = self.get_key().upper()
            msg = Twist()
            if key == 'F':
                msg.linear.x = 0.5
                self.get_logger().info('Moving Forward')
            elif key == 'B':
                msg.linear.x = -0.5
                self.get_logger().info('Moving Backward')
            elif key == 'S':
                msg.linear.x = 0.0
                self.get_logger().info('Stopping')
            elif key == 'Q':
                break
            self.publisher_.publish(msg)

def main():
    rclpy.init()
    teleop = SimpleTeleop()
    teleop.run()
    teleop.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
