from my_interfaces.srv import SetSpeed 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Node1(Node):
    def __init__(self):
        super().__init__('node1')

        self.publisher_ = self.create_publisher(String, 'Topic', 10)
        self.timer = self.create_timer(1.0, self.tc)

        self.client = self.create_client(SetSpeed, 'set_speed')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

        self.i = 0
        self.get_logger().info('Node1 started')

    def tc(self):
        msg = String()
        msg.data = f"Published number: {self.i}"
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {self.i}')

        if self.i % 5 == 0:
            self.send_request(self.i)

        self.i += 1

    def send_request(self, speed):
        req = SetSpeed.Request()
        req.speed = speed

        future = self.client.call_async(req)
        future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f"Service response: {response.status}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = Node1()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
