import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
import time

# >>> REPLACE THIS <<<
from circle_patrol.action import ExecuteCircle
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
# >>> REPLACE THIS <<<


class GenericActionServer(Node):

    ##### ================= USER CONFIG ================= #####

    #GOAL_ACCEPT_CONDITION = lambda goal: goal.radius > 0.0

    THRESHOLD = 1.0  # WALL THRESHOLD

    LOOP_SLEEP = 0.1  # small step for responsiveness

    ##### ================================================= #####

    def __init__(self):
        super().__init__('generic_action_server')

        ##### MULTITHREADING #####
        self.cb_group = ReentrantCallbackGroup()

        self._action_server = ActionServer(
            self,
            ExecuteCircle,
            'execute_circle',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=self.cb_group
        )
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(
    Pose, '/turtle1/pose', self.pose_callback, 10)
        self.current_pose = None
        self.info('Action server booted up :) ')

    ##### LOG HELPERS #####
    def info(self, msg): self.get_logger().info(msg)
    def warn(self, msg): self.get_logger().warning(msg)
    def error(self, msg): self.get_logger().error(msg)

    ##### ================= GOAL VALIDATION ================= #####
    def goal_callback(self, goal_request):
        self.info(
            f'recieved goal request: {goal_request.radius}... validating...')
        if not goal_request.radius>0.5:
            self.warn('Goal rejected by condition...EXITING')
            return GoalResponse.REJECT

        self.info('Goal accepted ... PASSED FOR EXECUTION ')
        return GoalResponse.ACCEPT

    ##### ================= EXECUTION ================= #####
    def pose_callback(self, pose_msg):
        self.current_pose = pose_msg

    def stop_turtle(self):
        twist_msg = Twist()
        self.cmd_pub.publish(twist_msg)
        self.warn('TURTLE STOPPED....')

    def angle_wrap(self, theta):
        return math.atan2(math.sin(theta), math.cos(theta))

    def execute_callback(self, goal_handle):

        ##### ===== INITIALIZE STATE ===== #####
        status = {
            "prev_theta": None,
            "total_angle": 0.0,
            "distance": 0.0,
        }

        radius = goal_handle.request.radius
        linear_speed = 1.5
        angular_speed = linear_speed / radius
        twist = Twist()
        twist.linear.x = linear_speed
        twist.angular.z = angular_speed

        feedback = ExecuteCircle.Feedback()
        self.info('executing circle task...')

        ##### ===== MAIN EXECUTION LOOP ===== #####
        while True:
            if self.current_pose is None:
                time.sleep(self.LOOP_SLEEP)
                continue

            if goal_handle.is_cancel_requested:
                self.warn('Cancel detected')
                goal_handle.canceled()
                self.stop_turtle()
                result = ExecuteCircle.Result()
                result.success = False
                result.final_report = "cancelled mid-execution"
                ##### FILL RESULT #####
                return result
            
            
            current_theta = self.current_pose.theta
            x = self.current_pose.x
            y = self.current_pose.y
            
            ABOUT_TO_HIT_WALL = (#condition to hit wall true-->about to hit false if not
                x > 11.0 - self.THRESHOLD or 
                y >  11.0 - self.THRESHOLD or
                x < self.THRESHOLD or 
                y < self.THRESHOLD
            )
           
            ##### ===== RUNTIME ABORT ===== #####
            if ABOUT_TO_HIT_WALL: 
                self.error('Runtime abort triggered')
                goal_handle.abort()
                self.stop_turtle()
                result = ExecuteCircle.Result()
                result.success = False
                result.final_report = "About to hit wall!!! stopped "
                return result
            
            if status['prev_theta'] is None:
                status['prev_theta'] = current_theta
                time.sleep(self.LOOP_SLEEP)
                continue
            delta = self.angle_wrap(current_theta - status['prev_theta']) 
            status['total_angle'] += abs(delta) 
            status['prev_theta'] = current_theta 
            status['distance'] = status['total_angle']*radius 
            
            ##### ===== FEEDBACK ===== #####
            self.cmd_pub.publish(twist) #MOVE THE TURTLE ACROSS THE BOARD :)
            ##### FILL FEEDBACK FIELDS #####
            feedback.distance_traveled = status['distance']
            feedback.current_status = f"angle = {status['total_angle']:.2f}"
            goal_handle.publish_feedback(feedback)
            
            ##### ===== LOOP EXIT CONDITION ===== #####


            if status['total_angle']>=2*math.pi:
                goal_handle.succeed()
                self.stop_turtle()
                result = ExecuteCircle.Result()
                result.success = True
                result.final_report = "TASK DONE ... (:)) "
                ##### FILL RESULT #####
                return result

            ##### ===== RESPONSIVE SLEEP ===== #####
            time.sleep(self.LOOP_SLEEP)

    ##### ================= CANCEL HANDLER ================= #####
    def cancel_callback(self, goal_handle):
        self.warn('Cancel request received')
        return CancelResponse.ACCEPT


##### ================= MAIN ================= #####
def main(args=None):
    rclpy.init(args=args)

    node = GenericActionServer()

    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        node.info('Shutdown')
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
