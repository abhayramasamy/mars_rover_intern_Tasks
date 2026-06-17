# TASK OF IMPLEMENTING SENSORS VIS USING ROS2 AND joint control 
The task involves implementing different sensors using ros2 lidar, cam, im sensors implement different bridges and viualize it in RVIZ2 and recieve data to be processable in ros2 nodes etc, implement a joint controller aon an arm and move the singular arm joint. using rqt_joint_controller to control the arm.

## concepts learnt:
1) setting up sensors and connecting them using ros gz bridges and connecting to ros2
2) visualize the sensor data on both gazebo and rviz2 for testing
3) implemented a joint controller to control the arm

## issues faced:
1) I was unable ot configure the gui part of joint_controller due to some issues and instead i used a workaround in writing a custom publisher node that one input an angle in radians (-1.5 to 1.5), and adjust the arm and camera as such.

##screenshots: 
![image]['screenshots/Screenshot from 2026-06-17 20-46-07.png']
![image]['screenshots/Screenshot from 2026-06-17 20-42-24.png']

## How to launch...
1) download the package `ROS2_TASK4_WS_HERE` and perform `colcon build` to build packages.
2) run... `ros2 run gx_xplore teleop_node` to start the telop node to move the robot forward or backward
3) run... `ros2 run gx_xplore angle_teleop_node` to start the camera arm joint controller node.
4) after downloading the packages  *copy your present file path* to the package and carefully reqrte the file path presen t in the file: `robo_pkg/launch_file.py` 
4) open new terminal from `robo_pkg` directory and run...`ros2 launch launch_file.py`
5) the gazebo recieves twist message info via /model/my_robo/cmd_vel and one needs to use parameter bridges to connect the teleop_node which publishes in /cmd_vel by using command: `ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/model/my_robo/cmd_vel` and one can control the robot using teleop keyboard standard.

## demo files:
1) demo video screen recording present in *demo files* directory.
