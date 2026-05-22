import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/abhay-07/funny_ros2_proj/src/ROS2_TASK2_WS_HERE/install/collision_avoidance'
