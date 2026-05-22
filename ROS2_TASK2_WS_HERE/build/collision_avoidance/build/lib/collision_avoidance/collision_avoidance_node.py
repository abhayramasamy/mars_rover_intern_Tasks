import rclpy
from rclpy.node import Node
import math
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy


class CollisionAvoidanceNode(Node):

    def __init__(self):
        super().__init__('collision_avoidance_node')
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )
        self.declare_parameter('safety_threshold', 1.5)
        self.safety_threshold = self.get_parameter(
            'safety_threshold').value
        self.add_on_set_parameters_callback(self.parameter_callback) #change the 
        self.pose_subscriber = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            qos_profile   #qos_profile included here 
        )
        self.cmd_publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )
        self.get_logger().info("Collision Avoidance Node Started")

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'safety_threshold':
                self.safety_threshold = param.value
                self.get_logger().info(
                    f"Updated safety_threshold: {self.safety_threshold}"
                )
        return rclpy.parameter.SetParametersResult(successful=True)

    def pose_callback(self, msg: Pose):

    	x = msg.x
    	y = msg.y
    	theta = msg.theta

    	t = self.safety_threshold

    	# Default command (important!)
    	cmd = Twist()

    	near_wall = (
        	x < t or
        	x > (11.0 - t) or
        	y < t or
        	y > (11.0 - t)
    	)

    	near_left   = x < t
    	near_right  = x > 11 - t
    	near_bottom = y < t
    	near_top    = y > 11 - t

    	top_left     = near_top and near_left
    	top_right    = near_top and near_right
    	bottom_left  = near_bottom and near_left
    	bottom_right = near_bottom and near_right

    	PI = math.pi

    	if near_wall:

        	if top_right:
        	    cmd = self.rotate_to_angle(theta, -3 * PI / 4)   # face center

        	elif top_left: cmd = self.rotate_to_angle(theta, -PI / 4)

        	elif bottom_right: cmd = self.rotate_to_angle(theta, 3 * PI / 4)

        	elif bottom_left: cmd = self.rotate_to_angle(theta, PI / 4)

        	elif near_top: cmd = self.rotate_to_angle(theta, -PI / 2)

        	elif near_bottom: cmd = self.rotate_to_angle(theta, PI / 2)

        	elif near_left: cmd = self.rotate_to_angle(theta, 0.0)

        	elif near_right: cmd = self.rotate_to_angle(theta, PI)

        	else: self.get_logger().error("Unexpected condition")

        	self.get_logger().info("Near wall! Turning...")

    	else:
        	# Normal forward motion
        	#cmd.linear.x = 2.0
        	#cmd.angular.z = 0.0
        	pass

    	self.cmd_publisher.publish(cmd)


###############################################
    def rotate_to_angle(self, current_theta, target_theta):
        import math
        from geometry_msgs.msg import Twist

        cmd = Twist()

        error = target_theta - current_theta
        error = math.atan2(math.sin(error), math.cos(error))

        if abs(error) > 0.05:
            cmd.angular.z = 2.0 * error
            cmd.linear.x = 0.0
        else:
            cmd.angular.z = 0.0
            cmd.linear.x = 1.5

        return cmd


def main(args=None):
    rclpy.init(args=args)
    node = CollisionAvoidanceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
