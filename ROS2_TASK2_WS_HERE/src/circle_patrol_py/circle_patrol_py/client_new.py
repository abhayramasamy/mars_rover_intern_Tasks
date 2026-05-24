import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus

from circle_patrol.action import ExecuteCircle
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class GenericActionClient(Node):
    SERVER_WAIT_TIMEOUT = 25.0

    def __init__(self):
        super().__init__('generic_action_client')
        self._action_client = ActionClient(
            self,
            ExecuteCircle,
            'execute_circle'
        )
        self._goal_handle = None

    def info(self, msg): self.get_logger().info(msg)
    def warn(self, msg): self.get_logger().warning(msg)
    def error(self, msg): self.get_logger().error(msg)

    def send_goal(self, radius):

        goal_msg = ExecuteCircle.Goal()
        goal_msg.radius = radius

        self.info('Waiting for server...')

        if not self._action_client.wait_for_server(timeout_sec=self.SERVER_WAIT_TIMEOUT):
            self.error('Server not available to connect....')
            return

        self.info('Connection successful, Sending goal...')

        future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):

        self._goal_handle = future.result()

        if not self._goal_handle.accepted:
            self.warn('Goal rejected BY SERVER')
            return

        self.info('Goal accepted passed for execution...')

        result_future = self._goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):

        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.info(f'SUCCESS → {result.final_report} STATUS: COMPLETED')
        elif status == GoalStatus.STATUS_ABORTED:
            self.error(f'ABORTED → {result.final_report} STATUS: ABORTED')
        else:
            self.error(f'UNKNOWN STATUS: {status}')
            
    def feedback_callback(self, feedback_msg):

        feedback = feedback_msg.feedback
        self.info(f'FEEDBACK RECIEVED: {feedback}')
def main(args=None):
    rclpy.init(args=args)

    node = GenericActionClient()
    node.send_goal(1.0)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.info('Shutdown')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
