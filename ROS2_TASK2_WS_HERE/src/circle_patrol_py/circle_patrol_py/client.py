import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from circle_patrol.action import ExecuteCircle

class CirclePatrolClient(Node):
	def __init__(self):
		super().__init__('circle_patrol_client')
		self._action_client = ActionClient(
			self,
			ExecuteCircle,
			'execute_circle'
		)
	def send_goal(self, radius, speed):
		goal_msg = ExecuteCircle.Goal()
		goal_msg.radius = radius
		#goal_msg.speed = speed
		self.speed = speed
		self.get_logger().info('client starting')
		self._action_client.wait_for_server()
		self._send_goal_future = self._action_client.send_goal_async(
			goal_msg,
			feedback_callback = self.feedback_callback
		)
		self._send_goal_future.add_done_callback(self.goal_response_callback)
	def goal_response_callback(self, future):
		goal_handle = future.result()
		if not goal_handle.accepted:
			self.get_logger().info('goal not accepted ')
			return 
		self.get_logger().info('goal accepted going on...')
		self._get_result_future = goal_handle.get_result_async()
		self._get_result_future.add_done_callback(self.result_callback)
		self._goal_handle = goal_handle 
	def feedback_callback(self, feedback_msg):
		feedback = feedback_msg.feedback
		self.get_logger().info(f'feedback recieved: {feedback.distance_traveled: .2f}')
	def result_callback(self, future):
		result = future.result().result 
		if result.success:
			self.get_logger().info('success yipeeeeeee') 
		else:
			self.get_logger().info('circle failed')
		rclpy.shutdown() 
	def cancel_goal(self):
		if hasattr(self, '_goal_handle'):
			self.get_logger().info('goal cancelling.........')
			self._goal_handle.cancel_goal_async() 
def main(args=None):
	rclpy.init(args=args)
	node = CirclePatrolClient() 
	radius = 2.0
	speed = 1.0 
	node.send_goal(radius, speed)
	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		node.get_logger().info('ctrl+c pressed cancelling node') 
		node.cancel_goal()
	finally:
		 
		node.destroy_node() 
	
		
