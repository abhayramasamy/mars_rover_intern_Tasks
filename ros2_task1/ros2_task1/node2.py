from my_interfaces.srv import SetSpeed 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Node2(Node):
    def __init__(self):
        super().__init__('node2')

        self.subscription = self.create_subscription(
            String,
            'Topic',
            self.subc,
            10
        )

        self.srv = self.create_service(
            SetSpeed,
            'set_speed',
            self.handle_set_speed
        )

        self.get_logger().info("Node2 (Service Server) Ready")

    def subc(self, msg):
        self.get_logger().info(f'I heard: {msg.data}')

    def handle_set_speed(self, request, response):
        speed = request.speed
        self.get_logger().info(f"Received speed request: {speed}")
        response.status = f"Speed set to {speed}"
        return response


def main(args=None):
    rclpy.init(args=args)
    node = Node2()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
