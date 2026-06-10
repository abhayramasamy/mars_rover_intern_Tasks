import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    world_path = '/home/abhay-07/Desktop/task4_files/my_world.sdf'
    urdf_file = '/home/abhay-07/Desktop/task4_files/my_robo_3.urdf'
    controller_urdf = '/home/abhay-07/arm_controllers.yaml'

    return LaunchDescription([

        # 1. Gazebo
        ExecuteProcess(
            cmd=['ign', 'gazebo', world_path],
            output='screen'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
        		'robot_description': ParameterValue(
            	Command(['cat ', urdf_file]),
            	value_type=str
        	),
                'use_sim_time': True
            }]
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='joint_state_bridge',
            arguments=['/world/empty/model/my_robo/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model'],
            remappings=[('/world/empty/model/my_robo/joint_state', '/joint_states')],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),
       
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='tf_bridge',
            arguments=['/model/my_robo/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'],
            remappings=[('/model/my_robo/tf', '/tf')],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),
#change the topci
		Node(
    		package='tf2_ros',
    		executable='static_transform_publisher',
    		name='odom_to_base',
    		arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_link'],
    		parameters=[{'use_sim_time': True}]
		),

####check for issues here #######
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='cmd_vel_bridge',
            arguments=['/model/my_robo/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist'],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),

        # 6. Lidar bridge ####need to check
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='lidar_bridge',
            arguments=['/model/my_robo/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'],
            remappings=[('/model/my_robo/lidar', '/scan')],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),

        # 7. IMU bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='imu_bridge',
            arguments=['/model/my_robo/imu@sensor_msgs/msg/Imu[gz.msgs.IMU'],
            remappings=[('/model/my_robo/imu', '/imu')],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='camera_bridge',
            arguments=['/model/my_robo/camera@sensor_msgs/msg/Image[gz.msgs.Image'],
            remappings=[('/model/my_robo/camera', '/camera/image_raw')],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='camera_info_bridge',
            arguments=['/model/my_robo/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo'],
            remappings=[('/model/my_robo/camera_info', '/camera/camera_info')],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),
        #fix lidar frame??
        Node(
    		package='tf2_ros',
    		executable='static_transform_publisher',
    		name='lidar_frame_fix',
    		arguments=['0', '0', '0', '0', '0', '0',
               'lidar_link', 'my_robo/base_link/lidar'],
    		parameters=[{'use_sim_time': True}]
		),
		
		Node(
    		package='controller_manager',
    		executable='spawner',
    		arguments=['joint_state_broadcaster'],
    		parameters=[{'use_sim_time': True}],
    		output='screen'
		),
		Node(
    		package='controller_manager',
    		executable='spawner',
    		arguments=['arm_controller'],
    		parameters=[{'use_sim_time': True}],
    		output='screen'
		),
		
    ])
